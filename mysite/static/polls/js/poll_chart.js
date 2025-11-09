document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('resultsChart').getContext('2d');
    
    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: JSON.parse(document.getElementById('chart-choices').textContent),
            datasets: [{
                label: 'Votes',
                data: JSON.parse(document.getElementById('chart-votes').textContent),
                backgroundColor: [
                    "#C6DEF1", "#D28A8C", "#FFD9CC", "#F2C6DE", "#F7E5EC", "#EEBEC6", "#FDBA90", "#F9D4B2", "#FAEDCB", "#C9E4DE", "#DBCDF0"
                ],
                borderColor: 'white',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' },
                title: { display: false, text: 'Poll Results' }
            }
        }
    });
});

