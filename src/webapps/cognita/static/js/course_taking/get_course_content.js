function populateRegister() {
    $.get("/registerbutton/"+window.location.pathname.split('/')[2])
        .done(
            function(data) {
                var button = $("#reg_button");
                button.html('');
                button.append(data);
                $("#take-or-drop").unbind().click(takeOrDrop);
            }
        );
}

function populateContent() {
    $.get("/coursecontent/"+window.location.pathname.split('/')[2])
        .done(
            function(data) {
                var list = $("#course-content-list");
                list.html('');
                list.append(data);
                $('.mark-progress').unbind().click(markComplete);
                $('.note').each(function () {
                     lecture_id = $(this).attr('id').split('_')[1];
                     console.log('in parent function');
                     console.log(lecture_id);
                     populateNote(lecture_id);
                });
            }
        )
}

function populateNote(lecture_id){
         //get notes
        $.get("/getnote/"+lecture_id)
            .done(
                function (data) {
                    console.log('in child function');
                    console.log(lecture_id);
                    var note = $("#note_"+lecture_id);
                    note.html('');
                    note.append(data);
                     CKEDITOR.replace('notearea'+lecture_id, {
                        height: 500,
                        width: 'auto',
                        toolbar: [
                            { name: 'clipboard', items: [ 'Undo', 'Redo' ] },
                            { name: 'styles', items: [ 'Styles', 'Format' ] },
                            { name: 'basicstyles', items: [ 'Bold', 'Italic','Strike' ] },
                            { name: 'insert', items: [ 'Image', 'Table' ] },
                            { name: 'links', items: [ 'Link', 'Unlink' ] }
                        ],
                         filebrowserUploadUrl: '/ckeditor/upload/',
                         // filebrowserBrowseUrl: '/ckeditor/upload/',
                         filebrowserBrowseUrl: ''
                    });
                    $(".save-note").unbind().click(savenote);
                }

            );
}

function savenote(e) {
    e.preventDefault();
    var id = $(this).attr('id').split('_')[1];
    console.log(id);
    var note = CKEDITOR.instances['notearea_'+id].getData();
    var lecture_id = $('#lecture_id_'+id).val();
    console.log(note);
    console.log(lecture_id);
    $.post("/savenote/", {"note":note, "lecture_id":lecture_id})
        .done(
            function(data){
                // console.log("******");
                // console.log(data);
                $('#save_info_'+id).html(data);
                $('#save_info_'+id).show().delay(1000).fadeOut();
            }
        )
}

function takeOrDrop(e) {
    e.preventDefault();
    var course_id = $('#take_course_id').val();
    $.post("/toggleregister/",  {"course": course_id})
        .done(
            function () {
                populateRegister();
                populateContent();
            }
        )
}
function markComplete(e) {
    e.preventDefault();
    console.log('mark completed');
    var button_id = $(this).attr('id');
    var id = button_id.split('_')[2];
    var part_id = $('#progress_part_'+id).val();
    $.post('/toggleprogress/', {'part':part_id})
        .done(
            function (data) {
                var button = $('#progress_button_'+id);
                button.val('');
                button.val(data);
                if(data === 'Completed')
                    button.attr('class','btn btn-xs btn-default mark-progress');
                else
                    button.attr('class','btn btn-xs btn-success mark-progress');
            }
        )
}
$(document).ready(function () {
    populateRegister();
    populateContent();
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
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });


  CKEDITOR.on('instanceReady', function(evt) {

        var editor = evt.editor;

        var timeoutId;
        editor.on('change',function () {
            lecture_id = editor.name.split('_')[1];
            console.log("this lecture note has benn edited:");
            console.log(lecture_id);
            if (timeoutId) clearTimeout(timeoutId);
            timeoutId = setTimeout(function () {
                $.post("/savenote/", {"note":editor.getData(), "lecture_id":lecture_id})
                    .done(
                        function(data){
                            console.log("auto-saved lecture: ");
                            console.log(lecture_id);
                            console.log(data);
                            $('#save_info_'+lecture_id).html(data);
                            $('#save_info_'+lecture_id).show().delay(1000).fadeOut();
                        }
                    )
            }, 750);
        });
    });

});