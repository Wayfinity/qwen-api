"""
QWEN VLM Model Loader using llama-cpp-python
Uses GGUF quantized model for faster inference
"""

import os
import logging
from typing import Optional, Tuple, Any

logger = logging.getLogger(__name__)

# Global model state
_llm = None
_chat_handler = None

# GGUF model configuration
# Using Q4_K_M quantization - good balance of speed and quality
GGUF_REPO_ID = "bartowski/thesby_Qwen2.5-VL-7B-NSFW-Caption-V3-GGUF"
GGUF_FILENAME = "*Q4_K_M.gguf"  # Q4_K_M is a good balance

# Optional overrides
# - QWEN_GGUF_FILENAME: exact GGUF filename (e.g. thesby_...-Q4_K_M.gguf)
# - QWEN_MMPROJ_FILENAME: exact mmproj filename (e.g. mmproj-...-f16.gguf)

# Context window size
N_CTX = 4096

# GPU layers - -1 means all layers on GPU
N_GPU_LAYERS = -1


def _select_mmproj_filename(repo_id: str) -> str:
    """Pick a single mmproj file from a repo that contains multiple mmproj variants."""
    try:
        from huggingface_hub import list_repo_files
    except Exception as e:  # pragma: no cover
        raise ValueError(
            "huggingface-hub is required to auto-select mmproj; set QWEN_MMPROJ_FILENAME"
        ) from e

    files = list_repo_files(repo_id=repo_id, repo_type="model")
    candidates = [f for f in files if "mmproj" in f and f.endswith(".gguf")]
    if not candidates:
        raise ValueError(f"No *mmproj*.gguf files found in {repo_id}")
    if len(candidates) == 1:
        return candidates[0]

    # Prefer f16 projector, then bf16, then deterministic fallback.
    for suffix in ("-f16.gguf", "-bf16.gguf"):
        for f in candidates:
            if f.endswith(suffix):
                return f

    return sorted(candidates)[0]


def ensure_cuda_available() -> bool:
    """Check CUDA availability."""
    try:
        import torch
        if torch.cuda.is_available():
            logger.info(f"CUDA Device: {torch.cuda.get_device_name(0)}")
            logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f}GB")
            return True
        else:
            logger.warning("CUDA not available - will use CPU (slower)")
            return False
    except ImportError:
        # If torch not available, check via llama-cpp
        logger.warning("PyTorch not available for CUDA check")
        return True  # Assume CUDA available, llama-cpp will handle it


def load_qwen_model() -> Tuple[Any, Any]:
    """
    Load QWEN2.5-VL GGUF model using llama-cpp-python.
    Uses Qwen25VLChatHandler for vision-language capabilities.
    
    Returns:
        Tuple of (llm, chat_handler)
    """
    global _llm, _chat_handler
    
    if _llm is not None:
        logger.debug("Using cached QWEN GGUF model")
        return _llm, _chat_handler
    
    logger.info(f"Loading QWEN GGUF model from: {GGUF_REPO_ID}")
    logger.info("This may take a moment on first download...")
    
    try:
        from llama_cpp import Llama
        from llama_cpp.llama_chat_format import Qwen25VLChatHandler
    except ImportError as e:
        logger.error("llama-cpp-python not installed. Install with: pip install llama-cpp-python")
        raise ImportError("llama-cpp-python required for GGUF models") from e
    
    # Load the vision chat handler from HuggingFace
    # The mmproj (multimodal projector) is bundled with the model
    logger.info("Loading Qwen2.5-VL chat handler...")
    mmproj_filename = os.environ.get("QWEN_MMPROJ_FILENAME")
    if not mmproj_filename:
        mmproj_filename = _select_mmproj_filename(GGUF_REPO_ID)
    logger.info(f"Using mmproj file: {mmproj_filename}")
    _chat_handler = Qwen25VLChatHandler.from_pretrained(
        repo_id=GGUF_REPO_ID,
        filename=mmproj_filename,
        verbose=False
    )
    
    # Load the main model from HuggingFace
    logger.info("Loading main GGUF model...")
    model_filename = os.environ.get("QWEN_GGUF_FILENAME") or GGUF_FILENAME
    if model_filename != GGUF_FILENAME:
        logger.info(f"Using model file: {model_filename}")
    _llm = Llama.from_pretrained(
        repo_id=GGUF_REPO_ID,
        filename=model_filename,
        chat_handler=_chat_handler,
        n_ctx=N_CTX,
        n_gpu_layers=N_GPU_LAYERS,
        verbose=False,
    )
    
    logger.info(f"✅ QWEN GGUF model loaded (n_gpu_layers={N_GPU_LAYERS})")
    return _llm, _chat_handler


def unload_qwen_model():
    """Unload model from memory to free GPU VRAM."""
    global _llm, _chat_handler
    
    if _llm is not None:
        del _llm
        del _chat_handler
        _llm = None
        _chat_handler = None
        
        # Try to clear CUDA cache if available
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass
        
        logger.info("✅ QWEN model unloaded from memory")


def get_device() -> str:
    """Get current computation device."""
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "unknown"


def generate_response(
    prompt: str,
    image_url: Optional[str] = None,
    max_tokens: int = 512,
    temperature: float = 0.7,
) -> str:
    """
    Generate a response using the QWEN model.
    
    Args:
        prompt: Text prompt
        image_url: Optional image URL or base64 data URI
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        
    Returns:
        Generated text response
    """
    llm, _ = load_qwen_model()
    
    # Build message content
    content = []
    if image_url:
        content.append({
            "type": "image_url",
            "image_url": {"url": image_url}
        })
    content.append({
        "type": "text",
        "text": prompt
    })
    
    messages = [
        {
            "role": "user",
            "content": content if image_url else prompt
        }
    ]
    
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    
    return response["choices"][0]["message"]["content"]
