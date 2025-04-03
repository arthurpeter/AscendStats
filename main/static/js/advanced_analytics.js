// advanced_analytics.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize chart instances
    let averageGradeChart, gradeDistributionChart, successRateChart;
    
    // API endpoints configuration
    const API_ENDPOINTS = {
        'grade-distribution': '/grade-distribution-data/',
        'success-rate': '/success-rate-data/',
        'average-grade': '/average-grade-data/'
    };

    // Get initial data from Django template
    const initialData = {
        averageGrade: JSON.parse(document.getElementById('average-grade-data').textContent),
        gradeDistribution: JSON.parse(document.getElementById('grade-distribution-data').textContent),
        successRate: JSON.parse(document.getElementById('success-rate-data').textContent)
    };

    // Initialize Charts
    function initCharts() {
        // Average Grade Chart
        averageGradeChart = new Chart(document.getElementById('averageGradeChart'), {
            type: 'line',
            data: initialData.averageGrade,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 0, title: { display: true, text: 'Grade' } },
                    x: { title: { display: true, text: 'Month' } }
                },
            }
        });

        // Grade Distribution Chart
        gradeDistributionChart = new Chart(document.getElementById('gradeDistributionChart'), {
            type: 'pie',
            data: initialData.gradeDistribution,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        // Success Rate Chart
        successRateChart = new Chart(document.getElementById('successRateChart'), {
            type: 'bar',
            data: initialData.successRate,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 0, max: 100, title: { display: true, text: 'Success Rate (%)' } },
                    x: { title: { display: true, text: 'Grade' } }
                }
            }
        });
    }

    // Update chart data
    async function updateChart(chartType, timeRange) {
        try {
            const response = await fetch(`${API_ENDPOINTS[chartType]}?time_range=${timeRange}`);
            const newData = await response.json();
            
            // Update the correct chart
            switch(chartType) {
                case 'grade-distribution':
                    gradeDistributionChart.data = newData;
                    gradeDistributionChart.update();
                    break;
                case 'success-rate':
                    successRateChart.data = newData;
                    successRateChart.update();
                    break;
                case 'average-grade':
                    averageGradeChart.data = newData;
                    averageGradeChart.update();
                    break;
            }
        } catch (error) {
            console.error('Error updating chart:', error);
        }
    }

    // Event listeners for time range changes
    function setupEventListeners() {
        document.querySelectorAll('.time-range-select').forEach(select => {
            select.addEventListener('change', function() {
                const chartType = this.dataset.chartType;
                const timeRange = this.value;
                updateChart(chartType, timeRange);
            });
        });
    }

    // Initial setup
    initCharts();
    setupEventListeners();
});