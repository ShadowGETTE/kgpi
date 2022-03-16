Highcharts.chart('container', {
  chart: {
    type: 'column'
  },
  title: {
    text: 'Коэффициенты расчитанные нейронной сетью для каждой эмоции:'
  },
  subtitle: {
    text: 'Отображение коэффициентов может быть не стабильным'
  },
  xAxis: {
    categories: [
      'Злость',
      'Радость',
      'Отвращение',
      'Грусть',
      'Удивление',
      'Нейтральное',
      'Страх'
    ],
    crosshair: true
  },
  yAxis: {
    min: 0,
    title: {
      text: 'Rainfall (mm)'
    }
  },
  tooltip: {
    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
      '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
    footerFormat: '</table>',
    shared: true,
    useHTML: true
  },
  plotOptions: {
    },
  series: [{
    name: 'photo 1',
    data: [0, 71.5, 0, 1, 0, 10, 0]

  }]
});