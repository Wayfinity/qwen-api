#!/bin/bash
# API Endpoint Examples - CURL Commands

# Start API first:
# python run.py

API_URL="http://localhost:8000"

echo "======================================"
echo "QWEN API - CURL Examples"
echo "======================================"
echo ""

# ============= HEALTH CHECK =============
echo "1️⃣  HEALTH CHECK"
echo "======================================"
echo ""
echo "Get API health status:"
echo ""
echo "curl -X GET '$API_URL/health'"
echo ""
curl -s -X GET "$API_URL/health" | python -m json.tool 2>/dev/null || echo "(API not running)"
echo ""
echo ""

# ============= ENHANCE PROMPT =============
echo "2️⃣  ENHANCE TEXT PROMPT"
echo "======================================"
echo ""
echo "Enhance a text prompt for image generation:"
echo ""
cat <<'EOF'
curl -X POST 'http://localhost:8000/enhance-prompt' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "woman in lingerie",
    "lora_triggers": ["wan", "pussy_lora"],
    "skip_enhancement": false
  }'
EOF
echo ""
echo ""

# ============= GENERATE DUAL PROMPTS =============
echo "3️⃣  GENERATE DUAL PROMPTS"
echo "======================================"
echo ""
echo "Generate 2 variations for video generation:"
echo ""
cat <<'EOF'
curl -X POST 'http://localhost:8000/generate-dual-prompts' \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "woman dancing",
    "lora_triggers": ["wan"],
    "skip_generation": false
  }'
EOF
echo ""
echo ""

# ============= TEXT-TO-IMAGE WORKFLOW =============
echo "4️⃣  TEXT-TO-IMAGE WORKFLOW"
echo "======================================"
echo ""
echo "Complete text-to-image pipeline:"
echo ""
cat <<'EOF'
curl -X POST 'http://localhost:8000/text-to-image' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "woman smiling",
    "lora_triggers": ["wan"],
    "skip_qwen": false
  }'
EOF
echo ""
echo ""

# ============= TEXT-TO-VIDEO WORKFLOW =============
echo "5️⃣  TEXT-TO-VIDEO WORKFLOW"
echo "======================================"
echo ""
echo "Complete text-to-video pipeline:"
echo ""
cat <<'EOF'
curl -X POST 'http://localhost:8000/text-to-video' \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "woman dancing sensually",
    "lora_triggers": ["wan"],
    "num_prompts": 2,
    "skip_qwen": false
  }'
EOF
echo ""
echo ""

# ============= FEASIBILITY ANALYSIS =============
echo "6️⃣  FEASIBILITY ANALYSIS"
echo "======================================"
echo ""
echo "Analyze action feasibility (requires image):"
echo ""
cat <<'EOF'
# First, encode image to base64:
IMAGE_B64=$(base64 -i /path/to/image.jpg)

curl -X POST 'http://localhost:8000/analyze-feasibility' \
  -H 'Content-Type: application/json' \
  -d "{
    \"image_base64\": \"$IMAGE_B64\",
    \"action\": \"solo masturbation fingering\",
    \"skip_analysis\": false
  }"
EOF
echo ""
echo ""

# ============= ENHANCE IMAGE PROMPT =============
echo "7️⃣  ENHANCE IMAGE PROMPT"
echo "======================================"
echo ""
echo "Enhance prompt with image context:"
echo ""
cat <<'EOF'
curl -X POST 'http://localhost:8000/enhance-image-prompt' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "masturbation",
    "image_description": "woman in bra and underwear, standing",
    "lora_triggers": ["pussy_lora"],
    "skip_enhancement": false
  }'
EOF
echo ""
echo ""

# ============= IMAGE-TO-VIDEO WORKFLOW =============
echo "8️⃣  IMAGE-TO-VIDEO WORKFLOW"
echo "======================================"
echo ""
echo "Complete image-to-video pipeline:"
echo ""
cat <<'EOF'
# First, encode image to base64:
IMAGE_B64=$(base64 -i /path/to/image.jpg)

curl -X POST 'http://localhost:8000/image-to-video' \
  -H 'Content-Type: application/json' \
  -d "{
    \"image_base64\": \"$IMAGE_B64\",
    \"action\": \"masturbation\",
    \"lora_triggers\": [\"pussy_lora\"],
    \"skip_feasibility\": false,
    \"skip_enhancement\": false
  }"
EOF
echo ""
echo ""

# ============= SKIP FEATURES =============
echo "⏭️  SKIP FEATURES"
echo "======================================"
echo ""
echo "Skip QWEN processing for faster responses:"
echo ""
cat <<'EOF'
# Skip enhancement
curl -X POST 'http://localhost:8000/enhance-prompt' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "woman smiling",
    "skip_enhancement": true
  }'

