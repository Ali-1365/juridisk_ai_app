# rattsfallsanalys.py
# Analyserar rättsfall från PUH API och bygger analysutdata för GPT

def analysera_rattsfall(data: dict) -> dict:
    ...
    referat = data.get("referat", "")
    if len(referat) > 2500:
        referat = referat[:2500].strip() + " [...]"

    # Datautdrag
    return {
        "rubrik": data.get("rubrik", "Okänd rubrik"),
        "lagrum": lagrum,
        "domstol": domstol,
        "datum": datum,
        "ecli": ecli,
        "referat": referat
    }
