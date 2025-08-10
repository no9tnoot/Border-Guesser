# app/models/country.py
from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any

class Country(BaseModel):
    name: str
    code: str
    borders: List[str]

    @classmethod
    def model_validate(cls, value: dict) -> "Country":
        # Preprocess dict to ensure required fields exist
        value = value.copy()
        if "code" not in value and "cca3" in value:
            value["code"] = value["cca3"]
        if isinstance(value.get("name"), dict):
            value["name"] = value["name"].get("common")
        return super().model_validate(value)

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