function LivevideoEditXBlock(runtime, element) {
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
    
    $(element).find('#live_image_cover').bind('change', function () {
        let file = $("#live_image_cover").val();
        if (file) {
            let filename = file.substr(file.lastIndexOf("."));
            if(filename != '.png' && filename != '.jpg' && filename != '.jpeg' && filename != '.gif'){
               alert("please upload image of .png,.jpg,.jpeg,.gif");
            }
        }
    });
    $(element).find('.action-save').bind('click', function() {
        var data = {}
        if ($('#house_number').val() != 100) {
            data['house_number'] = $('#house_number').val();
        } else {
            data['player'] = $('#player').val();
        }
        if ($('#subject').val() == '') {
            alert('subject cannot be empty');
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
        data['live_image_cover'] = $('#live_image_cover_show').attr("src");
        console.log(data);

        var saveconfig_url = runtime.handlerUrl(element, 'save_live_config');
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
        $.post(saveconfig_url, JSON.stringify(data)).done(function(response) {
            if (response.status === 10000) {
                // Reload the whole page :
                window.location.reload(true);
            } else {
                alert(response.msg);
            }
        });
    });
    $(element).find('#upload_cover').bind('click', function () {
        var get_upload_url = runtime.handlerUrl(element, 'get_upload_cover_url');
        var now_host = window.location.host;
        var protocolStr = document.location.protocol;

        var upload_file_url = '';
        var data = {};
        $.ajax({
            url: get_upload_url,
            type: 'post',
            data: JSON.stringify(data),
            dataType: "json",
            async: false,
            success: function (info) {
                if (info.msg == 'success') {
                    upload_file_url = protocolStr + '//' + now_host + info.data.url;
                }
            }
        });
        $('#cover_image_info').val(upload_file_url);

        var formData = new FormData();
        formData.append('file', $('#live_image_cover')[0].files[0])

        $.ajax({
            url:  upload_file_url,
            data: formData,
            type: "post",
            contentType: false,
            processData: false,
            success: function (info) {
                console.log(info.msg);
                var external_url = protocolStr + '//' + info.asset.external_url
                console.log(external_url);
                $('#live_image_cover_show').attr('src', external_url);
            }
        });

    });

}