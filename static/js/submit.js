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
		$('#best-dressed-images').css('display', 'none')	
	})

	$('.awards').click(function(IDofObject){
		$.post('/awards/'+this.id)
		$('#best-dressed-images').css('display', 'none')
	});

	$('#best-dressed-submit').click(function(){
		$('.loader').css('visibility','visible');
		$.post('/best-dressed.json', function(){
			$('.loader').css('visibility','hidden')	
			$('#best-dressed-images').css('display', 'initial')
		});
	});


});


$(function() {

    var $sidebar   = $("#sidebar"), 
        $window    = $(window),
        offset     = $sidebar.offset(),
        topPadding = 0;

    $window.scroll(function() {
        if ($window.scrollTop() > offset.top) {
            $sidebar.stop().animate({
                marginTop: $window.scrollTop() - offset.top + topPadding
            });
        } else {
            $sidebar.stop().animate({
                marginTop: 0
            });
        }
    });
    
});