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
                let img = document.getElementById('predictImg');
                img.src = ""
            },
            success: function (data) {
                let img = document.getElementById('predictImg');
                img.src = "data:image/jpeg;base64," + data;
                $("#loader").css("display", "none");
            },
            error: function (e) {
                console.log(e)
            }
        })

    });
});