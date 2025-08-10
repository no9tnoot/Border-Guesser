<!-- src/lib/ScoreBoard.svelte -->
<script>
  export let score = 0;
  export let maxScore = 0;
  
  $: progress = maxScore > 0 ? (score / maxScore) * 100 : 0;
  $: isComplete = score === maxScore && maxScore > 0;
</script>

<div class="scoreboard">
  <div class="score-header">
    <div class="score-numbers">
      <span class="current-score">{score}</span>
      <span class="separator">/</span>
      <span class="max-score">{maxScore}</span>
    </div>
    <div class="score-label">Countries Found</div>
  </div>
  
  <div class="progress-container">
    <div class="progress-bar">
      <div 
        class="progress-fill" 
        class:complete={isComplete}
        style="width: {progress}%"
      ></div>
    </div>
    <div class="progress-text">{Math.round(progress)}% Complete</div>
  </div>
  
  {#if isComplete && maxScore > 0}
    <div class="completion-badge">
      🏆 Perfect Score!
    </div>
  {/if}
</div>

<style>
  .scoreboard {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border: 2px solid #dee2e6;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .scoreboard::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #42a5f5, #66bb6a, #ffa726);
  }

  .score-header {
    margin-bottom: 1rem;
  }

  .score-numbers {
    display: flex;
    justify-content: center;
    align-items: baseline;
    gap: 0.25rem;
    margin-bottom: 0.5rem;
  }

  .current-score {
    font-size: 2.5rem;
    font-weight: 800;
    color: #2c3e50;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  }

  .separator {
    font-size: 1.8rem;
    color: #6c757d;
    font-weight: 400;
  }

  .max-score {
    font-size: 1.8rem;
    font-weight: 600;
    color: #6c757d;
  }

  .score-label {
    font-size: 1rem;
    color: #495057;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .progress-container {
    margin: 1rem 0;
  }

  .progress-bar {
    width: 100%;
    height: 12px;
    background: #e9ecef;
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 0.5rem;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #42a5f5, #66bb6a);
    border-radius: 6px;
    transition: width 0.6s ease-out;
    position: relative;
    overflow: hidden;
  }

  .progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
    );
    animation: shimmer 2s infinite;
  }

  .progress-fill.complete {
    background: linear-gradient(90deg, #ffd700, #ffb300);
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
  }

  @keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }

  .progress-text {
    font-size: 0.9rem;
    color: #6c757d;
    font-weight: 600;
  }

  .completion-badge {
    background: linear-gradient(135deg, #ffd700, #ffb300);
    color: #333;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.9rem;
    margin-top: 1rem;
    display: inline-block;
    box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
    animation: bounce 0.6s ease-out;
  }

  @keyframes bounce {
    0%, 20%, 53%, 80%, 100% {
      transform: translate3d(0, 0, 0);
    }
    40%, 43% {
      transform: translate3d(0, -8px, 0);
    }
    70% {
      transform: translate3d(0, -4px, 0);
    }
    90% {
      transform: translate3d(0, -2px, 0);
    }
  }

  @media (max-width: 768px) {
    .scoreboard {
      padding: 1rem;
    }
    
    .current-score {
      font-size: 2rem;
    }
    
    .separator, .max-score {
      font-size: 1.5rem;
    }
    
    .score-label {
      font-size: 0.9rem;
    }
  }
</style>