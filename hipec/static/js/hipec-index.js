(function($) {
	$.each($('input[slide=true]'), function(index, input) {
		// noUiSlider.js prep work
		var name = $(this).attr('name');
		var min = $(this).attr('min');
		var max = $(this).attr('max');
		var pips = $(this).attr('pips');
		min = parseInt(min, 10);
		max = parseInt(max, 10);
		pips = parseInt(pips, 10);
		var mid = Math.round((min + max) / 2);
		density = Math.floor(10 - ((max - min) / pips));
		
		// Creates better sliders via noUiSlider.js plugin
		var slider = document.getElementById('slide_' + name);
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
				values: pips,
				density: density,
				stepped: true
			}
		});
	});
	
	// Opens and closes variable categories
	$('.category-title').on('click', function() {
		$(this).toggleClass('collapsed');
	});
	
	// Updates the form input values; I don't think Django can access
	// the noUiSlider values directly as it is not an HTML form input.
	$.each($('.slider'), function(index, slider) {
		slider.noUiSlider.on('update', function() {
			name = $(slider).attr('slide');
			value = Math.round(slider.noUiSlider.get());
			$('input[name="' + name + '"]').val(value);
			$('#range-' + name).text(value);
		});
	});
	
	// Updates the sliders when a value is entered directly into the input box
	$('input[slide="true"]').on('change', function() {
		var value = $(this).val();
		var name = $(this).attr('name');
		var slider = document.getElementById('slide_' + name);
		slider.noUiSlider.set(value);
	});
	/*
	$('#prediction-form').on('submit', function(event) {
		if ()
			event.preventDefault();
		}
	})*/
})(jQuery);