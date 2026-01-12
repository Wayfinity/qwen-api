# WAN 2.2 LoRA Integration

The QWEN API now fully integrates with the WAN 2.2 LoRA system, automatically detecting actions and including canonical trigger words in all prompts.

## How It Works

### 1. Action Detection
When you send a prompt, the system automatically detects which WAN 2.2 LoRAs should be active:

```
Input: "woman fingering her pussy"
↓
Detection: has_fingering=True, has_pussy-lora=True
↓
Output: Includes fingering trigger words + pussy-lora trigger words
```

### 2. Canonical Trigger Words
Each action automatically includes the proper canonical trigger phrase:

| Action | Canonical Trigger |
|--------|-------------------|
| Fingering | `girl pushing fingers into pussy` |
| Twerking | `A woman is twerking and shaking her ass.` |
| Blowjob | `bl0wj0b` |
| Missionary | `A naked man and a naked woman having sex...` |
| Cowgirl | `c0wg1rl` |
| Handjob | `handj0b` |
| Cumshot | `f4c3spl4sh` |
| And more... | See `utils/wan_lora_integration.py` |

### 3. Automatic LoRA Activation

The system automatically detects and activates LoRAs:

```python
# Auto-detection examples:
"blowjob" → activates penis-lora (penis-related action)
"vagina visible" → activates pussy-lora (genital visibility)
"twerking" → activates twerking LoRA
"teasing" → activates tease LoRA (overrides boobplay/bounce)
```

### 4. Smart Preferences

Built-in preference rules:
- **Cowgirl overrides Missionary** - If both detected, cowgirl wins
- **Tease overrides Boobplay/Bounce** - Tease is preferred when detected
- **Auto Penis-LoRA** - Activated for penis-related actions

## Usage Examples

### Example 1: Automatic Trigger Word Injection

```python
import requests

response = requests.post(
    "http://localhost:8000/enhance-prompt",
    json={
        "prompt": "woman masturbating with fingers in her pussy"
    }
)

result = response.json()
# Enhanced: "girl pushing fingers into pussy, detailed vagina, woman masturbating..."
# Triggers automatically detected and included!
```

### Example 2: With Manual LoRA Triggers

```python
response = requests.post(
    "http://localhost:8000/enhance-prompt",
    json={
        "prompt": "woman masturbating",
        "lora_triggers": ["wan"]  # Manual trigger in addition to auto-detected
    }
)

result = response.json()
# Enhanced: "wan, girl pushing fingers into pussy, detailed vagina, woman..."
```

### Example 3: Dual Prompts with WAN Triggers

```python
response = requests.post(
    "http://localhost:8000/generate-dual-prompts",
    json={
        "action": "blowjob"
    }
)

result = response.json()
# prompt_1: "bl0wj0b, PENISLORA, woman performing blowjob..."
# prompt_2: "bl0wj0b, PENISLORA, woman engaging in oral sex..."
# Both include automatic canonical trigger words!
```

### Example 4: Image-to-Video with WAN

```python
response = requests.post(
    "http://localhost:8000/image-to-video",
    json={
        "image_base64": "...",
        "action": "woman is twerking and shaking her ass"
    }
)

result = response.json()
# Detected: has_twerking=True, has_boob_bounce=True
# Enhanced with: "A woman is twerking and shaking her ass., natural twerking motion..."
```

## Detected Actions (18 Total)

The system detects these actions:

1. **Fingering** - `has_fingering`
2. **Twerking** - `has_twerking`
3. **Boob Bounce** - `has_boob_bounce`
4. **Boobplay** - `has_boobplay`
5. **Blowjob** - `has_blowjob`
6. **Missionary** - `has_missionary`
7. **Cowgirl** - `has_cowgirl`
8. **Handjob** - `has_handjob`
9. **Cunnilingus** - `has_cunnilingus`
10. **Footjob** - `has_footjob`
11. **Dildo** - `has_dildo`
12. **Penis Insert** - `has_penis_insert`
13. **Cumshot** - `has_cumshot`
14. **Creampie** - `has_creampie`
15. **Tease** - `has_tease`
16. **Penis-LoRA** - `has_penis-lora`
17. **Pussy-LoRA** - `has_pussy-lora`
18. **Anime Style** - `has_anime`

## Trigger Word Categories

### By Type

