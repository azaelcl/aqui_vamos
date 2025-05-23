// Obtener datos del servidor y generar gráficos
fetch('/data')
    .then(response => response.json())
    .then(data => {
        // Gráfico 1: Conteo de Publicaciones por Año
        const yearCounts = {};
        data.years.forEach(year => {
            yearCounts[year] = (yearCounts[year] || 0) + 1;
        });

        const yearData = {
            x: Object.keys(yearCounts),
            y: Object.values(yearCounts),
            type: 'bar',
            marker: { color: '#a0522d' }
        };

        const layout1 = {
            title: 'Conteo de Publicaciones por Año',
            xaxis: { title: 'Año' },
            yaxis: { title: 'Número de Publicaciones' }
        };

        Plotly.newPlot('chart1', [yearData], layout1);

        // Gráfico 2: Distribución de Publicaciones por Autor
        const authorCounts = {};
        data.authors.forEach(author => {
            authorCounts[author] = (authorCounts[author] || 0) + 1;
        });

        const authorData = {
            labels: Object.keys(authorCounts),
            values: Object.values(authorCounts),
            type: 'pie',
            marker: { colors: ['#8B4513', '#CD853F', '#D2691E', '#F4A460', '#DEB887'] }
        };

        const layout2 = {
            title: 'Distribución de Publicaciones por Autor'
        };

        Plotly.newPlot('chart2', [authorData], layout2);

        // Gráfico 3: Número Promedio de Publicaciones por Año
        const uniqueYears = [...new Set(data.years)];
        const yearAverages = uniqueYears.map(year => {
            const numbersInYear = data.numbers.filter((_, i) => data.years[i] === year);
            const sum = numbersInYear.reduce((a, b) => a + b, 0);
            return sum / numbersInYear.length;
        });

        const avgData = {
            x: uniqueYears,
            y: yearAverages,
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#a0522d' }
        };

        const layout3 = {
            title: 'Número Promedio de Publicaciones por Año',
            xaxis: { title: 'Año' },
            yaxis: { title: 'Promedio de Publicaciones' }
        };

        Plotly.newPlot('chart3', [avgData], layout3);
    })
    .catch(error => console.error('Error al cargar los datos:', error));
