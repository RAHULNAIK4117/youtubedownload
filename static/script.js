$(document).ready(function() {
    $('#get-info').click(function() {
        const url = $('#video-url').val();
        $.ajax({
            url: '/get_video_info',
            type: 'POST',
            contentType: 'application/json',  // Set content type to JSON
            data: JSON.stringify({url: url}),
            success: function(data) {
                $('#error-message').text('Success');
                $('#format-select').empty();
                $('#format-select').append('<option disabled selected>Select a format</option>');
                data.formats.forEach(format => {
                    $('#format-select').append(`<option value="${format.format_id}">${format.resolution}p (${format.ext})</option>`);
                });
                $('#video-info').show();
            },
            error: function(jqXHR) {
                $('#error-message').text(jqXHR.responseJSON.error);
            }
        });
    });

    $('#download-video').click(function() {
        const url = $('#video-url').val();
        const format_id = $('#format-select').val();
        $.ajax({
            url: '/download',
            type: 'POST',
            contentType: 'application/json',  // Set content type to JSON
            data: JSON.stringify({url: url, format_id: format_id}),
            success: function(data) {
                const blob = new Blob([data], { type: 'video/mp4' });
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = downloadUrl;
                a.download = `${data.title}.mp4`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(downloadUrl);
            },
            error: function(jqXHR) {
                $('#error-message').text(jqXHR.responseJSON.error);
            }
        });
    });
});