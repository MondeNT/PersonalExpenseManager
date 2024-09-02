document.addEventListener('DOMContentLoaded', function () {
    // Expense Distribution Pie Chart
    var ctx1 = document.getElementById('expenseDistributionChart').getContext('2d');
    var expenseLabels = JSON.parse(document.getElementById('expenseDistributionLabels').textContent);
    var expenseData = JSON.parse(document.getElementById('expenseDistributionData').textContent);

    if (expenseLabels.length && expenseData.length) {
        new Chart(ctx1, {
            type: 'pie',
            data: {
                labels: expenseLabels,
                datasets: [{
                    data: expenseData,
                    backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745', '#6f42c1', '#e83e8c'],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
});
