package hipec_tests;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.*;
//import org.openqa.selenium.firefox.FirefoxDriver;		// Not yet needed
import org.openqa.selenium.htmlunit.HtmlUnitDriver;

public class SkeletonTest {
	
	static WebDriver driver = new HtmlUnitDriver();
	
	@Before
	public void setup() throws Exception {
		
		// Selenium doesn't like relative paths so this will have to be changed on a per PC basis :(
		driver.get("file:///B:/My Documents/GitHub/HIPEC-Analysis/index.html");
	}
	
	// Simple test of the app's title
	@Test
	public void testTitle() {
		
		String title = driver.getTitle();
		assertTrue(title.contains("CRS-HIPEC Risk & Survival Prediction Tool"));
	}
}
