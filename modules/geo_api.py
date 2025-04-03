import requests

class GeoAPI:
    BASE_URL = "https://geo.api.gouv.fr"

    def get_population_by_departement(self, code_dept: str):
        url = f"{self.BASE_URL}/departements/{code_dept}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("population")
        except requests.RequestException:
            return None

    def get_population_by_commune(self, code_postal: str):
        url = f"{self.BASE_URL}/communes?codePostal={code_postal}&fields=population&format=json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0].get("population"), data[0].get("nom")
            else:
                return None, None
        except requests.RequestException:
            return None, None
