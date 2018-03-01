function activeList(id) {
    var question_list = document.getElementsByClassName("question_list");
    for (var i = 0; i < question_list.length; i++) {
        question_list[i].classList.remove("active");
    }
    document.getElementById(id).parentNode.classList.add("active");  
}