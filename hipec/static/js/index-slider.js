var coreSliders = [
	{
		'name': 'core_age',
		'type': 'continuous',
		'min': 18,
		'max': 99,
		'pips': 10,
		'steps': 1,
		'density': 4
	},
	{
		'name': 'core_charlson',
		'type': 'continuous',
		'min': 6,
		'max': 18,
		'pips': 13,
		'steps': 1,
		'density': 10
	},
	{
		'name': 'core_karnofsky',
		'type': 'categorical',
		'min': 10,
		'max': 100,
		'pips': 10,
		'steps': 10,
		'density': 10
	},
	{
		'name': 'core_peritoneal',
		'type': 'continuous',
		'min': 0,
		'max': 39,
		'pips': 14,
		'steps': 1,
		'density': 3
	},
	{
		'name': 'core_num_hipecs',
		'type': 'continuous',
		'min': 0,
		'max': 5,
		'pips': 6,
		'steps': 1,
		'density': 20
	},
	{
		'name': 'dem_bmi',
		'type': 'continuous',
		'min': 10,
		'max': 70,
		'pips': 11,
		'steps': 1,
		'density': 3
	},
	{
		'name': 'dem_smoke_pack',
		'type': 'continuous',
		'min': 0,
		'max': 60,
		'pips': 11,
		'steps': 1,
		'density': 3
	}
];

(function($) {
	$.each(coreSliders, function(index, slideInfo) {
		// noUiSlider.js prep work
		var lower, mid, upper, range;
		
		if (slideInfo.type == 'continuous') {
			lower = Math.round((slideInfo.min + slideInfo.max) * (1 / 3));
			upper = Math.round((slideInfo.min + slideInfo.max) * (2 / 3));
			range = true;
		}
		else {
			mid = Math.round((slideInfo.min + slideInfo.max) / 2);
			range = false;
		}
		
		// Creates better sliders via noUiSlider.js plugin
		var slider = document.getElementById('slide_' + slideInfo.name);
		slider.style.width = '85%';
		noUiSlider.create(slider, {
			start: range ? [lower, upper] : [mid],
			connect: range,
			step: slideInfo.steps,
			range: {
				'min': slideInfo.min,
				'max': slideInfo.max
			},
			pips: {
				mode: 'count',
				values: slideInfo.pips,
				density: slideInfo.density,
				stepped: true
			}
		});
	});
	
	// Updates the form input values; I don't think Django can access
	// the noUiSlider values directly as it is not an HTML form input.
	$.each($('.slider'), function(index, slider) {
		slider.noUiSlider.on('update', function() {
			name = $(slider).attr('slide');
			value = slider.noUiSlider.get();
			if (isNaN(value)) {
				$('input[name="' + name + '__lower"]').val(Math.round(value[0]));
				$('input[name="' + name + '__upper"]').val(Math.round(value[1]));
			}
			else {
				$('input[name="' + name + '"]').val(Math.round(value));
			}
		});
	});
	
	// Updates the sliders when a value is entered directly into the input box
	$('input[slide="true"]').on('change', function() {
		var name, value;
		if ($(this).attr('spread') == 'true') {
			name = $(this).attr('name').split('__');
			name = name[0];
			var valMin = $('input[name="' + name + '__lower"]').val();
			var valMax = $('input[name="' + name + '__upper"]').val();
			value = [valMin, valMax];
		}
		else {
			value = $(this).val();
			name = $(this).attr('name');
		}
		
		var slider = document.getElementById('slide_' + name);
		slider.noUiSlider.set(value);
	});
})(jQuery);