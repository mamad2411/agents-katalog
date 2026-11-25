const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    console.log('🌐 Navigating to http://localhost:8080/');
    await page.goto('http://localhost:8080/', { waitUntil: 'networkidle' });
    
    // Wait a bit for dynamic content
    await page.waitForTimeout(3000);
    
    console.log('\n📸 Taking screenshot...');
    await page.screenshot({ path: 'webui-diagnostic.png', fullPage: true });
    console.log('✅ Screenshot saved to webui-diagnostic.png');
    
    console.log('\n🔍 Page HTML structure (first 5000 chars):');
    const html = await page.content();
    console.log(html.substring(0, 5000));
    
    console.log('\n\n🔍 Searching for model/router mentions:');
    const lines = html.split('\n');
    let found = false;
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].toLowerCase();
      if (line.includes('model') || line.includes('router') || line.includes('codebrewrouter')) {
        console.log(`Line ${i}: ${lines[i].substring(0, 200)}`);
        found = true;
      }
    }
    if (!found) console.log('❌ No model/router mentions found');
    
    console.log('\n✅ Diagnostic complete - browser will stay open for 10 seconds');
    await page.waitForTimeout(10000);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: 'webui-error-diagnostic.png' });
  } finally {
    await browser.close();
  }
})();
