/* Javascript for LivevideostreamingXBlock. */
function LivevideostreamingXBlock(runtime, element) {
    $('.image-block', element).click(function (eventObject) {
        $('.image-block').css({
            display: 'none'
        });
        var teacher_live_url = $('#teacher_live_url').text();
        var student_live_url = $('#student_live_url').text();
        var now_host = window.location.host;
        var live_url = '';

        if (/^.*\.studio\..*$/.test(now_host)) {
            live_url = teacher_live_url
        } else {
            live_url = student_live_url
        }
        var operation_html = '<div class="iframe-container" id="iframe-container">\n' +
            '\t<iframe border="0" src="'+ live_url +'" allow="microphone;camera" class="iframe-box"></iframe>\n' +
            '\t<button class="fullscreen">点你</button>\n' +
            '</div>\n';
        $('#livevideo-big-box').prepend(operation_html);
        LivevideostreamingXBlock()
    });

    $('.fullscreen', element).click(function(eventObject) {
        var iframe = document.querySelector('#iframe-container');
        var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
        (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
        (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
        (document.msFullscreenElement && document.msFullscreenElement !== null);

        if (!isInFullScreen) {
            if (iframe.requestFullscreen) {
              iframe.requestFullscreen();
            } else if (iframe.webkitRequestFullscreen) {
              iframe.webkitRequestFullscreen();
            } else if (iframe.mozRequestFullScreen) {
              iframe.mozRequestFullScreen();
            } else if (iframe.msRequestFullscreen) {
                iframe.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }

    });
}
