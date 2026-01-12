#!/usr/bin/env python3
"""
QWEN API Client Example
Demonstrates how to use the API endpoints
"""

import requests
import base64
import json
from pathlib import Path
from typing import Optional

class QWENAPIClient:
    """Client for QWEN API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> dict:
        """Check API health."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def analyze_feasibility(
        self,
        image_path: str,
        action: str,
        skip_analysis: bool = False
    ) -> dict:
        """Analyze action feasibility."""
        
        # Load image as base64
        with open(image_path, 'rb') as f:
            image_b64 = base64.b64encode(f.read()).decode()
        
        response = self.session.post(
            f"{self.base_url}/analyze-feasibility",
            json={
                "image_base64": image_b64,
                "action": action,
                "skip_analysis": skip_analysis
            }
        )
        response.raise_for_status()
        return response.json()
    
    def enhance_prompt(
        self,
        prompt: str,
        lora_triggers: Optional[list] = None,
        skip_enhancement: bool = False
    ) -> dict:
        """Enhance text prompt."""
        
        response = self.session.post(
            f"{self.base_url}/enhance-prompt",
            json={
                "prompt": prompt,
                "skip_enhancement": skip_enhancement,
                "lora_triggers": lora_triggers or []
            }
        )
        response.raise_for_status()
        return response.json()
    
    def enhance_image_prompt(
        self,
        prompt: str,
        image_description: str = "",
        lora_triggers: Optional[list] = None,
        skip_enhancement: bool = False
    ) -> dict:
        """Enhance prompt based on image context."""
        
        response = self.session.post(
            f"{self.base_url}/enhance-image-prompt",
            json={
                "prompt": prompt,
                "image_description": image_description,
                "skip_enhancement": skip_enhancement,
                "lora_triggers": lora_triggers or []
            }
        )
        response.raise_for_status()
        return response.json()
    
    def generate_dual_prompts(
        self,
        action: str,
        lora_triggers: Optional[list] = None,
        skip_generation: bool = False
    ) -> dict:
        """Generate two prompt variations."""
        
        response = self.session.post(
            f"{self.base_url}/generate-dual-prompts",
            json={
                "action": action,
                "skip_generation": skip_generation,
                "lora_triggers": lora_triggers or []
            }
        )
        response.raise_for_status()
        return response.json()
    
    def text_to_video(
        self,
        action: str,
        lora_triggers: Optional[list] = None,
        num_prompts: int = 2,
        skip_qwen: bool = False
    ) -> dict:
        """Generate prompts for text-to-video."""
        
        response = self.session.post(
            f"{self.base_url}/text-to-video",
            json={
                "action": action,
                "skip_qwen": skip_qwen,
                "lora_triggers": lora_triggers or [],
                "num_prompts": num_prompts
            }
        )
        response.raise_for_status()
        return response.json()
    
    def text_to_image(
        self,
        prompt: str,
        lora_triggers: Optional[list] = None,
        skip_qwen: bool = False
    ) -> dict:
        """Generate prompt for text-to-image."""
        
        response = self.session.post(
            f"{self.base_url}/text-to-image",
            json={
                "prompt": prompt,
                "skip_qwen": skip_qwen,
                "lora_triggers": lora_triggers or []
            }
        )
        response.raise_for_status()
        return response.json()
    
    def image_to_video(
        self,
        image_path: str,
        action: str,
        lora_triggers: Optional[list] = None,
        skip_feasibility: bool = False,
        skip_enhancement: bool = False
    ) -> dict:
        """Generate video prompts from image and action."""
        
        # Load image
        with open(image_path, 'rb') as f:
            image_b64 = base64.b64encode(f.read()).decode()
        
        response = self.session.post(
            f"{self.base_url}/image-to-video",
            json={
                "image_base64": image_b64,
                "action": action,
                "skip_feasibility": skip_feasibility,
                "skip_enhancement": skip_enhancement,
                "lora_triggers": lora_triggers or []
            }
        )
        response.raise_for_status()
        return response.json()


