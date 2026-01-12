# QWEN API - Complete Index

## 📚 Documentation Files

### Getting Started
1. **[README.md](README.md)** - Project overview and quick start
   - Installation steps
   - Running the API
   - Usage examples
   - Performance metrics
   - Troubleshooting

2. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What's included
   - Complete feature list
   - Architecture overview
   - Key features
   - LoRA integration
   - Next steps

### API Reference
3. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
   - 8 endpoint specifications
   - Request/response formats
   - Python client examples
   - LoRA management
   - Performance characteristics

4. **[STRUCTURE.md](STRUCTURE.md)** - Project organization
   - Directory layout
   - Data flow diagrams
   - Component descriptions
   - Integration points
   - Code organization

### Configuration & Usage
5. **[CONFIGURATION.md](CONFIGURATION.md)** - Configuration options
   - Server settings
   - Model selection
   - CUDA configuration
   - LoRA customization
   - Performance tuning
   - Security settings

6. **[CURL_EXAMPLES.sh](CURL_EXAMPLES.sh)** - HTTP API examples
   - All 8 endpoints with curl
   - Base64 encoding
   - Response formats
   - Common patterns
   - Troubleshooting

## 🔧 Application Files

### Core API
- **[app/main.py](app/main.py)** - FastAPI application
  - 8 HTTP endpoints
  - Request/response handling
  - CORS configuration
  - Model lifecycle management
  - Health checks

- **[app/schemas.py](app/schemas.py)** - Pydantic validation models
  - Request schemas
  - Response schemas
  - Type definitions
  - Field validation

### Machine Learning Models
- **[models/qwen_loader.py](models/qwen_loader.py)** - QWEN model loading
  - Lazy singleton loader
  - CUDA detection
  - Memory management
  - Model caching

- **[models/feasibility_analyzer.py](models/feasibility_analyzer.py)** - Action feasibility
  - Image loading
  - Feasibility analysis
  - JSON response generation
  - Hallucination risk assessment

- **[models/prompt_enhancer.py](models/prompt_enhancer.py)** - Prompt enhancement
  - Text prompt enhancement
  - Image-aware enhancement
  - Dual prompt generation
  - LoRA trigger preservation

### Utilities
- **[utils/helpers.py](utils/helpers.py)** - Helper functions
  - JSON extraction
  - Image validation
  - LoRA trigger merging
  - Response formatting

- **[utils/lora_manager.py](utils/lora_manager.py)** - LoRA management
  - LoRA definitions
  - LoRA manager class
  - 7 built-in LoRAs
  - Custom LoRA support
  - Action-to-LoRA suggestions

## 🚀 Execution Files

- **[run.py](run.py)** - API startup script
  - Environment checking
  - Dependency verification
  - Server startup
  - Configuration options

- **[examples.py](examples.py)** - Python client examples
  - QWENAPIClient class
  - 6 example workflows
  - Error handling
  - Complete usage patterns

- **[quickstart.sh](quickstart.sh)** - Quick setup script
  - Environment checks
  - Dependency installation
  - Virtual environment setup
  - Verification steps

## 🔗 Quick Links

### Start Here
```bash
# 1. Install
pip install -r requirements.txt

# 2. Run API
python run.py

# 3. Test
python examples.py
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

### Common Tasks

#### Enhance Text Prompt
**File**: [models/prompt_enhancer.py](models/prompt_enhancer.py)  
**Endpoint**: `POST /enhance-prompt`  
**Example**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#2-enhance-text-prompt)

#### Analyze Feasibility
**File**: [models/feasibility_analyzer.py](models/feasibility_analyzer.py)  
**Endpoint**: `POST /analyze-feasibility`  
**Example**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#1-analyze-action-feasibility)

#### Manage LoRAs
**File**: [utils/lora_manager.py](utils/lora_manager.py)  
**Built-in**: 7 default LoRAs (wan, penis, pussy, arousal, clothing_removal, spread, close_up)  
**Custom**: Add in [utils/lora_manager.py](utils/lora_manager.py#L21)

#### Generate Dual Prompts
**File**: [models/prompt_enhancer.py](models/prompt_enhancer.py)  
**Endpoint**: `POST /generate-dual-prompts`  
**Example**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#4-generate-dual-prompts)

#### Run Image-to-Video
**File**: [app/main.py](app/main.py)  
**Endpoint**: `POST /image-to-video`  
**Example**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#7-image-to-video)

## 📊 Feature Matrix

| Feature | File | Endpoint | Status |
|---------|------|----------|--------|
| Text Prompt Enhancement | prompt_enhancer.py | /enhance-prompt | ✅ |
| Image Feasibility Analysis | feasibility_analyzer.py | /analyze-feasibility | ✅ |
| Dual Prompt Generation | prompt_enhancer.py | /generate-dual-prompts | ✅ |
| Image-aware Enhancement | prompt_enhancer.py | /enhance-image-prompt | ✅ |
| LoRA Management | lora_manager.py | (Integrated) | ✅ |
| Text-to-Image Workflow | main.py | /text-to-image | ✅ |
| Text-to-Video Workflow | main.py | /text-to-video | ✅ |
| Image-to-Video Workflow | main.py | /image-to-video | ✅ |
| Health Checking | main.py | /health | ✅ |
| API Documentation | main.py | /docs | ✅ |

## 🎯 Code Map by Task

### I want to...

**Modify QWEN prompts**
→ Edit [models/prompt_enhancer.py](models/prompt_enhancer.py) function `_build_*_prompt()`

**Change model size**
→ Edit [models/qwen_loader.py](models/qwen_loader.py) line ~19 `QWEN_MODEL_ID`

**Add custom LoRAs**
→ Edit [utils/lora_manager.py](utils/lora_manager.py) add to `DEFAULT_LORAS` dict

**Change generation temperature**
→ Edit [models/prompt_enhancer.py](models/prompt_enhancer.py) and [models/feasibility_analyzer.py](models/feasibility_analyzer.py) `temperature` parameter

**Add new API endpoint**
→ Edit [app/main.py](app/main.py) add `@app.post()` function and schema in [app/schemas.py](app/schemas.py)

**Adjust image validation**
→ Edit [utils/helpers.py](utils/helpers.py) function `validate_image_base64()`

**Configure CORS**
→ Edit [app/main.py](app/main.py) around line ~60 `CORSMiddleware`

**Change port/host**
→ Run with flags: `python run.py --port 8080 --host 127.0.0.1`

**Enable auto-reload**
→ Run with flag: `python run.py --reload`

**Skip QWEN processing**
→ Use `skip_enhancement: true` or `skip_analysis: true` in request

**Suggest LoRAs for action**
→ Call `lora_manager.suggest_loras_for_action(action_string)`

## 🔍 File Dependencies

```
app/main.py
├── models/qwen_loader.py        (load_qwen_model)
├── models/feasibility_analyzer.py (analyze_action_feasibility)
├── models/prompt_enhancer.py     (enhance_text_prompt, etc)
├── utils/helpers.py             (format_feasibility_response)
└── app/schemas.py               (Pydantic models)

