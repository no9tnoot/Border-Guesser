# app/services/game_service.py
import random
from typing import Optional, List, Dict
from app.models.countries import Country, GameState, GameField, RevealAnswersResponse
from app.data_access.data_interface import DataInterface
from app.data_access.RESTCountries_client import RESTCountriesClient

class GameService:
    def __init__(self):
        self.country_repo = RESTCountriesClient()
        self.current_game: Optional[GameState] = None
        self._all_country_names = None
        self.all_countries = [Country.model_validate(c) for c in self.country_repo.get_all_countries()]
    
    def _get_all_country_names(self) -> List[str]:
        """Get all country names for autocomplete"""
        if self._all_country_names is None:
            self._all_country_names = [country.name for country in self.all_countries]
        return self._all_country_names
        
    def get_country_data_by_code(self, country_code: str) -> Optional[Country]:
        """Get country data by its code"""
        for country in self.all_countries:
            if country.code == country_code:
                return country
        return None
    
    def get_country_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """Get country name suggestions based on partial input"""
        if len(query) < 2:
            return []
        
        query = query.lower().strip()
        all_countries = self._get_all_country_names()
        
        # Exact matches first
        exact_matches = [name for name in all_countries if name.lower().startswith(query)]
        
        # Contains matches
        contains_matches = [name for name in all_countries 
                          if query in name.lower() and not name.lower().startswith(query)]
        
        suggestions = exact_matches + contains_matches
        return suggestions[:limit]
    
    def start_new_game(self) -> GameState:
        """Start a new game with blank fields for each border country"""
        countries = self.all_countries
        countries_with_borders = [c for c in countries if len(c.borders) >= 3]
        
        if not countries_with_borders:
            raise ValueError("No countries with borders available")
        
        target_country = random.choice(countries_with_borders)
        border_countries = target_country.borders
        
        # Create field structure - one field per border country
        border_country_fields: List[GameField] = []
        for i, border_country in enumerate(border_countries):
            country = self.get_country_data_by_code(border_country) 
            border_country_fields.append(GameField(
                id = i,
                value = "",
                is_correct = False,
                is_filled = False,
                correct_answer = country.name  # Hidden from client
            ))
        
        # Shuffle fields so answers aren't in a predictable order
        random.shuffle(border_country_fields)
        
        game_data = GameState(
            target_country = target_country.name,
            target_country_code = target_country.code,
            fields = border_country_fields,
            total_fields = len(border_country_fields),
            completed_fields = 0,
            game_complete = False
        )
        
        self.current_game = game_data
        
        # Return sanitized version (without correct answers)
        client_fields: List[GameField] = []
        for field in border_country_fields:
            client_fields.append(GameField(
                id = field.id,
                value = field.value,
                is_correct = field.is_correct,
                is_filled = field.is_filled
            ))
        
        client_game_data = self.current_game
        client_game_data.fields = client_fields
        return client_game_data
    
    def update_field(self, field_id: int, country_name: str) -> GameState:
        """Update a specific field with user input"""
        if not self.current_game:
            raise ValueError("No active game. Start a new game first.")
        
        country_name = country_name.strip()
        
        # Find the field
        field = None
        for f in self.current_game.fields:
            if f.id == field_id:
                field = f
                break
        
        if not field:
            raise ValueError("Invalid field ID")
        
        # Update field
        old_is_correct = field.is_correct
        field.value = country_name
        field.is_filled = len(country_name) > 0
        
        # Check if correct (case insensitive)
        field.is_correct = (
            field.is_filled and 
            country_name.lower() == field.correct_answer.lower()
        )
        
        # Update completed count
        if field.is_correct and not old_is_correct:
            self.current_game.completed_fields += 1
        elif not field.is_correct and old_is_correct:
            self.current_game.completed_fields -= 1
        
        # Check if game is complete
        self.current_game.game_complete = (
            self.current_game.completed_fields == self.current_game.total_fields
        )
        
        # Return sanitized game state
        return self._get_client_game_state()
    
    def _get_client_game_state(self) -> GameState:
        """Get game state without revealing correct answers"""
        if not self.current_game:
            return {}
        
        client_fields: List[GameField] = []
        for field in self.current_game.fields:
            client_fields.append(GameField(
                id = field.id,
                value = field.value,
                is_correct = field.is_correct,
                is_filled = field.is_filled
            ))
        
        
        client_game_data = self.current_game
        client_game_data.fields = client_fields
        return client_game_data
    
    def get_current_game(self) -> GameState:
        """Get the current game state"""
        return self._get_client_game_state()
    
    def reveal_answers(self) -> RevealAnswersResponse:
        """Reveal all correct answers"""
        if not self.current_game:
            raise ValueError("No active game")
        
        return RevealAnswersResponse(
            target_country = self.current_game.target_country,
            fields = self.current_game.fields
        )
    
    def get_hint(self) -> str:
        """Get a hint for unfilled fields"""
        if not self.current_game:
            return "No active game"
        
        unfilled_fields = [f for f in self.current_game.fields if not f.is_correct]
        
        if not unfilled_fields:
            return "All fields completed!"
        
        # Give hint about one random unfilled field
        hint_field = random.choice(unfilled_fields)
        correct_name = hint_field.correct_answer
        
        hints = [
            f"💡 One country starts with '{correct_name[0]}'",
            f"💡 One country has {len(correct_name)} letters",
            f"💡 One country contains the letter '{random.choice(correct_name.lower())}'"
        ]
        
        return random.choice(hints)