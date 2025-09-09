import re

RULES = {
    "food": ["kafe", "kofe", "coffee", "ovqat", "non", "bread", "food"],
    "transport": ["taksi", "taxi", "bus", "yoqilgi", "benzin", "ai-92"],
    "utilities": ["svet", "elektr", "gaz", "suv", "internet"],
    "shopping": ["market", "store", "bozor", "do‘kon", "magazin"],
    "salary": ["oylik", "ish haqi", "zarplata", "salary"],
}

DEFAULT_CATEGORY = "other"

_token_re = re.compile(r"[\w\-’'`]+", re.UNICODE)

def guess_category(text: str, default: str = DEFAULT_CATEGORY) -> str:
    if not text:
        return default
    low = text.lower()
    for cat, keys in RULES.items():
        for k in keys:
            if k in low:
                return cat
    # Simple token-based fallback
    tokens = _token_re.findall(low)
    if any(tok in ("oylik", "salary", "zarplata") for tok in tokens):
        return "salary"
    return default
