"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class HallucinationRiskEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class PositionChangeEnum(str, Enum):
    NONE = "none"
    MINOR = "minor"
    MAJOR = "major"
    COMPLETE = "complete"
    UNKNOWN = "unknown"


# ============= FEASIBILITY ANALYZER =============

class AnalyzeFeasibilityRequest(BaseModel):
    """Request for action feasibility analysis."""
    image_base64: str = Field(..., description="Base64-encoded image")
    action: str = Field(..., description="Target action to analyze")
    skip_analysis: bool = Field(False, description="Skip QWEN analysis and return empty response")


class FeasibilityAnalysis(BaseModel):
    """Feasibility analysis response."""
    feasibility_score: float = Field(0.0, description="0.0 to 1.0 feasibility score")
    pose_similarity: float = Field(0.0, description="How similar current pose is to target")
    current_pose: str = Field("unknown", description="Description of current pose")
    current_clothing: List[str] = Field(default_factory=list, description="Visible clothing items")
    target_action: str = Field("", description="The target action")
    missing_elements: List[str] = Field(default_factory=list, description="Missing elements needed")
    needs_second_person: bool = Field(False, description="Does action require second person?")
    needs_penis: bool = Field(False, description="Does action require visible penis?")
    needs_vagina_visible: bool = Field(False, description="Does action require visible vagina?")
    needs_clothing_removal: bool = Field(False, description="Does action require clothing removal?")
    needs_position_change: PositionChangeEnum = Field(PositionChangeEnum.UNKNOWN, description="What position change is needed?")
    hallucination_risk: HallucinationRiskEnum = Field(HallucinationRiskEnum.EXTREME, description="Risk of hallucination in generation")
    recommended_approach: str = Field("", description="Recommended approach to achieve action")
    blockers: List[str] = Field(default_factory=list, description="Blockers preventing action")
    skipped: bool = Field(False, description="Was analysis skipped?")
    error: Optional[str] = Field(None, description="Error message if analysis failed")


class AnalyzeFeasibilityResponse(BaseModel):
    """Response wrapper for feasibility analysis."""
    success: bool
    data: FeasibilityAnalysis
    message: str = ""


# ============= PROMPT ENHANCEMENT =============

class EnhancePromptRequest(BaseModel):
    """Request for text prompt enhancement."""
    prompt: str = Field(..., description="Original prompt to enhance")
    skip_enhancement: bool = Field(False, description="Skip enhancement and return original")
    lora_triggers: Optional[List[str]] = Field(None, description="LoRA trigger words to preserve")


class EnhancedPromptResponse(BaseModel):
    """Response for prompt enhancement."""
    original: str = Field(description="Original prompt")
    enhanced: str = Field(description="Enhanced prompt with LoRA triggers included")
    suggested_keywords: Optional[List[str]] = Field(None, description="Suggested keywords")
    style_notes: Optional[str] = Field(None, description="Style recommendations")
    quality_modifiers: Optional[List[str]] = Field(None, description="Quality modifiers")
    lora_triggers: List[str] = Field(default_factory=list, description="LoRA triggers used")
    skipped: bool = Field(False, description="Was enhancement skipped?")
    error: Optional[str] = Field(None, description="Error if enhancement failed")


class EnhancePromptResponse(BaseModel):
    """Response wrapper for prompt enhancement."""
    success: bool
    data: EnhancedPromptResponse
    message: str = ""


# ============= IMAGE PROMPT ENHANCEMENT =============

class EnhanceImagePromptRequest(BaseModel):
    """Request for enhancing prompts based on image context."""
    prompt: str = Field(..., description="Original prompt")
    image_description: str = Field("", description="Description of current image/pose")
    skip_enhancement: bool = Field(False, description="Skip enhancement")
    lora_triggers: Optional[List[str]] = Field(None, description="LoRA trigger words")


