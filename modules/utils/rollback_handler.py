"""
rollback_handler.py – Hanterar rollback vid otillåtna GPT-svar
Funktion: Avbryter svar som innehåller exempel, hypotetiska påståenden eller saknar bevisunderlag.
"""

from typing import Optional


FORBIDDEN_MARKERS = [
    "exempel:", "exempelvis", "anta att", "föreställ dig", "hypotetiskt", "tänk om",
    "det skulle kunna vara så att", "låt oss säga att", "ett möjligt scenario", "tänk t.ex.",
    "kan illustreras med", "hallucinerat", "fiktivt"
]


def should_rollback(svar: str) -> Optional[str]:
    """
    Undersöker om GPT-svaret innehåller otillåtet innehåll.
    Returnerar orsaken till rollback om funnet – annars None.
    """
    lower = svar.lower()
    for marker in FORBIDDEN_MARKERS:
        if marker in lower:
            return f"Otilåtet innehåll upptäckt: '{marker}'"
    if "otillräckligt underlag" in lower or "jag kan inte avgöra" in lower:
        return "Otillräckligt underlag – rollback krävs"
    return None


def enforce_rollback(svar: str) -> str:
    """
    Om rollback krävs, returnera standardfras.
    Annars returnera det godkända svaret.
    """
    rollback_reason = should_rollback(svar)
    if rollback_reason:
        return f"🚫 Svar avbröts: {rollback_reason}. GPT får endast svara vid verifierbart underlag."
    return svar
