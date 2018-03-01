

$(document).ready(function () {

    save_answer();
    $(".question_list a").on('click', function(event) {
        activeList(event.target.id)
    });

    function activeList(id) {
        var question_list = $(".question_list");
        for (var i = 0; i < question_list.length; i++) {
            question_list.eq(i).removeClass("active");
        }
        $("#"+id).parent().addClass("active");
    }

    function save_answer() {
        var data = $("form").serializeArray();
        var pathstrings = window.location.pathname.split('/');
        data.push({name:'quiz_or_test', value:pathstrings[1]});
        data.push({name:'quiz_or_test_id', value:pathstrings[2]});
        $.post("/save_quiz_test_answer/", data
            ).done(function () {
                $(".saved").show().delay(400).fadeOut()
            })
    }

    $(".question_option").on('change', function() {
        save_answer()
    });

    $(".question_blank input").on('change', function() {
        save_answer()
    });

    $("#btn-save").click(function(event) {
        event.preventDefault();
        save_answer();
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