const { chromium } = require('playwright');
const fs = require('fs');

async function captureScreenshots() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('📸 Capturing screenshots...\n');
  
  // Screenshot 1: Landing Page
  console.log('1️⃣ Capturing landing page...');
  await page.goto('http://localhost:5022', { waitUntil: 'load', timeout: 10000 });
  await page.screenshot({ path: 'screenshots/01-landing-page.png', fullPage: true });
  console.log('✓ Saved: screenshots/01-landing-page.png');
  
  // Screenshot 2: Scalar UI
  console.log('2️⃣ Capturing Scalar UI...');
  await page.goto('http://localhost:5022/scalar', { waitUntil: 'load', timeout: 10000 });
  await page.waitForSelector('[class*="scalar"]', { timeout: 5000 });
  await page.screenshot({ path: 'screenshots/02-scalar-ui.png', fullPage: true });
  console.log('✓ Saved: screenshots/02-scalar-ui.png');
  
  // Screenshot 3: Models endpoint in Scalar
  console.log('3️⃣ Testing models endpoint via Scalar...');
  try {
    // Try to click on the /v1/models endpoint
    await page.click('text=/v1/models');
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'screenshots/03-models-endpoint.png', fullPage: true });
    console.log('✓ Saved: screenshots/03-models-endpoint.png');
  } catch (e) {
    console.log(`⚠️ Could not interact with models endpoint: ${e.message}`);
  }
  
  console.log('\n✅ Screenshot capture complete!');
  await browser.close();
}

captureScreenshots().catch(console.error);
