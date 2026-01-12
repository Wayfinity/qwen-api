"""
Action Feasibility Analyzer - QWEN2.5-VL
Evaluates how feasible an action is given a current image
"""

import torch
import json
import base64
import io
from pathlib import Path
from typing import Optional, Dict, Any, Union
from PIL import Image
import logging

from models.qwen_loader import load_qwen_model, get_device
from utils.helpers import extract_json

logger = logging.getLogger(__name__)


def analyze_action_feasibility(
    image_source: Union[str, bytes, Path],
    action: str,
    skip_analysis: bool = False,
) -> Dict[str, Any]:
    """
    Analyze how feasible an action is given the current image.
    
    Args:
        image_source: Image as base64 string, bytes, or file path
        action: Target action to analyze (e.g., "solo masturbation fingering")
        skip_analysis: If True, return empty feasibility dict without QWEN analysis
    
    Returns:
        Dict with feasibility analysis including score, blockers, recommendations
    """
    
    if skip_analysis:
        logger.debug("Skipping QWEN feasibility analysis")
        return {
            "skipped": True,
            "feasibility_score": None,
            "message": "Analysis skipped by request"
        }
    
    try:
        # Load image
        image = _load_image(image_source)
        
        # Load model
        model, processor = load_qwen_model()
        device = get_device()
        
        # Build prompt for feasibility analysis
        prompt = _build_feasibility_prompt(action)
        
        logger.debug(f"Analyzing feasibility for action: {action}")
        
        # Prepare inputs
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # Apply chat template
        text_prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        
        # Prepare inputs
        inputs = processor(
            text=text_prompt,
            images=[image],
            return_tensors="pt"
        )
        
        # Move to device
        for key in inputs:
            if isinstance(inputs[key], torch.Tensor):
                inputs[key] = inputs[key].to(device)
        
        # Generate response
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=600,
                temperature=0.2,
                top_p=0.9,
            )
        
        # Decode response
        response_text = processor.decode(output_ids[0])
        
        # Extract JSON from response
        feasibility_data = extract_json(response_text)
        
        logger.debug(f"Feasibility analysis complete: score={feasibility_data.get('feasibility_score')}")
        
        return feasibility_data
        
    except Exception as e:
        logger.error(f"Error analyzing action feasibility: {e}", exc_info=True)
        return {
            "error": str(e),
            "feasibility_score": 0.0,
            "hallucination_risk": "extreme"
        }


def _build_feasibility_prompt(action: str) -> str:
    """Build the prompt for feasibility analysis."""
    return f"""Analyze this image and evaluate how feasible it is to create a video of: "{action}"

Return JSON only (no other text):
{{
  "current_pose": "describe what the person is currently doing",
  "current_clothing": ["list of clothing items visible"],
  "target_action": "{action}",
  "feasibility_score": 0.0 to 1.0 (1.0 = perfect match, 0.0 = impossible),
  "pose_similarity": 0.0 to 1.0 (how close current pose is to target),
  "missing_elements": ["list of things needed but not in image"],
  "needs_second_person": true/false,
  "needs_penis": true/false,
  "needs_vagina_visible": true/false,
  "needs_clothing_removal": true/false,
  "needs_position_change": "none" or "minor" or "major" or "complete",
  "hallucination_risk": "low" or "medium" or "high" or "extreme",
  "recommended_approach": "describe best way to achieve this action",
  "blockers": ["list of things that make this difficult/impossible"]
}}

Consider:
- Does this action need a second person (sex acts)?
- Does this action need genitals visible?
- How different is the current pose from the target?
- What would need to be "hallucinated" (generated from nothing)?

Return ONLY valid JSON."""


def _load_image(image_source: Union[str, bytes, Path]) -> Image.Image:
    """Load image from various sources."""
    
    # If it's a file path
    if isinstance(image_source, (str, Path)):
        source_str = str(image_source)
        
        # Check if it's a base64 string
        if len(source_str) > 100 and source_str.startswith("iVBOR") or source_str.startswith("/9j/"):
            # Likely base64 PNG or JPG
            try:
                image_bytes = base64.b64decode(source_str)
                return Image.open(io.BytesIO(image_bytes)).convert("RGB")
            except Exception:
                pass
        
        # Try as file path
        if Path(source_str).exists():
            return Image.open(source_str).convert("RGB")
        
        # Last resort - try base64 decode
        try:
            image_bytes = base64.b64decode(source_str)
            return Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            raise ValueError(f"Could not load image from source: {e}")
    
    # If it's bytes
    elif isinstance(image_source, bytes):
        return Image.open(io.BytesIO(image_source)).convert("RGB")
    
    # If it's already a PIL Image
    elif isinstance(image_source, Image.Image):
        return image_source.convert("RGB")
    
    raise TypeError(f"Unsupported image source type: {type(image_source)}")
