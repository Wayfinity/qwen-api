# QWEN VLM API - Production Ready Setup

Complete QWEN2.5-VL integration for RTX Ada 2000 with prompt enhancement, action feasibility analysis, and LoRA management.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
python run.py

# In another terminal, run examples
python examples.py

# Access API documentation
# http://localhost:8000/docs
```

## 📋 Features

### ✅ Core Capabilities

- **Action Feasibility Analysis** - Judge if an action is possible given a current image
- **Prompt Enhancement** - Improve text prompts with detail and specificity
- **Dual Prompt Generation** - Create 2 variations for text-to-video generation
- **LoRA Trigger Integration** - Preserve and manage LoRA trigger words
- **Combined Workflows** - Full text-to-image, text-to-video, and image-to-video pipelines

### ✅ GPU Optimized
- Built for NVIDIA RTX Ada 2000 (supports any CUDA-capable GPU)
- Automatic device detection (CUDA/CPU)
- Efficient memory management
- Lazy model loading on first request
- Model caching between requests

### ✅ Production Ready
- FastAPI with Pydantic validation
- Comprehensive error handling
- Full API documentation (Swagger/ReDoc)
- Health check endpoints
- Structured logging
- CORS support

## 📁 Project Structure

```
qwen-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & endpoints
│   └── schemas.py           # Pydantic request/response models
├── models/
│   ├── __init__.py
│   ├── qwen_loader.py       # QWEN model loading (singleton)
│   ├── feasibility_analyzer.py  # Action feasibility analysis
│   └── prompt_enhancer.py   # Prompt enhancement & generation
├── utils/
│   ├── __init__.py
│   ├── helpers.py           # Utility functions (JSON extraction, etc.)
│   └── lora_manager.py      # LoRA configuration & management
├── run.py                   # Startup script
├── examples.py              # Client usage examples
├── requirements.txt         # Python dependencies
├── API_DOCUMENTATION.md     # Complete API docs
└── README.md               # This file
```

## 🔧 Installation

### System Requirements
- Ubuntu 20.04+, macOS, or Windows with WSL2
- NVIDIA RTX Ada 2000 (or compatible GPU with CUDA support)
- Python 3.10+
- 16GB+ RAM (8GB for model + 8GB for OS/buffers)

### Step 1: Clone/Setup Project

```bash
cd /Users/davidadams/qwen-api
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **torch** - PyTorch with CUDA support
- **transformers** - QWEN model library
- **pillow** - Image processing

### Step 4: Verify Installation

```bash
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
python -c "from transformers import AutoProcessor; print('✅ Transformers installed')"
```

## ▶️ Running the API

### Development Mode (with auto-reload)

```bash
python run.py --reload
```

### Production Mode

```bash
python run.py --workers 4
```

### Custom Configuration

```bash
python run.py --host 0.0.0.0 --port 8000 --workers 2
```

### API will start at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Run Example Client

```bash
python examples.py
```

This runs several example workflows demonstrating:
1. Health check
2. Text prompt enhancement
3. Dual prompt generation
4. Text-to-video workflow
5. Text-to-image workflow
6. Feasibility analysis

## 📚 API Endpoints

### Primary Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | API health & model status |
| `/analyze-feasibility` | POST | Analyze action feasibility |
| `/enhance-prompt` | POST | Enhance text prompts |
| `/enhance-image-prompt` | POST | Enhance prompts with image context |
| `/generate-dual-prompts` | POST | Generate 2 prompt variations |

### Workflow Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/text-to-image` | POST | Complete text-to-image pipeline |
| `/text-to-video` | POST | Complete text-to-video pipeline |
| `/image-to-video` | POST | Complete image-to-video pipeline |

## 🎯 Usage Examples

### Example 1: Enhance Text Prompt

```python
import requests

response = requests.post(
    "http://localhost:8000/enhance-prompt",
    json={
        "prompt": "woman in lingerie",
        "lora_triggers": ["wan", "pussy_lora"]
    }
)

result = response.json()
print(result['data']['enhanced'])
# Output: "wan, pussy_lora, detailed woman in elegant lingerie..."
```

### Example 2: Analyze Feasibility

```python
import requests
import base64

# Load image
with open("image.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/analyze-feasibility",
    json={
        "image_base64": image_b64,
        "action": "solo masturbation fingering"
    }
)

result = response.json()
data = result['data']
print(f"Feasibility: {data['feasibility_score']:.1%}")
print(f"Risk: {data['hallucination_risk']}")
print(f"Blockers: {data['blockers']}")
```

### Example 3: Generate Dual Prompts

```python
response = requests.post(
    "http://localhost:8000/generate-dual-prompts",
    json={
        "action": "woman dancing",
        "lora_triggers": ["wan"]
    }
)

result = response.json()
print("Prompt 1:", result['data']['prompt_1'])
print("Prompt 2:", result['data']['prompt_2'])
```

