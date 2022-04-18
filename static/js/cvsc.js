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
    };
    options.data = {
        csvURL: '/static/img/test.csv',
        enablePolling: true,
        dataRefreshRate: 1
    };

    Highcharts.chart('container', options);
});