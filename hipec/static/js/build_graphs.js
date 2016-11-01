function buildGraphs(jsonStr) {
	// Remove the ugly JSON string from the clientside HTML
	$('#grapher').remove();
	
	// Convert the Python dictionary into a JSON object
	jsonStr = jsonStr.replace(/u*\&\#39;/g, '"');
	jsonStr = jsonStr.replace(/True/g, '"True"')
	jsonStr = jsonStr.replace(/False/g, '"False"')
	jsonStr = jsonStr.replace(/None/g, 'null');
	jsonStr = jsonStr.replace(/datetime\.date\((\d*?), (\d*?), (\d*?)\)/g,
		"[$1, $2, $3]");
	jasonBourne = $.parseJSON(jsonStr);
	
	google.charts.load('current', {'packages': ['corechart']});
	google.charts.setOnLoadCallback(buildHospitalHistogram);
	
	// Fake median and IQR
	var phony = [];
	
	for (var i = 0; i < 3; i++) {
		phony.push(Math.floor(Math.random() * 50) + 1);
	}
	
	phony.sort(function(a, b) { return a - b; });
	$('#median').text(phony[1] + (phony[1] == 1 ? ' day' : ' days'));
	$('#iqr').html(phony[0] + '&ndash;' + phony[2]);
	
	function buildHospitalHistogram() {
		// To build a histogram, Google Charts wants every value to be assigned
		// to a label, something completely and utterly unncessary for a
		// histogram.  As a result, a simple array of values must be converted
		// into an array of arrays.
		var googleDesignFlaw = [['Unused', 'Value']];
		$.each(jasonBourne.HospitalHistogram, function(index, value) {
			googleDesignFlaw.push(['', value]);
		});
		var histData = new google.visualization.arrayToDataTable(googleDesignFlaw);
		var options = {
			legend: {position: 'none'},
			width: screen.width,
			height: screen.height * 0.6,
			colors: ['#d9534f']
		};
		var histogram = new google.visualization.Histogram(
			document.getElementById('hospital-histogram')
		);
		histogram.draw(histData, options);
	}
}