function validate() {
	var check = true;

	var a1= $("#input_1").val();
	if (a1 == "") {
		check = false;
		$('#input_1').focus();
		alert("Please fill in all the fields.");
		return check
	}

	var b1 = $('#input_2').val();
	var b2 = isNaN(b1);
	if (b2 == true || b1 == ""){
		check = false;
		$('#input_2').focus();
		alert("Please enter a number.");
		return check
	}

	var c1 = $("input:radio[name='season']:checked").val();
	if(c1 == null){
		check = false;
		$('#input_3_1').focus();
		alert("Please fill in all the fields.");
		return check
	}

	var d1 = $("input:checkbox[name='food']:checked").val();
	
	if(d1 ==null){
		check = false;
		$('#input_4_1').focus();
		alert("Please fill in all the fields.");
		return check
	}

	var e1 = $("#input_5").val();
	if (e1 == "") {
		check = false;
		$('#input_5').focus();
		alert("Please fill in all the fields.");
		return check
	}

	return check
}

function insert(a1, b1, c1, e1){
	$('#madlib-input-overall').hide();
	$('#madlib-output').show();

	$("#output_1").text(a1);
	$("#output_2").text(b1);
	
	var c1 = $("input:radio[name='season']:checked").val();
	$("#output_3").text(c1);

	var d1="";
	$("input[name='food']:checked").each(function(){
		each_item=" "+$(this).val();
		d1+=each_item;
	});
	$("#output_4").text(d1);

	$('#output_5').text(e1);
}

$(document).ready(function() {
	$('#madlib-output').hide();
	$('#input_1').focus();
	$("#submitButton").click(function(){
		check_result = validate();				
		if(check_result == true){

			val_a1 = $('#input_1').val();
			val_b1 = $('#input_2').val();
			val_c1 = $('#input_3').val();
			val_e1 = $('#input_5').val();

			insert(val_a1, val_b1, val_c1, val_e1);
		};
	});
});
