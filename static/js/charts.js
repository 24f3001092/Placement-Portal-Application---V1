document.addEventListener('DOMContentLoaded', () => {
  const chartCanvas = document.getElementById('placementChart');
  if (!chartCanvas || typeof Chart === 'undefined') {
    return;
  }

  const labels = chartCanvas.dataset.labels ? JSON.parse(chartCanvas.dataset.labels) : [];
  const values = chartCanvas.dataset.values ? JSON.parse(chartCanvas.dataset.values) : [];

  new Chart(chartCanvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: chartCanvas.dataset.label || 'Count',
        data: values,
        backgroundColor: '#0d6efd'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });
});
