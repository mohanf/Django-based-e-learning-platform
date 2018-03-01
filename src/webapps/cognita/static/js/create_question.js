$(document).ready(function () {
    $("#all_choice").delegate("button", "click", function (event) {
        event.preventDefault();
        $(this).parent().remove();
        if ($("#all_choice").children().length <= 2) {
            for (var i = 0; i < $("#all_choice").children().length; i++) {
                $(".choice").eq(i).children("button").eq(0).attr('disabled', 'True');
            }
        }
        for (var i = 0; i < $("#all_choice").children().length; i++) {
            $(".choice").eq(i).attr('id', "choice_"+i);
            $(".choice").eq(i).children("button").eq(0).attr('id', "delete_"+i);
            $(".choice").eq(i).children("label").eq(0).html('Choice ' + String.fromCharCode(65 + i) + ' : ');
            $(".choice").eq(i).children("input").eq(1).val(String.fromCharCode(65 + i) );
        }
    });


     $("#correct_answer").on(".delete_answer", "click", function (event) {
        event.preventDefault();
        $(this).parent().remove();
        if ($("#correct_answer").children().length <= 1) {
            $(".answer").eq(0).children("button").eq(0).attr('disabled', 'True');
        }
        for (var i = 0; i < $("#correct_answer").children().length; i++) {
            $(".answer").eq(i).attr('id', "answer_"+i);
            $(".answer").eq(i).children("button").eq(0).attr('id', "delete_"+i);
            $(".answer").eq(i).children("label").eq(0).html('Choice ' + String.fromCharCode(65 + i) + ' : ');
            $(".answer").eq(i).children("input").eq(1).val(String.fromCharCode(65 + i) );
        }
    });

    $("#question_type").change(function () {
        getCreateForm()
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


function getCreateForm() {
    var type = $("#question_type").val();
    var div = $("#question_form");
    var all_choice = $('<div id="all_choice"></div>');

    if (type === "MC") {
        div.empty();
        div.append(all_choice);
        $("#all_choice").delegate("button", "click", function (event) {
            event.preventDefault();
            console.log();
            $(this).parent().remove();
            if ($("#all_choice").children().length <= 2) {
                for (var i = 0; i < $("#all_choice").children().length; i++) {
                    $(".choice").eq(i).children("button").eq(0).attr('disabled', 'True');
                }
            }
            for (var i = 0; i < $("#all_choice").children().length; i++) {
                $(".choice").eq(i).children("label").eq(0).html('Choice ' + String.fromCharCode(65 + i) + ' : ');
            }
        });
        for (var i = 0; i < 3; i++) {
            var choicegroup = $('<div class="form-group choice"><button class="btn btn-success delete_choice"" id="delete_choice_button' + i + '">Delete</button>&nbsp;</div>');
            var a_label = $('<label class="choice-label">Choice ' + String.fromCharCode(65 + i) + ' : </label>');
            choicegroup.append(a_label);
            var a_content = $('<input class="form-control choice_content" required name="content">&nbsp;<input type="checkbox" name="choice_correct">&nbsp;<label class="mark_label">Mark as correct</label>');
            choicegroup.append(a_content);
            all_choice.append(choicegroup)
        }
        var add_choice_button = $('<button type="button" id="add_choice_button" href="javascript:void(0)"' +
            ' class="btn btn-primary add_choice_button">Add another choice</button>');
        add_choice_button.click(function () {
            add_choice()
        });
        div.append(add_choice_button);

    } else if (type === "BF") {
        div.empty();
        var correct_answer = $('<div id="correct_answer"><div class="form-group answer"><button class="btn btn-success delete_answer" disabled id="delete_answer_button_0">Delete</button>&nbsp;<label>Correct Answer: </label><input class="form-control choice_content" name="answer" required></div></div>');
        div.append(correct_answer);
        correct_answer.delegate("button", "click", function (event) {
            event.preventDefault();
            $(this).parent().remove();
            if (correct_answer.children().length <= 1) {
                for (var i = 0; i < correct_answer.children().length; i++) {
                    $(".answer").eq(i).children("button").eq(0).attr('disabled', 'True');
                }
            }
        });
        var add_answer_button = $('<button type="button" id="add_answer_button" onclick="add_correct_answer()" href="javascript:void(0)" class="btn btn-primary add_answer_button">Add another correct answer</button>');
        div.append(add_answer_button);
    } else {
        div.empty();
    }
}

function add_choice() {
    var all_choice = $("#all_choice");
    var choicegroup = $('<div id="choice_' + (all_choice.children().length) + '" class="form-group choice"><button id="delete_' + (all_choice.children().length + 1) + '" class="btn btn-success delete_choice">Delete</button>&nbsp;</div>');
    var a_label = $('<label class="choice-label">Choice ' + String.fromCharCode(65 + all_choice.children().length) + ' :</label>');
    choicegroup.append(a_label);
    var a_content = $('<input class="form-control choice_content" name="content">&nbsp;<input type="checkbox" name="choice_correct" value="'+String.fromCharCode(65 + all_choice.children().length)+'">&nbsp;<label class="mark_label">Mark as correct</label>');
    choicegroup.append(a_content);
    all_choice.append(choicegroup);
    if ($("#all_choice").children().length > 2) {
        for (var i = 0; i < 2; i++) {
            $(".choice").eq(i).children("button").eq(0).removeAttr('disabled');
        }
    }
}


function add_correct_answer() {
    var correct_answer = $("#correct_answer");
    var group = $('<div class="form-group answer"><button class="btn btn-success delete_answer" id="delete_answer_button_' + correct_answer.children().length + '">Delete</button>&nbsp;<label>Correct Answer: </label><input class="form-control choice_content" required name="answer"></div>');
    correct_answer.append(group);
    if (correct_answer.children().length > 1) {
        $(".delete_answer").removeAttr('disabled');
    }
}
