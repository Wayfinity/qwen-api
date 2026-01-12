"""
WAN 2.2 LoRA Integration for QWEN API
Integrates trigger words from WAN 2.2 LoRA system
Ensures canonical trigger phrases are present in enhanced prompts
"""

import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


def detect_lora_intents(prompt_text: str) -> Dict[str, bool]:
    """
    Detect which LoRAs should activate based on tokens/phrases (WAN 2.2 set).
    This identifies what action/intent is in the prompt.
    """
    prompt_lower = prompt_text.lower()
    
    # Remove intent flag strings that might be appended to the prompt
    intent_flags = [
        "has_fingering", "has_twerking", "has_boob_bounce", "has_boobplay",
        "has_blowjob", "has_missionary", "has_cowgirl", "has_cunnilingus",
        "has_footjob", "has_dildo", "has_penis_insert", "has_cumshot",
        "has_creampie", "has_handjob", "has_anime", "has_tease",
        "has_penis-lora", "has_pussy-lora",
    ]
    
    for flag in intent_flags:
        prompt_lower = prompt_lower.replace(flag, "")
    
    # Trigger phrases for WAN 2.2 LoRAs
    triggers = {
        "has_fingering": ["girl pushing fingers into pussy", "fingering"],
        "has_twerking": [
            "a woman is twerking and shaking her ass.",
            "a woman is twerking",
            "twerking",
            "twerking motion",
            "shaking her ass",
        ],
        "has_boob_bounce": [
            "her breasts are bouncing",
            "breasts are bouncing",
            "boob bounce",
            "bouncing breasts",
        ],
        "has_boobplay": ["nippull", "niprub", "titty drop", "breast play"],
        "has_blowjob": ["bl0wj0b", "blowjob"],
        "has_missionary": [
            "a naked man and a naked woman having sex. he thrusts his penis in and out of her vagina.",
            "missionary",
            "doggy",
            "doggystyle",
            "doggy style",
            "anal",
            "anal sex",
            "from behind",
        ],
        "has_cowgirl": [
            "c0wg1rl",
            "r3v3rs3_c0wg1rl",
            "cowgirl",
            "reverse cowgirl",
            "straddling a man and having sex",
        ],
        "has_cunnilingus": ["cunn1l1ngu5", "cunnilingus", "pussy licking"],
        "has_footjob": [
            "footjob",
            "the woman's feet move up and down",
            "her toes surround his penis",
            "the woman is performing a footjob",
        ],
        "has_dildo": ["piston_dildo_style", "dildo"],
        "has_penis_insert": ["penis is inserted into vagina", "penis-insert"],
        "has_cumshot": ["f4c3spl4sh", "cumshot", "cum shot"],
        "has_creampie": [
            "a woman, the camera quickly pulls back to reveal her vagina, with sperm on her vagina, and the sperm continues to drip down from her vagina,",
            "creampie",
            "sperm on her vagina",
            "sperm dripping down from her vagina",
        ],
        "has_handjob": [
            "handj0b",
            "handjob",
            "hand job",
            "hand-job",
            "giving a handjob",
            "gives him a handjob",
            "she gives him a handjob",
            "manual stimulation",
            "stroking his penis",
            "using her hand on his penis",
        ],
        "has_anime": ["masterpiece, very aesthetic"],
        "has_tease": [
            "exposing breasts",
            "exposing her breasts",
            "sexy dance",
            "solo woman being horny",
            "showing tits",
            "showing her tits",
            "sexy dancing",
            "teasing",
            "tease",
            "seductive dance",
            "stripping",
            "flashing",
            "horny expression",
            "titty drop",
            "titdrop",
            "titydrop",
            "seductive pose",
        ],
        "has_penis-lora": [
            "penis-lora",
            "penis",
            "cock",
            "dick",
            "erection",
            "phallus",
            "shaft",
        ],
        "has_pussy-lora": [
            "pussy-lora",
            "vagina",
            "anus",
            "ass",
            "naked woman",
            "pussy",
        ],
    }

    detected = {key: False for key in triggers.keys()}
    
    for key, phrases in triggers.items():
        for phrase in phrases:
            pattern = r"\b" + re.escape(phrase) + r"\b" if phrase.isalpha() else re.escape(phrase)
            if re.search(pattern, prompt_lower):
                detected[key] = True
                logger.debug(f"Matched {key} with: '{phrase}'")
                break

    # Preference rule: cowgirl overrides missionary when both present
    if detected.get("has_cowgirl"):
        detected["has_missionary"] = False

    # Tease overrides boobplay and boob_bounce
    if detected.get("has_tease"):
        detected["has_boobplay"] = False
        detected["has_boob_bounce"] = False

    # Auto-enable penis-lora if any penis-related intent is active
    penis_related = [
        "has_blowjob", "has_missionary", "has_cowgirl", "has_footjob",
        "has_penis_insert", "has_handjob", "has_cumshot"
    ]
    if any(detected.get(k) for k in penis_related):
        detected["has_penis-lora"] = True

    logger.debug(f"Detected intents: {detected}")
    return detected


