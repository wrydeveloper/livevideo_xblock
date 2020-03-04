function LivevideoEditXBlock(runtime, element) {

    $(element).find('.action-save').bind('click', function() {
        var data = {
            'house_number': $('#house_number').val(),
            'live_type': $('#live_type').val()
        };

        var handlerUrl = runtime.handlerUrl(element, 'save_live_config')
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.msg === 'success') {
                // Reload the whole page :
                window.location.reload(true);
            }
        });
    });

}