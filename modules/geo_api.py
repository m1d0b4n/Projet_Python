import requests

class GeoAPI:
    BASE_URL = "https://geo.api.gouv.fr"

    def get_population_by_code(self, code: str):
        if len(code) == 2:
            code += "000"  # Transforme le code département en code postal
        url = f"{self.BASE_URL}/communes?codePostal={code}&fields=population&format=json"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0].get("population"), data[0].get("nom"), code
            else:
                return None, None, code
        except requests.RequestException:
            return None, None, code