def get_trigger_words(intents: Dict[str, bool], base_text: str = "") -> str:
    """
    Return comma-separated canonical trigger phrases for active LoRAs
    that are NOT already present in base_text (case-insensitive check).
    
    Ensures LoRA trigger tokens are present in prompts.
    """
    base_lower = base_text.lower() if isinstance(base_text, str) else ""
    
    # Canonical triggers to inject per intent
    canonical: Dict[str, List[str]] = {
        "has_fingering": ["girl pushing fingers into pussy"],
        "has_twerking": ["A woman is twerking and shaking her ass."],
        "has_boob_bounce": ["her breasts are bouncing"],
        "has_boobplay": ["nipPull", "nipRub"],
        "has_blowjob": ["bl0wj0b"],
        "has_missionary": [
            "A naked man and a naked woman having sex. He thrusts his penis in and out of her vagina.",
        ],
        "has_cowgirl": ["c0wg1rl"],
        "has_handjob": ["handj0b"],
        "has_cunnilingus": ["cunn1l1ngu5"],
        "has_footjob": [
            "footjob",
            "the woman's feet move up and down",
            "her toes surround his penis",
            "the woman is performing a footjob",
        ],
        "has_dildo": ["piston_dildo_style"],
        "has_penis_insert": ["penis is inserted into vagina"],
        "has_cumshot": ["f4c3spl4sh"],
        "has_creampie": [
            "A woman, the camera quickly pulls back to reveal her vagina, with sperm on her vagina, and the sperm continues to drip down from her vagina,"
        ],
        "has_tease": ["solo woman being horny", "naughty horny woman"],
        "has_penis-lora": ["PENISLORA"],
        "has_pussy-lora": ["detailed vagina"],
    }

    tokens: List[str] = []
    
    for intent, phrases in canonical.items():
        if intents.get(intent):
            for phrase in phrases:
                # Case-insensitive containment check
                if phrase.lower() not in base_lower:
                    tokens.append(phrase)

    # Deduplicate while preserving order
    seen = set()
    unique_tokens = []
    for t in tokens:
        if t.lower() not in seen:
            unique_tokens.append(t)
            seen.add(t.lower())
    
    result = ", ".join(unique_tokens)
    logger.debug(f"Trigger words for intents: {result}")
    return result


