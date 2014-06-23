$().ready(function() {
	$("#buscar").submit(function (e) {
		var termo = $("#termo").val();
		e.preventDefault();
		window.location.href = "/busca/"+termo;
	});

	$(".explicacao").sticky({topSpacing:0});
    $(".tramitacao a").click(function(e) {
    	e.preventDefault();

    	var t = $(this).data("tramitacao");
    	$(".explica").hide('slow').removeClass("explica-ativa");
    	$("#T-"+t).show('slow').addClass("explica-ativa");
        //Do stuff when clicked
    });
});