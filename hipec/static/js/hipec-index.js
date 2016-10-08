(function($) {
	$.each($('input[type=range]'), function(index, input) {
		// noUiSlider.js prep work
		var name = $(this).attr('name');
		var min = $(this).attr('min');
		var max = $(this).attr('max');
		min = parseInt(min, 10);
		max = parseInt(max, 10);
		var mid = Math.round((min + max) / 2);
		
		// Creates better sliders via noUiSlider.js plugin
		var slider = document.getElementById('nouisl-' + name);
		slider.style.width = '85%';
		noUiSlider.create(slider, {
			start: [mid],
			step: 1,
			range: {
				'min': min,
				'max': max
			},
			pips: {
				mode: 'count',
				values: 10,
				density: 3
			}
		});
	});
	
	// Opens and closes variable categories
	$('.category-title').on('click', function() {
		$(this).toggleClass('collapsed');
	});
	
	// Updates the input slider values; I don't think Django can access
	// the noUiSlider values directly as it is not a form input.
	$.each($('.slider'), function(index, slider) {
		slider.noUiSlider.on('update', function() {
			name = $(slider).attr('slide');
			value = Math.round(slider.noUiSlider.get());
			$('input[slide="' + name + '"]').val(value);
			$('#range-' + name).text(value);
		});
	});
})(jQuery);