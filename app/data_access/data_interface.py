from abc import ABC, abstractmethod

class DataInterface(ABC):

    @abstractmethod
    def get_country_borders(self, country_code: str) -> list:
        """Fetch the borders of a given country by its code."""
        pass

    @abstractmethod
    def get_all_countries(self) -> list:
        """Fetch data for all countries."""
        pass
    
    @abstractmethod
    def get_country_by_code(self, country_code: str) -> str:
        """Fetch name of country by country code."""
        pass