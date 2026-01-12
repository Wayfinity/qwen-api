# QWEN API Configuration

This file documents the configuration options for the QWEN API.

## Server Configuration

### Port Configuration

Default: Port 8000

```bash
# Custom port
python run.py --port 8080

# Custom host and port
python run.py --host 0.0.0.0 --port 9000
```

## Model Configuration

### Model Selection

Edit `models/qwen_loader.py`:

```python
# Line 19 - Available options:
QWEN_MODEL_ID = "Qwen/Qwen2.5-VL-7B-Instruct"    # Full size (14GB)
QWEN_MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"    # Smaller (7GB)
```

### Generation Parameters

Adjust in `models/prompt_enhancer.py` and `models/feasibility_analyzer.py`:

```python
# Temperature (0.0 = deterministic, 1.0 = random)
temperature=0.7

# Max tokens to generate
max_new_tokens=400

# Top-P sampling (0.0-1.0)
top_p=0.9
```

## CUDA Configuration

### GPU Selection

```bash
# Use specific GPU
export CUDA_VISIBLE_DEVICES=0

# Use multiple GPUs
export CUDA_VISIBLE_DEVICES=0,1
```

### Memory Optimization

```python
# In qwen_loader.py - use fp32 instead of fp16 for better accuracy
torch_dtype=torch.float32  # Instead of torch.float16
```

## Logging Configuration

### Log Level

```bash
# Set in run.py
logging.basicConfig(level=logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR
```

### Log Output

Logs written to: `qwen_api.log` and stdout

## LoRA Configuration

### Add Custom LoRAs

Edit `utils/lora_manager.py`:

```python
from utils.lora_manager import LoRA

custom_loras = {
    "my_custom_lora": LoRA(
        name="my_custom_lora",
        trigger_word="my_trigger",
        description="Description of my LoRA",
        category="custom_category"
    )
}
```

### LoRA Categories

- `genital` - Penis/vagina generation
- `expression` - Facial expressions
- `clothing` - Clothing states
- `position` - Body positions
- `framing` - Camera framing
- `custom` - Custom categories

## API Request Configuration

### Max Request Size

FastAPI default: 25MB

To change, edit `app/main.py`:

```python
# Add to FastAPI initialization
max_request_size=100_000_000  # 100MB
```

### Timeouts

Set in client code:

```python
requests.post(url, json=data, timeout=30)  # 30 seconds
```

## CORS Configuration

Edit `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Specific domains
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
```

## Environment Variables

```bash
# HuggingFace Model Cache
export HF_HOME=/custom/path

# CUDA Device
export CUDA_VISIBLE_DEVICES=0

# Torch Settings
export TORCH_HOME=/custom/cache
export TRANSFORMERS_CACHE=/custom/cache
```

## Performance Tuning

### For Faster Inference

1. Use smaller model (3B instead of 7B)
2. Reduce `max_new_tokens` (256 instead of 400)
3. Set `temperature=0.1` (deterministic)

### For Better Quality

1. Use larger model (7B)
2. Increase `max_new_tokens` (600)
3. Set `temperature=0.7` (more variation)

### For GPU Memory

```python
# Reduce batch size
# Enable gradient checkpointing (if implementing training)
# Clear cache regularly
torch.cuda.empty_cache()
```

## Production Deployment

### Use Gunicorn + Uvicorn

```bash
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Environment for Production

```bash
export CUDA_VISIBLE_DEVICES=0
export HF_HOME=/var/cache/huggingface
export LOG_LEVEL=INFO

python run.py --workers 4 --host 127.0.0.1 --port 8000
```

## Health Checks

API includes health endpoint for monitoring:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "ok",
  "model_loaded": true,
  "device": "cuda"
}
```

## Security Considerations

1. **Input Validation**: All endpoints validate input with Pydantic
2. **Image Size Limits**: Images validated as PNG/JPG
3. **Base64 Validation**: Images must be properly encoded
4. **Prompt Sanitization**: LoRA triggers validated

## Monitoring

### Logs

Monitor real-time logs:
```bash
tail -f qwen_api.log
```

### CUDA Memory

```python
import torch
print(torch.cuda.memory_allocated() / 1e9, "GB")
print(torch.cuda.max_memory_allocated() / 1e9, "GB")
```

### API Usage

Implement logging middleware or use external monitoring (Prometheus, etc.)

## Common Issues & Solutions

### Issue: Model not loading
**Solution**: Check CUDA availability and disk space

### Issue: API slow
**Solution**: Check GPU memory, reduce batch size, use smaller model

### Issue: Out of memory errors
**Solution**: Restart API, use 3B model, reduce `max_new_tokens`

### Issue: CORS errors
**Solution**: Check CORS configuration in `app/main.py`

---

For more help, see [README.md](README.md) and [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