def example_feasibility_analysis():
    """Example: Analyze action feasibility."""
    print("\n" + "="*60)
    print("EXAMPLE: Feasibility Analysis")
    print("="*60)
    
    client = QWENAPIClient()
    
    try:
        # You need an actual image file for this
        image_path = "test_image.jpg"
        
        result = client.analyze_feasibility(
            image_path=image_path,
            action="solo masturbation fingering"
        )
        
        print(f"\n✅ Analysis Success: {result['success']}")
        
        if result['success']:
            data = result['data']
            print(f"\nFeasibility Score: {data['feasibility_score']:.1%}")
            print(f"Hallucination Risk: {data['hallucination_risk']}")
            print(f"Missing Elements: {', '.join(data['missing_elements'])}")
            print(f"\nRecommendation:")
            print(f"  {data['recommended_approach'][:100]}...")
    
    except FileNotFoundError:
        print("⚠️  Test image not found. Skipping feasibility example.")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_text_enhancement():
    """Example: Enhance text prompt."""
    print("\n" + "="*60)
    print("EXAMPLE: Text Prompt Enhancement")
    print("="*60)
    
    client = QWENAPIClient()
    
    try:
        result = client.enhance_prompt(
            prompt="woman in lingerie",
            lora_triggers=["wan", "pussy_lora"]
        )
        
        print(f"\n✅ Enhancement Success: {result['success']}")
        
        if result['success']:
            data = result['data']
            print(f"\nOriginal: {data['original']}")
            print(f"Enhanced: {data['enhanced']}")
            print(f"LoRA Triggers: {', '.join(data['lora_triggers'])}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_dual_prompts():
    """Example: Generate dual prompts."""
    print("\n" + "="*60)
    print("EXAMPLE: Dual Prompt Generation")
    print("="*60)
    
    client = QWENAPIClient()
    
    try:
        result = client.generate_dual_prompts(
            action="woman dancing",
            lora_triggers=["wan"]
        )
        
        print(f"\n✅ Generation Success: {result['success']}")
        
        if result['success']:
            data = result['data']
            print(f"\nPrompt 1:\n  {data['prompt_1']}")
            print(f"\nPrompt 2:\n  {data['prompt_2']}")
            print(f"\nDifferences:")
            print(f"  {data.get('variations', 'N/A')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_text_to_video():
    """Example: Text-to-video workflow."""
    print("\n" + "="*60)
    print("EXAMPLE: Text-to-Video Workflow")
    print("="*60)
    
    client = QWENAPIClient()
    
    try:
        result = client.text_to_video(
            action="woman dancing sensually",
            lora_triggers=["wan"],
            num_prompts=2
        )
        
        print(f"\n✅ Workflow Success: {result['success']}")
        print(f"Action: {result['action']}")
        print(f"Generated Prompts: {len(result['prompts'])}")
        
        for i, prompt in enumerate(result['prompts'], 1):
            print(f"\nPrompt {i}:")
            print(f"  {prompt}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_text_to_image():
    """Example: Text-to-image workflow."""
    print("\n" + "="*60)
    print("EXAMPLE: Text-to-Image Workflow")
    print("="*60)
    
    client = QWENAPIClient()
    
    try:
        result = client.text_to_image(
            prompt="woman smiling",
            lora_triggers=["wan"]
        )
        
        print(f"\n✅ Workflow Success: {result['success']}")
        print(f"Original: {result['original_prompt']}")
        print(f"Enhanced: {result['enhanced_prompt']}")
        print(f"LoRA Triggers: {', '.join(result['lora_triggers'])}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def example_health_check():
    """Example: Health check."""
    print("\n" + "="*60)
    print("EXAMPLE: Health Check")
    print("="*60)
    
    client = QWENAPIClient()
    
    try:
        result = client.health_check()
        
        print(f"\n✅ API Status: {result['status']}")
        print(f"Model Loaded: {result['model_loaded']}")
        print(f"Device: {result['device']}")
        print(f"Message: {result['message']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the API is running: python run.py")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("QWEN API Client Examples")
    print("="*60)
    
    # Try health check first
    try:
        example_health_check()
    except Exception as e:
        print(f"\n❌ Could not connect to API: {e}")
        print("Please start the API server first:")
        print("  python run.py")
        return
    
    # Run examples
    example_text_enhancement()
    example_dual_prompts()
    example_text_to_video()
    example_text_to_image()
    example_feasibility_analysis()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