### Example 4: Complete Image-to-Video Workflow

```python
import base64

with open("image.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/image-to-video",
    json={
        "image_base64": image_b64,
        "action": "masturbation",
        "lora_triggers": ["pussy_lora"]
    }
)

result = response.json()

# Check feasibility
if result['feasibility']['feasibility_score'] > 0.5:
    prompt = result['enhanced_prompt']
    print(f"Generate video with: {prompt}")
else:
    print(f"Not feasible: {result['feasibility']['recommended_approach']}")
```

## 🔐 LoRA Management

### Built-in LoRAs

| Name | Trigger | Category | Purpose |
|------|---------|----------|---------|
| `wan_lora` | wan | expression | Facial expressions |
| `penis_lora` | penis | genital | Penis generation |
| `pussy_lora` | pussy | genital | Vagina/vulva generation |
| `arousal_lora` | aroused | expression | Arousal indicators |
| `clothing_removal_lora` | clothing_removed | clothing | Clothing transitions |
| `spread_lora` | spread | position | Leg spreading |
| `close_up_lora` | close_up | framing | Close-up details |

### Adding Custom LoRAs

Edit [utils/lora_manager.py](utils/lora_manager.py):

```python
from utils.lora_manager import LoRA, add_custom_loras

custom_loras = {
    "my_lora": LoRA(
        name="my_lora",
        trigger_word="my_trigger",
        description="My custom LoRA",
        category="custom"
    )
}

add_custom_loras(custom_loras)
```

## ⚙️ Configuration

### Environment Variables

```bash
# GPU Selection
export CUDA_VISIBLE_DEVICES=0

# Hugging Face Cache
export HF_HOME=/path/to/cache

# Logging Level
export LOG_LEVEL=DEBUG
```

### Model Selection

In [models/qwen_loader.py](models/qwen_loader.py):

```python
# Change model (line ~17)
QWEN_MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"  # 7B
# Or use 3B for faster inference:
# QWEN_MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"
```

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| **GPU Memory** | ~14GB (7B) or ~7GB (3B) |
| **First Load** | 5-10 seconds |
| **Feasibility Analysis** | 2-3 seconds per image |
| **Prompt Enhancement** | 1-2 seconds |
| **Throughput** | 30-50 tokens/sec |
| **Concurrent Requests** | 2-4 (depends on GPU memory) |

## 🔍 Troubleshooting

### CUDA Not Available

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

**Solution**: Install CUDA and cuDNN for your GPU driver version.

### Out of Memory

1. Use smaller model: `Qwen/Qwen2.5-VL-3B-Instruct`
2. Reduce `max_tokens` in generation
3. Reduce image size
4. Clear cache: `torch.cuda.empty_cache()`

### Model Downloading Slowly

First download may be slow (4GB model). Subsequent requests use cache:
```
~/.cache/huggingface/hub/
```

### API Won't Start

Check logs:
```bash
python run.py 2>&1 | grep -i error
```

Verify all dependencies:
```bash
pip list | grep -E "torch|transformers|fastapi"
```

## 📖 Documentation

- **Full API Docs**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Pydantic Models**: See [app/schemas.py](app/schemas.py)
- **LoRA Configuration**: See [utils/lora_manager.py](utils/lora_manager.py)

## 🚀 Deployment

### Docker (Optional)

```dockerfile
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

Build and run:
```bash
docker build -t qwen-api .
docker run --gpus all -p 8000:8000 qwen-api
```

### Production Server

Use with nginx as reverse proxy:

```nginx
upstream qwen_api {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://qwen_api;
    }
}
```

## 📝 Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Description"
}
```

### Error Response

```json
{
  "success": false,
  "data": { ... },
  "error": "Error message",
  "message": "What went wrong"
}
```

## 🤝 Integration

### With Existing Pipeline

1. Replace prompt generation with `/text-to-image` endpoint
2. Add feasibility check before expensive video generation
3. Use `/image-to-video` for action continuation
4. All LoRA triggers automatically managed

### With External Services

```python
# Get enhanced prompt from QWEN
response = requests.post(
    "http://localhost:8000/text-to-image",
    json={"prompt": user_prompt, "lora_triggers": lora_list}
)
enhanced_prompt = response.json()['enhanced_prompt']

# Pass to image generation service
image = generate_image(enhanced_prompt)
```

## 📄 License

[Your License Here]

## 🆘 Support

For issues or questions:
1. Check logs: `tail -f qwen_api.log`
2. Check documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. Test with examples: `python examples.py`
4. Verify CUDA: `python -c "import torch; print(torch.cuda.is_available())"`

---

**Version**: 1.0.0  
**Updated**: 2026-01-12  
**Model**: QWEN2.5-VL-7B-Instruct  
**GPU**: NVIDIA RTX Ada 2000+
