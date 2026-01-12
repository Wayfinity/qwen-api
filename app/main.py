"""
QWEN API - FastAPI application
Provides endpoints for QWEN VLM integration for prompt enhancement and feasibility analysis
"""

import os
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import torch

from app.schemas import (
    AnalyzeFeasibilityRequest, AnalyzeFeasibilityResponse,
    EnhancePromptRequest, EnhancePromptResponse, EnhancedPromptResponse,
    EnhanceImagePromptRequest, EnhanceImagePromptResponseWrapper, EnhanceImagePromptResponse,
    GenerateDualPromptsRequest, GenerateDualPromptsResponse, DualPromptsResponse,
    TextToVideoRequest, TextToVideoResponse,
    TextToImageRequest, TextToImageResponse,
    ImageToVideoRequest, ImageToVideoResponse,
    HealthCheckResponse, FeasibilityAnalysis
)
from models.qwen_loader import load_qwen_model, unload_qwen_model, ensure_cuda_available, get_device
from models.feasibility_analyzer import analyze_action_feasibility
from models.prompt_enhancer import (
    enhance_text_prompt, enhance_image_prompt, generate_dual_prompts_for_video
)
from utils.helpers import format_feasibility_response, merge_lora_triggers

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============= API AUTHENTICATION =============

API_TOKEN = os.environ.get("API_TOKEN", None)
security = HTTPBearer(auto_error=False)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify API token if API_TOKEN env var is set.
    If API_TOKEN is not set, authentication is disabled.
    """
    if API_TOKEN is None:
        # Auth disabled - no token required
        return None
    
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Invalid authentication token"
        )
    
    return credentials.credentials


# ============= LIFECYCLE =============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events for the FastAPI app.
    Loads QWEN model on startup, unloads on shutdown.
    """
    
    # Startup
    logger.info("🚀 QWEN API Starting...")
    logger.info(f"📊 PyTorch Version: {torch.__version__}")
    
    # Check CUDA availability
    cuda_available = ensure_cuda_available()
    logger.info(f"✅ CUDA Available: {cuda_available}")
    
    # Pre-load QWEN model on startup
    try:
        logger.info("📥 Pre-loading QWEN model...")
        load_qwen_model()
        logger.info("✅ QWEN model loaded successfully on startup")
    except Exception as e:
        logger.error(f"❌ Failed to load QWEN model: {e}", exc_info=True)
    
    yield
    
    # Shutdown
    logger.info("🛑 QWEN API Shutting down...")
    try:
        unload_qwen_model()
        logger.info("✅ QWEN model unloaded")
    except Exception as e:
        logger.error(f"Error unloading model: {e}")


