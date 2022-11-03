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
    xAxis: {
        categories: ['Злость', 'Отвращение', 'Страх', 'Счастье', 'Грусть', 'Удивление', 'Нейтральное выражение']
    },
    series: [{
        name: 'image_statistic',
        data: [0, 0, 0, 0, 0, 0, 0],
        dataLabels: [{
            enabled: true,
            inside: true,
            style: {
                fontSize: '16px'
            }
        }]
    }]
};

let chart = null;

document.addEventListener('DOMContentLoaded', () => {
    chart = Highcharts.chart('container', options);
});

$(function () {
    $('#imageInput').on('change', function (e) {
        let image = e.target.files[0];
        var formData = new FormData();
        formData.append('image', image);

        // Send image to server
        $.ajax({
            url: 'predict/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            beforeSend: function () {
                $("#loader").css("display", "block");
                const img = document.getElementById('predictImg');
                img.src = ""
            },
            success: function (data) {
                const img = document.getElementById('predictImg');
                img.src = "data:image/jpeg;base64," + data['image'];
                chart.series[0].update({
                    data: Object.values(data['statistic'])
                });
                chart.setTitle({text: data['title']});
                $("#loader").css("display", "none");
            },
            error: function (e) {
                console.log(e)
            }
        })

    });
});