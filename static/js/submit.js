$(document).ready(function($){
	$('.submit').click(function(){
		$('.loader').css('visibility','visible');
		console.log('clicked');
		$.post('/submit/' + this.id, function(){
			alert("success")
			$('.loader').css('visibility','hidden')
			$.post('/host')		
		});
	})

	$('#host').click(function(){
		$.post('/host')	
	})

	$('.awards').click(function(IDofObject){
		$.post('/awards/'+this.id)
	});


});
