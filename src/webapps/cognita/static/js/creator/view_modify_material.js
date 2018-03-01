$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    console.log('abc');
    var mode = $("#mode");
    if (mode.val() == 'view') {
        $("#view_button").tab('show');
    } else {
        $("#modify_button").tab('show');
    }

    /*setInterval(function () {
        var data = $('#material_input');
        console.log(data.html());

        /!*$.ajax({
            type: "POST",
            url: url,
            data: formData,
            dataType: "json",

    }, 10000);*!/
    });*/
    CKEDITOR.on('instanceReady', function(evt) {
        // Do your bindings and other actions here for example
        // You can access each editor that this event has fired on from the event
        var editor = evt.editor;
        /*editor.on('change', function () {
        console.log('save');
    })*/
        var timeoutId;
        editor.on('change',function () {
        if (timeoutId) clearTimeout(timeoutId);
        timeoutId = setTimeout(function () {
            console.log(editor.getData());
            $.ajax({
                type: 'POST',
                url: '/save_material/' + $('#View').attr('name'),
                data: {
                    material: editor.getData()
            },
                dataType: 'json',
                success: function (data) {
                    if (data.stat == 'success') {
                        $('#save_info').html('Saved!');
                        $("#save_info").show().delay(1000).fadeOut();
                    }
                }

            });
        }, 750);

        });
    });

});