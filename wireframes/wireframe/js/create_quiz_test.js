function edit_title(value) {
    if (value == "Edit") {
        btn = document.getElementById("edit_title_btn");
        title_shown = document.getElementById("quiz_title_shown");
        input_title = document.createElement("input");
        input_title.id="quiz_title_input";
        input_title.value=title_shown.innerHTML;
        document.getElementById("quiz_title").insertBefore(input_title,document.getElementById("quiz_span"));
        btn.innerHTML = "Save";
        btn.id = "save_title_btn";
        title_shown.remove();
    } else {
        btn = document.getElementById("save_title_btn");
        input_title = document.getElementById("quiz_title_input");
        title_shown = document.createElement("span");
        title_shown.id="quiz_title_shown";
        title_shown.innerHTML = input_title.value.trim();
        document.getElementById("quiz_title").insertBefore(title_shown,document.getElementById("quiz_span"));
        btn.innerHTML = "Edit";
        btn.id = "edit_title_btn"
        input_title.remove();
    }
}

function edit_description(value) {
    if (value == "Edit") {
        btn = document.getElementById("edit_description_btn");
        description_shown = document.getElementById("quiz_description_shown");
        input_decription_div = document.createElement("div");
        input_decription = document.createElement("textarea");
        input_decription.id="quiz_description_input";
        input_decription.value=description_shown.innerText;
        input_decription.classList.add("form-control");
        input_decription.setAttribute("rows","3");
        document.getElementById("quiz_description").appendChild(input_decription);
        btn.innerHTML = "Save";
        btn.id = "save_description_btn";
        description_shown.remove();
    } else {
        btn = document.getElementById("save_description_btn");
        input_description = document.getElementById("quiz_description_input");
        description_shown = document.createElement("div");
        description_shown.id="quiz_description_shown";
        description_shown.innerHTML = input_description.value.trim().replace(/\n\r?/g, '<br />');
        document.getElementById("quiz_description").appendChild(description_shown);
        btn.innerHTML = "Edit";
        btn.id = "edit_description_btn"
        input_description.remove();
    }
}
