import unittest
from modules.bl.proof_chain_builder import ProofChainBuilder


class TestProofChainBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = ProofChainBuilder()

    def test_add_single_link(self):
        self.builder.add_link(
            rättsfaktum="Hyresavtal träffat",
            bevis="Avtalskopian",
            bilaga="Bilaga 12",
            källa="RB 35 kap. 1 §",
            kommentar="Autentiskt avtal från 2018"
        )
        kedja = self.builder.get_chain()
        self.assertEqual(len(kedja), 1)
        self.assertEqual(kedja[0]["rättsfaktum"], "Hyresavtal träffat")
        self.assertEqual(kedja[0]["bilaga"], "Bilaga 12")

    def test_empty_comment_is_handled(self):
        self.builder.add_link(
            rättsfaktum="Betalning skedde",
            bevis="Banköverföring",
            bilaga="Bilaga 9",
            källa="Transaktionsdata"
        )
        kedja = self.builder.get_chain()
        self.assertEqual(kedja[0]["kommentar"], "")

    def test_summarize_format(self):
        self.builder.add_link(
            rättsfaktum="Föreläggande mottaget",
            bevis="Tingsrättens beslut",
            bilaga="Bilaga 23",
            källa="Aktbilaga 131",
            kommentar="Motsvarar svaromål 2023-06-02"
        )
        output = self.builder.summarize()
        self.assertIn("Rättsfaktum: Föreläggande mottaget", output)
        self.assertIn("Bilaga: Bilaga 23", output)


if __name__ == "__main__":
    unittest.main()
