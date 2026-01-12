# QWEN API - Complete Documentation

## Overview

This API provides QWEN2.5-VL integration for prompt enhancement and action feasibility analysis, optimized for RTX Ada 2000 GPUs.

### Key Features

- **Action Feasibility Analysis**: Analyzes if an action is feasible given a current image
- **Prompt Enhancement**: Improves text prompts with more detail and specificity
- **Dual Prompt Generation**: Generates 2 variations for text-to-video
- **LoRA Integration**: Preserves LoRA trigger words in all prompts
- **Combined Endpoints**: Full workflows for text-to-image, text-to-video, and image-to-video

## Installation

```bash
cd /Users/davidadams/qwen-api
pip install -r requirements.txt
```

### CUDA Requirements

- NVIDIA RTX Ada 2000 GPU
- CUDA 12.1+
- cuDNN 8.x
- PyTorch with CUDA support

## Running the API

```bash
# Development mode
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Core Endpoints

### 1. Analyze Action Feasibility

**POST** `/analyze-feasibility`

Analyzes how feasible an action is given a current image.

**Request:**
```json
{
  "image_base64": "iVBORw0KGgo... (base64 PNG/JPG)",
  "action": "solo masturbation fingering",
  "skip_analysis": false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "feasibility_score": 0.0,
    "pose_similarity": 0.0,
    "current_pose": "standing upright, hands at sides",
    "current_clothing": ["shirt", "pants"],
    "target_action": "solo masturbation fingering",
    "missing_elements": ["clothing removal", "visible genitalia", "position change"],
    "needs_second_person": false,
    "needs_penis": true,
    "needs_vagina_visible": false,
    "needs_clothing_removal": true,
    "needs_position_change": "major",
    "hallucination_risk": "high",
    "recommended_approach": "This action cannot be achieved in the current image...",
    "blockers": ["clothing", "visibility of genitalia", "position"],
    "skipped": false,
    "error": null
  },
  "message": "Feasibility analysis complete"
}
```

**Parameters:**
- `image_base64`: Base64-encoded image (PNG/JPG)
- `action`: Target action to analyze
- `skip_analysis`: Skip QWEN processing (optional, default: false)

---

### 2. Enhance Text Prompt

**POST** `/enhance-prompt`

Enhances a text-only prompt for image generation. Preserves LoRA trigger words.

**Request:**
```json
{
  "prompt": "woman in lingerie",
  "skip_enhancement": false,
  "lora_triggers": ["wan", "pussy_lora"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original": "woman in lingerie",
    "enhanced": "wan, pussy_lora, detailed portrait of a woman in elegant lingerie, professional photography",
    "suggested_keywords": ["lingerie", "fashion", "portrait"],
    "style_notes": "Professional lighting, focus on details",
    "quality_modifiers": ["8k", "high quality", "detailed"],
    "lora_triggers": ["wan", "pussy_lora"],
    "skipped": false,
    "error": null
  },
  "message": "Prompt enhanced successfully"
}
```

---

### 3. Enhance Image Prompt

**POST** `/enhance-image-prompt`

Enhances a prompt based on current image context for image-to-video.

**Request:**
```json
{
  "prompt": "masturbation",
  "image_description": "woman standing, wearing bra and underwear",
  "skip_enhancement": false,
  "lora_triggers": ["pussy_lora"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original": "masturbation",
    "enhanced": "pussy_lora, woman continues from standing position, begins masturbating...",
    "pose_continuity": "smooth transition from standing to seated position",
    "suggested_loras": ["pussy_lora", "arousal_lora"],
    "consistency_notes": "Maintains visual consistency with original image",
    "lora_triggers": ["pussy_lora"],
    "skipped": false,
    "error": null
  },
  "message": "Image prompt enhanced successfully"
}
```

---

### 4. Generate Dual Prompts

**POST** `/generate-dual-prompts`

Generates 2 different prompt variations for text-to-video generation.

**Request:**
```json
{
  "action": "woman dancing",
  "skip_generation": false,
  "lora_triggers": ["wan"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "prompt_1": "wan, woman dancing gracefully with fluid movements, sensual motions",
    "prompt_2": "wan, woman dancing energetically with rhythmic body movements and confidence",
    "variations": "First focuses on sensuality, second on energy and movement",
    "shared_elements": "Both maintain the woman's facial expression and dancing focus",
    "lora_triggers": ["wan"],
    "skipped": false,
    "error": null
  },
  "message": "Dual prompts generated successfully"
}
```

---

## Combined Workflow Endpoints

### 5. Text-to-Video

**POST** `/text-to-video`

Complete text-to-video workflow.

**Request:**
```json
{
  "action": "woman dancing",
  "skip_qwen": false,
  "lora_triggers": ["wan"],
  "num_prompts": 2
}
```

**Response:**
```json
{
  "success": true,
  "action": "woman dancing",
  "prompts": [
    "wan, woman dancing gracefully with fluid movements",
    "wan, woman dancing energetically with rhythmic movements"
  ],
  "lora_triggers": ["wan"],
  "message": "Generated 2 prompts for video generation"
}
```

---

### 6. Text-to-Image

**POST** `/text-to-image`

Complete text-to-image workflow with prompt enhancement.

**Request:**
```json
{
  "prompt": "woman smiling",
  "skip_qwen": false,
  "lora_triggers": ["wan"]
}
```

**Response:**
```json
{
  "success": true,
  "original_prompt": "woman smiling",
  "enhanced_prompt": "wan, woman with beautiful smile, professional portrait photography",
  "lora_triggers": ["wan"],
  "message": "Prompt enhanced for image generation"
}
```

---

### 7. Image-to-Video

**POST** `/image-to-video`

Complete image-to-video workflow with feasibility analysis and enhancement.

**Request:**
```json
{
  "image_base64": "iVBORw0KGgo...",
  "action": "masturbation",
  "skip_feasibility": false,
  "skip_enhancement": false,
  "lora_triggers": ["pussy_lora"]
}
```

**Response:**
```json
{
  "success": true,
  "action": "masturbation",
  "feasibility": {
    "feasibility_score": 0.2,
    "hallucination_risk": "high",
    ...
  },
  "enhanced_prompt": "pussy_lora, woman begins masturbating...",
  "lora_triggers": ["pussy_lora"],
  "message": "Image-to-video analysis complete"
}
```

---

## LoRA Management

### Default LoRAs

The system includes these default LoRA configurations:

| Name | Trigger | Category | Purpose |
|------|---------|----------|---------|
| `wan_lora` | `wan` | expression | Facial expressions and arousal |
| `penis_lora` | `penis` | genital | Penis generation |
| `pussy_lora` | `pussy` | genital | Vagina/vulva generation |
| `arousal_lora` | `aroused` | expression | Arousal indicators |
| `clothing_removal_lora` | `clothing_removed` | clothing | Clothing removal transitions |
| `spread_lora` | `spread` | position | Leg spreading and exposure |
| `close_up_lora` | `close_up` | framing | Close-up details |

### Using LoRAs

LoRA trigger words are automatically:
1. Preserved in enhanced prompts
2. Added to the beginning of the final prompt
3. Never duplicated in the final output

**Example with multiple LoRAs:**

```python
# Request
{
  "prompt": "woman sitting",
  "lora_triggers": ["wan", "pussy_lora", "spread_lora"]
}