# Create FastAPI app
app = FastAPI(
    title="QWEN VLM API",
    description="QWEN2.5-VL integration for prompt enhancement and feasibility analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= HEALTH & STATUS =============

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Check API health and model status."""
    device = get_device()
    
    # Try to ensure model is loaded
    try:
        model, processor = load_qwen_model()
        model_loaded = True
    except Exception as e:
        logger.error(f"Model health check failed: {e}")
        model_loaded = False
    
    return HealthCheckResponse(
        status="ok" if model_loaded else "degraded",
        model_loaded=model_loaded,
        device=device,
        message=f"QWEN API running on {device}"
    )


# ============= FEASIBILITY ANALYSIS =============

@app.post("/analyze-feasibility", response_model=AnalyzeFeasibilityResponse)
async def analyze_feasibility(request: AnalyzeFeasibilityRequest, _: str = Depends(verify_token)):
    """
    Analyze how feasible an action is given a current image.
    
    Returns feasibility score, blockers, and recommendations.
    """
    try:
        logger.info(f"Analyzing feasibility for action: {request.action}")
        
        # Analyze feasibility
        result = analyze_action_feasibility(
            image_source=request.image_base64,
            action=request.action,
            skip_analysis=request.skip_analysis
        )
        
        # Format response
        feasibility_data = format_feasibility_response(result)
        
        return AnalyzeFeasibilityResponse(
            success=True,
            data=FeasibilityAnalysis(**feasibility_data),
            message="Feasibility analysis complete"
        )
        
    except Exception as e:
        logger.error(f"Feasibility analysis error: {e}", exc_info=True)
        return AnalyzeFeasibilityResponse(
            success=False,
            data=FeasibilityAnalysis(
                feasibility_score=0.0,
                pose_similarity=0.0,
                current_pose="unknown",
                target_action=request.action,
                hallucination_risk="extreme",
                error=str(e)
            ),
            message=f"Error: {str(e)}"
        )


# ============= PROMPT ENHANCEMENT =============

@app.post("/enhance-prompt", response_model=EnhancePromptResponse)
async def enhance_prompt(request: EnhancePromptRequest, _: str = Depends(verify_token)):
    """
    Enhance a text-only prompt with more detail and specificity.
    Preserves LoRA trigger words.
    
    Used for text-to-image generation.
    """
    try:
        logger.info(f"Enhancing prompt (skip={request.skip_enhancement})")
        
        result = enhance_text_prompt(
            prompt=request.prompt,
            skip_enhancement=request.skip_enhancement,
            lora_triggers=request.lora_triggers
        )
        
        response_data = EnhancedPromptResponse(**result)
        
        return EnhancePromptResponse(
            success=True,
            data=response_data,
            message="Prompt enhanced successfully"
        )
        
    except Exception as e:
        logger.error(f"Prompt enhancement error: {e}", exc_info=True)
        return EnhancePromptResponse(
            success=False,
            data=EnhancedPromptResponse(
                original=request.prompt,
                enhanced=request.prompt,
                lora_triggers=request.lora_triggers or [],
                error=str(e)
            ),
            message=f"Error: {str(e)}"
        )


@app.post("/enhance-image-prompt", response_model=EnhanceImagePromptResponseWrapper)
async def enhance_image_prompt_endpoint(request: EnhanceImagePromptRequest, _: str = Depends(verify_token)):
    """
    Enhance a prompt based on current image context.
    Ensures smooth transition from current state to target action.
    
    Used for image-to-video generation.
    """
    try:
        logger.info(f"Enhancing image prompt (skip={request.skip_enhancement})")
        
        result = enhance_image_prompt(
            original_prompt=request.prompt,
            image_description=request.image_description,
            skip_enhancement=request.skip_enhancement,
            lora_triggers=request.lora_triggers
        )
        
        response_data = EnhanceImagePromptResponse(**result)
        
        return EnhanceImagePromptResponseWrapper(
            success=True,
            data=response_data,
            message="Image prompt enhanced successfully"
        )
        
    except Exception as e:
        logger.error(f"Image prompt enhancement error: {e}", exc_info=True)
        return EnhanceImagePromptResponseWrapper(
            success=False,
            data=EnhanceImagePromptResponse(
                original=request.prompt,
                enhanced=request.prompt,
                lora_triggers=request.lora_triggers or [],
                error=str(e)
            ),
            message=f"Error: {str(e)}"
        )


# ============= DUAL PROMPT GENERATION =============

@app.post("/generate-dual-prompts", response_model=GenerateDualPromptsResponse)
async def generate_dual_prompts(request: GenerateDualPromptsRequest, _: str = Depends(verify_token)):
    """
    Generate 2 different prompt variations for text-to-video.
    
    Creates variety while maintaining core action.
    Useful for generating multiple video versions from one action.
    """
    try:
        logger.info(f"Generating dual prompts for action: {request.action}")
        
        result = generate_dual_prompts_for_video(
            action=request.action,
            skip_generation=request.skip_generation,
            lora_triggers=request.lora_triggers
        )
        
        response_data = DualPromptsResponse(**result)
        
        return GenerateDualPromptsResponse(
            success=True,
            data=response_data,
            message="Dual prompts generated successfully"
        )
        
    except Exception as e:
        logger.error(f"Dual prompt generation error: {e}", exc_info=True)
        return GenerateDualPromptsResponse(
            success=False,
            data=DualPromptsResponse(
                prompt_1=request.action,
                prompt_2=request.action,
                lora_triggers=request.lora_triggers or [],
                error=str(e)
            ),
            message=f"Error: {str(e)}"
        )


# ============= COMBINED ENDPOINTS =============

@app.post("/text-to-video", response_model=TextToVideoResponse)
async def text_to_video(request: TextToVideoRequest, _: str = Depends(verify_token)):
    """
    Complete text-to-video endpoint.
    
    Generates multiple prompt variations with QWEN enhancement.
    Returns prompts ready for video generation model.
    """
    try:
        logger.info(f"Text-to-video for action: {request.action}")
        
        if request.skip_qwen:
            prompts = [request.action] * request.num_prompts
        else:
            # Generate dual prompts
            result = generate_dual_prompts_for_video(
                action=request.action,
                skip_generation=False,
                lora_triggers=request.lora_triggers
            )
            prompts = [result.get("prompt_1", request.action)]
            if request.num_prompts > 1:
                prompts.append(result.get("prompt_2", request.action))
            
            # Generate additional variations if needed
            while len(prompts) < request.num_prompts:
                prompts.append(request.action)
        
        lora_triggers = request.lora_triggers or []
        
        return TextToVideoResponse(
            success=True,
            action=request.action,
            prompts=prompts,
            lora_triggers=lora_triggers,
            message=f"Generated {len(prompts)} prompts for video generation"
        )
        
    except Exception as e:
        logger.error(f"Text-to-video error: {e}", exc_info=True)
        return TextToVideoResponse(
            success=False,
            action=request.action,
            prompts=[request.action],
            lora_triggers=request.lora_triggers or [],
            error=str(e),
            message=f"Error: {str(e)}"
        )


@app.post("/text-to-image", response_model=TextToImageResponse)
async def text_to_image(request: TextToImageRequest, _: str = Depends(verify_token)):
    """
    Complete text-to-image endpoint.
    
    Enhances prompt with QWEN, preserves LoRA triggers.
    Returns enhanced prompt ready for image generation.
    """
    try:
        logger.info(f"Text-to-image with prompt: {request.prompt[:50]}...")
        
        if request.skip_qwen:
            enhanced_prompt = request.prompt
        else:
            result = enhance_text_prompt(
                prompt=request.prompt,
                skip_enhancement=False,
                lora_triggers=request.lora_triggers
            )
            enhanced_prompt = result.get("enhanced", request.prompt)
        
        # Merge LoRA triggers with prompt
        lora_triggers = request.lora_triggers or []
        final_prompt = enhanced_prompt
        for trigger in lora_triggers:
            if trigger not in final_prompt:
                final_prompt = f"{trigger}, {final_prompt}"
        
        return TextToImageResponse(
            success=True,
            original_prompt=request.prompt,
            enhanced_prompt=final_prompt,
            lora_triggers=lora_triggers,
            message="Prompt enhanced for image generation"
        )
        
    except Exception as e:
        logger.error(f"Text-to-image error: {e}", exc_info=True)
        lora_triggers = request.lora_triggers or []
        return TextToImageResponse(
            success=False,
            original_prompt=request.prompt,
            enhanced_prompt=request.prompt,
            lora_triggers=lora_triggers,
            error=str(e),
            message=f"Error: {str(e)}"
        )


@app.post("/image-to-video", response_model=ImageToVideoResponse)
async def image_to_video(request: ImageToVideoRequest, _: str = Depends(verify_token)):
    """
    Complete image-to-video endpoint.
    
    Analyzes feasibility of action, enhances prompt for image context.
    Returns feasibility analysis and enhanced prompt.
    """
    try:
        logger.info(f"Image-to-video for action: {request.action}")
        
        feasibility_data = None
        if not request.skip_feasibility:
            feasibility_data = analyze_action_feasibility(
                image_source=request.image_base64,
                action=request.action,
                skip_analysis=False
            )
            feasibility_data = format_feasibility_response(feasibility_data)
        
        # Enhance prompt
        if request.skip_enhancement:
            enhanced_prompt = request.action
        else:
            result = enhance_image_prompt(
                original_prompt=request.action,
                image_description="",
                skip_enhancement=False,
                lora_triggers=request.lora_triggers
            )
            enhanced_prompt = result.get("enhanced", request.action)
        
        # Merge LoRA triggers
        lora_triggers = request.lora_triggers or []
        final_prompt = enhanced_prompt
        for trigger in lora_triggers:
            if trigger not in final_prompt:
                final_prompt = f"{trigger}, {final_prompt}"
        
        return ImageToVideoResponse(
            success=True,
            action=request.action,
            feasibility=FeasibilityAnalysis(**feasibility_data) if feasibility_data else None,
            enhanced_prompt=final_prompt,
            lora_triggers=lora_triggers,
            message="Image-to-video analysis complete"
        )
        
    except Exception as e:
        logger.error(f"Image-to-video error: {e}", exc_info=True)
        return ImageToVideoResponse(
            success=False,
            action=request.action,
            enhanced_prompt=request.action,
            lora_triggers=request.lora_triggers or [],
            error=str(e),
            message=f"Error: {str(e)}"
        )


# ============= ROOT =============

@app.get("/")
async def root():
    """API information endpoint."""
    return {
        "name": "QWEN VLM API",
        "version": "1.0.0",
        "description": "QWEN2.5-VL integration for prompt enhancement and feasibility analysis",
        "device": get_device(),
        "docs": "/docs",
        "endpoints": {
            "health": "GET /health",
            "feasibility": "POST /analyze-feasibility",
            "enhance_prompt": "POST /enhance-prompt",
            "enhance_image_prompt": "POST /enhance-image-prompt",
            "dual_prompts": "POST /generate-dual-prompts",
            "text_to_video": "POST /text-to-video",
            "text_to_image": "POST /text-to-image",
            "image_to_video": "POST /image-to-video"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run with: python -m app.main
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
