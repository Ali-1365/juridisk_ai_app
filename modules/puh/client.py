import requests

class PuhClient:
    def __init__(self):
        self.base_url = "https://rattspraxis.domstol.se/etjanst/puh/api"
        self.headers = {
            "Accept": "application/json"
        }

    def sok_publiceringar(self, sokfras, max_antal=5):
        """
        Sök rättsfall via sökfras, returnerar en lista av matchande publiceringar.
        """
        endpoint = f"{self.base_url}/publicering/sok"
        params = {
            "sokfras": sokfras,
            "sortering": "PubliceringsdatumNer",
            "skip": 0,
            "take": max_antal
        }

        response = requests.get(endpoint, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json().get("resultatLista", [])

    def hamta_publicering(self, publicering_id):
        """
        Hämta en fullständig publicering (inkl. bilagor) med angivet ID.
        """
        endpoint = f"{self.base_url}/publicering/{publicering_id}"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()
