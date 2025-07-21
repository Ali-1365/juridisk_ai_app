def generate_pm(publicering: dict) -> str:
    """
    Genererar ett juridiskt strukturerat yttrande (PM) från rättsfallshämtning via PUH API.
    Följer fastställd GPT-policy och stilguide.
    """
    rubrik = publicering.get("rubrik", "Okänd rubrik")
    domstol = publicering.get("avgorandedomstol", "Okänd domstol")
    datum = publicering.get("avgorandedatum", "Okänt datum")
    lagrum = publicering.get("lagrumLista", [])
    referat = publicering.get("referat", "Inget referat tillgängligt.")

    lagrum_str = ", ".join(lagrum) if isinstance(lagrum, list) and lagrum else "Ej angivet"

    pm = f"""
1. INLEDNING OCH IDENTIFIKATION
Rubrik: {rubrik}
Domstol: {domstol}
Avgörandedatum: {datum}

2. LAGRUM OCH TILLÄMPNING
Tillämpade lagrum: {lagrum_str}

3. REFERAT OCH DOMSKÄL
{referat}

4. SLUTSATS
Rättsfallet illustrerar betydelsen av korrekt tillämpning av ovanstående lagrum
och ger vägledning i liknande rättsliga bedömningar enligt RB och gällande praxis.
""".strip()

    return pm


def wrap_pm_with_policy(pm_text: str) -> str:
    """
    Inkluderar GPT-policy i början av dokumentet för korrekt visning i AI-systemet.
    """
    policy = """
⚖️ GPT-POLICY (AKTIV)
– Endast verkliga rättsfall (PUH API)
– Ingen spekulation eller export
– Följer RB, rättsfallstaktik och juridisk metodik
– Avsedd för undervisning och domstolsinlagor
""".strip()

    return f"{policy}\n\n{pm_text.strip()}"
