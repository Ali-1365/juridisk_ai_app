"""
proof_chain_builder.py – Skapar beviskedjor enligt RB 35–38 kap.
Funktion: Binder rättsfakta till bevis, bilagor och källa med verifierbar struktur.
"""

from typing import List, Dict


class ProofChainBuilder:
    def __init__(self):
        self.chain: List[Dict[str, str]] = []

    def add_link(self, rättsfaktum: str, bevis: str, bilaga: str, källa: str, kommentar: str = "") -> None:
        """
        Lägger till en länk i beviskedjan.
        Alla poster loggas strikt enligt struktur: rättsfaktum – bevis – bilaga – källa – kommentar.
        """
        self.chain.append({
            "rättsfaktum": rättsfaktum.strip(),
            "bevis": bevis.strip(),
            "bilaga": bilaga.strip(),
            "källa": källa.strip(),
            "kommentar": kommentar.strip()
        })

    def get_chain(self) -> List[Dict[str, str]]:
        """
        Returnerar hela beviskedjan som en lista av länkar.
        """
        return self.chain

    def summarize(self) -> str:
        """
        Genererar en textöversikt av beviskedjan.
        Används endast för intern granskning – inte för domstolsinlagor.
        """
        output = []
        for i, link in enumerate(self.chain, 1):
            output.append(f"{i}. Rättsfaktum: {link['rättsfaktum']}")
            output.append(f"   Bevis: {link['bevis']}")
            output.append(f"   Bilaga: {link['bilaga']}")
            output.append(f"   Källa: {link['källa']}")
            if link["kommentar"]:
                output.append(f"   Kommentar: {link['kommentar']}")
            output.append("")  # Radbrytning
        return "\n".join(output)
