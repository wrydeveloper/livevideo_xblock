function LivevideoEditXBlock(runtime, element) {
    $('#start_time').cxCalendar();
    $(element).find('#player').bind('change', function () {
        var player = $(this).val();
        var is_interact = $('#is_interact').val();
        if (player_type == 2) {
            if (is_interact == 1) {
                $("#layout option[value='1']").remove();
                $("#layout option[value='2']").remove();
            } else {
                $("#layout option[value='1']").remove();
            }
        }
    });
    $(element).find('.action-save').bind('click', function() {
        var data = {}
        if ($('#house_number').val() != 100) {
            data['house_number'] = $('#house_number').val();
            data['is_interact'] = $('#is_interact').val();
            data['player'] = $('#player').val();
        }

        data['subject'] = $('#subject').val();
        data['start_time'] = $('#start_time').val();
        data['introduction'] = $('#introduction').val();
        data['layout'] = $('#layout').val();
        data['topics'] = $('#topics').val();
        data['is_chat'] = $('#is_chat').val();
        data['auto_record'] = $('#auto_record').val();

        var handlerUrl = runtime.handlerUrl(element, 'save_live_config')
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.msg === 'success') {
                // Reload the whole page :
                window.location.reload(true);
            }
        });
    });

}