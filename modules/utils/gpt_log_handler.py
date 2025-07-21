"""
gpt_log_handler.py – Hanterar loggning av GPT-anrop och API-svar
"""

import datetime
import os

LOG_FILE_PATH = "gpt_log.txt"

def log_gpt_interaction(sokfras: str, svar: str, ecli: str = "okänd") -> None:
    """
    Loggar en GPT-interaktion med sökfras, svar, ecli och tidsstämpel.
    """
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"[{timestamp}] Sökfras: {sokfras}\nECLI: {ecli}\nSvar: {svar}\n{'='*40}\n"

    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)

def clear_log() -> None:
    """
    Rensar loggfilen.
    """
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)

def show_log(n: int = 10) -> str:
    """
    Visar de senaste n loggade posterna.
    """
    if not os.path.exists(LOG_FILE_PATH):
        return "Ingen logg finns ännu."

    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = "".join(lines).strip().split("="*40)
    latest_entries = entries[-n:]
    return "\n".join([entry.strip() + "\n" + "="*40 for entry in latest_entries if entry.strip()])
