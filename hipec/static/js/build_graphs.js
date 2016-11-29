var histData, kapMeiData1, kapMeiData2;

// Build the histogram and Kaplan-Meier curves; takes the Python object string
// as a parameter.
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
	
	window.addEventListener('resize', function() {
		resizeGraphs(0.8, 0.45);
	}, false);
	
	// Build the histogram for hospital stay length
	function buildHospitalHistogram() {
		var chartData = [['Value']];
		$.each(jasonBourne.HospitalHistogram, function(index, value) {
			chartData.push([value]);
		});
		histData = new google.visualization.arrayToDataTable(chartData);
		var options = {
			legend: { position: 'none' },
			width: $(window).width() * 0.8,
			height: $(window).width() * 0.45,
			colors: ['#d9534f']
		};
		var histogram = new google.visualization.Histogram(
			document.getElementById('hospital-histogram')
		);
		histogram.draw(histData, options);
	}
	
	// Build the Kaplan Meier curves for progression-free and overall survival
	function buildKaplanMeier() {
		kapMeiData1 = new google.visualization.DataTable();
		kapMeiData1.addColumn('number', 'Months');
		kapMeiData1.addColumn('number', 'Survival');
		kapMeiData1.addRows(jasonBourne.OverallSurvival.Coordinates);
		
		var options = {
			hAxis: { title: 'Months' },
			vAxis: { title: 'Survival' },
			legend: { position: 'none' },
			width: $(window).width() * 0.8,
			height: $(window).width() * 0.45,
			colors: ['#d9534f']
		};
		var chart = new google.visualization.LineChart(
			document.getElementById('overall-graph')
		);
		
		chart.draw(kapMeiData1, options);
		
		kapMeiData2 = new google.visualization.DataTable();
		kapMeiData2.addColumn('number', 'Months');
		kapMeiData2.addColumn('number', 'Survival');
		kapMeiData2.addRows(jasonBourne.ProgressionFree.Coordinates);
		
		chart = new google.visualization.LineChart(
			document.getElementById('progression-free-graph')
		);
		
		chart.draw(kapMeiData2, options);
	}
}

// Resizes the graphs--mod1 is a decimal modifier for the graph widths, mod2
// for the graph heights.
function resizeGraphs(mod1, mod2) {
	
	var histOptions = {
		legend: { position: 'none' },
		width: $(window).width() * mod1,
		height: $(window).width() * mod2,
		colors: ['#d9534f']
	};
	var lineOptions = {
		hAxis: { title: 'Months' },
		vAxis: { title: 'Survival' },
		legend: { position: 'none' },
		width: $(window).width() * mod1,
		height: $(window).width() * mod2,
		colors: ['#d9534f']
	};
	var histogram = new google.visualization.Histogram(
		document.getElementById('hospital-histogram')
	);
	var kapMei1 = new google.visualization.LineChart(
		document.getElementById('overall-graph')
	);
	var kapMei2 = new google.visualization.LineChart(
		document.getElementById('progression-free-graph')
	);
	
	// Redraw all graphs with the new size modifiers
	histogram.draw(histData, histOptions);
	kapMei1.draw(kapMeiData1, lineOptions);
	kapMei2.draw(kapMeiData2, lineOptions);
}