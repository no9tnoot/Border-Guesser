# app/api/routes/game.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.models.countries import (
    UpdateFieldRequest, GameStateResponse, 
    SuggestionsRequest, SuggestionsResponse
)
from app.services.game_service import GameService

router = APIRouter()
game_service = GameService()

@router.get("/game/start")
async def start_game() -> GameStateResponse:
    """Start a new game with blank fields"""
    try:
        current_game_state = game_service.start_new_game()
        return GameStateResponse(   
        success = True,
        game_state = current_game_state,
        message = "Game started successfully"
    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/game/current")
async def get_current_game() -> GameStateResponse:
    """Get current game state"""
    current_game_state = game_service.get_current_game()
    if not current_game_state:
        raise HTTPException(status_code=404, detail="No active game")
    return GameStateResponse(   
        success = True,
        game_state = current_game_state,
        message = "Current game state retrieved successfully"
    )

@router.post("/game/update-field", response_model=GameStateResponse)
async def update_field(request: UpdateFieldRequest):
    """Update a specific field with user input"""
    try:
        game_state = game_service.update_field(request.field_id, request.country_name)
        
        # Generate appropriate message
        field = next((f for f in game_state.fields if f.id == request.field_id), None)
        if field:
            if field.is_correct:
                remaining = game_state.total_fields - game_state.completed_fields
                if remaining == 0:
                    message = "🎉 Congratulations! You completed all countries!"
                else:
                    message = f"✅ Correct! {remaining} more to go."
            elif field.is_filled:
                message = f"❌ '{request.country_name}' doesn't border {game_state.target_country}."
            else:
                message = "Field cleared."
        else:
            message = "Field updated."
        
        return GameStateResponse(
            success=True,
            message=message,
            game_state=game_state
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/game/suggestions", response_model=SuggestionsResponse)
async def get_country_suggestions(request: SuggestionsRequest):
    """Get country name suggestions for autocomplete"""
    try:
        suggestions = game_service.get_country_suggestions(request.query, request.limit)
        return SuggestionsResponse(suggestions=suggestions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/game/hint")
async def get_hint():
    """Get a hint for the current game"""
    hint = game_service.get_hint()
    return {"hint": hint}

@router.get("/game/reveal")
async def reveal_answers():
    """Reveal all correct answers"""
    try:
        revealed = game_service.reveal_answers()
        return {
            "success": True,
            "revealed_answers": revealed
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))