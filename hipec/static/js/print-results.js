// Readies the document for printing by temporarily altering the CSS
function printResults() {
	// Stash and remove the CSS for viewing
	var mainCss = document.getElementById('main-css');
	$('#main-css').remove();
	
	// A new CSS for printing
	var printCss =
		'<style id="print-css">'
			+ "body {"
				+ "font-family: 'Garamond', serif;"
			+ "}"
			
			+ ".registry {"
				+ "width: 100%;"
			+ "}"
			
			+ ".registry td:last-of-type {"
				+ "text-align: right;"
			+ "}"
			
			+ "h2.category-title {"
				+ "font-family: 'Verdana', sans-serif"
			+ "}"
			
			+ "ul.percent h4 {"
				+ "font-weight: normal;"
				+ "display: list-item;"
				+ "list-style-type: disc;"
			+ "}"
			
			+ ".graph {"
				+ "position: relative;"
				+ "z-index: -9000;"
			+ "}"
			
			+ ".form-category {"
				+ "border-bottom: 2px solid black;"
			+ "}"
		+ "</style>";
	
	// Add a patient header, add the printing CSS, hide the buttons, and resize the graphs
	$('.registry').before('<h2 id="temp-title" class="category-title">Patient Information</h2>');
	$('head').append(printCss);
	$('.results-nav').hide();
	resizeGraphs(0.6, 0.3);
	
	// Bring up the print page window
	window.print();
	
	// Restore the CSS and elements for viewing on a device
	$('#temp-title').remove();
	$('#print-css').remove();
	$('head').append(mainCss);
	$('.results-nav').show();
	// Resize graphs to original specs
	resizeGraphs(0.8, 0.45);
}