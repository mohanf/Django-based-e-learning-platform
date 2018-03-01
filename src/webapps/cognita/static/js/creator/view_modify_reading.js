$(document).ready(function () {
    var mode = $("#mode");
    if (mode.val() == 'view') {
        $("#view_button").tab('show');
    } else {
        $("#modify_button").tab('show');
    }
});