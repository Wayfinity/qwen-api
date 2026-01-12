# Project Structure Overview

## 📁 Complete Directory Layout

```
qwen-api/
│
├── 📄 Core Files
│   ├── run.py                          # Startup script with environment checks
│   ├── examples.py                     # Client usage examples
│   ├── requirements.txt                # Python dependencies
│   └── quickstart.sh                   # Quick setup script
│
├── 📁 app/                             # FastAPI Application
│   ├── __init__.py                     # Package marker
│   ├── main.py                         # FastAPI app & 8 endpoints
│   │   ├── GET /health
│   │   ├── GET /
│   │   ├── POST /analyze-feasibility
│   │   ├── POST /enhance-prompt
│   │   ├── POST /enhance-image-prompt
│   │   ├── POST /generate-dual-prompts
│   │   ├── POST /text-to-image
│   │   ├── POST /text-to-video
│   │   └── POST /image-to-video
│   └── schemas.py                      # Pydantic models for validation
│       ├── AnalyzeFeasibilityRequest/Response
│       ├── EnhancePromptRequest/Response
│       ├── GenerateDualPromptsRequest/Response
│       ├── TextToImageRequest/Response
│       ├── TextToVideoRequest/Response
│       ├── ImageToVideoRequest/Response
│       └── HealthCheckResponse
│
├── 📁 models/                          # ML Models & Analysis
│   ├── __init__.py
│   ├── qwen_loader.py                  # QWEN model loading
│   │   ├── load_qwen_model()           # Lazy singleton loader
│   │   ├── ensure_cuda_available()     # CUDA check
│   │   ├── unload_qwen_model()         # Cleanup
│   │   └── get_device()                # Device info
│   │
│   ├── feasibility_analyzer.py         # Action feasibility analysis
│   │   ├── analyze_action_feasibility()
│   │   ├── _build_feasibility_prompt()
│   │   └── _load_image()
│   │
│   └── prompt_enhancer.py              # Prompt enhancement
│       ├── enhance_text_prompt()       # Text enhancement
│       ├── enhance_image_prompt()      # Image-aware enhancement
│       ├── generate_dual_prompts_for_video()  # Dual generation
│       ├── _build_text_enhancement_prompt()
│       ├── _build_image_enhancement_prompt()
│       ├── _parse_enhancement_response()
│       └── _parse_dual_prompt_response()
│
├── 📁 utils/                           # Utilities & Configuration
│   ├── __init__.py
│   ├── helpers.py                      # Utility functions
│   │   ├── extract_json()              # JSON extraction from text
│   │   ├── merge_lora_triggers()       # LoRA management
│   │   ├── validate_image_base64()     # Image validation
│   │   └── format_feasibility_response()
│   │
│   └── lora_manager.py                 # LoRA Configuration
│       ├── LoRA class                  # LoRA definition
│       ├── LoRAManager class           # LoRA management
│       │   ├── get_lora()
│       │   ├── get_trigger_word()
│       │   ├── list_loras()
│       │   ├── suggest_loras_for_action()
│       │   ├── format_prompt_with_loras()
│       │   └── extract_trigger_words_from_prompt()
│       ├── DEFAULT_LORAS               # 7 built-in LoRAs
│       │   ├── wan_lora
│       │   ├── penis_lora
│       │   ├── pussy_lora
│       │   ├── arousal_lora
│       │   ├── clothing_removal_lora
│       │   ├── spread_lora
│       │   └── close_up_lora
│       ├── get_lora_manager()          # Singleton getter
│       └── add_custom_loras()          # Add custom LoRAs
│
└── 📄 Documentation
    ├── README.md                       # Project overview & quick start
    ├── API_DOCUMENTATION.md            # Complete API reference
    ├── CONFIGURATION.md                # Configuration options
    ├── IMPLEMENTATION_SUMMARY.md       # This implementation summary
    └── IMPLEMENTATION.md               # This file
```

## 🔄 Data Flow

### Text-to-Image Request Flow

```
Client Request
    ↓
POST /text-to-image
    ↓
Input Validation (Pydantic Schema)
    ↓
enhance_text_prompt() [models/prompt_enhancer.py]
    ↓
Load QWEN Model (models/qwen_loader.py)
    ↓
Build Enhancement Prompt
    ↓
Run QWEN Inference
    ↓
Extract JSON from Response (utils/helpers.py)
    ↓
Merge LoRA Triggers (utils/lora_manager.py)
    ↓
Format Response
    ↓
Return JSON Response
```

### Image-to-Video Request Flow

```
Client Request (with image + action)
    ↓
POST /image-to-video
    ↓
Input Validation + Image Decode
    ↓
analyze_action_feasibility() [models/feasibility_analyzer.py]
    ├─ Load Image
    ├─ Load QWEN Model
    ├─ Build Feasibility Prompt
    ├─ Run Inference
    └─ Extract Feasibility JSON
    ↓
enhance_image_prompt() [models/prompt_enhancer.py]
    ├─ Build Image-Aware Prompt
    ├─ Run Inference
    └─ Extract Enhancement JSON
    ↓
Merge Results + LoRA Triggers
    ↓
Return Combined Response
```

