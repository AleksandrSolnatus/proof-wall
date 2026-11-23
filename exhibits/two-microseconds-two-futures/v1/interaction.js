(() => {
  const meal = document.querySelector('#meal');
  if (meal) {
    const representation = meal.querySelector('select');
    const advance = meal.querySelector('[data-advance]');
    const reset = meal.querySelector('[data-reset]');
    const output = meal.querySelector('[role="status"]');
    let advanced = false;
    function showMeal() {
      const omit = representation.value === 'omit';
      for (const clock of meal.querySelectorAll('[data-clock]')) clock.hidden = omit;
      for (const result of meal.querySelectorAll('[data-result]')) result.hidden = !advanced;
      const input = omit ? 'Equal input codes.' : 'The handling clocks distinguish the input codes.';
      output.textContent = advanced ? input + ' The successor codes differ in retained resource state.' : input;
      advance.disabled = advanced;
    }
    representation.addEventListener('change', showMeal);
    advance.addEventListener('click', () => { advanced = true; showMeal(); reset.focus(); });
    reset.addEventListener('click', () => { representation.value = 'keep'; advanced = false; showMeal(); advance.focus(); });
    showMeal();
    meal.hidden = false;
  }

  const fork = document.querySelector('#fork');
  if (fork) {
    const scenario = fork.querySelector('select');
    function showScenario() {
      for (const panel of fork.querySelectorAll('[data-scenario]')) {
        panel.hidden = panel.dataset.scenario !== scenario.value;
      }
    }
    scenario.addEventListener('change', showScenario);
    showScenario();
    fork.hidden = false;
  }
})();
