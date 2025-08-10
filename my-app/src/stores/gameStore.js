// src/lib/stores/gameStore.js
import { writable } from 'svelte/store';

const API_BASE = 'http://localhost:8000/api';

// Game state store
export const gameState = writable({
  target_country: '',
  target_country_code: '',
  fields: [],
  total_fields: 0,
  completed_fields: 0,
  game_complete: false
});

// UI state
export const isLoading = writable(false);
export const message = writable('');
export const showHint = writable('');

// Update debounce timeout
let updateTimeout = null;

// API functions
export const gameApi = {
  async startNewGame() {
    isLoading.set(true);
    message.set('');
    showHint.set('');
    
    try {
      const response = await fetch(`${API_BASE}/game/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Failed to start game');
      }
      
      const data = await response.json();
      gameState.set(data.game_state);
      message.set(`Fill in all ${data.game_state.total_fields} countries that border ${data.game_state.target_country}!`);
    } catch (error) {
      message.set('Error starting game: ' + error.message);
    } finally {
      isLoading.set(false);
    }
  },

  async updateField(fieldId, countryName, immediate = false) {
    // Clear existing timeout
    if (updateTimeout) {
      clearTimeout(updateTimeout);
    }
    
    const performUpdate = async () => {
      try {
        const response = await fetch(`${API_BASE}/game/update-field`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            field_id: fieldId, 
            country_name: countryName 
          }),
        });
        
        if (!response.ok) {
          throw new Error('Failed to update field');
        }
        
        const result = await response.json();
        gameState.set(result.game_state);
        
        // Only show success/error messages for filled fields
        if (countryName.trim().length > 0) {
          message.set(result.message);
        } else {
          message.set('');
        }
        
        return result;
      } catch (error) {
        message.set('Error updating field: ' + error.message);
        return null;
      }
    };
    
    if (immediate) {
      // For final submissions (Enter key, autocomplete selection)
      return await performUpdate();
    } else {
      // For real-time typing (debounced)
      updateTimeout = setTimeout(performUpdate, 300);
    }
  },

  async getCurrentGame() {
    try {
      const response = await fetch(`${API_BASE}/game/current`);
      
      if (!response.ok) {
        if (response.status === 404) {
          // No active game, start a new one
          return this.startNewGame();
        }
        throw new Error('Failed to get current game');
      }
      
      const data = await response.json();
      gameState.set(data.game_state);
      return data.game_state;
    } catch (error) {
      message.set('Error getting game state: ' + error.message);
      return null;
    }
  },

  async getHint() {
    try {
      const response = await fetch(`${API_BASE}/game/hint`);
      
      if (!response.ok) {
        throw new Error('Failed to get hint');
      }
      
      const result = await response.json();
      showHint.set(result.hint);
      
      // Clear hint after 10 seconds
      setTimeout(() => {
        showHint.set('');
      }, 10000);
    } catch (error) {
      showHint.set('No hint available');
    }
  },

  async revealAnswers() {
    try {
      const response = await fetch(`${API_BASE}/game/reveal`);
      
      if (!response.ok) {
        throw new Error('Failed to reveal answers');
      }
      
      const result = await response.json();
      return result.revealed_answers;
    } catch (error) {
      message.set('Error revealing answers: ' + error.message);
      return null;
    }
  }
};