# Result
# Enhanced prompt: "wan, pussy_lora, spread_lora, woman sitting with detailed features..."
```

---

## Python Client Example

```python
import requests
import base64
from pathlib import Path

BASE_URL = "http://localhost:8000"

# Load image
image_path = Path("test_image.jpg")
with open(image_path, 'rb') as f:
    image_b64 = base64.b64encode(f.read()).decode()

# 1. Analyze feasibility
response = requests.post(
    f"{BASE_URL}/analyze-feasibility",
    json={
        "image_base64": image_b64,
        "action": "masturbation",
        "skip_analysis": False
    }
)
feasibility = response.json()
print(f"Feasibility Score: {feasibility['data']['feasibility_score']}")
print(f"Blockers: {feasibility['data']['blockers']}")

# 2. Enhance text prompt
response = requests.post(
    f"{BASE_URL}/enhance-prompt",
    json={
        "prompt": "woman masturbating",
        "lora_triggers": ["pussy_lora", "wan"]
    }
)
enhanced = response.json()
print(f"Enhanced: {enhanced['data']['enhanced']}")

# 3. Generate dual prompts
response = requests.post(
    f"{BASE_URL}/generate-dual-prompts",
    json={
        "action": "woman masturbating",
        "lora_triggers": ["pussy_lora"]
    }
)
dual = response.json()
print(f"Prompt 1: {dual['data']['prompt_1']}")
print(f"Prompt 2: {dual['data']['prompt_2']}")

# 4. Image-to-video workflow
response = requests.post(
    f"{BASE_URL}/image-to-video",
    json={
        "image_base64": image_b64,
        "action": "masturbation",
        "lora_triggers": ["pussy_lora"]
    }
)
result = response.json()
if result['feasibility']['feasibility_score'] > 0.5:
    print(f"Action is feasible: {result['enhanced_prompt']}")
else:
    print(f"Action not feasible: {result['feasibility']['recommended_approach']}")
```

---

## Configuration

### Modify LoRA Configuration

Edit [utils/lora_manager.py](utils/lora_manager.py) to add custom LoRAs:

```python
from utils.lora_manager import LoRA, add_custom_loras

custom_loras = {
    "custom_lora": LoRA(
        name="custom_lora",
        trigger_word="custom_trigger",
        description="Custom LoRA for specific effect",
        category="custom"
    )
}

add_custom_loras(custom_loras)
```

### Environment Variables

```bash
# CUDA device selection
export CUDA_VISIBLE_DEVICES=0

# Model cache directory
export HF_HOME=/path/to/cache
```

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **GPU** | NVIDIA RTX Ada 2000 |
| **Model** | Qwen2.5-VL-7B-Instruct |
| **Speed** | ~30-50 tokens/sec (image) |
| **Memory** | ~14GB VRAM (fp16) |
| **First Load** | ~5-10 seconds |
| **Cached Load** | <100ms |

---

## Troubleshooting

### CUDA Out of Memory

1. Use smaller model: `mlx-community/Qwen2.5-VL-3B-Instruct`
2. Reduce `max_tokens` in generation
3. Clear cache: `torch.cuda.empty_cache()`

### Model Not Loading

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

### API Errors

Check logs:
```bash
tail -f api.log
```

---

## API Response Format

All successful responses follow this format:

```json
{
  "success": true,
  "data": { ... },
  "message": "Description of what happened"
}
```

All error responses:

```json
{
  "success": false,
  "data": { ... },
  "error": "Error message",
  "message": "Description"
}
```

---

## Rate Limiting

No built-in rate limiting. For production, use nginx or API gateway.

---

## Security Notes

- Input validation on all fields
- Base64 image validation
- LoRA trigger words sanitized
- No arbitrary code execution

---

## License

[Add your license here]
