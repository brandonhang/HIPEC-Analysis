(function($) {
	$.each($('input[type=range]'), function(index, input) {			// Displays initial values of input sliders
		var value = $(input).val();
		var name = $(input).attr('name');
		$('#range-' + name).text(value);
	});
	
	$('.category-title').on('click', function() {			// Opens and closes variable categories
		$(this).toggleClass('collapsed');
	});
	
	$('input[type=range]').on('change', function() {		// Updates the input slider values
		var value = $(this).val();
		var name = $(this).attr('name');
		$('#range-' + name).text(value);
	});
})(jQuery);