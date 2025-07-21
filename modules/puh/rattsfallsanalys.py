# rattsfallsanalys.py
# Analyserar rättsfall från PUH API och bygger analysutdata för GPT

def analysera_rattsfall(data: dict) -> dict:
    referat = data.get("referat", "")
    if len(referat) > 2500:
        referat = referat[:2500].strip() + " [...]"

    # Hämta fält säkert från indata
    rubrik = data.get("rubrik", "Okänd rubrik")
    lagrum = data.get("lagrum", "Okänt lagrum")
    domstol = data.get("domstol", "Okänd domstol")
    datum = data.get("datum", "Okänt datum")
    ecli = data.get("ecli", "Okänd ECLI")

    # Returnera strukturerad analys
    return {
        "rubrik": rubrik,
        "lagrum": lagrum,
        "domstol": domstol,
        "datum": datum,
        "ecli": ecli,
        "referat": referat
    }
