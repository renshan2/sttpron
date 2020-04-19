var html;
	$('.input').keypress(function(e) {
        if(e.which == 13) {
            jQuery(this).blur();
            jQuery('#submit').focus().click();
    	}
    });
	function send_text() {
	var nowObj = new Date();
		var nowString = nowObj.toLocaleTimeString('en-US');
		var text= $('#input_text').val();
	  	$.ajax({
				  url: "/sendtext",
				  type: "POST",
				  data: {text:text}
			  }).done(function(response) {
				var htmlquestion= "";
				var htmlresponse= "";
				response =response.result;
					 $.each(response,function(key,val){
						console.log(key);
					 	console.log(val);
					 	if (key == '1')
							htmlquestion += val;
					 	else htmlresponse += val;
					});
					htmlquestion ="<div class='selfmsg' align='right'>"+htmlquestion+"</div>";
					htmlresponse ="<div class='sysmsg' align='left' font='color=red'>"+htmlresponse+"</div>";
					html = "<div align='center'>" + nowString +"</div>" + htmlquestion+htmlresponse;
					console.log(html)
					$(".content1").append(html);
				});
	};

	function send_cmd(cmd) {
	var nowObj = new Date();
		var nowString = nowObj.toLocaleTimeString('en-US');
		var text= cmd;
		var htmlcmd = "";
	  	$.ajax({
				  url: "/sendcmd",
				  type: "POST",
				  data: {text:text}
			  }).done(function(response) {
				var htmlquestion= "";
				var htmlresponse= "";
				response =response.result;
					 $.each(response,function(key,val){						
					 	console.log(val);
						htmlcmd += val;
					});
					console.log(htmlcmd)
					$(".content2").append(htmlcmd);
				});
	};

	function send_audio() {
		var nowObj = new Date();
		var nowString = nowObj.toLocaleTimeString('en-US');
	  	$.ajax({
				  url: "/sendaudio",
				  type: "GET"
			  }).done(function(response) {
				var htmlquestion= "";
				var htmlresponse= "";
				response =response.result;
					 $.each(response,function(key,val){
						console.log(key);
					 	console.log(val);
					 	if (key == '1')
							htmlquestion += val;
					 	else htmlresponse += val;
					});
					htmlquestion ="<div class='selfmsg' align='right'>"+htmlquestion+"</div>";
					htmlresponse ="<div class='sysmsg' align='left' font='blue'>"+htmlresponse+"</div>";
					html = "<div align='center'>" + nowString +"</div>" + htmlquestion+htmlresponse;
					console.log(html)
					$(".content1").append(html);
				});
	};
