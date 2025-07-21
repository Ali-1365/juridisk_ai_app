def analyze_risk(document_text):
    risk_analysis = "✅ Låg risk – föreslår offensiv strategi."
    details = []
    if "Belopp att betala" in document_text:
        lines = document_text.split("\n")
        for line in lines:
            if "Belopp att betala" in line:
                parts = line.split()
                for part in parts:
                    if part.replace(".", "").isdigit():
                        amount = part
                        details.append(f"Belopp: {amount} SEK")
                        if float(amount) < 1000:
                            risk_analysis = "✅ Låg risk – belopp under 1000 SEK."
                        break
    if "Betalas senast" in document_text:
        for line in lines:
            if "Betalas senast" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("202"):
                        details.append(f"Förfallodatum: {part}")
                        break
    return {"analysis": risk_analysis, "details": details}


def analyze_evidence(document_text):
    chunks = []
    if "Fakturanummer" in document_text:
        lines = document_text.split("\n")
        for line in lines:
            if "Fakturanummer" in line:
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        chunks.append(f"Fakturanummer: {part}")
                        break
    if "Kundnummer" in document_text:
        for line in lines:
            if "Kundnummer" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("198"):
                        chunks.append(f"Kundnummer: {part}")
                        break
    if chunks:
        return {"analysis": "✅ Bevis funna.", "chunks": chunks}
    return {"analysis": "❌ Inga tydliga bevis funna.", "chunks": []}