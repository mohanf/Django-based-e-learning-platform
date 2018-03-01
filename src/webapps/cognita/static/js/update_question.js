$(document).ready(function () {
    $(function () {
        $('body').confirmation({
            selector: '[data-toggle="confirmation"]'
        });
        $('#all_choice').confirmation({
            selector: '.btn-delete-choice',
            onConfirm: function (event) {
                // event.preventDefault();
                if (!isNaN(parseInt($(this).parent().parent().attr("id")))) {
                    $.post("/delete_choice/", {
                            choice_id: $(this).parent().parent().attr("id")
                        }
                    ).done(function (data) {
                        $(".val_error").remove();
                        if (data['error_message']) {
                            var error = $('<div class="val_error">' + data['error_message'] + '<br></div>');
                            error.insertBefore($("#question_form"))
                        } else {
                            $("#" + data['choice_id']).remove();
                            if ($("#all_choice").children().length <= 2) {
                                for (var i = 0; i < $("#all_choice").children().length; i++) {
                                    $(".choice").eq(i).children("td").eq(2).children("button").attr('disabled', 'True');
                                }
                            }
                            for (var i = 0; i < $("#all_choice").children().length; i++) {
                                $(".choice").eq(i).children("th").eq(0).html(String.fromCharCode(65 + i));
                            }
                        }
                    });
                } else {
                    $(".val_error").remove();
                    $(this).parent().parent().remove();
                    for (var i = 0; i < $("#all_choice").children().length; i++) {
                        $(".choice").eq(i).children("th").eq(0).html(String.fromCharCode(65 + i));
                    }
                }
            }
        });

        $('#correct_answer').confirmation({
            selector: '.btn-delete-answer',
            onConfirm: function (event) {
                deleteAnswer($(this).parent().parent());
            }
        });
    });

    if ($("#all_choice").children().length <= 2) {
        for (var i = 0; i < $("#all_choice").children().length; i++) {
            $(".choice").eq(i).children("td").eq(2).children("button").attr('disabled', 'True');
        }
    }
    $("#all_choice").on('change', "input[type=checkbox]", function () {
        if ($(this).val() == "true") {
            $(this).val("false")
        } else {
            $(this).val("true")
        }
    });

    if ($("#correct_answer").children("tr").length <= 1) {
        $(".answer").eq(0).children("td").eq(1).children("button").eq(1).attr('disabled', 'True');
    }

    $("#all_choice").on("click", ".btn-edit-choice", function (event) {
        event.preventDefault();
        editChoice($(this))
    });

    $("#all_choice").on("click", ".btn-add-choice", function (event) {
        event.preventDefault();
        saveAddChoice($(this).parent().parent().parent())
    });

    // $("#correct_answer").on("click", ".btn-delete-answer", function (event) {
    //     event.preventDefault();
    //     // deleteAnswer($(this).parent().parent());
    // });

    $("#correct_answer").on("click", ".btn-edit-answer", function (event) {
        event.preventDefault();
        editAnswer($(this));
    });

    $("#correct_answer").on("click", ".btn-save-answer", function (event) {
        event.preventDefault();
        updateAnswer($(this).parent().parent().attr("id"));
    });

    $("#correct_answer").on("click", ".btn-add-answer", function (event) {
        event.preventDefault();
        saveAddAnswer($(this).parent().parent());
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


function add_choice() {
    var all_choice = $("#all_choice");
    var choicegroup = $('<tr id="choice_' + (all_choice.children().length) + '" class="add_choice"><th><label class="choice-label">' + String.fromCharCode(65 + all_choice.children().length) + '</label></th></tr>');
    var correct = $('<td><input type="checkbox" name="choice_correct" value="false"><label class="mark_label">Mark as correct</label></td>');
    choicegroup.append(correct);
    var a_content = $('<td><input class="form-control choice_content_updatepage" name="content"></td>');
    choicegroup.append(a_content);
    var button = $('<td><a><button class="btn btn-primary btn-choice-answer btn-add-choice" type="button">Save</button></a>&nbsp;<button class="btn btn-success btn-choice-answer btn-delete-choice" data-toggle="confirmation" type="button">Delete</button></td>');
    choicegroup.append(button);
    all_choice.append(choicegroup);
}

function add_correct_answer() {
    var correct_answer = $("#correct_answer");
    var answer_tr = $('<tr id="answer_' + (correct_answer.children().length) + '" class="add_answer"><th>' + (correct_answer.children().length + 1 ) + '</label></th></tr>');
    var answer = $('<td><input class="form-control choice_content_updatepage" name="answer"></td>');
    answer_tr.append(answer);
    var button = $('<td><button class="btn btn-primary btn-choice-answer btn-add-answer" type="button">Save</button>&nbsp;<button class="btn btn-success btn-choice-answer btn-delete-answer" data-toggle="confirmation" type="button">Delete</button></td>');
    answer_tr.append(button);
    correct_answer.append(answer_tr);
}

function editChoice(obj) {
    var choice_id = obj.parent().parent().parent().attr("id");
    var correct_tr = obj.parent().parent().parent().children("td").eq(0);
    if (correct_tr.children("i").eq(0).attr("class") === "glyphicon glyphicon-ok") {
        correct_tr.empty();
        // $(this).parent().parent().parent().children("th").eq(0).html()
        correct_tr.append($('<input type="checkbox" name="choice_correct" checked value="true"><label class="mark_label">Mark as correct</label>'))
    } else {
        correct_tr.empty();
        correct_tr.append($('<input type="checkbox" name="choice_correct" value="false"><label class="mark_label">Mark as correct</label>'))
    }
    var content_tr = obj.parent().parent().parent().children("td").eq(1);
    var content = content_tr.text();
    var a_content = $('<input class="form-control choice_content_updatepage" name="content" value="' + content + '">');
    content_tr.empty();
    content_tr.append(a_content);
    obj.html("Save");
    obj.removeClass("btn-edit-choice");
    obj.addClass("btn-save-choice");
    obj.click(function (event) {
        event.preventDefault();
        updateChoice(choice_id)
    });
}

function editAnswer(obj) {
    var answer_id = obj.parent().parent().attr("id");
    var answer_tr = obj.parent().parent().children("td").eq(0);
    var answer = answer_tr.text();
    var a_answer = $('<input class="form-control choice_content_updatepage" name="answer" value="' + answer + '">');
    answer_tr.empty();
    answer_tr.append(a_answer);
    obj.html("Save");
    obj.removeClass("btn-edit-answer");
    obj.addClass("btn-save-answer");
}

function saveAddChoice(obj) {
    $.post("/add_choice/", {
        question_id: parseInt(window.location.pathname.split('/')[2]),
        content: obj.children("td").eq(1).children("input").val(),
        correct: obj.children("td").eq(0).children("input").val()
    }).done(function (data) {
        $(".val_error").remove();
        $("#all_choice .choice:last").nextAll().remove();
        if (data['error_message']) {

            var error = $('<div class="val_error">' + data['error_message'] + '<br></div>');
            error.insertBefore($("#question_form"));
            var choice_tr = $('<tr></tr>');
            var choice_th = $('<th><label class="choice-label">' + String.fromCharCode($("#all_choice").children(".choice").length + 65) + '</label></th>')
            choice_tr.append(choice_th);
            var correct_td = $('<td></td>');
            if (data['correct'] == true) {
                correct_td.append($('<input type="checkbox" name="choice_correct" checked value="true"><label class="mark_label">Mark as correct</label>'))
            } else {
                correct_td.append($('<input type="checkbox" name="choice_correct" value="false"><label class="mark_label">Mark as correct</label>'))
            }
            choice_tr.append(correct_td);
            if (data['content'] == null) {
                data['content'] = '';
            }
            var a_content = $('<input class="form-control choice_content_updatepage" name="content" value="' + data['content'] + '">');
            choice_tr.append(a_content);
            var button = $('<td><button class="btn btn-primary btn-choice-answer btn-add-choice" type="button">Save</button>&nbsp;<button class="btn btn-success btn-choice-answer btn-delete-choice" data-toggle="confirmation" type="button">Delete</button></td>')
            choice_tr.append(button);
            choice_tr.insertAfter($("#all_choice .choice:last"));
        } else {
            var choice_tr = $('<tr id="' + data["choice_id"] + '" class="choice"></tr>');
            var choice_th = $('<th><label class="choice-label">' + String.fromCharCode($("#all_choice").children(".choice").length + 65) + '</label></th>');
            choice_tr.append(choice_th);
            var correct_td = $('<td></td>');
            if (data['correct'] == true) {
                correct_td.empty();
                correct_td.append($('<i class="glyphicon glyphicon-ok"></i>'))
            } else {
                correct_td.empty();
                correct_td.append($('<i class="glyphicon glyphicon-remove"></i>'))
            }
            choice_tr.append(correct_td);
            var a_content = $('<td></td>');
            a_content.text(data['content'])
            choice_tr.append(a_content);
            var button = $('<td><a><button class="btn btn-primary btn-choice-answer btn-edit-choice" type="button">Edit</button></a>&nbsp;<button class="btn btn-success btn-choice-answer btn-delete-choice" data-toggle="confirmation" type="button">Delete</button></td>')
            choice_tr.append(button);
            choice_tr.insertAfter($("#all_choice .choice:last"));
        }
    });
}

function updateChoice(choice_id) {
    $.post("/update_choice/", {
        choice_id: choice_id,
        content: $("#all_choice #" + choice_id).children("td").eq(1).children("input").val(),
        correct: $("#all_choice #" + choice_id).children("td").eq(0).children("input").val()
    }).done(function (data) {
        $(".val_error").remove();
        if (data['error_message']) {
            var error = $('<div class="val_error">' + data['error_message'] + '<br></div>');
            error.insertBefore($("#question_form"));
            var choice_tr = $("#all_choice #" + data['choice_id']);
            var correct_td = choice_tr.children("td").eq(0);
            if (data['correct'] == true) {
                correct_td.empty();
                correct_td.append($('<input type="checkbox" name="choice_correct" checked value="true"><label class="mark_label">Mark as correct</label>'))
            } else {
                correct_td.empty();
                correct_td.append($('<input type="checkbox" name="choice_correct" value="false"><label class="mark_label">Mark as correct</label>'))
            }
            var a_content = $('<input class="form-control choice_content_updatepage" name="content" value="' + data['content'] + '">');
            choice_tr.children("td").eq(1).empty();
            choice_tr.children("td").eq(1).append(a_content);
        } else {
            var btn = $("#all_choice #" + data["choice_id"]).children("td").eq(2).children("a").eq(0).children("button").eq(0);
            var choice_tr = $("#all_choice #" + data['choice_id']);
            var correct_td = choice_tr.children("td").eq(0);
            if (data['correct'] == true) {
                correct_td.empty();
                correct_td.append($('<i class="glyphicon glyphicon-ok"></i>'))
            } else {
                correct_td.empty();
                correct_td.append($('<i class="glyphicon glyphicon-remove"></i>'))
            }

            choice_tr.children("td").eq(1).text(data['content']);
            btn.html("Edit");
            btn.removeClass("btn-save-choice");
            btn.off('click');
            btn.addClass("btn-edit-choice");
        }
    });
}

function updateAnswer(answer_id) {
    $.post("/update_answer/", {
        answer_id: answer_id,
        answer: $("#correct_answer #" + answer_id).children("td").eq(0).children("input").val().trim()
    }).done(function (data) {
        $(".val_error").remove();
        if (data['error_message']) {
            var error = $('<div class="val_error">' + data['error_message'] + '<br></div>');
            error.insertBefore($("#question_form"));
            var answer_tr = $("#correct_answer #" + data['answer_id']);
            var a_answer = $('<input class="form-control choice_content_updatepage" name="answer" value="' + data['answer'] + '">');
            answer_tr.children("td").eq(1).empty();
            answer_tr.children("td").eq(1).append(a_answer);
        } else {
            var btn = $("#correct_answer #" + data["answer_id"]).children("td").eq(1).children("button").eq(0);
            var answer_tr = $("#correct_answer #" + data['answer_id']);
            var answer_td = answer_tr.children("td").eq(0);
            answer_tr.children("td").eq(0).text(data['answer']);
            btn.html("Edit");
            btn.removeClass("btn-save-answer");
            btn.off('click');
            btn.addClass("btn-edit-answer");
        }
    });
}

function deleteAnswer(obj) {
    if (!isNaN(parseInt(obj.attr("id")))) {
        $.post("/delete_answer/", {
                answer_id: obj.attr("id")
            }
        ).done(function (data) {
            $(".val_error").remove();
            if (data['error_message']) {
                var error = $('<div class="val_error">' + data['error_message'] + '<br></div>');
                error.insertBefore($("#question_form"))
            } else {
                $("#" + data['answer_id']).remove();
                if ($("#correct_answer").children(".answer").length <= 2) {
                    for (var i = 0; i < $("#correct_answer").children(".answer").length; i++) {
                        $(".answer").eq(0).children("td").eq(1).children("button").eq(1).attr('disabled', 'True');
                    }
                }
                for (var i = 0; i <= $("#correct_answer").children().length; i++) {
                    $(".answer").eq(i).children("th").eq(0).html(i + 1);
                }
            }
        });
    } else {
        $(".val_error").remove();
        obj.remove();
        for (var i = 1; i <= $("#correct_choice").children().length; i++) {
            $(".answer").eq(i).children("th").eq(0).html(i);
        }
    }
}

function saveAddAnswer(obj) {
    $.post("/add_answer/", {
        question_id: parseInt(window.location.pathname.split('/')[2]),
        answer: obj.children("td").eq(0).children("input").val().trim()
    }).done(function (data) {
        $(".val_error").remove();
        $("#correct_answer .answer:last").nextAll().remove();
        if (data['error_message']) {
            var error = $('<div class="val_error">' + data['error_message'] + '<br></div>');
            error.insertBefore($("#question_form"));
            var answer_tr = $('<tr></tr>');
            var answer_th = $('<th><label class="choice-label">' + ($("#correct_answer").children(".answer").length + 1) + '</label></th>');
            answer_tr.append(answer_th);
            var a_content = $('<td><input class="form-control choice_content_updatepage" name="content" value="' + data['answer'].toString() + '"></td>');
            answer_tr.append(a_content);
            var button = $('<td><button class="btn btn-primary btn-choice-answer btn-add-answer" type="button">Save</button>&nbsp;<button class="btn btn-success btn-choice-answer btn-delete-answer" data-toggle="confirmation" type="button">Delete</button></td>')
            answer_tr.append(button);
            answer_tr.insertAfter($("#correct_answer .answer:last"));
        } else {
            var answer_tr = $('<tr id="' + data["answer_id"] + '" class="answer"></tr>');
            var answer_th = $('<th><label class="choice-label">' + ($("#correct_answer").children(".answer").length + 1) + '</label></th>');
            answer_tr.append(answer_th);
            var a_content = $('<td>' + data['answer'] + '</td>');
            answer_tr.append(a_content);
            var button = $('<td><button class="btn btn-primary btn-choice-answer btn-edit-answer" type="button">Edit</button>&nbsp;<button class="btn btn-success btn-choice-answer btn-delete-answer" data-toggle="confirmation" type="button">Delete</button></td>')
            answer_tr.append(button);
            answer_tr.insertAfter($("#correct_answer .answer:last"));
            if ($("#correct_answer").children(".answer").length > 1) {
                for (var i = 0; i < $("#correct_answer").children(".answer").length; i++) {
                    $(".answer").eq(0).children("td").eq(1).children("button").eq(1).attr('disabled', 'False');
                }
            }
        }
    });
}