$( document ).ready(function() {  // Runs when the document is ready

    // using jQuery
    // https://docs.djangoproject.com/en/1.10/ref/csrf/
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

    if (!!window.performance && window.performance.navigation.type === 2) {
            // value 2 means "The page was accessed by navigating into the history"
            console.log('Reloading');
            window.location.reload(); // reload whole page

        }

    $('body').on('click', '.delete-tag', function() {
        var course_id = $('#tag-div').attr('name');
        var url = "/delete_tag/" + course_id;
        var tag_id = $(this).parent().attr('name');
        var new_this = $(this);
        $.ajax({
            type: "POST",
            url: url,
            data: {
                tag_id: tag_id
            },
            dataType: "json",
            success: function (data) {
                if (data.stat == 'success') {

                    new_this.parent().remove();
                }
            }
        });
    });

    $('.display-add-tag').click(function() {
        $('#tag-add-area').show();
        $('.display-add-tag').hide();
    });

    $('#cancel-tag').click(function() {
        $('.tag-form')[0].reset();
        $('#tag-add-area').hide();
        $('.display-add-tag').show();
    });

    $('#add-tag-button').click(function (event) {
        event.preventDefault();
        var data = $('#tag-form').serialize();
        var course_id = $('#tag-div').attr('name');
        $.ajax({
            type: "POST",
            url: "/add_tag/" + course_id,
            data: data,
            dataType: "json",
            success: function (data) {
                if (data.stat == 'success') {
                    var html = data.html;
                    var new_tag = $(html);
                    $("#tag-div").prepend(new_tag);
                    $('.tag-form')[0].reset();
                    $('#tag-add-area').hide();
                    $('.display-add-tag').show();
                }
            }
        });
    });


    $('.sortable-small').sortable({
        handle: '.handle',

        update: function(event, ui) {
            var order = $(this).sortable('serialize');
            //console.log(order);
            panel_id = $(this).parent().attr('id');
            lecture_id = panel_id.replace('panel-', '');
            var url = '/reorder_part/' + lecture_id;
            $.ajax({
                type: "POST",
                url: url,
                data: order,
                dataType: "json",
                success: function(data) {
                    if (data.stat != 'success') {
                        window.location.reload();
                    }
                }
            });
        }
    });

    $(".sortable-small").disableSelection();

    $(".sortable-large").sortable({
        handle: '.handle',

    });

    $('body').on('click', '#reorder_module_button', function(event) {
        var order = $('#sortable-large').sortable('serialize');
        var course_id = $(this).attr("name");
        //console.log($(this));
        var url = "/reorder_module/" + course_id;
        $.ajax({
            type: "POST",
            url: url,
            data: order,
            dataType: "json",
            success: function(data) {
                window.location.reload();
            }
        });
    });


    $('body').on('click', '#add_lecture_button', function (event) {

        event.preventDefault();
        var content = $(this).parent().serialize();
        var course_id = $(this).parent().attr("name");
        var url = "/add_lecture/" + course_id;
        $.ajax({
            type: "POST",
            url: url,
            data: content,
            dataType: "json",
            success: function(data) {
                if (data.stat == "success") {
                    var count = $(".anchor").length;
                    count += 1;
                    window.location.reload(true);
                } else {
                    console.log(data);
                    var field;
                    for (var i = 0; i < Object.keys(data).length; i++) {

                        field = Object.keys(data)[i];

                        for (var i = 0; i < data[field].length; i++) {
                            var errori = data[field][i].message;
                            var error_area = $("#lecture_error_" + field);
                            console.log(error_area);
                            error_area.html(errori);
                        }
                    }
                }
            }
        });
    });

    $('body').on('click', '.add_reading_button', function(event) {
        event.preventDefault();
        var form = $(this).parent();
        var formData = new FormData(form[0]);
        var lecture_id = $(this).parent().attr('name');
        var url = "/add_reading/" + lecture_id;
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            dataType: "json",
            cache: false,
            processData: false,
            contentType: false,

            success: function (data) {
                console.log(data.stat);
                if (data.stat == "success") {
                    var html = data.html;

                    var panel_id = data.id;
                    var target_panel = $("#sortable-" + panel_id.toString());

                    //console.log('aaa');
                    var new_part = $(html);
                    target_panel.append(new_part);
                    $("#part-modal-" + lecture_id.toString()).modal('hide');
                    form[0].reset();
                } else {
                    //console.log(data);
                    console.log('else');
                    var field;
                    for (var i = 0; i < Object.keys(data).length; i++) {

                        field = Object.keys(data)[i];

                        for (var j = 0; j < data[field].length; j++) {
                            var errori = data[field][j].message;
                            var error_area = $("#reading_error_" + lecture_id + "_" + field);
                            //console.log(error_area);
                            error_area.html(errori);
                        }
                    }
                }
            }
        })
    });

    $('body').on('click', '.add_material_button', function(event) {
        event.preventDefault();
        var form = $(this).parent();
        var formData = new FormData(form[0]);
        var lecture_id = $(this).parent().attr('name');
        var url = "/add_material/" + lecture_id;
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            dataType: "json",
            cache: false,
            processData: false,
            contentType: false,

            success: function (data) {
                console.log(data.stat);
                if (data.stat == "success") {
                    var part_id = data.part_id;
                    window.location.href = "/start_material/" + part_id;
                } else {
                    //console.log(data);
                    console.log('else');
                    var field;
                    for (var i = 0; i < Object.keys(data).length; i++) {

                        field = Object.keys(data)[i];

                        for (var j = 0; j < data[field].length; j++) {
                            var errori = data[field][j].message;
                            var error_area = $("#material_error_" + lecture_id + "_" + field);
                            //console.log(error_area);
                            error_area.html(errori);
                        }
                    }
                }
            }
        })
    });

    $('body').on('click', '.add_video_button', function(event) {
        event.preventDefault();
        var form = $(this).parent();
        var formData = new FormData(form[0]);
        var lecture_id = $(this).parent().attr('name');
        var url = "/add_video/" + lecture_id;
        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            dataType: "json",
            cache: false,
            processData: false,
            contentType: false,

            success: function (data) {
                console.log(data.stat);
                if (data.stat == "success") {
                    console.log('aaa');
                    var html = data.html;

                    var panel_id = data.id;
                    var target_panel = $("#sortable-" + panel_id.toString());
                    //console.log('aaa');
                    var new_part = $(html);
                    console.log(new_part);
                    target_panel.append(new_part);
                    $("#part-modal-" + lecture_id.toString()).modal('hide');
                    form[0].reset();
                } else {
                    console.log(data);
                    console.log('else');
                    var field;
                    for (var i = 0; i < Object.keys(data).length; i++) {

                        field = Object.keys(data)[i];

                        for (var j = 0; j < data[field].length; j++) {
                            var errori = data[field][j].message;
                            var error_area = $("#video_error_" + lecture_id + "_" + field);
                            //console.log(error_area);
                            error_area.html(errori);
                        }
                    }
                }
            }
        })
    });

    $('body').on('click', '.delete-button', function(event) {
        var delete_modal = $('#delete-confirm-modal');

        delete_modal.data("part_id", $(this).attr("name"));
        //delete_modal.modal('toggle');
    });

    $('body').on('click', '.delete-module-button', function(event) {
        var delete_modal = $('#delete-module-confirm-modal');

        delete_modal.data("module_id", $(this).attr("name"));
        //delete_modal.modal('toggle');
    });


    $('body').on('click', '#delete_confirm_button', function(event) {
        var modal = $('#delete-confirm-modal');
        var part_id = modal.data("part_id");

        $.ajax({
            type: "POST",
            url: "/delete_part",
            data: {
                part_id: part_id
            },
            dataType: "json",
            success: function(data) {
                console.log('abc');
                console.log(data.stat);
                if (data.stat == 'success') {
                    console.log('bbb');
                    var to_be_deleted = $("#part_" + part_id.toString());
                    console.log(to_be_deleted);
                    to_be_deleted.remove();
                }
                console.log('ccc');
            },
            complete: function(data) {

                modal.data("part_id", "");
            }
        });
        modal.modal('hide');
    });

    $('body').on('click', '#delete_module_confirm_button', function(event) {
        var modal = $('#delete-module-confirm-modal');
        var module_id = modal.data("module_id");

        $.ajax({
            type: "POST",
            url: "/delete_module",
            data: {
                module_id: module_id
            },
            dataType: "json",
            success: function(data) {
                window.location.reload();

            },
            complete: function(data) {

                modal.data("module_id", "");
            }
        });
        modal.modal('hide');
    });

});