## 🎯 Key Components

### 1. QWEN Model Layer
- **File**: `models/qwen_loader.py`
- **Purpose**: Load and cache QWEN2.5-VL model
- **Pattern**: Lazy-loading singleton
- **Scope**: Module-level (one instance across all requests)

### 2. Analysis Layer
- **File**: `models/feasibility_analyzer.py`
- **Purpose**: Analyze action feasibility from images
- **Input**: Base64 image + action description
- **Output**: JSON with feasibility metrics

### 3. Enhancement Layer
- **File**: `models/prompt_enhancer.py`
- **Purpose**: Improve and generate prompts
- **Features**:
  - Text enhancement
  - Image-aware enhancement
  - Dual prompt generation

### 4. LoRA Management Layer
- **File**: `utils/lora_manager.py`
- **Purpose**: Manage LoRA triggers and configuration
- **Features**:
  - Preserve triggers in prompts
  - Suggest LoRAs for actions
  - Add custom LoRAs

### 5. API Layer
- **File**: `app/main.py`
- **Purpose**: FastAPI routes and request handling
- **Middleware**: CORS, logging
- **Lifecycle**: Model loading/unloading

## 📊 Request/Response Types

### Feasibility Analysis
```
Request: Base64 image + action string
Response: Feasibility score + blockers + recommendations
```

### Prompt Enhancement
```
Request: Prompt string + optional LoRA triggers
Response: Enhanced prompt + suggestions
```

### Dual Prompt Generation
```
Request: Action string + optional LoRA triggers
Response: Two prompt variations + metadata
```

### Combined Workflows
```
Text-to-Image: Text → Enhancement → Response
Text-to-Video: Action → Dual Prompts → Response
Image-to-Video: Image + Action → Analysis + Enhancement → Response
```

## 🔌 Integration Points

### Input Types
- Base64-encoded images (PNG/JPG)
- Text prompts/descriptions
- List of LoRA names
- Boolean skip flags

### Output Types
- Enhanced prompts with LoRA triggers
- Feasibility analysis JSON
- Health status
- Error messages with details

### Extensibility
- Add custom LoRAs in `utils/lora_manager.py`
- Customize prompts in `models/prompt_enhancer.py`
- Add endpoints in `app/main.py`
- Modify feasibility criteria in `models/feasibility_analyzer.py`

## 🚀 Startup Sequence

1. **Python Startup** (run.py)
   - Check environment
   - Validate dependencies

2. **FastAPI Initialization** (app/main.py)
   - Setup CORS middleware
   - Register routes

3. **Lifespan Events**
   - **Startup**: Load QWEN model into GPU memory
   - **Shutdown**: Unload model and clean VRAM

4. **Request Handling**
   - Validate input with Pydantic
   - Load model (cached)
   - Run inference
   - Format response

## 💾 Memory Management

### Model Caching
- Model loads once on first request
- Stays in VRAM for subsequent requests
- Unloads on API shutdown
- GPU memory: ~14GB (7B model)

### Image Processing
- Images loaded into CPU RAM temporarily
- Converted to PIL Image
- Deleted after processing
- Temporary files cleaned up

## 🔐 Security & Validation

### Input Validation
- Pydantic schemas validate all inputs
- Base64 images validated (PNG/JPG magic bytes)
- Prompt strings sanitized
- LoRA names validated against registry

### Error Handling
- Try/catch blocks around inference
- Graceful degradation
- Detailed error messages
- Partial responses on failure

## 📈 Scalability

### Current Setup
- Single GPU (RTX Ada 2000)
- Synchronous requests
- Model cached in memory
- ~2-4 concurrent requests

### For Production Scale
- Implement async/await
- Add request queuing
- Use GPU batch processing
- Multi-worker deployment
- Load balancing

## 📝 Code Organization

### By Responsibility
- **Loading**: `models/qwen_loader.py`
- **Analysis**: `models/feasibility_analyzer.py`
- **Enhancement**: `models/prompt_enhancer.py`
- **Configuration**: `utils/lora_manager.py`
- **Utilities**: `utils/helpers.py`
- **API**: `app/main.py`
- **Schemas**: `app/schemas.py`

### By Layer
- **Presentation**: FastAPI routes (app/main.py)
- **Business Logic**: Analysis & enhancement (models/)
- **Data Access**: Model loading (models/)
- **Configuration**: LoRA management (utils/)

## 🎓 Learning Path

1. Start with `README.md` for overview
2. Read `API_DOCUMENTATION.md` for endpoints
3. Run `examples.py` to see usage
4. Check `CONFIGURATION.md` for customization
5. Review `models/` for implementation details
6. See `utils/lora_manager.py` for extensibility

---

This structure is designed for:
- ✅ Easy maintenance
- ✅ Clear separation of concerns
- ✅ Easy testing
- ✅ Simple extension
- ✅ Production deployment
