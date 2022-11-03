document.addEventListener('DOMContentLoaded', () => {
    const options = {
        chart: {
            type: 'column',
            zoomType: 'xy'
        },
        title: {
            text: 'График'
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Коэффициент эмоции (%)'
            }
        },
        legend: {
            enabled: false
        }
    };

    Highcharts.chart('container', options);
});