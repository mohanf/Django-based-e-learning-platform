//document.getElementsByClassName("form-area").style.display = "none";
var n = document.getElementsByClassName("form-area");
var big_form = document.getElementsByClassName("course-form-area");
for (var i = 0; i < n.length; i++) {
    n[i].style.display = "none";
}
for (var i = 0; i < big_form.length; i++) {
    big_form[i].style.display = "none";
}

var manage = document.getElementsByClassName("manage");
var modify = document.getElementById("modify");
modify.addEventListener("click", function() {
    console.log(this.parentNode.parentNode.nextSibling.nextSibling);
    this.parentNode.parentNode.nextSibling.nextSibling.childNodes[1].style.display = "inline";
});
for (var j = 0; j < manage.length; j++) {
    manage[j].addEventListener("click", function() {
        var a = this.parentNode;
    var b = a.parentNode;
    var c = b.parentNode;
    var d = c.nextElementSibling;
    var e = d.childNodes[1];
    //console.log(d.innerHTML);

    //console.log(f);
    //var form = this.parentNode.parentNode.parentNode.nextSibling.childNodes[0].childNodes[0].childNodes[0];
    e.style.display = "inline";
    })
}

var save_button_small = document.getElementsByClassName("save-button-small");
for (var k = 0; k < save_button_small.length; k++) {
    save_button_small[k].addEventListener("click", function () {
        var hided = this.parentNode.parentNode.parentNode;
        hided.style.display = "none";
    })
}




