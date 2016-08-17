function ProctoruStaffBlock(runtime, element) {

    $(".get-result").click(function(){
        $(element).find("#block-loader").show();
        $(element).find(".result-box").hide();
        $(element).find(".result-box-no-data").hide();
        post_data = {
            student_id : $(this).attr("data-pk")
        }
        var activity_url = runtime.handlerUrl(element, 'get_student_activity')
        $.post(activity_url,JSON.stringify(post_data),function(data,status){
            if(data != null){
                $(element).find(".student-name").text(data.Student);
                $(element).find(".start-date").text(data.StartDate);
                $(element).find(".completd-date").text(data.EndDate);
                $(element).find(".session-notes").text(data.ProctorNotes);

                if(data.TestSubmitted == false) {
                    $(element).find("#exam-submit-marked").hide();
                }
                else {
                    $(element).find("#exam-submit-marked").show();
                }

                if(data.Authenticated == false) {
                    $(element).find("#auth-marked").hide();
                }
                else {
                    $(element).find("#auth-marked").show();
                }

                if(data.CheckID == false) {
                    $(element).find("#chk-identity-marked").hide();
                }
                else {
                    $(element).find("#chk-identity-marked").show();
                }

                $(element).find(".result-box").show();
            } else {
                $(element).find(".result-box").hide();
                $(element).find(".result-box-no-data").text('No data available');
                $(element).find(".result-box-no-data").show();
            }
            $(element).find("#block-loader").hide();
        });
    });
}
