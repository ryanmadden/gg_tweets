$(document).ready(function($){
	$('#submit').click(function(){
		console.log('clicked');
		$.post('/submit');
	})



});
