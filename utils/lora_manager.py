"""
LoRA Configuration and Management
Handles LoRA trigger words and model selection
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class LoRA:
    """LoRA model configuration."""
    name: str
    trigger_word: str
    description: str
    category: str  # "genital", "clothing", "position", "expression", etc.
    compatible_with: List[str] = None  # List of base model names


# Default LoRA configurations
DEFAULT_LORAS = {
    "wan_lora": LoRA(
        name="wan_lora",
        trigger_word="wan",
        description="Wan facial expression and arousal indicator",
        category="expression"
    ),
    "penis_lora": LoRA(
        name="penis_lora",
        trigger_word="penis",
        description="Enhanced penis generation and visibility",
        category="genital"
    ),
    "pussy_lora": LoRA(
        name="pussy_lora",
        trigger_word="pussy",
        description="Enhanced pussy/vagina generation and visibility",
        category="genital"
    ),
    "arousal_lora": LoRA(
        name="arousal_lora",
        trigger_word="aroused",
        description="Arousal indicators and physical responses",
        category="expression"
    ),
    "clothing_removal_lora": LoRA(
        name="clothing_removal_lora",
        trigger_word="clothing_removed",
        description="Assists with clothing removal transitions",
        category="clothing"
    ),
    "spread_lora": LoRA(
        name="spread_lora",
        trigger_word="spread",
        description="Leg spreading and vulva exposure",
        category="position"
    ),
    "close_up_lora": LoRA(
        name="close_up_lora",
        trigger_word="close_up",
        description="Close-up details and focus",
        category="framing"
    ),
}


class LoRAManager:
    """Manages LoRA configurations and selection."""
    
    def __init__(self, custom_loras: Optional[Dict[str, LoRA]] = None):
        """
        Initialize LoRA manager.
        
        Args:
            custom_loras: Custom LoRA configurations to add/override defaults
        """
        self.loras = DEFAULT_LORAS.copy()
        if custom_loras:
            self.loras.update(custom_loras)
        
        logger.info(f"Initialized LoRA manager with {len(self.loras)} models")
    
    def get_lora(self, name: str) -> Optional[LoRA]:
        """Get LoRA by name."""
        return self.loras.get(name)
    
    def get_trigger_word(self, lora_name: str) -> Optional[str]:
        """Get trigger word for a LoRA."""
        lora = self.get_lora(lora_name)
        return lora.trigger_word if lora else None
    
    def get_trigger_words(self, lora_names: List[str]) -> List[str]:
        """Get trigger words for multiple LoRAs."""
        triggers = []
        for name in lora_names:
            trigger = self.get_trigger_word(name)
            if trigger:
                triggers.append(trigger)
        return triggers
    
    def list_loras(self, category: Optional[str] = None) -> Dict[str, LoRA]:
        """List all LoRAs, optionally filtered by category."""
        if category:
            return {
                name: lora for name, lora in self.loras.items()
                if lora.category == category
            }
        return self.loras
    
    def list_categories(self) -> List[str]:
        """List all available categories."""
        categories = set()
        for lora in self.loras.values():
            categories.add(lora.category)
        return sorted(list(categories))
    
    def suggest_loras_for_action(self, action: str) -> List[str]:
        """
        Suggest LoRAs based on action description.
        
        Args:
            action: Action description (e.g., "solo masturbation fingering")
        
        Returns:
            List of suggested LoRA names
        """
        suggested = []
        action_lower = action.lower()
        
        # Keywords that suggest specific LoRAs
        lora_keywords = {
            "penis_lora": ["penis", "cock", "dick", "masturbation", "handjob", "blowjob"],
            "pussy_lora": ["pussy", "vagina", "vulva", "masturbation", "fingering", "clit"],
            "arousal_lora": ["aroused", "horny", "excited", "moaning"],
            "spread_lora": ["spread", "legs", "open", "exposing"],
            "clothing_removal_lora": ["undress", "remove", "stripping", "naked", "nude"],
            "close_up_lora": ["close", "closeup", "zoom", "detail"],
            "wan_lora": ["wan", "expression", "face", "pleasure"],
        }
        
        for lora_name, keywords in lora_keywords.items():
            if any(keyword in action_lower for keyword in keywords):
                suggested.append(lora_name)
        
        return suggested
    
    def format_prompt_with_loras(self, prompt: str, lora_names: List[str]) -> str:
        """
        Format prompt with LoRA trigger words.
        Adds trigger words to the beginning of the prompt.
        
        Args:
            prompt: Original prompt
            lora_names: List of LoRA names to apply
        
        Returns:
            Formatted prompt with trigger words
        """
        triggers = self.get_trigger_words(lora_names)
        
        if not triggers:
            return prompt
        
        # Remove duplicates and maintain order
        unique_triggers = []
        seen = set()
        for trigger in triggers:
            if trigger not in seen:
                unique_triggers.append(trigger)
                seen.add(trigger)
        
        # Prepend triggers to prompt
        trigger_string = ", ".join(unique_triggers)
        
        # Avoid duplicate triggers in prompt
        if trigger_string not in prompt:
            formatted = f"{trigger_string}, {prompt}"
        else:
            formatted = prompt
        
        return formatted.strip()
    
    def extract_trigger_words_from_prompt(self, prompt: str) -> List[str]:
        """
        Extract recognized trigger words from a prompt.
        
        Args:
            prompt: Prompt text
        
        Returns:
            List of recognized trigger words found
        """
        found_triggers = []
        prompt_lower = prompt.lower()
        
        for lora in self.loras.values():
            if lora.trigger_word.lower() in prompt_lower:
                found_triggers.append(lora.trigger_word)
        
        return found_triggers


# Global LoRA manager instance
_lora_manager = None


def get_lora_manager() -> LoRAManager:
    """Get global LoRA manager instance (lazy singleton)."""
    global _lora_manager
    
    if _lora_manager is None:
        _lora_manager = LoRAManager()
    
    return _lora_manager


def add_custom_loras(custom_loras: Dict[str, LoRA]):
    """Add or override LoRA configurations."""
    global _lora_manager
    
    manager = get_lora_manager()
    manager.loras.update(custom_loras)
    logger.info(f"Added {len(custom_loras)} custom LoRA configurations")
