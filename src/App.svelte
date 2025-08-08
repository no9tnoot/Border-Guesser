<!-- App.svelte -->
<script>
  import GameBoard from './lib/GameBoard.svelte';
  import { onMount } from 'svelte';

  let darkMode = false;

  onMount(() => {
    // Check for saved theme preference or default to light
    darkMode = localStorage.getItem('theme') === 'dark';
  });

  function toggleTheme() {
    darkMode = !darkMode;
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
  }
</script>

<main class:dark={darkMode}>
  <header>
    <div class="header-content">
      <h1>🌍 Border Guesser</h1>
      <p class="subtitle">Test your geography knowledge!</p>
      <button class="theme-toggle" on:click={toggleTheme}>
        {darkMode ? '☀️' : '🌙'}
      </button>
    </div>
  </header>

  <GameBoard />

  <footer>
    <p>Can you name all the countries that border the given country?</p>
  </footer>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    transition: all 0.3s ease;
  }

  main {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    transition: all 0.3s ease;
  }

  main.dark {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  }

  header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    position: relative;
  }

  .header-content h1 {
    font-size: 3rem;
    margin: 0;
    font-weight: 800;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    background: linear-gradient(45deg, #fff, #f0f8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: 1.2rem;
    margin: 0.5rem 0 0;
    opacity: 0.9;
    font-weight: 300;
  }

  .theme-toggle {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: rgba(255,255,255,0.2);
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
    cursor: pointer;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
  }

  .theme-toggle:hover {
    background: rgba(255,255,255,0.3);
    transform: scale(1.1);
  }

  footer {
    text-align: center;
    padding: 2rem;
    opacity: 0.8;
    font-style: italic;
  }

  @media (max-width: 768px) {
    .header-content h1 {
      font-size: 2rem;
    }
    
    .theme-toggle {
      width: 40px;
      height: 40px;
      font-size: 1.2rem;
    }
  }
</style>