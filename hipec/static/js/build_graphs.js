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
	google.charts.setOnLoadCallback(buildKaplanMeier);
	
	// Fake median and IQR
	var phony = [];
	
	for (var i = 0; i < 3; i++) {
		phony.push(Math.floor(Math.random() * 50) + 1);
	}
	
	phony.sort(function(a, b) { return a - b; });
	$('#hospital-median').text(phony[1] + (phony[1] == 1 ? ' day' : ' days'));
	$('#hospital-iqr').html(phony[0] + '&ndash;' + phony[2]);
	
	$.each($('.percent span'), function(index, perc) {
		$(perc).text(Math.round((Math.random() * 100) * 100) / 100);
	});
	
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
	
	function buildKaplanMeier() {
		var ids = ['progression-free-graph', 'overall-graph'];
		
		$.each(ids, function(index, graphID) {
			var data = new google.visualization.DataTable();
			var x = [];
			var y = [];
			var xy = [];
			
			for (var i = 0; i < 98; i++) {
				x.push(Math.random() * 50);
				y.push(Math.random());
			}
			
			x.push(0);
			x.push(50);
			y.push(0);
			y.push(1);
			x.sort(function(a, b) { return a - b; });
			y.sort(function(a, b) { return a - b; });
			y.reverse();
			
			for (var i = 0; i < 100; i++) {
				xy.push([x[i], y[i]]);
			}
			
			data.addColumn('number', 'Months');
			data.addColumn('number', 'Survival');
			data.addRows(xy);
			
			var options = {
				hAxis: { title: 'Months' },
				vAxis: { title: 'Survival' },
				legend: { position: 'none' },
				width: screen.width,
				height: screen.height * 0.6,
				colors: ['#d9534f']
			};
			var chart = new google.visualization.LineChart(
				document.getElementById(graphID));
			
			chart.draw(data, options);
		});
	}
}