models/feasibility_analyzer.py
├── models/qwen_loader.py        (load_qwen_model)
└── utils/helpers.py             (extract_json)

models/prompt_enhancer.py
├── models/qwen_loader.py        (load_qwen_model)
└── utils/helpers.py             (extract_json)

utils/lora_manager.py
└── (no internal dependencies)
```

## 📈 Performance Tuning

| Goal | File to Edit | Change |
|------|--------------|--------|
| Faster responses | prompt_enhancer.py | ↓ max_tokens, ↑ temperature |
| Better quality | prompt_enhancer.py | ↑ max_tokens, use 7B model |
| Save GPU memory | qwen_loader.py | Use 3B model |
| Reduce latency | utils/helpers.py | Use skip flags |

## 🧪 Testing

**Health Check**
```bash
curl http://localhost:8000/health
```

**Example Workflows**
```bash
python examples.py
```

**Manual Testing**
```bash
bash CURL_EXAMPLES.sh
```

## 📋 Checklist for Deployment

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify CUDA: `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] Start API: `python run.py`
- [ ] Check health: `curl http://localhost:8000/health`
- [ ] Run examples: `python examples.py`
- [ ] Review API docs: http://localhost:8000/docs
- [ ] Test with your data
- [ ] Configure CORS if needed
- [ ] Add custom LoRAs if needed
- [ ] Deploy to production (Docker, etc.)

## 🆘 Getting Help

1. **Can't start API?**
   - Check: [CONFIGURATION.md](CONFIGURATION.md#troubleshooting)
   - Run: `python run.py --no-check` to skip environment validation

2. **API endpoint not working?**
   - See: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
   - Try: [examples.py](examples.py) for working examples

3. **Want to customize something?**
   - See: [CONFIGURATION.md](CONFIGURATION.md)
   - Code: Specific file locations above

4. **Need CURL examples?**
   - See: [CURL_EXAMPLES.sh](CURL_EXAMPLES.sh)

5. **Want to add features?**
   - See: [STRUCTURE.md](STRUCTURE.md) for code organization

## 📞 File Purposes (Quick Reference)

| File | Purpose | Language |
|------|---------|----------|
| run.py | Start server | Python |
| examples.py | Test client | Python |
| app/main.py | API routes | Python |
| app/schemas.py | Data validation | Python |
| models/qwen_loader.py | Load QWEN | Python |
| models/feasibility_analyzer.py | Analyze images | Python |
| models/prompt_enhancer.py | Enhance prompts | Python |
| utils/lora_manager.py | LoRA config | Python |
| utils/helpers.py | Utilities | Python |
| requirements.txt | Dependencies | Text |
| README.md | Overview | Markdown |
| API_DOCUMENTATION.md | API specs | Markdown |
| CONFIGURATION.md | Config options | Markdown |
| STRUCTURE.md | Code layout | Markdown |
| CURL_EXAMPLES.sh | HTTP examples | Bash |
| IMPLEMENTATION_SUMMARY.md | What's included | Markdown |
| quickstart.sh | Quick setup | Bash |

---

## 🎉 You're All Set!

Everything is documented and ready to use. Start with [README.md](README.md) then dive into [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

**Happy coding! 🚀**
