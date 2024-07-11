document.addEventListener('DOMContentLoaded', function() {
    fetch('statistics.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const statisticsDiv = document.getElementById('statistics');

            for (const [title, stats] of Object.entries(data)) {
                const groupDiv = document.createElement('div');
                groupDiv.classList.add('stat-group');

                const groupTitle = document.createElement('h2');
                groupTitle.textContent = title;
                groupDiv.appendChild(groupTitle);

                for (const [statName, statValue] of Object.entries(stats)) {
                    const statItem = document.createElement('div');
                    statItem.classList.add('stat-item');
                    statItem.textContent = `${statName}: ${statValue.toFixed(2)}`;
                    groupDiv.appendChild(statItem);
                }

                statisticsDiv.appendChild(groupDiv);
            }
        })
        .catch(error => {
            console.error('Error fetching statistics:', error);
            const statisticsDiv = document.getElementById('statistics');
            statisticsDiv.textContent = `Error fetching statistics: ${error.message}`;
        });
});
