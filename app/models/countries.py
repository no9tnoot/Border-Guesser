# app/models/country.py
from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any

class Country(BaseModel):
    name: str
    code: str
    borders: List[str]  # List of country codes that border this country
    
    @field_validator("name", mode="before")
    def extract_common_name(cls, value):
        if isinstance(value, dict):
            return value.get("common")
        return value

    @field_validator("code", mode="before")
    def extract_code(cls, value, values):
        # The API JSON uses "cca3" instead of "code"
        if "cca3" in values:
            return values["cca3"]
        return value

class GameField(BaseModel):
    id: int
    value: str
    is_correct: bool
    is_filled: bool
    correct_answer: str

class GameState(BaseModel):
    target_country: str
    target_country_code: str
    fields: List[GameField]
    total_fields: int
    completed_fields: int
    game_complete: bool = False

class UpdateFieldRequest(BaseModel):
    field_id: int
    country_name: str
    
class GameStateResponse(BaseModel):
    success: bool
    message: str
    game_state: GameState

class SuggestionsRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

class SuggestionsResponse(BaseModel):
    suggestions: List[str]

class RevealAnswersResponse(BaseModel):
    fields: List[GameField]
    target_country: str