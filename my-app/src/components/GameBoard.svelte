<!-- src/lib/GameBoard.svelte -->
<script>
  import { gameState, isLoading, message, showHint, gameApi } from '../stores/gameStore.js';
  import AutocompleteInput from './AutoComplete.svelte';
  import ScoreBoard from './ScoreBoard.svelte';
  import { onMount } from 'svelte';

  let showAnswers = false;
  let revealedAnswers = null;

  onMount(() => {
    gameApi.startNewGame();
  });

  function handleFieldSubmit(event) {
    const { fieldId, value } = event.detail;
    gameApi.updateField(fieldId, value, true); // Immediate update
  }

  function startNewGame() {
    showAnswers = false;
    revealedAnswers = null;
    gameApi.startNewGame();
  }

  function getHint() {
    gameApi.getHint();
  }

  async function toggleAnswers() {
    if (!showAnswers) {
      revealedAnswers = await gameApi.revealAnswers();
    }
    showAnswers = !showAnswers;
  }

  function focusEmptyField() {
    const emptyFields = $gameState.fields.filter(f => !f.is_filled);
    if (emptyFields.length > 0) {
      // Focus first empty field
      const firstEmptyId = emptyFields[0].id;
      const inputElement = document.querySelector(`[data-field-id="${firstEmptyId}"] input`);
      if (inputElement) {
        inputElement.focus();
      }
    }
  }
</script>

