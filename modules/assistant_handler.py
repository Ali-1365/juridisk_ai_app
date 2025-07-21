"""
assistant_handler.py – Central hantering av GPT-anrop med rollback, loggning och verifiering
"""

import openai
from modules.utils.gpt_log_handler import log_gpt_interaction
from modules.utils.rollback_handler import enforce_rollback

# ❗ Kontroll: API-nyckel måste sättas i din miljö eller konfigfil
openai.api_key = "din-API-nyckel-här"

def ask_gpt(prompt: str, model="gpt-4") -> str:
    """
    Skickar prompt till GPT, tillämpar rollback-kontroll och loggar resultatet.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        reply = response.choices[0].message["content"].strip()

        # Kontrollera om rollback krävs
        verifierat_svar = enforce_rollback(reply)

        # Logga interaktionen
        log_gpt_interaction(prompt, verifierat_svar)

        return verifierat_svar

    except Exception as e:
        return f"❌ Fel vid GPT-anrop: {str(e)}"
