/* Javascript for StudioEditableXBlockMixin. */
function ProctoruStudio(runtime, element) {
    "use strict";

    $("#exam-start-date").datepicker();
    $("#exam-end-date").datepicker();

    $(element).find('.cancel-button').bind('click', function(e) {
        e.preventDefault();
        runtime.notify('cancel', {});
    });

    this.save = function (){

        var exam_data = {
            'exam_name': $("#exam-name").val(),
            'exam_description': $("#exam-description").val(),
            'exam_duration': $("#exam-duration").val(),
            'exam_start_date': $('#exam-start-date').val(),
            'exam_end_date': $('#exam-end-date').val(),
            'exam_start_time': $('#exam-start-time').val(),
            'exam_end_time': $('#exam-end-time').val(),
            'exam_notes': $("#exam-notes").val(),
            'time_zone':$("#time-zone").val()
        };

        var validate = validateExamFormData(exam_data)

        if(validate){
            var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
            $.post(handlerUrl, JSON.stringify(exam_data), function(data,status){
                if(data.status==='success'){
                    location.reload();
                }
            });
        }
    }

}

var validateExamFormData = function(data){
    if (data.exam_start_date == ""){
        $("#exam-start-date-error").css("display", "inline-block");
        return false
    } else {
        $("#exam-start-date-error").hide();
    }

    if(data.exam_end_date == ""){
        $("#exam-end-date-error").css("display", "inline-block");
        return false
    } else {
        $("#exam-end-date-error").hide();
    }


    if(data.exam_name == ""){
        $("#exam-name-error").css("display", "inline-block");
        return false
    } else {
        $("#exam-name-error").hide();
    }


    if(data.exam_description == "" | data.exam_description.length > 255){
        $("#exam-description-error").css("display", "inline-block");
        return false
    } else {
        $("#exam-description-error").hide();
    }


    if(data.exam_start_time == ""){
        $("#exam-start-time-error").css("display", "inline-block");
        retustart-time
    } else {
        $("#exam-start-time-error").hide();
    }


    if(data.exam_end_time == ""){
        $("#exam-end-time-error").css("display", "inline-block");
        return false
    } else {
        $("#exam-end-time-error").hide();
    }

    if(data.exam_notes == ""){
        $("#exam-notes-error").css("display", "inline-block");
        return false
    } else {
        $("#exam-notes-error").hide();
    }

    if(data.exam_password == ""){
        $("#exam-password-error").css("display", "inline-block");
        return false
    } else {
        $("#exam-password-error").hide();
    }

    if(data.time_zone == "Fuseau horaire"){
        $("#timezone-error").css("display", "inline-block");
        return false
    } else {
        $("#timezone-error").hide();
        return true
    }
}
