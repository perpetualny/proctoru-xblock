function ProctoruStaffBlock(runtime, element) {

    $(".get-result").click(function(){
        $(element).find(".student-name").text($(this).attr('student-name'));
        $(element).find(".start-date").text($(this).attr('start-date'));
        $(element).find(".completd-date").text($(this).attr('end-date'));
        $(element).find(".result-box").show();
    });
}
