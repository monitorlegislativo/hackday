$().ready(function() {
    $(".tramitacao a").click(function(e) {
    	e.preventDefault();
    	var t = $(this).data("tramitacao");
    	$(".explica").hide('slow');
    	$("#T-"+t).show('slow');
        //Do stuff when clicked
    });
});