const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    console.log('🌐 Testing Open WebUI model discovery...\n');
    
    // Intercept all API calls
    page.on('response', response => {
      if (response.url().includes('/api/') || response.url().includes('/v1/')) {
        console.log(`📡 [${response.status()}] ${response.url()}`);
      }
    });

    console.log('Opening http://localhost:8080/');
    await page.goto('http://localhost:8080/', { waitUntil: 'networkidle', timeout: 30000 });
    
    console.log('\n⏳ Waiting for page to fully load...');
    await page.waitForTimeout(3000);
    
    console.log('\n🔍 Checking console for errors...');
    page.on('console', msg => {
      if (msg.type() === 'error' || msg.type() === 'warning') {
        console.log(`  [${msg.type().toUpperCase()}] ${msg.text()}`);
      }
    });

    console.log('\n🔍 Checking for model list in page...');
    
    // Look for model elements
    const buttons = await page.locator('button, div[role="button"]').all();
    console.log(`\nFound ${buttons.length} buttons/clickable divs on page`);
    
    for (const btn of buttons.slice(0, 15)) {
      const text = await btn.textContent();
      const classes = await btn.getAttribute('class');
      if (text && (text.includes('model') || text.includes('Model') || text.includes('codebrewRouter') || text.length < 50)) {
        console.log(`  - "${text.trim()}" (classes: ${classes?.substring(0, 80) || 'none'})`);
      }
    }

    // Check page HTML for API references
    const html = await page.content();
    const apiMatch = html.match(/openai|v1|api|model/gi);
    console.log(`\n✅ Found ${apiMatch?.length || 0} API/model references in HTML`);
    
    console.log('\n📸 Taking screenshot for visual inspection...');
    await page.screenshot({ path: 'webui-test-models.png', fullPage: true });
    console.log('✅ Screenshot saved');

  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
})();
