const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    console.log('🌐 Opening Open WebUI at http://localhost:8080/');
    await page.goto('http://localhost:8080/', { waitUntil: 'networkidle' });
    
    console.log('⏳ Waiting for model selector...');
    await page.waitForSelector('[data-testid="model-selector"], select, .model-select, [aria-label*="model"]', { timeout: 10000 }).catch(() => null);
    
    // Try to find model selector by looking at the page
    console.log('📋 Available model options:');
    
    // Method 1: Look for select elements
    const selects = await page.$$('select');
    for (const select of selects) {
      const options = await select.$$('option');
      console.log(`  Found select with ${options.length} options:`);
      for (const option of options) {
        const text = await option.textContent();
        const value = await option.getAttribute('value');
        console.log(`    - ${text} (${value})`);
      }
    }
    
    // Method 2: Look for divs with role="option"
    const optionDivs = await page.$$('[role="option"]');
    if (optionDivs.length > 0) {
      console.log(`  Found ${optionDivs.length} option divs:`);
      for (const div of optionDivs.slice(0, 10)) {
        const text = await div.textContent();
        console.log(`    - ${text}`);
      }
    }
    
    // Method 3: Look for any element containing "codebrewRouter" or "model"
    const allText = await page.content();
    if (allText.includes('codebrewRouter')) {
      console.log('✅ Found "codebrewRouter" in page');
    } else {
      console.log('❌ "codebrewRouter" NOT found in page');
    }
    
    if (allText.includes('local-model')) {
      console.log('✅ Found "local-model" in page');
    } else {
      console.log('❌ "local-model" NOT found in page');
    }
    
    // Try to send a chat message with codebrewRouter
    console.log('\n📨 Attempting to send chat message...');
    
    // Look for chat input
    const inputSelectors = ['input[type="text"]', 'textarea', '[contenteditable="true"]', '[data-testid="chat-input"]'];
    let input = null;
    for (const selector of inputSelectors) {
      input = await page.$(selector);
      if (input) {
        console.log(`Found input with selector: ${selector}`);
        break;
      }
    }
    
    if (!input) {
      console.log('⚠️ Could not find chat input');
      console.log('\n📸 Page screenshot saved to webui-test.png');
      await page.screenshot({ path: 'webui-test.png' });
    } else {
      await input.fill('Tell me a dad joke');
      console.log('✅ Entered message: "Tell me a dad joke"');
      
      // Look for send button
      const sendButton = await page.$('button:has-text("Send"), [data-testid="send-button"], button[aria-label*="send"]');
      if (sendButton) {
        await sendButton.click();
        console.log('✅ Clicked send button');
        
        // Wait for response
        console.log('⏳ Waiting for response...');
        await page.waitForTimeout(5000);
        
        console.log('📸 Saving screenshot...');
        await page.screenshot({ path: 'webui-response.png' });
      } else {
        console.log('⚠️ Could not find send button');
      }
    }
    
    console.log('\n✅ Test complete');
  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: 'webui-error.png' });
  } finally {
    await browser.close();
  }
})();
