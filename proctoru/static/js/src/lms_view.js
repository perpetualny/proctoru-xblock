function ProctoruStaffBlock(runtime, element) {

    $(".get-result").click(function(){
        $(element).find("#block-loader").show();
        $(element).find(".result-box").hide();
        post_data = {
            student_id : $(this).attr("data-pk")
        }
        var activity_url = runtime.handlerUrl(element, 'get_student_activity')
        $.post(activity_url,JSON.stringify(post_data),function(data,status){
            $(element).find(".student-name").text(data.Student);
            $(element).find(".start-date").text(data.StartDate);
            $(element).find(".completd-date").text(data.EndDate);
            $(element).find(".session-notes").text(data.ProctorNotes);
            $(element).find(".result-box").show();
            $(element).find("#block-loader").hide();
        });
    });
}
