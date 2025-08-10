
import requests
from app.data_access import data_interface
from app.models import countries
import json 


class RESTCountriesClient(data_interface.DataInterface):
    def __init__(self, base_url: str = "https://restcountries.com/v3.1"):
        self.base_url = base_url

    def get_country_borders(self, country_code: str) -> list:
        """Fetch the borders of a given country by its name."""
        response = requests.get(f"{self.base_url}/alpha/{country_code}?fields=borders")
        response.raise_for_status()
        country_data = response.json()
        
        if not country_data:
            return []

        borders = country_data[0].get("borders", [])
        return borders

    def get_all_countries(self) -> list[countries.Country]:
        """Fetch data for all countries."""
        response = requests.get(f"{self.base_url}/all?fields=name,cca3,borders")
        response.raise_for_status()
        return response.json()
    
    def get_country_by_code(self, country_code: str) -> str:
        """Fetch data for all countries."""
        response = requests.get(f"{self.base_url}/alpha/{country_code}?fields=name")
        response.raise_for_status()
        return response.json()