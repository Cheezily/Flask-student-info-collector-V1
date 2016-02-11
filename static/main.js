$(document).ready( function() {
	$("#warning").hide();
	$(".container").slideDown(600, function() {$(".logos").fadeIn(900);});
	
});

$("#infoform").submit( function(event) {
	if (!checkForm()) {
		event.preventDefault();
	}
});

$("#name").focus( function() {
	$("#name_error").html("");
});

$("#school").focus( function() {
	$("#school_error").html("");
});

$("#instructor").focus( function() {
	$("#instructor_error").html("");
});

function checkForm() {
	
	var name = $("#name").val(),
		school = $("#school").val(),
		instructor = $("#instructor").val(),
		email = $("#email").val(),
		checkFail = false;
	
	if (name.length < 3) {
		$("#name_error").html("Required");
		checkFail = true;
	}
	if (!school) {
		$("#school_error").html("Required");
		checkFail = true;
	}
	if (instructor.length < 3) {
		$("#instructor_error").html("Required");
		checkFail = true;
	}
		if (email.length < 3) {
		$("#email_error").html("Required");
		checkFail = true;
	}
	if (checkFail == true) {
		return false;
	} else {
		return true;
	}
};