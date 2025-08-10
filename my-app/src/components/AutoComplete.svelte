<!-- src/lib/Autocomplete.svelte -->
<script>
  import { createEventDispatcher, onMount } from 'svelte';
  
  export let value = '';
  export let fieldId = 0;
  export let isCorrect = false;
  export let isFilled = false;
  export let disabled = false;
  export let placeholder = 'Enter country name...';
  
  const dispatch = createEventDispatcher();
  
  let inputElement;
  let suggestions = [];
  let showSuggestions = false;
  let selectedIndex = -1;
  let isLoading = false;
  let debounceTimeout;
  
  const API_BASE = 'http://localhost:8000/api';
  
  async function getSuggestions(query) {
    if (query.length < 2) {
      suggestions = [];
      showSuggestions = false;
      return;
    }
    
    isLoading = true;
    
    try {
      const response = await fetch(`${API_BASE}/game/suggestions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, limit: 8 }),
      });
      
      if (response.ok) {
        const data = await response.json();
        suggestions = data.suggestions;
        showSuggestions = suggestions.length > 0;
        selectedIndex = -1;
      }
    } catch (error) {
      console.error('Error getting suggestions:', error);
      suggestions = [];
      showSuggestions = false;
    } finally {
      isLoading = false;
    }
  }
  
  function handleInput(event) {
    const newValue = event.target.value;
    value = newValue;
    
    // Debounce the suggestions API call
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      getSuggestions(newValue);
    }, 200);
    
    // Emit change event immediately for real-time validation
    dispatch('input', {
      fieldId,
      value: newValue
    });
  }
  
  function handleKeyDown(event) {
    if (!showSuggestions) {
      if (event.key === 'Enter') {
        dispatch('submit', { fieldId, value });
      }
      return;
    }
    
    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        selectedIndex = Math.min(selectedIndex + 1, suggestions.length - 1);
        break;
        
      case 'ArrowUp':
        event.preventDefault();
        selectedIndex = Math.max(selectedIndex - 1, -1);
        break;
        
      case 'Enter':
        event.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
          selectSuggestion(suggestions[selectedIndex]);
        } else {
          dispatch('submit', { fieldId, value });
        }
        break;
        
      case 'Escape':
        event.preventDefault();
        hideSuggestions();
        break;
        
      case 'Tab':
        if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
          event.preventDefault();
          selectSuggestion(suggestions[selectedIndex]);
        } else {
          hideSuggestions();
        }
        break;
    }
  }
  
  function selectSuggestion(suggestion) {
    value = suggestion;
    hideSuggestions();
    dispatch('input', {
      fieldId,
      value: suggestion
    });
    dispatch('submit', { fieldId, value: suggestion });
  }
  
  function hideSuggestions() {
    showSuggestions = false;
    selectedIndex = -1;
  }
  
  function handleBlur() {
    // Delay hiding to allow for suggestion clicks
    setTimeout(() => {
      hideSuggestions();
    }, 200);
  }
  
  function handleFocus() {
    if (suggestions.length > 0 && value.length >= 2) {
      showSuggestions = true;
    }
  }
  
  onMount(() => {
    return () => {
      clearTimeout(debounceTimeout);
    };
  });
</script>

<div class="autocomplete-container">
  <div class="input-wrapper" 
       class:correct={isCorrect} 
       class:filled={isFilled && !isCorrect}
       class:empty={!isFilled}>
    <input
      bind:this={inputElement}
      bind:value
      on:input={handleInput}
      on:keydown={handleKeyDown}
      on:blur={handleBlur}
      on:focus={handleFocus}
      {disabled}
      {placeholder}
      class="country-input"
      autocomplete="off"
      spellcheck="false"
    />
    
    <!-- Status indicator -->
    <div class="status-indicator">
      {#if isCorrect}
        ✅
      {:else if isFilled}
        ❌
      {:else}
        <div class="empty-circle"></div>
      {/if}
    </div>
    
    <!-- Loading indicator -->
    {#if isLoading}
      <div class="loading-spinner"></div>
    {/if}
  </div>
  
  <!-- Suggestions dropdown -->
  {#if showSuggestions}
    <div class="suggestions-dropdown">
      {#each suggestions as suggestion, index}
        <div 
          class="suggestion-item" 
          class:selected={index === selectedIndex}
          on:click={() => selectSuggestion(suggestion)}
          on:keydown={(e) => e.key === 'Enter' && selectSuggestion(suggestion)}
          tabindex="0"
          role="button"
        >
          {suggestion}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .autocomplete-container {
    position: relative;
    width: 100%;
  }
  
  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    transition: all 0.3s ease;
    overflow: hidden;
  }
  
  .input-wrapper:focus-within {
    border-color: #2196f3;
    box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
  }
  
  .input-wrapper.correct {
    border-color: #4caf50;
    background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
  }
  
  .input-wrapper.filled {
    border-color: #f44336;
    background: linear-gradient(135deg, #ffebee, #ffcdd2);
  }
  
  .input-wrapper.empty {
    border-color: #e0e0e0;
    background: white;
  }
  
  .country-input {
    flex: 1;
    padding: 0.875rem 1rem;
    border: none;
    outline: none;
    font-size: 1rem;
    font-weight: 500;
    color: #333;
    background: transparent;
    border-radius: 12px;
  }
  
  .country-input::placeholder {
    color: #999;
    font-weight: 400;
  }
  
  .country-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .status-indicator {
    padding: 0 0.75rem;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
  }
  
  .empty-circle {
    width: 16px;
    height: 16px;
    border: 2px solid #ccc;
    border-radius: 50%;
    background: white;
  }
  
  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(33, 150, 243, 0.3);
    border-top: 2px solid #2196f3;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: 0.75rem;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .suggestions-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 2px solid #e0e0e0;
    border-top: none;
    border-radius: 0 0 12px 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    max-height: 200px;
    overflow-y: auto;
  }
  
  .suggestion-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    color: #333;
    border-bottom: 1px solid #f0f0f0;
    transition: all 0.2s ease;
  }
  
  .suggestion-item:last-child {
    border-bottom: none;
  }
  
  .suggestion-item:hover,
  .suggestion-item.selected {
    background: linear-gradient(135deg, #e3f2fd, #bbdefb);
    color: #1976d2;
  }
  
  .suggestion-item.selected {
    font-weight: 600;
  }
  
  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .country-input {
      font-size: 0.9rem;
      padding: 0.75rem 0.875rem;
    }
    
    .suggestion-item {
      font-size: 0.9rem;
      padding: 0.625rem 0.875rem;
    }
    
    .suggestions-dropdown {
      max-height: 150px;
    }
  }
</style>