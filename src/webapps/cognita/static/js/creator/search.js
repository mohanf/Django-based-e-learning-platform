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

    if (!!window.performance && window.performance.navigation.type === 2) {
            // value 2 means "The page was accessed by navigating into the history"
            console.log('Reloading');
            var content = $("#search_option_form").serialize();
        $.ajax({
            type: "GET",
            url: '/search_with_option',
            data: content,
            dataType: "json",
            success: function (data) {
                //console.log('aaa');
                if (data.stat == 'success') {
                    //console.log('abc');
                    var replace_area = $('#result_area');
                    replace_area.html(data.html);
                }
            }

        });// reload whole page

        }

    var last_search = $('#last_search');
    //console.log($('#srch-term'));
    $('#srch-term').val(last_search.val());

    $("#search_option_form").change(function() {
        var content = $(this).serialize();
        $.ajax({
            type: "GET",
            url: '/search_with_option',
            data: content,
            dataType: "json",
            success: function (data) {
                //console.log('aaa');
                if (data.stat == 'success') {
                    //console.log('abc');
                    var replace_area = $('#result_area');
                    replace_area.html(data.html);
                }
            }

        });
    });
});