#!/bin/bash
# QWEN API + WAN 2.2 LoRA Integration - Quick Reference

# ============================================================
# START API SERVER
# ============================================================
# python run.py

# ============================================================
# TEST TRIGGER WORD DETECTION
# ============================================================

# Test 1: Fingering detection
curl -X POST http://localhost:8000/enhance-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "woman pushing fingers into her pussy"
  }'
# Expected: Includes "girl pushing fingers into pussy" + "detailed vagina"

# Test 2: Blowjob detection
curl -X POST http://localhost:8000/enhance-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "blowjob"
  }'
# Expected: Includes "bl0wj0b" + "PENISLORA"

# Test 3: Multiple actions
curl -X POST http://localhost:8000/enhance-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "woman twerking while showing her breasts"
  }'
# Expected: Includes "A woman is twerking and shaking her ass."

# Test 4: Dual prompts with triggers
curl -X POST http://localhost:8000/generate-dual-prompts \
  -H "Content-Type: application/json" \
  -d '{
    "action": "cumshot"
  }'
# Expected: Both prompts include "f4c3spl4sh"

# Test 5: Image-to-video workflow
curl -X POST http://localhost:8000/image-to-video \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "base64_encoded_image_here",
    "action": "handjob"
  }'
# Expected: Enhanced prompt includes "handj0b"

# ============================================================
# DETECTABLE ACTIONS (18 total)
# ============================================================
# 1. fingering              → "girl pushing fingers into pussy"
# 2. twerking               → "A woman is twerking and shaking her ass."
# 3. boob_bounce            → "her breasts are bouncing"
# 4. boobplay               → "nipPull", "nipRub"
# 5. blowjob                → "bl0wj0b"
# 6. missionary             → "A naked man and a naked woman having sex..."
# 7. cowgirl                → "c0wg1rl"
# 8. handjob                → "handj0b"
# 9. cunnilingus            → "cunn1l1ngu5"
# 10. footjob               → "footjob"
# 11. dildo                 → "piston_dildo_style"
# 12. penis_insert          → "penis is inserted into vagina"
# 13. cumshot               → "f4c3spl4sh"
# 14. creampie              → Full sperm description
# 15. tease                 → "solo woman being horny"
# 16. penis-lora            → "PENISLORA"
# 17. pussy-lora            → "detailed vagina"
# 18. anime                 → "masterpiece, very aesthetic"

# ============================================================
# PYTHON DIRECT USAGE
# ============================================================

# From Python, directly import and use:
# from utils.wan_lora_integration import detect_lora_intents, get_trigger_words, enrich_prompt_with_lora_triggers
#
# # Detect actions
# intents = detect_lora_intents("woman fingering")
# print(intents)  # {'has_fingering': True, 'has_pussy-lora': True, ...}
#
# # Get trigger words
# triggers = get_trigger_words(intents)
# print(triggers)  # "girl pushing fingers into pussy, detailed vagina"
#
# # Full enhancement
# enriched = enrich_prompt_with_lora_triggers("woman fingering")
# print(enriched)  # "girl pushing fingers into pussy, detailed vagina, ..."

# ============================================================
# API ENDPOINTS WITH WAN INTEGRATION
# ============================================================

# 1. Text Enhancement (AUTO TRIGGERS)
# POST /enhance-prompt
# {
#   "prompt": "your text here",
#   "skip_enhancement": false,
#   "lora_triggers": ["optional", "manual", "triggers"]
# }

# 2. Dual Prompts (AUTO TRIGGERS)
# POST /generate-dual-prompts
# {
#   "action": "action description",
#   "skip_generation": false,
#   "lora_triggers": ["optional"]
# }

# 3. Image-to-Video (AUTO TRIGGERS)
# POST /image-to-video
# {
#   "image_base64": "base64_image",
#   "action": "action description",
#   "skip_feasibility": false,
#   "skip_enhancement": false,
#   "lora_triggers": ["optional"]
# }

# ============================================================
# SMART PREFERENCES (AUTOMATIC)
# ============================================================

# If both cowgirl and missionary detected:
#   → Uses cowgirl triggers (cowgirl wins)
#
# If tease detected with boobplay/bounce:
#   → Uses tease triggers (tease wins)
#
# If any penis-related action detected:
#   → Auto-activates penis-lora triggers

# ============================================================
# FILES INVOLVED
# ============================================================
# utils/wan_lora_integration.py     ← Core WAN 2.2 integration
# models/prompt_enhancer.py         ← Enhanced with WAN detection
# app/main.py                       ← All endpoints use integration
# WAN_LORA_INTEGRATION.md           ← Full documentation
# INTEGRATION_COMPLETE.md           ← Setup guide

# ============================================================
# LOGS & DEBUGGING
# ============================================================

# Enable debug logging:
# python -c "
# import logging
# logging.basicConfig(level=logging.DEBUG)
# from utils.wan_lora_integration import detect_lora_intents
# intents = detect_lora_intents('woman fingering')
# "

# Check logs in qwen_api.log or terminal output

# ============================================================
# QUICK TEST SCRIPT
# ============================================================

# Save as test_wan.py:
# #!/usr/bin/env python3
# import requests
# 
# BASE_URL = "http://localhost:8000"
# 
# test_prompts = [
#     "woman fingering her pussy",
#     "blowjob",
#     "woman twerking",
#     "cumshot",
#     "handjob",
# ]
# 
# for prompt in test_prompts:
#     response = requests.post(
#         f"{BASE_URL}/enhance-prompt",
#         json={"prompt": prompt}
#     )
#     result = response.json()
#     print(f"\nInput: {prompt}")
#     print(f"Output: {result['data']['enhanced'][:100]}...")

# Run with: python test_wan.py

# ============================================================
# EXPECTED BEHAVIOR
# ============================================================

# ✅ Every action automatically has trigger words added
# ✅ Trigger words appear at beginning of final prompt
# ✅ No duplicate triggers (case-insensitive check)
# ✅ Quality modifiers added automatically
# ✅ Negative prompts generated for each LoRA
# ✅ Works across all API endpoints
# ✅ Zero configuration required

# ============================================================
# COMMON ISSUES
# ============================================================

# Q: Trigger words not appearing?
# A: Check logs, enable DEBUG logging, verify prompt contains action keywords

# Q: Want to skip auto-detection?
# A: Use skip_enhancement=true on endpoint, or use enrich_prompt=false

# Q: Want to add manual triggers?
# A: Use lora_triggers parameter with ["trigger1", "trigger2"]

# Q: Different output each time?
# A: QWEN uses temperature=0.7 for variety - expected behavior

# ============================================================
# STATUS
# ============================================================

echo "✅ QWEN API with WAN 2.2 LoRA Integration"
echo "✅ All 18 actions detectable"
echo "✅ Canonical trigger words automatic"
echo "✅ All endpoints enabled"
echo "✅ Ready for production use"
echo ""
echo "Start with: python run.py"
echo "Then test: curl -X POST http://localhost:8000/health"
echo ""
echo "See WAN_LORA_INTEGRATION.md for full guide"
