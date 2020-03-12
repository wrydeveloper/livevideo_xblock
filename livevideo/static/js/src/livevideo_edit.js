function LivevideoEditXBlock(runtime, element) {
    // xvDate({
    //     'targetId':'start_time',//时间写入对象的id
    //     'triggerId':['start_time'],//触发事件的对象id
    //     'alignId':'start_time_box',//日历对齐对象
    //     'format':'-',//时间格式 默认'YYYY-MM-DD HH:MM:SS'
    //     'min':'1970-01-01 10:00:00',//最大时间
    //     'max':'2099-01-30 10:00:00'//最小时间
    // });
    var layout_select = $("#layout").clone();
    var layout_option_video = layout_select.find("option[value=1]").clone();
    var layout_option_doc = layout_select.find("option[value=2]").clone();
    var layout_option_doc_video = layout_select.find("option[value=3]").clone();

    var is_new_version_select = $("#is_new_version").clone();
    var is_new_version_option_old_version = is_new_version_select.find("option[value=0]").clone();
    var is_new_version_option_new_version = is_new_version_select.find("option[value=1]").clone();

    var is_interact_select = $("#is_interact").clone();
    var is_interact_option_video_live = is_interact_select.find("option[value=0]").clone();
    var is_interact_option_interact_live = is_interact_select.find("option[value=1]").clone();

    var player_select = $('#player').clone();
    var player_option_flash_player = player_select.find("option[value=1]").clone();
    var player_option_h5_player = player_select.find("option[value=2]").clone();

    var player = '';
    var is_interact = '';
    var is_new_version = '';
    var action = '';


    function init_choose(action) {
        $("#layout").find('option').remove();
        $("#layout").append(layout_option_video);
        $("#layout").append(layout_option_doc);
        $("#layout").append(layout_option_doc_video);

        if (action != 'is_new_version') {
            $("#is_new_version").find('option').remove();
            $("#is_new_version").append(is_new_version_option_old_version);
            $("#is_new_version").append(is_new_version_option_new_version);
        }
    }

    function change_status(action) {
        init_choose(action);
        player = $('#player').val();
        if (player == 2) {
            $('#is_new_version').find('option').remove();
            $('#is_new_version').append(is_new_version_option_new_version);
            $('#is_new_version').val(1)
        }
        is_interact = $('#is_interact').val();
        is_new_version = $('#is_new_version').val();
        if (is_new_version == 1) {
            $('#layout').find('option').remove();
            if (is_interact == 1) {
                $('#layout').append(layout_option_doc_video);
                $('#layout').val(3);
            }  else {
                $('#layout').append(layout_option_doc);
                $('#layout').append(layout_option_doc_video);
                $('#layout').val(3);
            }
        }
    }

    change_status(action);
    $(element).find('#player, #is_interact, #is_new_version').bind('change', function () {
        change_status($(this).attr("id"));
    });
    $(element).find('.action-save').bind('click', function() {
        var data = {}
        if ($('#house_number').val() != 100) {
            data['house_number'] = $('#house_number').val();
        } else {
            data['player'] = $('#player').val();
        }
        if ($('#subject').val() == '') {
            alert('标题不能为空');
        }

        data['is_new_version'] = $('#is_new_version').val();
        data['is_interact'] = $('#is_interact').val();
        data['subject'] = $('#subject').val();
        data['start_time'] = $('#start_time').val();
        data['introduction'] = $('#introduction').val();
        data['layout'] = $('#layout').val();
        data['topics'] = $('#topics').val();
        data['is_chat'] = $('#is_chat').val();
        data['auto_record'] = $('#auto_record').val();
        console.log(data);

        var handlerUrl = runtime.handlerUrl(element, 'save_live_config');
        // var handlerUrl = 'http://127.0.0.1:8001/save_live_config/'
        // $.ajax({
        //     url: handlerUrl,
        //     type: 'post',
        //     data: data,
        //     dataType: "json",
        //     success: function (info) {
        //         console.log(info)
        //     }
        // })
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.status === 10000) {
                // Reload the whole page :
                window.location.reload(true);
            } else {
                alert(response.msg)
            }
        });
    });

}