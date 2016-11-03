(function($) {
	$('input[type=checkbox].optional').on('change', function() {
		if ($(this).is(':checked')) {
			var name = $(this).attr('name');
			$('input[name=' + name + ']').not(this).each(function(index, value) {
				value.checked = false;
			});
		}
	});
})(jQuery);