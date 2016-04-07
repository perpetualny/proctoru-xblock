function ProctorUXBlockCreate(runtime, element) {

    $(element).ready(function() {
    });

    $(element).find('.schedule-exam').click(function(){
        var create_account_url = runtime.handlerUrl(element, 'create_proctoru_account')

        post_data = {
            'phone':$(element).find("#phone").val(),
            'time_zone':$(element).find("#time-zone option:selected").val(),
            'tz_disp_name':$(element).find("#time-zone option:selected").text(),
            'address':$(element).find("#address").val(),
            'city':$(element).find("#city").val(),
            'country':$(element).find("#country option:selected").val(),
        }


        var validator = createAccountFormValidation(post_data)

        if (validator == true){
            $.post(create_account_url, JSON.stringify(post_data) , function(data,status) {
                if(data.status==="success"){
                    // render to schedule page
                    location.reload();
                }
            });
        } else {
            return false;
        }
    });
}


function ProctorUXBlockSchedule(runtime, element) {

    $(element).ready(function(){
        $(element).find("#datepicker" ).datepicker({
                onSelect: function(dateText) {
                    $.ajax({
                        type: "POST",
                        url: runtime.handlerUrl(element, 'get_available_schedule'),
                        data: JSON.stringify({"date": dateText}),
                        success: function(data,status){
                            if(data.status==='success'){
                                location.reload();
                            }
                        }
                    });
                },
                minDate: $(element).find('#start-date').val(),
                maxDate:  $(element).find('#end-date').val(),
                monthNames: [ "janvier", "fevrier", "mars", "avril", "mai", "juin",
		"juillet", "aout", "septembre", "octobre", "novembre", "decembre" ],
         	monthNamesShort: [ "janv.", "fevr.", "mars", "avr.", "mai", "juin",
		"juil.", "aout", "sept.", "oct.", "nov.", "dec." ],
	        dayNames: [ "dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi" ],
         	dayNamesShort: [ "dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam." ],
	        dayNamesMin: [ "D","L","M","M","J","V","S" ],
         	firstDay: 1
            }
        );

        date = $("#selected-date").val();
        if(date != "" || date != null){
            $(element).find('#datepicker').datepicker('setDate', date);
        }
    });

    $(document).on('click','.select-shedule-time', function() {
        var sheduleTime = $(this).attr("data-value");
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'call_addhoc'),
            data: JSON.stringify({"shedule_time": sheduleTime}),
            success: function(data,status){
                if(data.status==='success'){
                    location.reload();
                }
                else{
                    alert('examen d\xE9j\xE0 pr\xE9vu');
                }
            }
        });
    });

    $(document).find('#btn-keep-time').click(function(){
        var keep_time_url = runtime.handlerUrl(element, 'cancle_rescheduling');
        $.post(keep_time_url, JSON.stringify({}), function(data,status){
            location.reload();
        });
    });
}

var createAccountFormValidation = function(data){
    if (data.phone != "" & data.phone.length < 16){
        if(!isNaN(data.phone)){
            $("#phone-error-message").hide();
        } else {
            $("#phone-error-message").show();
            return false; 
        } 
    } else {
        $("#phone-error-message").show();
        return false; 
    }

    if(data.address == "" | data.address.length > 100){
        $("#address-error-message").show();
        return false;
    } else {
        $("#address-error-message").hide();
    }

    if(data.city == "" | data.city.length > 50){
        $("#city-error-message").show();
        return false;
    } else {
        $("#city-error-message").hide();
    }

    if (data.time_zone == "Fuseau horaire"){
        $("#timezone-error-message").show();
        return false;
    } else {
        $("#timezone-error-message").hide();
    }

    if(data.country == ""){
        $("#country-error-message").show();
        return false;
    } else {
        $("#country-error-message").hide();
        return true;
    }

}