def get_lora_prompt_additions(intents: Dict[str, bool]) -> Tuple[str, str]:
    """
    Return (positive_additions, negative_additions) to enrich prompts when LoRA is active.
    These are prompt modifiers that work well with each LoRA.
    """
    lora_prompts = {
        "has_fingering": (
            "detailed finger insertion with precise anatomy, natural hand positioning",
            "floating fingers, disconnected hands, unrealistic finger placement",
        ),
        "has_twerking": (
            "natural twerking motion with realistic hip movement and body physics",
            "stiff movement, unnatural body positioning, frozen poses",
        ),
        "has_boob_bounce": (
            "natural breast bouncing with realistic physics and motion blur",
            "stiff breasts, unnatural bounce, frozen breast movement",
        ),
        "has_boobplay": (
            "breast play with natural motion, realistic jiggle and hand interaction",
            "unnatural breast deformation, static hands, floating fingers",
        ),
        "has_blowjob": (
            "bl0wj0b, natural oral interaction with proper positioning and realistic anatomy",
            "disconnected oral contact, floating penis, unrealistic positioning",
        ),
        "has_missionary": (
            "natural missionary position with proper body alignment and connection",
            "disconnected penetration, misaligned bodies, unrealistic positioning",
        ),
        "has_handjob": (
            "natural hand gripping with proper finger positioning and anatomy",
            "floating hands, unrealistic grip, disconnected contact",
        ),
        "has_cowgirl": (
            "consistent up-and-down motion with proper alignment, natural bounce",
            "no movement, misaligned bodies, penetration artifacts",
        ),
        "has_cunnilingus": (
            "natural oral contact with realistic positioning and anatomy",
            "floating head, disconnected contact, unrealistic mouth positioning",
        ),
        "has_footjob": (
            "feet gripping with realistic toe positioning and motion",
            "floating feet, unrealistic grip, disconnected contact",
        ),
        "has_dildo": (
            "realistic dildo motion and contact, proper hand positioning",
            "floating dildo, unrealistic motion, disconnected contact",
        ),
        "has_penis_insert": (
            "clear insertion with anatomically correct alignment and motion",
            "misaligned bodies, unrealistic insertion, deformation",
        ),
        "has_cumshot": (
            "visible cumshot with natural fluid behavior",
            "unrealistic fluids, floating particles, texture artifacts",
        ),
        "has_creampie": (
            "sperm on her vagina, sperm dripping down from her vagina",
            "no sperm, dry vagina",
        ),
        "has_tease": (
            "seductive teasing pose, exposing breasts, sexy dance movements, horny expression",
            "covered body, modest pose, non-sexual expression, static position",
        ),
        "has_penis-lora": (
            "detailed penis, anatomical penis, veins, glans",
            "bad anatomy, blurred penis, missing penis",
        ),
        "has_pussy-lora": (
            "detailed vagina, anatomical accuracy",
            "bad anatomy, missing anatomy",
        ),
    }
    
    positive_additions = []
    negative_additions = []
    
    for intent, (pos, neg) in lora_prompts.items():
        if intents.get(intent):
            positive_additions.append(pos)
            negative_additions.append(neg)

    str_pos = ", ".join(positive_additions)
    str_neg = ", ".join(negative_additions)
    
    logger.debug(f"Positive additions: {str_pos}")
    logger.debug(f"Negative additions: {str_neg}")
    
    return str_pos, str_neg


def enrich_prompt_with_lora_triggers(prompt: str) -> str:
    """
    Main function: Takes a prompt, detects intents, and adds canonical trigger words.
    Returns the enriched prompt with trigger words included.
    """
    # Detect what LoRAs should be active
    intents = detect_lora_intents(prompt)
    
    # Get trigger words that aren't already in the prompt
    trigger_words = get_trigger_words(intents, prompt)
    
    # Get prompt additions
    positive_additions, negative_additions = get_lora_prompt_additions(intents)
    
    # Build enriched prompt
    enriched = prompt
    
    # Add trigger words at the beginning if any detected
    if trigger_words:
        enriched = f"{trigger_words}, {enriched}".strip()
    
    # Add positive quality modifiers
    if positive_additions:
        enriched = f"{enriched}, {positive_additions}".strip()
    
    logger.info(f"Original: {prompt}")
    logger.info(f"Enriched: {enriched}")
    
    return enriched


def get_negative_prompt_additions(prompt: str) -> str:
    """
    Get negative prompt additions based on active LoRAs in the prompt.
    """
    intents = detect_lora_intents(prompt)
    _, negative_additions = get_lora_prompt_additions(intents)
    return negative_additions
