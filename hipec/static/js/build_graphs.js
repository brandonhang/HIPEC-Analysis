function buildGraphs(jsonStr) {
	// Remove the ugly JSON string from the clientside HTML
	$('#grapher').remove();
	
	// Convert the Python dictionary into a JSON object
	jsonStr = jsonStr.replace(/u*\&\#39;/g, '"');
	jsonStr = jsonStr.replace(/True/g, '"True"')
	jsonStr = jsonStr.replace(/False/g, '"False"')
	jsonStr = jsonStr.replace(/None/g, 'null');
	jsonStr = jsonStr.replace(/null:/, '"null":')
	jsonStr = jsonStr.replace(/datetime\.date\((\d*?), (\d*?), (\d*?)\)/g,
		"[$1, $2, $3]");
	var jasonBourne = $.parseJSON(jsonStr);
	
	google.charts.load('current', {'packages': ['corechart']});
	google.charts.setOnLoadCallback(buildHospitalHistogram);
	google.charts.setOnLoadCallback(buildKaplanMeier);
	
	function buildHospitalHistogram() {
		// To build a histogram, Google Charts wants every value to be assigned
		// to a label, something completely and utterly unncessary for a
		// histogram.  As a result, a simple array of values must be converted
		// into an array of arrays.
		var googleDesignFlaw = [['Value']];
		$.each(jasonBourne.HospitalHistogram, function(index, value) {
			googleDesignFlaw.push([value]);
		});
		var histData = new google.visualization.arrayToDataTable(googleDesignFlaw);
		var options = {
			legend: { position: 'none' },
			width: screen.width,
			height: screen.height * 0.6,
			colors: ['#d9534f']
		};
		var histogram = new google.visualization.Histogram(
			document.getElementById('hospital-histogram')
		);
		histogram.draw(histData, options);
	}
	
	// Build the Kaplan Meier curves for progression-free and overall survival
	function buildKaplanMeier() {
		var data = new google.visualization.DataTable();
		
		data.addColumn('number', 'Months');
		data.addColumn('number', 'Survival');
		data.addRows(jasonBourne.OverallSurvival.Coordinates);
		
		var options = {
			hAxis: { title: 'Months' },
			vAxis: { title: 'Survival' },
			legend: { position: 'none' },
			width: screen.width,
			height: screen.height * 0.6,
			colors: ['#d9534f']
		};
		var chart = new google.visualization.LineChart(
			document.getElementById('overall-graph'));
		
		chart.draw(data, options);
		
		data = new google.visualization.DataTable();
		
		data.addColumn('number', 'Months');
		data.addColumn('number', 'Survival');
		data.addRows(jasonBourne.ProgressionFree.Coordinates);
		
		options = {
			hAxis: { title: 'Months' },
			vAxis: { title: 'Survival' },
			legend: { position: 'none' },
			width: screen.width,
			height: screen.height * 0.6,
			colors: ['#d9534f']
		};
		chart = new google.visualization.LineChart(
			document.getElementById('progression-free-graph'));
		
		chart.draw(data, options);
	}
}