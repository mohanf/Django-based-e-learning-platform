$(document).ready(function () {

    $(function () {
        $('body').confirmation({
            selector: '[data-toggle="confirmation"]'
        });
        $('#question_list_table').confirmation({
            selector: '.btn-delete-question',
            onConfirm: function (event) {
                $.post("/delete_question/", {
                        question_id: $(this).parent().parent().attr("id")
                    }
                ).done(function (data) {
                    $("#" + data['question_id']).nextAll().each(function () {

                        if ($('#save-order')) {
                            var current = parseInt($(this).children("th").eq(0).text())-1;
                            $(this).children("th").eq(0).html('<span class="ui-icon ui-icon-arrow-4-diag handle"></span>'+current);
                        } else {
                            var current = $(this).children("th").eq(0).html();
                            $(this).children("th").eq(0).html(parseInt(current) - 1);
                        }
                    });
                    $("#" + data['question_id']).remove();

                });
            }
        });
    });

    $("#edit_btn").click(function (event) {
        $(".val_error").remove();
        if (event.target.innerHTML === "Edit") {
            var title_shown = $("#title_shown");
            var title_input = $('<input id="title_input" class="form-control title-input" value="' + title_shown.html() + '">');
            $("#title").prepend(title_input);
            var description_shown = $("#description_shown");
            var description_input = $('<div><textarea class="form-control" id="description_input" rows="2">' + description_shown.html().trim() + '</textarea></div>');
            description_shown.remove();
            $("#description").append(description_input);
            var full_score_shown = $("#full_score_shown");
            var full_score_input = $('<input class="form-control full-score-input" id="full_score_input" value="' + full_score_shown.html() + '">');
            full_score_shown.remove();
            $("#full_score").append(full_score_input);
            var expected_hour_shown = $("#expected_hour_shown");
            var expected_hour_input = $('<input class="form-control expected-hour-input" id="expected_hour_input" value="' + expected_hour_shown.html() + '">');
            expected_hour_shown.remove();
            $("#expected_hour").append(expected_hour_input);
            $(this).html('Save');
            title_shown.remove();
        } else {
            var input_title = $("#title_input");
            var path = window.location.pathname;
            if (path.substring(1, 12) === "update_test") {
                var test_id = path.substring(path.indexOf('update_test/') + 12, path.lastIndexOf('/'));
                url = "/update_test_info/" + test_id + '/'
            }
            if (path.substring(1, 12) === "update_quiz") {
                var quiz_id = path.substring(path.indexOf('update_quiz/') + 12, path.lastIndexOf('/'));
                url = "/update_quiz_info/" + quiz_id + '/'
            }
            $.post(url, {
                    title: input_title.val().trim(),
                    description: $("#description_input").val().trim(),
                    full_score: $("#full_score_input").val().trim(),
                    expected_hour: $("#expected_hour_input").val().trim()
                }
            ).done(function (data) {
                if (data['success'] == true) {
                    var title_shown = $('<span id="title_shown">' + data['form'].title + '</span>');
                    $("#title").prepend(title_shown);
                    input_title.remove();
                    var description_shown = $('<div id="description_shown">' + data['form'].description + '</div>');
                    $("#description").append(description_shown);
                    $("#description_input").remove();
                    var full_score_input = $("#full_score_input");
                    var full_score_shown = $('<span id="full_score_shown">' + data['form'].full_score + '</span>');
                    full_score_input.remove();
                    $("#full_score").append(full_score_shown);
                    var expected_hour_input = $("#expected_hour_input");
                    var expected_hour_shown = $('<span id="expected_hour_shown">' + data['form'].expected_hour + '</span>');
                    expected_hour_input.remove();
                    $("#expected_hour").append(expected_hour_shown);
                    $("#edit_btn").html('Edit');
                } else {
                    input_title.val(data['form'].title);
                    $("#description_input").val(data['form'].description);
                    $("#full_score_input").val(data['form'].full_score);
                    $("#expected_hour_input").val(data['form'].expected_hour);
                    if (typeof((data['error'].title)) != 'undefined') {
                        var title_error = $('<div class="val_error">' + data['error'].title + '</div>');
                        $("#title").append(title_error)
                    }
                    if (typeof((data['error'].description)) != 'undefined') {
                        var description_error = $('<div class="val_error">' + data['error'].description + '</div>');
                        $("#description").append(description_error)
                    }
                    if (typeof((data['error'].full_score)) != 'undefined') {
                        var full_score_error = $('<div class="val_error">' + data['error'].full_score + '</div>');
                        $("#full_score").append(full_score_error)
                    }
                    if (typeof((data['error'].expected_hour)) != 'undefined') {
                        var expected_hour_error = $('<div class="val_error">' + data['error'].expected_hour + '</div>');
                        $("#expected_hour").append(expected_hour_error)
                    }
                }
            });

        }
    });

    $("table").on('click', '#reorder-questions', function (event) {
        $("table tbody").sortable({
            update: function (event, ui) {
                $(this).children().each(function (index) {
                    $(this).find('th').first().html('<span class="ui-icon ui-icon-arrow-4-diag handle"></span>'+(index + 1))
                });
            }
        });
        var options = $("table tbody").sortable("enable");
        $('<div class="alert alert-warning reorder-alert"><strong>Please drag the questions to reorder them.</strong></div>').insertBefore($("table"))
        $('table tbody').addClass('reorder-table');
        $('table tbody').children().each(function() {
            $(this).children().eq(0).prepend('<span class="ui-icon ui-icon-arrow-4-diag handle"></span>')
        });
        $(this).html(' Save Order ');
        $(this).attr('id', 'save-order');
    });

    $("table").on('click', '#save-order', function (event) {
        var trs = $("tbody").find("tr");
        var question_ids = {};
        for (var i = 0; i < trs.length; i++) {
            question_ids[i] = trs.get(i).id;
        }

        $.post("/reorder_questions/", {
            id: parseInt(window.location.pathname.split('/')[2]),
            question_ids: question_ids,
            type: window.location.pathname.split('/')[1].split('_')[1]
        }).done(function (data) {
            $("table tbody").sortable('disable');
            $(".alert").remove();
            $("table tbody").removeClass('reorder-table');
            $("#save-order").html(' Reorder Questions ');
            $("#save-order").attr('id', 'reorder-questions');
            $('.ui-icon-arrow-4-diag').remove();
        });
    });

    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });


});

