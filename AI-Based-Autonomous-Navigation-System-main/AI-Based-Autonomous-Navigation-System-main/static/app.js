(() => {
  const runButtons = [document.getElementById('runBtn'), document.getElementById('runBtnSecondary')];
  const runBtnText = document.getElementById('runBtnText');
  const dynamicToggle = document.getElementById('dynamicToggle');
  const message = document.getElementById('runMessage');
  const toast = document.getElementById('toast');
  let toastTimer;

  function notify(text) {
    toast.textContent = text;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
  }
  function setMetric(id, value) { document.getElementById(id).textContent = value; }
  function setBadge(id, text, tone = 'neutral') {
    const el = document.getElementById(id);
    el.textContent = text;
    el.className = `metric-badge ${tone}`;
  }
  function showMetrics(m) {
    setMetric('goalValue', m.goal_reached ? 'Reached' : 'Not reached');
    setBadge('goalBadge', m.goal_reached ? 'Success' : 'Needs attention', m.goal_reached ? 'good' : 'warn');
    setMetric('stepsValue', Number(m.movement_steps ?? 0).toLocaleString());
    setMetric('replansValue', Number(m.replans ?? 0).toLocaleString());
    setBadge('replanBadge', m.dynamic_obstacle_introduced ? 'Dynamic obstacle handled' : 'Static route only', m.dynamic_obstacle_introduced ? 'good' : 'neutral');
    setMetric('collisionValue', m.collision_detected ? 'Detected' : 'None');
    setBadge('collisionBadge', m.collision_detected ? 'Safety stop' : 'Safe run', m.collision_detected ? 'warn' : 'good');
    document.getElementById('lastRunLabel').textContent = `Last run · ${new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}`;
    const mapStatus = document.getElementById('mapStatus');
    mapStatus.innerHTML = '<i></i> Results available';
    mapStatus.classList.add('ready');
    document.getElementById('mapImage').src = `/outputs/navigation_map.png?t=${Date.now()}`;
    document.getElementById('mapImage').hidden = false;
    document.querySelector('.empty-state').hidden = true;
    document.getElementById('fileCount').textContent = '5 outputs';
  }
  async function runSimulation() {
    runButtons.forEach(b => b.disabled = true);
    runBtnText.textContent = 'Running…';
    message.classList.remove('error');
    message.textContent = 'Planning route and simulating movement…';
    try {
      const response = await fetch('/api/run', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({dynamic_obstacle: dynamicToggle.checked})
      });
      const data = await response.json();
      if (!response.ok || !data.ok) throw new Error(data.error || 'The simulation could not be completed.');
      showMetrics(data.metrics);
      message.textContent = data.metrics.goal_reached ? 'Simulation completed successfully.' : 'Simulation finished, but the goal was not reached.';
      notify(data.metrics.goal_reached ? 'Simulation completed successfully.' : 'Simulation finished. Review the metrics.');
    } catch (error) {
      message.textContent = error.message;
      message.classList.add('error');
      notify(`Unable to run simulation: ${error.message}`);
    } finally {
      runButtons.forEach(b => b.disabled = false);
      runBtnText.textContent = 'Run simulation';
    }
  }
  runButtons.forEach(button => button.addEventListener('click', runSimulation));
  document.getElementById('viewResultsBtn').addEventListener('click', () => document.getElementById('results').scrollIntoView({behavior:'smooth'}));

  async function loadPreviousRun() {
    try {
      const response = await fetch('/api/status');
      const data = await response.json();
      if (data.ready && data.metrics) showMetrics(data.metrics);
    } catch (_) { /* dashboard remains usable; user can start a new run */ }
  }
  loadPreviousRun();
})();
