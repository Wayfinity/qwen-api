"""
QWEN VLM Model Loader for RTX Ada 2000 (CUDA)
Uses transformers library for cross-platform compatibility
"""

import torch
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Global model state
_model = None
_processor = None

# Use Qwen2.5-VL model for vision-language tasks
# 7B requires ~16GB VRAM, use 3B for smaller GPUs
QWEN_MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"
# Alternative: "Qwen/Qwen2.5-VL-3B-Instruct" for faster inference if needed

def ensure_cuda_available():
    """Check CUDA availability and device."""
    if not torch.cuda.is_available():
        logger.warning("CUDA not available - will use CPU (much slower)")
        return False
    
    logger.info(f"CUDA Device: {torch.cuda.get_device_name(0)}")
    logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f}GB")
    return True


def load_qwen_model() -> Tuple[Qwen2_5_VLForConditionalGeneration, AutoProcessor]:
    """
    Load QWEN2.5-VL model for vision-language tasks.
    Lazy loads on first call, cached on subsequent calls.
    
    Returns:
        Tuple of (model, processor)
    """
    global _model, _processor
    
    if _model is not None:
        logger.debug("Using cached QWEN model")
        return _model, _processor
    
    logger.info(f"Loading QWEN model: {QWEN_MODEL_ID}")
    logger.info("This may take a moment on first run (~5-10 seconds)...")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load processor
    _processor = AutoProcessor.from_pretrained(QWEN_MODEL_ID, trust_remote_code=True)
    
    # Load model with optimized settings
    _model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        QWEN_MODEL_ID,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map="auto",  # Automatic device placement for multi-GPU support
        trust_remote_code=True,
    )
    
    # Set to eval mode
    _model.eval()
    
    logger.info(f"✅ QWEN model loaded on {device}")
    return _model, _processor


def unload_qwen_model():
    """Unload model from memory to free GPU VRAM."""
    global _model, _processor
    if _model is not None:
        del _model
        del _processor
        _model = None
        _processor = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info("✅ QWEN model unloaded from memory")


def get_device():
    """Get current computation device."""
    return "cuda" if torch.cuda.is_available() else "cpu"
