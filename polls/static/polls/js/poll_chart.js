document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('resultsChart').getContext('2d');
    
    console.log(document.getElementById('chart-choices'));
    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: JSON.parse(document.getElementById('chart-choices').textContent),
            datasets: [{
                label: 'Votes',
                data: JSON.parse(document.getElementById('chart-votes').textContent),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
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
                title: { display: true, text: 'Poll Results' }
            }
        }
    });
});

