"""
Helper utilities for QWEN API
"""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def extract_json(text: str) -> Dict[str, Any]:
    """
    Extract first JSON object from text.
    Handles nested structures and malformed JSON gracefully.
    
    Args:
        text: Text potentially containing JSON
    
    Returns:
        Parsed JSON dict, or empty dict if extraction fails
    """
    if not text:
        return {}
    
    # Find start of JSON
    start = text.find('{')
    if start == -1:
        logger.debug("No JSON object found in response")
        return {}
    
    # Find end of JSON by tracking braces
    depth = 0
    end = start
    for i, char in enumerate(text[start:], start):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    
    if end == start:
        logger.debug("Could not find matching closing brace")
        return {}
    
    try:
        json_str = text[start:end]
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.debug(f"JSON parse error: {e}")
        return {}


def merge_lora_triggers(prompts: list, lora_triggers: Optional[list] = None) -> list:
    """
    Merge LoRA trigger words with prompts.
    Ensures triggers appear at the beginning of each prompt.
    
    Args:
        prompts: List of prompt strings
        lora_triggers: List of LoRA trigger words
    
    Returns:
        List of prompts with LoRA triggers
    """
    if not lora_triggers:
        return prompts
    
    result = []
    for prompt in prompts:
        enhanced = prompt
        for trigger in lora_triggers:
            # Only add if not already in prompt
            if trigger.lower() not in prompt.lower():
                enhanced = f"{trigger}, {enhanced}"
        
        result.append(enhanced.strip())
    
    return result


def validate_image_base64(image_b64: str) -> bool:
    """Check if string looks like valid base64 image data."""
    import base64
    
    if not image_b64:
        return False
    
    try:
        # Check length
        if len(image_b64) < 100:
            return False
        
        # Try to decode
        decoded = base64.b64decode(image_b64, validate=True)
        
        # Check for PNG or JPG magic bytes
        is_png = decoded[:8] == b'\x89PNG\r\n\x1a\n'
        is_jpg = decoded[:3] == b'\xff\xd8\xff'
        
        return is_png or is_jpg
        
    except Exception:
        return False


def format_feasibility_response(feasibility_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format feasibility analysis for API response.
    Ensures all fields are present with sensible defaults.
    """
    return {
        "feasibility_score": feasibility_data.get("feasibility_score", 0.0),
        "pose_similarity": feasibility_data.get("pose_similarity", 0.0),
        "current_pose": feasibility_data.get("current_pose", "unknown"),
        "current_clothing": feasibility_data.get("current_clothing", []),
        "target_action": feasibility_data.get("target_action", ""),
        "missing_elements": feasibility_data.get("missing_elements", []),
        "needs_second_person": feasibility_data.get("needs_second_person", False),
        "needs_penis": feasibility_data.get("needs_penis", False),
        "needs_vagina_visible": feasibility_data.get("needs_vagina_visible", False),
        "needs_clothing_removal": feasibility_data.get("needs_clothing_removal", False),
        "needs_position_change": feasibility_data.get("needs_position_change", "unknown"),
        "hallucination_risk": feasibility_data.get("hallucination_risk", "extreme"),
        "recommended_approach": feasibility_data.get("recommended_approach", ""),
        "blockers": feasibility_data.get("blockers", []),
        "error": feasibility_data.get("error"),
        "skipped": feasibility_data.get("skipped", False)
    }