**Physical Actions:**
- Fingering
- Twerking
- Handjob
- Footjob
- Dildo use
- Penetration types (missionary, cowgirl, cunnilingus)

**Cumulative Actions:**
- Cumshot
- Creampie

**Visual Styles:**
- Boob bounce
- Boobplay (titjob)
- Tease

**Genital Focus:**
- Penis-LoRA (automatically activated for penis actions)
- Pussy-LoRA (for vagina/genital visibility)

## How Prompts Are Enhanced

### Flow

```
Original Prompt
    ↓
Detect Intents (WAN 2.2)
    ↓
Extract Canonical Triggers
    ↓
Get Prompt Additions (positive/negative)
    ↓
Build Final Prompt
    ↓
Triggers + Quality Modifiers + Original + Additions
```

### Example Transformation

```
Input:
  "woman fingering herself"

Step 1 - Detect:
  has_fingering: True
  has_pussy-lora: True

Step 2 - Get Canonical Triggers:
  "girl pushing fingers into pussy"
  "detailed vagina"

Step 3 - Get Additions:
  Positive: "detailed finger insertion with precise anatomy..."
  Negative: "floating fingers, disconnected hands..."

Step 4 - Output:
  "girl pushing fingers into pussy, detailed vagina, woman fingering herself, detailed finger insertion with precise anatomy, natural hand positioning"
```

## Integration Points

### QWEN API Endpoints Using WAN Triggers

All these endpoints now include WAN trigger detection:

- ✅ `POST /enhance-prompt` - Text enhancement with WAN triggers
- ✅ `POST /enhance-image-prompt` - Image-aware enhancement
- ✅ `POST /generate-dual-prompts` - Dual prompts with WAN triggers
- ✅ `POST /text-to-image` - Complete workflow
- ✅ `POST /text-to-video` - Complete workflow  
- ✅ `POST /image-to-video` - Complete workflow

### Direct Usage

```python
from utils.wan_lora_integration import (
    detect_lora_intents,
    get_trigger_words,
    get_lora_prompt_additions,
    enrich_prompt_with_lora_triggers
)

# Detect what should be active
intents = detect_lora_intents("woman fingering pussy")
# Result: {"has_fingering": True, "has_pussy-lora": True, ...}

# Get trigger words to add
triggers = get_trigger_words(intents)
# Result: "girl pushing fingers into pussy, detailed vagina"

# Get quality modifiers
pos_add, neg_add = get_lora_prompt_additions(intents)
# Positive: "detailed finger insertion..."
# Negative: "floating fingers..."

# All in one function
enriched = enrich_prompt_with_lora_triggers("woman fingering")
# Result: "girl pushing fingers into pussy, detailed vagina, woman fingering, detailed finger insertion..."
```

## Important Notes

1. **No Duplicates** - System checks case-insensitively to avoid duplicate trigger words
2. **Canonical Forms** - Uses exact trigger phrases from WAN 2.2 system
3. **Automatic Activation** - You don't need to manually specify; detection is automatic
4. **Combination Support** - Multiple actions can be combined (fingering + twerking, etc.)
5. **Quality Reduction** - When 3+ LoRAs active, strengths auto-reduce to 0.85x (prevents overwhelming)

## Performance Impact

- Detection: <1ms (regex pattern matching)
- Trigger extraction: <1ms
- Total overhead: Negligible (adds to existing QWEN processing time)

## Debugging

Enable debug logging to see detection:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now see:
# DEBUG: Matched has_fingering with: 'girl pushing fingers into pussy'
# DEBUG: Trigger words for intents: girl pushing fingers into pussy, ...
```

## Testing

Test the integration:

```bash
python examples.py
```

Look for prompts that now include the canonical WAN trigger words.

---

## Summary

✅ **Automatic Action Detection** - Detects 18 different sexual actions  
✅ **Canonical Trigger Words** - Includes exact WAN 2.2 trigger phrases  
✅ **Smart Preferences** - Handles conflicts (cowgirl vs missionary, etc.)  
✅ **Quality Modifiers** - Adds positive/negative prompt enhancements  
✅ **Zero Configuration** - Works automatically without manual setup  
✅ **Fully Integrated** - All API endpoints use the system  

The QWEN API now ensures that **all appropriate WAN 2.2 LoRA trigger words are automatically included in every enhanced prompt**.
