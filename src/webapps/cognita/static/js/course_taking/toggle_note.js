function toggle_note(module_id) {
    console.log(module_id);
    $("#note"+module_id).toggleClass("note");
    $("#content"+module_id).toggleClass("col-sm-12 col-sm-8");
    if ($("#toggle-note-button"+module_id).html() == "Show Notes") {
        $("#toggle-note-button"+module_id).html("Hide Notes");
    }
    else {
        $("#toggle-note-button"+module_id).html("Show Notes");
    }
    if ( !$("#module"+module_id).hasClass("in") ) {
        $("#expand-link" + module_id).trigger('click');
    }
}
