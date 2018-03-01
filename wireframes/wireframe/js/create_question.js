function getCreateForm() {
        var type = document.getElementById("question_type").value;
        var div = document.getElementById("question_form");
        var all_choice = document.createElement("div");
        all_choice.setAttribute("id", "all_choice");
        if (type === "MC") {

            div.innerHTML = "";
            for (var i = 0; i < 3; i++) {
                var choicegroup = document.createElement('div');
                choicegroup.classList.add("form-group");
                var a_label = document.createElement("label");
                a_label.innerHTML = "Choice " + String.fromCharCode(65 + i) + " : ";
                choicegroup.appendChild(a_label);
                var a_content = document.createElement("input");
                a_content.classList.add("form-control");
                a_content.classList.add("choice_content");
                choicegroup.appendChild(a_content);
                var a_correct = document.createElement("input");
                a_correct.setAttribute("type", "checkbox");
                choicegroup.appendChild(a_correct);
                var a_correct_label = document.createElement("label");
                a_correct_label.classList.add("mark_label");
                a_correct_label.innerHTML = "Mark as correct";
                choicegroup.appendChild(a_correct_label);
                all_choice.appendChild(choicegroup)
            }
            div.appendChild(all_choice);
            var add_choice_button = document.createElement("button");
            add_choice_button.innerHTML = "Add another choice";
            add_choice_button.classList.add("btn");
            add_choice_button.classList.add("btn-primary");
            add_choice_button.classList.add("add_choice_button");
            add_choice_button.setAttribute("type", "button");
            add_choice_button.setAttribute("id", "add_choice_button");
            add_choice_button.setAttribute("onclick", "add_choice()");
            add_choice_button.setAttribute("href", "javascript:void(0)");
            div.appendChild(add_choice_button);
            var delete_choice_button = document.createElement("button");
            delete_choice_button.innerHTML = "Delete last choice";
            delete_choice_button.classList.add("btn");
            delete_choice_button.classList.add("btn-secondary");
            delete_choice_button.classList.add("delete_choice_button");
            delete_choice_button.setAttribute("type", "button");
            delete_choice_button.setAttribute("id", "delete_choice_button");
            delete_choice_button.setAttribute("onclick", "delete_last_choice()");
            delete_choice_button.setAttribute("href", "javascript:void(0)");
            div.appendChild(delete_choice_button)

        } else if (type === "BF") {
            div.innerHTML = "";
            var correct_answer = document.createElement("div");
            correct_answer.setAttribute("id","correct_answer");
            var group = document.createElement('div');
            group.classList.add("form-group");
            var label = document.createElement("label");
            label.innerHTML = "Correct Answer: ";
            group.appendChild(label);
            var answer = document.createElement("input");
            answer.classList.add("form-control");
            answer.classList.add("choice_content");
            group.appendChild(answer);
            correct_answer.appendChild(group);
            div.appendChild(correct_answer);
            var add_answer_button = document.createElement("button");
            add_answer_button.innerHTML = "Add another correct answer"
            add_answer_button.classList.add("btn");
            add_answer_button.classList.add("btn-primary");
            add_answer_button.classList.add("add_answer_button");
            add_answer_button.setAttribute("type", "button");
            add_answer_button.setAttribute("id", "add_answer_button");
            add_answer_button.setAttribute("onclick", "add_correct_answer()");
            add_answer_button.setAttribute("href", "javascript:void(0)");
            div.appendChild(add_answer_button);
            var delete_answer_button = document.createElement("button");
            delete_answer_button.innerHTML = "Delete last correct answer";
            delete_answer_button.classList.add("btn");
            delete_answer_button.classList.add("btn-secondary");
            delete_answer_button.classList.add("delete_answer_button");
            delete_answer_button.setAttribute("type", "button");
            delete_answer_button.setAttribute("id", "delete_answer_button");
            delete_answer_button.setAttribute('disabled', 'disabled');
            delete_answer_button.setAttribute("onclick", "delete_correct_answer()");
            delete_answer_button.setAttribute("href", "javascript:void(0)");
            div.appendChild(delete_answer_button)
        } else {
            div.innerHTML = "";
        }
    }

    function add_choice() {
        var all_choice = document.getElementById("all_choice");
        var choicegroup = document.createElement('div');
        choicegroup.classList.add("form-group");
        var a_label = document.createElement("label");
        a_label.innerHTML = "Choice " + String.fromCharCode(65 + all_choice.childElementCount) + " : ";
        choicegroup.appendChild(a_label);
        var a_content = document.createElement("input");
        a_content.classList.add("form-control");
        a_content.classList.add("choice_content");
        choicegroup.appendChild(a_content);
        var a_correct = document.createElement("input");
        a_correct.setAttribute("type", "checkbox");
        choicegroup.appendChild(a_correct);
        var a_correct_label = document.createElement("label");
        a_correct_label.classList.add("mark_label");
        a_correct_label.innerHTML = "Mark as correct";
        choicegroup.appendChild(a_correct_label);
        all_choice.appendChild(choicegroup);
        if (all_choice.childElementCount > 2) {
            document.getElementById("delete_choice_button").removeAttribute("disabled")
        }
    }

    function delete_last_choice() {
        var all_choice = document.getElementById("all_choice");
        if (all_choice.childElementCount > 2) {
            all_choice.removeChild(all_choice.lastElementChild);
        }
        if (all_choice.childElementCount <= 2) {
            document.getElementById("delete_choice_button").setAttribute('disabled', 'disabled');
        }
    }

    function add_correct_answer() {
        var correct_answer = document.getElementById("correct_answer");
        console.log(correct_answer);
        var group = document.createElement('div');
        group.classList.add("form-group");
        var label = document.createElement("label");
        label.innerHTML = "Correct Answer: ";
        group.appendChild(label);
        var answer = document.createElement("input");
        answer.classList.add("form-control");
        answer.classList.add("choice_content");
        group.appendChild(answer);
        correct_answer.appendChild(group);
        if (correct_answer.childElementCount > 1) {
            document.getElementById("delete_answer_button").removeAttribute('disabled');
        }
    }

    function delete_correct_answer() {
        var correct_answer = document.getElementById("correct_answer");
        if (correct_answer.childElementCount > 1) {
            correct_answer.removeChild(correct_answer.lastElementChild);
        }
        if (correct_answer.childElementCount <= 1) {
            document.getElementById("delete_answer_button").setAttribute('disabled', 'disabled');
        }
    }