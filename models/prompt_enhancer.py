"""
Prompt Enhancement Module - QWEN2.5-VL
Improves and expands prompts for better generation quality
Integrates WAN 2.2 LoRA trigger words
"""

import json
import logging
from typing import Optional, Dict, Any, List
from models.qwen_loader import generate_response
from utils.wan_lora_integration import enrich_prompt_with_lora_triggers, get_trigger_words, detect_lora_intents

logger = logging.getLogger(__name__)


def enhance_text_prompt(
    prompt: str,
    skip_enhancement: bool = False,
    lora_triggers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Enhance a text-only prompt with QWEN analysis.
    Used for text-to-image generation.
    
    Args:
        prompt: Original text prompt
        skip_enhancement: If True, return original prompt unchanged
        lora_triggers: List of LoRA trigger words to preserve
    
    Returns:
        Dict with original and enhanced prompts, and LoRA suggestions
    """
    
    if skip_enhancement:
        logger.debug("Skipping prompt enhancement")
        return {
            "original": prompt,
            "enhanced": prompt,
            "skipped": True,
            "lora_triggers": lora_triggers or []
        }
    
    try:
        enhancement_prompt = _build_text_enhancement_prompt(prompt)
        
        logger.debug(f"Enhancing text prompt")
        
        # Generate response using GGUF model
        response_text = generate_response(
            prompt=enhancement_prompt,
            image_url=None,
            max_tokens=400,
            temperature=0.7
        )
        
        # Parse response
        result = _parse_enhancement_response(response_text, prompt, lora_triggers)
        
        return result
        
    except Exception as e:
        logger.error(f"Error enhancing prompt: {e}", exc_info=True)
        return {
            "original": prompt,
            "enhanced": prompt,
            "error": str(e),
            "lora_triggers": lora_triggers or []
        }


def enhance_image_prompt(
    original_prompt: str,
    image_description: str = "",
    skip_enhancement: bool = False,
    lora_triggers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Enhance a prompt for image-to-video with context from original image.
    
    Args:
        original_prompt: The original prompt
        image_description: Description of the current image/pose
        skip_enhancement: If True, return original prompt unchanged
        lora_triggers: List of LoRA trigger words to preserve
    
    Returns:
        Dict with enhanced prompt maintaining image consistency
    """
    
    if skip_enhancement:
        logger.debug("Skipping image prompt enhancement")
        return {
            "original": original_prompt,
            "enhanced": original_prompt,
            "skipped": True,
            "lora_triggers": lora_triggers or []
        }
    
    try:
        enhancement_prompt = _build_image_enhancement_prompt(original_prompt, image_description)
        
        logger.debug(f"Enhancing image prompt")
        
        # Generate response using GGUF model
        response_text = generate_response(
            prompt=enhancement_prompt,
            image_url=None,
            max_tokens=400,
            temperature=0.7
        )
        
        result = _parse_enhancement_response(response_text, original_prompt, lora_triggers)
        
        return result
        
    except Exception as e:
        logger.error(f"Error enhancing image prompt: {e}", exc_info=True)
        return {
            "original": original_prompt,
            "enhanced": original_prompt,
            "error": str(e),
            "lora_triggers": lora_triggers or []
        }


def generate_dual_prompts_for_video(
    action: str,
    skip_generation: bool = False,
    lora_triggers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Generate 2 different prompt variations for text-to-video generation.
    Creates variety while keeping core action consistent.
    
    Args:
        action: Target action for video (e.g., "person dancing")
        skip_generation: If True, return single prompt
        lora_triggers: List of LoRA trigger words to preserve
    
    Returns:
        Dict with prompt_1, prompt_2, and metadata
    """
    
    if skip_generation:
        logger.debug("Skipping dual prompt generation")
        return {
            "prompt_1": action,
            "prompt_2": action,
            "skipped": True,
            "lora_triggers": lora_triggers or []
        }
    
    try:
        dual_prompt_instruction = _build_dual_prompt_instruction(action)
        
        logger.debug(f"Generating dual prompts for action: {action}")
        
        # Generate response using GGUF model
        response_text = generate_response(
            prompt=dual_prompt_instruction,
            image_url=None,
            max_tokens=500,
            temperature=0.8
        )
        
        result = _parse_dual_prompt_response(response_text, action, lora_triggers)
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating dual prompts: {e}", exc_info=True)
        return {
            "prompt_1": action,
            "prompt_2": action,
            "error": str(e),
            "lora_triggers": lora_triggers or []
        }


def _build_text_enhancement_prompt(prompt: str) -> str:
    """Build enhancement prompt for text-only input."""
    return f"""Enhance this adult content prompt with more detail and specificity:

Original: "{prompt}"

Return JSON:
{{
  "original": "{prompt}",
  "enhanced": "enhanced prompt with more detail",
  "suggested_keywords": ["keyword1", "keyword2"],
  "style_notes": "any style or artistic direction",
  "quality_modifiers": ["modifier1", "modifier2"]
}}

Make it more specific without changing the core action. Return ONLY JSON."""


def _build_image_enhancement_prompt(original: str, image_desc: str) -> str:
    """Build enhancement prompt for image-based input."""
    return f"""Enhance this prompt to match the current image state:

Current image: {image_desc}
Action prompt: "{original}"

Return JSON:
{{
  "enhanced": "enhanced prompt that flows from current state to action",
  "pose_continuity": "how the pose should transition",
  "suggested_loras": ["lora1", "lora2"],
  "consistency_notes": "notes on visual consistency"
}}

Ensure smooth transition from current state. Return ONLY JSON."""


def _build_dual_prompt_instruction(action: str) -> str:
    """Build instruction for generating two prompt variations."""
    return f"""Generate 2 different prompt variations for text-to-video of this action:

Action: "{action}"

Return JSON:
{{
  "prompt_1": "first detailed variation focusing on [aspect]",
  "prompt_2": "second detailed variation focusing on [different aspect]",
  "variations": "explain the differences",
  "shared_elements": "core elements preserved in both"
}}

Keep both coherent and detailed. Return ONLY JSON."""


def _parse_enhancement_response(response: str, original: str, lora_triggers: Optional[List[str]] = None) -> Dict[str, Any]:
    """Parse enhancement response and preserve LoRA triggers + WAN trigger words."""
    try:
        # Extract JSON from response
        start = response.find("{")
        end = response.rfind("}") + 1
        
        if start == -1 or end == 0:
            return {
                "original": original,
                "enhanced": original,
                "lora_triggers": lora_triggers or [],
                "parse_error": True
            }
        
        json_str = response[start:end]
        data = json.loads(json_str)
        
        # Ensure LoRA triggers are preserved in enhanced prompt
        enhanced = data.get("enhanced", original)
        
        # Detect intents and add WAN trigger words if not already present
        intents = detect_lora_intents(enhanced)
        wan_triggers = get_trigger_words(intents, enhanced)
        
        if wan_triggers:
            enhanced = f"{wan_triggers}, {enhanced}".strip()
        
        # Add manual LoRA triggers if provided
        if lora_triggers:
            for trigger in lora_triggers:
                if trigger.lower() not in enhanced.lower():
                    enhanced = f"{trigger}, {enhanced}"
            enhanced = enhanced.strip()
        
        data["enhanced"] = enhanced
        data["lora_triggers"] = lora_triggers or []
        
        return data
        
    except json.JSONDecodeError:
        return {
            "original": original,
            "enhanced": original,
            "lora_triggers": lora_triggers or [],
            "parse_error": True
        }


def _parse_dual_prompt_response(response: str, action: str, lora_triggers: Optional[List[str]] = None) -> Dict[str, Any]:
    """Parse dual prompt response and preserve LoRA triggers + WAN trigger words."""
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        
        if start == -1 or end == 0:
            return {
                "prompt_1": action,
                "prompt_2": action,
                "lora_triggers": lora_triggers or [],
                "parse_error": True
            }
        
        json_str = response[start:end]
        data = json.loads(json_str)
        
        # Detect intents from action and add WAN trigger words to both prompts
        intents = detect_lora_intents(action)
        wan_triggers = get_trigger_words(intents, action)
        
        # Process both prompts
        if lora_triggers or wan_triggers:
            for i in [1, 2]:
                key = f"prompt_{i}"
                prompt = data.get(key, action)
                
                # Add WAN triggers
                if wan_triggers and wan_triggers.lower() not in prompt.lower():
                    prompt = f"{wan_triggers}, {prompt}"
                
                # Add manual LoRA triggers
                if lora_triggers:
                    for trigger in lora_triggers:
                        if trigger.lower() not in prompt.lower():
                            prompt = f"{trigger}, {prompt}"
                
                data[key] = prompt.strip()
        
        data["lora_triggers"] = lora_triggers or []
        
        return data
        
    except json.JSONDecodeError:
        return {
            "prompt_1": action,
            "prompt_2": action,
            "lora_triggers": lora_triggers or [],
            "parse_error": True
        }