<div class="game-container">
  <div class="game-card">
    <!-- Game Status -->
    <div class="game-status">
      {#if $gameState.target_country}
        <h2 class="target-country">
          <span class="flag">🏴</span>
          {$gameState.target_country}
        </h2>
        <ScoreBoard 
          score={$gameState.completed_fields} 
          maxScore={$gameState.total_fields} 
        />
      {/if}
    </div>

    <!-- Message Display -->
    {#if $message}
      <div class="message-box" 
           class:success={$message.includes('✅')} 
           class:error={$message.includes('❌')}
           class:complete={$message.includes('🎉')}>
        <p>{$message}</p>
      </div>
    {/if}

    <!-- Input Fields Grid -->
    {#if $gameState.fields && $gameState.fields.length > 0}
      <div class="fields-section">
        <h3 class="fields-title">Countries that border {$gameState.target_country}:</h3>
        
        <div class="fields-grid">
          {#each $gameState.fields as field (field.id)}
            <div class="field-container" data-field-id={field.id}>
              <div class="field-number">{field.id + 1}</div>
              <AutocompleteInput
                bind:value={field.value}
                fieldId={field.id}
                isCorrect={field.is_correct}
                isFilled={field.is_filled}
                disabled={$isLoading}
                placeholder="Country name..."
                on:submit={handleFieldSubmit}
              />
            </div>
          {/each}
        </div>

        <!-- Progress Indicator -->
        <div class="progress-summary">
          <p class="progress-text">
            {$gameState.completed_fields} of {$gameState.total_fields} completed
            {#if $gameState.total_fields - $gameState.completed_fields > 0}
              • {$gameState.total_fields - $gameState.completed_fields} remaining
            {/if}
          </p>
        </div>
      </div>
    {/if}

    <!-- Action Buttons -->
    {#if $gameState.target_country}
      <div class="action-buttons">
        <button class="btn hint-btn" on:click={getHint} disabled={$isLoading}>
          💡 Hint
        </button>
        <button class="btn focus-btn" on:click={focusEmptyField} disabled={$isLoading || $gameState.game_complete}>
          🎯 Next Empty
        </button>
        <button class="btn new-game-btn" on:click={startNewGame} disabled={$isLoading}>
          🔄 New Game
        </button>
      </div>

      <!-- Hint Display -->
      {#if $showHint}
        <div class="hint-box">
          <p>{$showHint}</p>
        </div>
      {/if}
    {/if}

    <!-- Game Complete -->
    {#if $gameState.game_complete}
      <div class="game-complete">
        <h3>🎉 Perfect Score!</h3>
        <p>You found all {$gameState.total_fields} countries that border {$gameState.target_country}!</p>
        <button class="btn play-again-btn" on:click={startNewGame}>
          🎮 Play Again
        </button>
      </div>
    {:else if $gameState.target_country}
      <!-- Reveal Answers Section -->
      <div class="reveal-section">
        <button class="btn reveal-btn" on:click={toggleAnswers}>
          {showAnswers ? '🙈 Hide' : '👁️ Show'} All Answers
        </button>
        
        {#if showAnswers && revealedAnswers}
          <div class="answers-box">
            <h4>All countries that border {revealedAnswers.target_country}:</h4>
            <div class="answers-grid">
              {#each revealedAnswers.fields as field}
                <div class="answer-item" 
                     class:found={field.is_correct}>
                  <span class="answer-number">{field.id + 1}.</span>
                  <span class="answer-name">{field.correct_answer}</span>
                  <span class="answer-status">
                    {field.is_correct ? '✅' : '❌'}
                  </span>
                </div>
              {/each}
            </div>
          </div>
        {/if}
      </div>
    {/if}

    <!-- Loading Overlay -->
    {#if $isLoading}
      <div class="loading-overlay">
        <div class="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .game-container {
    display: flex;
    justify-content: center;
    padding: 2rem 1rem;
  }

  .game-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 2rem;
    max-width: 800px;
    width: 100%;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    color: #333;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .game-status {
    text-align: center;
    margin-bottom: 2rem;
  }

  .target-country {
    font-size: 2rem;
    margin: 0;
    color: #2c3e50;
    font-weight: 700;
  }

  .flag {
    margin-right: 0.5rem;
  }

  .message-box {
    background: #e3f2fd;
    border: 2px solid #2196f3;
    border-radius: 12px;
    padding: 1rem;
    margin: 1.5rem 0;
    text-align: center;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .message-box.success {
    background: #e8f5e8;
    border-color: #4caf50;
    color: #2e7d32;
  }

  .message-box.error {
    background: #ffebee;
    border-color: #f44336;
    color: #c62828;
  }

  .message-box.complete {
    background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
    border-color: #4caf50;
    color: #2e7d32;
    font-size: 1.1rem;
    font-weight: 600;
  }

  .fields-section {
    margin: 2rem 0;
  }

  .fields-title {
    color: #2c3e50;
    margin-bottom: 1.5rem;
    font-size: 1.3rem;
    text-align: center;
    font-weight: 600;
  }

  .fields-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .field-container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .field-number {
    background: linear-gradient(135deg, #42a5f5, #1976d2);
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.9rem;
    flex-shrink: 0;
  }

  .progress-summary {
    text-align: center;
    margin-top: 1rem;
  }

  .progress-text {
    color: #666;
    font-size: 0.9rem;
    font-weight: 500;
  }

  .action-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 2rem 0 1rem;
    flex-wrap: wrap;
  }

  .btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 25px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
    white-space: nowrap;
  }

  .hint-btn {
    background: linear-gradient(135deg, #ffd54f, #ffb300);
    color: #333;
  }

  .focus-btn {
    background: linear-gradient(135deg, #ab47bc, #7b1fa2);
    color: white;
  }

  .new-game-btn {
    background: linear-gradient(135deg, #42a5f5, #1976d2);
    color: white;
  }

  .play-again-btn {
    background: linear-gradient(135deg, #66bb6a, #388e3c);
    color: white;
    padding: 1rem 2rem;
    font-size: 1.1rem;
  }

  .reveal-btn {
    background: linear-gradient(135deg, #ff7043, #d84315);
    color: white;
  }

  .btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }

  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .hint-box {
    background: #fff3e0;
    border: 2px solid #ff9800;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    font-weight: 500;
    color: #ef6c00;
    margin: 1rem 0;
  }

  .game-complete {
    text-align: center;
    background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
    border: 2px solid #4caf50;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
  }

  .game-complete h3 {
    color: #2e7d32;
    margin: 0 0 1rem;
    font-size: 1.8rem;
  }

  .game-complete p {
    color: #2e7d32;
    margin: 0 0 1.5rem;
    font-size: 1.1rem;
  }

  .reveal-section {
    text-align: center;
    margin: 2rem 0;
  }

  .answers-box {
    background: #fce4ec;
    border: 2px solid #e91e63;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
  }

  .answers-box h4 {
    color: #ad1457;
    margin: 0 0 1rem;
    font-size: 1.1rem;
  }

  .answers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
  }

  .answer-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.7);
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-weight: 500;
  }

  .answer-item.found {
    background: linear-gradient(135deg, #c8e6c9, #a5d6a7);
    color: #2e7d32;
  }

  .answer-number {
    font-weight: 700;
    color: #666;
    min-width: 20px;
  }

  .answer-name {
    flex: 1;
    text-align: left;
  }

  .answer-status {
    font-size: 1.1rem;
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-radius: 20px;
    gap: 1rem;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e3f2fd;
    border-top: 4px solid #2196f3;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Mobile Responsiveness */
  @media (max-width: 768px) {
    .game-card {
      padding: 1.5rem;
      margin: 1rem;
    }

    .target-country {
      font-size: 1.5rem;
    }

    .fields-grid {
      grid-template-columns: 1fr;
      gap: 0.875rem;
    }

    .action-buttons {
      flex-direction: column;
      align-items: center;
      gap: 0.75rem;
    }

    .btn {
      width: 100%;
      max-width: 250px;
    }

    .answers-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 480px) {
    .field-container {
      gap: 0.5rem;
    }

    .field-number {
      width: 28px;
      height: 28px;
      font-size: 0.8rem;
    }

    .fields-title {
      font-size: 1.1rem;
    }
  }
</style>