# Skip feasibility analysis
curl -X POST 'http://localhost:8000/analyze-feasibility' \
  -H 'Content-Type: application/json' \
  -d '{
    "image_base64": "...",
    "action": "...",
    "skip_analysis": true
  }'
EOF
echo ""
echo ""

# ============= BASE64 ENCODING =============
echo "🔐 BASE64 ENCODING"
echo "======================================"
echo ""
echo "How to encode images to base64:"
echo ""
cat <<'EOF'
# macOS/Linux
base64 -i image.jpg

# or for inline
$(base64 -i image.jpg)

# Python
python -c "import base64; print(base64.b64encode(open('image.jpg', 'rb').read()).decode())"

# Result: iVBORw0KGgoAAAAN...
EOF
echo ""
echo ""

# ============= RESPONSE FORMATS =============
echo "📋 RESPONSE FORMATS"
echo "======================================"
echo ""
echo "All successful responses:"
cat <<'EOF'
{
  "success": true,
  "data": { ... },
  "message": "Description"
}
EOF
echo ""
echo "All error responses:"
cat <<'EOF'
{
  "success": false,
  "data": { ... },
  "error": "Error message",
  "message": "Description"
}
EOF
echo ""
echo ""

# ============= TESTING SCRIPT =============
echo "🧪 AUTOMATED TESTING"
echo "======================================"
echo ""
echo "Save as test.sh and run: bash test.sh"
echo ""
cat <<'EOF'
#!/bin/bash

API="http://localhost:8000"

echo "Testing QWEN API..."

# Test 1: Health Check
echo "1. Health Check"
curl -s -X GET "$API/health" | python -m json.tool

# Test 2: Enhance Prompt
echo "2. Enhance Prompt"
curl -s -X POST "$API/enhance-prompt" \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "woman smiling", "lora_triggers": ["wan"]}' \
  | python -m json.tool

# Test 3: Generate Dual Prompts
echo "3. Generate Dual Prompts"
curl -s -X POST "$API/generate-dual-prompts" \
  -H 'Content-Type: application/json' \
  -d '{"action": "dancing", "lora_triggers": ["wan"]}' \
  | python -m json.tool

echo "✅ Tests complete"
EOF
echo ""
echo ""

# ============= COMMON PATTERNS =============
echo "🎯 COMMON PATTERNS"
echo "======================================"
echo ""
echo "Pattern 1: Text-to-Image with LoRAs"
cat <<'EOF'
curl -X POST 'http://localhost:8000/text-to-image' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "woman",
    "lora_triggers": ["wan", "pussy_lora"]
  }' | jq '.data.enhanced_prompt'
EOF
echo ""
echo ""
echo "Pattern 2: Check Feasibility Before Generation"
cat <<'EOF'
# 1. Check feasibility
FEASIBILITY=$(curl -s -X POST 'http://localhost:8000/analyze-feasibility' \
  -d "{\"image_base64\": \"...\", \"action\": \"...\"}" \
  | jq '.data.feasibility_score')

# 2. Only proceed if feasible
if (( $(echo "$FEASIBILITY > 0.5" | bc -l) )); then
  echo "Action is feasible, proceeding with generation"
else
  echo "Action not feasible, skipping expensive GPU operation"
fi
EOF
echo ""
echo ""
echo "Pattern 3: Generate Multiple Variations"
cat <<'EOF'
curl -X POST 'http://localhost:8000/text-to-video' \
  -H 'Content-Type: application/json' \
  -d '{
    "action": "woman dancing",
    "num_prompts": 3,
    "lora_triggers": ["wan"]
  }' | jq '.data.prompts[]'
EOF
echo ""
echo ""

# ============= TROUBLESHOOTING =============
echo "🔧 TROUBLESHOOTING"
echo "======================================"
echo ""
echo "API not running?"
echo "  python run.py"
echo ""
echo "Connection refused?"
echo "  curl http://localhost:8000/health"
echo ""
echo "Invalid JSON response?"
echo "  Add: | python -m json.tool"
echo ""
echo "Check logs?"
echo "  tail -f qwen_api.log"
echo ""
echo "Model not loaded?"
echo "  Check CUDA: python -c \"import torch; print(torch.cuda.is_available())\""
echo ""
echo ""

echo "======================================"
echo "✅ CURL Examples Complete"
echo "======================================"
echo ""
echo "For full documentation, see:"
echo "  - API_DOCUMENTATION.md"
echo "  - examples.py (Python client)"
echo "  - run.py (Start API)"
echo ""
