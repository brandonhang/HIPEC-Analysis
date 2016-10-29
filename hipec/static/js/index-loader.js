(function($) {
	var notificationTimeout;
	
	// Checks that the core variable radio buttons are checked before submission
	$('#prediction-form').on('submit', function(event) {
		// If the required radio buttons are unchecked, prevent form submission
		if ($('input[name=core_primary_tumor]:checked').length == 0
				|| $('input[name=core_cytoreduction]:checked').length == 0) {
			event.preventDefault();
			
			// Build the notification if it doesn't exist
			if ($('.notification').length == 0) {
				$('body').append(
					'<div class="notification">'
					+ '<p>All <em>Core Variables</em> must be filled out!</p>'
					+ '</div>'
				);
			}
			
			// Informs the user that core variables are required
			$('.notification').stop().fadeIn('fast');
			clearTimeout(notificationTimeout);
			notificationTimeout = setTimeout(function() {
				hideNotification();
			}, 3000);
		}
		// Otherwise, show the loading spinner
		else {
			$('#loading').show();
		}
	});
	
	// Hide the required variables notification
	function hideNotification() {
		$('.notification').fadeOut('slow');
	}
})(jQuery);