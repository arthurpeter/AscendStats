function getLastSixMonths() {
    const months = [];
    const now = new Date();
    for (let i = 5; i >= 0; i--) {
        const date = new Date(now.getFullYear(), now.getMonth() - i, 1); // Go back i months
        const monthName = date.toLocaleString('default', { month: 'short' }); // Get short month name (e.g., "Jan")
        months.push(monthName);
    }
    return months;
}

// Get chart data from Django template
//const chartData = [1, 2, 4, 3, 5, 4]; // Example data
const chartData = JSON.parse(document.getElementById('chart-data').textContent);

new Chart(document.getElementById('progressChart'), {
    type: 'line',
    data: {
        labels: getLastSixMonths(),
        datasets: [{
            label: 'Max Grade (V Scale)',
            data: chartData,
            borderColor: '#e94f37',
            tension: 0.3,
            spanGaps: true
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                title: { display: true, text: 'Grade' },
                ticks: {
                    stepSize: 1,
                    callback: function(value) {
                        return value !== null ? `V${value}` : '';
                    }
                },
                min: 0,
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.parsed.y;
                        return value !== null ? `V${value}` : 'No climbs';
                    }
                }
            }
        }
    }
});

