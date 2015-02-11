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


// $(function() {

//     var $sidebar   = $("#sidebar"), 
//         $window    = $(window),
//         offset     = $sidebar.offset(),
//         topPadding = 15;

//     $window.scroll(function() {
//         if ($window.scrollTop() > offset.top) {
//             $sidebar.stop().animate({
//                 marginTop: $window.scrollTop() - offset.top + topPadding
//             });
//         } else {
//             $sidebar.stop().animate({
//                 marginTop: 0
//             });
//         }
//     });
    
// });