class EnhanceImagePromptResponse(BaseModel):
    """Response for image-aware prompt enhancement."""
    original: str = Field(description="Original prompt")
    enhanced: str = Field(description="Enhanced prompt")
    pose_continuity: Optional[str] = Field(None, description="How pose should transition")
    suggested_loras: Optional[List[str]] = Field(None, description="Suggested LoRA models")
    consistency_notes: Optional[str] = Field(None, description="Visual consistency notes")
    lora_triggers: List[str] = Field(default_factory=list, description="LoRA triggers used")
    skipped: bool = Field(False, description="Was enhancement skipped?")
    error: Optional[str] = Field(None, description="Error if failed")


class EnhanceImagePromptResponseWrapper(BaseModel):
    """Response wrapper."""
    success: bool
    data: EnhanceImagePromptResponse
    message: str = ""


# ============= DUAL PROMPT GENERATION =============

class GenerateDualPromptsRequest(BaseModel):
    """Request for generating two prompt variations."""
    action: str = Field(..., description="Target action for video")
    skip_generation: bool = Field(False, description="Skip generation and return single prompt")
    lora_triggers: Optional[List[str]] = Field(None, description="LoRA trigger words to preserve")


class DualPromptsResponse(BaseModel):
    """Response for dual prompt generation."""
    prompt_1: str = Field(description="First prompt variation")
    prompt_2: str = Field(description="Second prompt variation")
    variations: Optional[str] = Field(None, description="Explanation of variations")
    shared_elements: Optional[str] = Field(None, description="Core elements in both prompts")
    lora_triggers: List[str] = Field(default_factory=list, description="LoRA triggers used")
    skipped: bool = Field(False, description="Was generation skipped?")
    error: Optional[str] = Field(None, description="Error if generation failed")


class GenerateDualPromptsResponse(BaseModel):
    """Response wrapper for dual prompt generation."""
    success: bool
    data: DualPromptsResponse
    message: str = ""


# ============= COMBINED TEXT-TO-VIDEO =============

class TextToVideoRequest(BaseModel):
    """Complete request for text-to-video generation with QWEN."""
    action: str = Field(..., description="Target action for video")
    skip_qwen: bool = Field(False, description="Skip QWEN processing")
    lora_triggers: Optional[List[str]] = Field(None, description="LoRA triggers to use")
    num_prompts: int = Field(2, ge=1, le=5, description="Number of prompt variations")


class TextToVideoResponse(BaseModel):
    """Complete response for text-to-video with QWEN analysis."""
    success: bool
    action: str
    prompts: List[str] = Field(description="Generated prompts")
    lora_triggers: List[str] = Field(description="LoRA triggers to use")
    message: str = ""
    error: Optional[str] = None


# ============= COMBINED TEXT-TO-IMAGE =============

class TextToImageRequest(BaseModel):
    """Request for text-to-image with prompt enhancement."""
    prompt: str = Field(..., description="Text description of image to generate")
    skip_qwen: bool = Field(False, description="Skip QWEN enhancement")
    lora_triggers: Optional[List[str]] = Field(None, description="LoRA triggers to use")


class TextToImageResponse(BaseModel):
    """Response for text-to-image with QWEN analysis."""
    success: bool
    original_prompt: str
    enhanced_prompt: str
    lora_triggers: List[str]
    message: str = ""
    error: Optional[str] = None


# ============= COMBINED IMAGE-TO-VIDEO =============

class ImageToVideoRequest(BaseModel):
    """Request for image-to-video with feasibility analysis."""
    image_base64: str = Field(..., description="Base64-encoded current image")
    action: str = Field(..., description="Target action for video")
    skip_feasibility: bool = Field(False, description="Skip feasibility analysis")
    skip_enhancement: bool = Field(False, description="Skip prompt enhancement")
    lora_triggers: Optional[List[str]] = Field(None, description="LoRA triggers to use")


class ImageToVideoResponse(BaseModel):
    """Response for image-to-video with analysis."""
    success: bool
    action: str
    feasibility: Optional[FeasibilityAnalysis] = None
    enhanced_prompt: str
    lora_triggers: List[str]
    message: str = ""
    error: Optional[str] = None


# ============= HEALTH CHECK =============

class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    device: str
    message: str = ""