function ProctorUXBlockArrived(runtime, element) {

    $(element).ready(function(){
        dt = $(element).find("#rem_time").val();
        var deadline = new Date(dt);
        initializeClock('clockdiv', deadline);
    });

    $(element).find(".check-equipmnt-btn").click(function(){
        window.open("http://www.proctoru.com/testitout/index_fr.php", "ProctorU Equipment Test Window", "toolbar=yes, scrollbars=yes, resizable=yes, width=1100, height=500px");
    });

    $(element).find(".start-exam-btn").click(function(){
        exam_url = $("#exam-url").val();
        window.open(exam_url, "ProctorU Equipment Test Window", "toolbar=yes, scrollbars=yes, resizable=yes, width=1100, height=500px");
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'start_exam'),
            data: JSON.stringify({"start_exam": true}),
            success: function(data,status){
                if(data.status==='success'){
                    location.reload();
                }
            }
        });
    });

    $(element).find(".reschedule-exam-btn").click(function(){
         $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'reschedule_exam'),
            data: JSON.stringify({"reschedule_exam": true}),
            success: function(data,status){
                if(data.status==='success'){
                    location.reload();
                }
            }
        });
    });

    $(element).find(".cancel-exam-btn").click(function(){
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'cancel_exam'),
            data: JSON.stringify({"cancel_exam": true}),
            success: function(data,status){
                if(data.status==='success'){
                    $.cookie("remaining_time",null)
                    if(data.status=='success'){
                        alert('examen annul\xE9 avec succ\xE8s');
                    }
                    location.reload();
                }else{
                    location.reload();
                }
            }
        });
    });
}

function ProctorUXBlockExamPassword(runtime, element) {
    $(element).find(".unlock-exam-btn").click(function(){
        exam_password = $(element).find('#exam-password').val();
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'unlock_exam'),
            data: JSON.stringify({"unlock_exam": true,"password":exam_password}),
            success: function(data,status){
                if(data.status==='success'){
                    location.reload();
                }else{
                    alert('Mot de passe incorrect');
                }
            }
        });
    });

    $(element).find(".cancel-exam-btn").click(function(){
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'cancel_exam'),
            data: JSON.stringify({"cancel_exam": true}),
            success: function(data,status){
                if(data.status==='success'){
                    $.cookie("remaining_time",null)
                    if(data.status=='success'){
                        alert('examen annul\xE9 avec succ\xE8s');
                    }
                    location.reload();
                }else{
                    location.reload();
                }
            }
        });
    });

    $(element).find("#reconnect-proctor").click(function(){
        var proctor_tab_url = $(element).find("#proctor-tab-url").val();
        window.open(proctor_tab_url, "_blank");
    });

}

var countdownTimer = null;

function ProctorUXBlockExamEnabled(runtime, element) {
    
    $(element).find(".end-exam-btn").click(function(){
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'end_exam'),
            data: JSON.stringify({"end_exam": true}),
            success: function(data,status){
                if(data.status==='success'){
                    location.reload();
                }else{
                    alert('Erreur de la base de donn\xE9es');
                }
            }
        });
    });

    $(element).ready(function(){
        if($.cookie("remaining_time")==null){
            $.cookie("remaining_time",parseInt($("#countdown").attr("data")))
            countdownTimer = setInterval('remainingExamTime()', 1000);
        }else if($.cookie("remaining_time")>0){
            countdownTimer = setInterval('remainingExamTime()', 1000);
        }else{
            $(document).find(".end-exam-btn").trigger("click");
            console.log("Completed");
        }
    });
}

function remainingExamTime() {
    var seconds = parseInt($.cookie("remaining_time"));
    var days        = Math.floor(seconds/24/60/60);
    var hoursLeft   = Math.floor((seconds) - (days*86400));
    var hours       = Math.floor(hoursLeft/3600);
    var minutesLeft = Math.floor((hoursLeft) - (hours*3600));
    var minutes     = Math.floor(minutesLeft/60);
    var remainingSeconds = seconds % 60;
    if (remainingSeconds < 10) {
        remainingSeconds = "0" + remainingSeconds; 
    }
    document.getElementById('countdown').innerHTML = hours + ":" + minutes + ":" + remainingSeconds;
    if (seconds == 0) {
        try{
            clearInterval(countdownTimer);
        }
        catch(e){
            console.log(e);
        }
        $(document).find(".end-exam-btn").trigger("click");
        document.getElementById('countdown').innerHTML = "Completed";
        $(document).find(".rm-label").hide()
        $.cookie("remaining_time",null)
    } else {
        seconds--;
        $.cookie("remaining_time",seconds);
    }
}


function getTimeRemaining(endtime) {
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
  var days = Math.floor(t / (1000 * 60 * 60 * 24));
  return {
    'total': t,
    'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(id, endtime) {
  var clock = document.getElementById(id);
  var daysSpan = clock.querySelector('.days');
  var hoursSpan = clock.querySelector('.hours');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);
    if(t.minutes <= 2 && t.hours <= 0 && t.days <=0){
        $(document).find('.exam-invisible').hide();
        $(document).find('.exam-visible').show();
    }
    daysSpan.innerHTML = t.days;
    hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    if (t.total <= 0) {
      clearInterval(timeinterval);
    }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}
