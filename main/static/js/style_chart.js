document.addEventListener("DOMContentLoaded", function () {

    const viewDistributionButton = document.getElementById("viewDistributionButton");
    const styleDistributionModal = new bootstrap.Modal(document.getElementById("styleDistributionModal"));
    const styleDistributionChartCanvas = document.getElementById("styleDistributionChart");
    const styleSuggestion = document.getElementById("styleSuggestion");

    let styleDistributionChart;

    viewDistributionButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default link behavior

        // Get the URL from the data-url attribute
        const url = viewDistributionButton.getAttribute("data-url");

        // Fetch data from the server
        fetch(url)
            .then(response => response.json())
            .then(data => {

                // Update the chart
                const styles = data.styles;
                const labels = Object.keys(styles);
                const values = Object.values(styles);

                if (styleDistributionChart) {
                    styleDistributionChart.destroy(); // Destroy the old chart if it exists
                }

                styleDistributionChart = new Chart(styleDistributionChartCanvas, {
                    type: "pie",
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Number of ascents',
                            data: values,
                            backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: "top",
                            }
                        }
                    }
                });

                // Update the quote
                styleSuggestion.textContent = data.suggestion;

                // Show the modal
                styleDistributionModal.show();
            })
            .catch(error => {
                console.error("Error fetching style distribution data:", error);
            });
    });
});