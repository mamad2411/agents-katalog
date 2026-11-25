const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    console.log('🌐 Testing CodebrewRouter via Open WebUI chat interface\n');
    
    // Intercept network requests to see chat completion calls
    await page.route('**/v1/chat/completions', async route => {
      console.log('📡 Intercepted chat/completions request');
      console.log('  URL:', route.request().url());
      console.log('  Method:', route.request().method());
      const body = route.request().postDataJSON();
      console.log('  Model:', body?.model);
      console.log('  Messages:', body?.messages?.length);
      await route.continue();
    });

    console.log('1️⃣ Opening http://localhost:8080/');
    await page.goto('http://localhost:8080/', { waitUntil: 'networkidle', timeout: 30000 });
    
    console.log('2️⃣ Waiting for page to fully load...');
    await page.waitForTimeout(2000);
    
    console.log('3️⃣ Checking if codebrewRouter model is in dropdown...');
    const modelSelector = await page.$('[data-testid="model-selector"], select, .model-select');
    if (modelSelector) {
      console.log('  ✅ Found model selector');
    } else {
      console.log('  ⚠️ Could not find explicit model selector - looking for buttons...');
    }

    console.log('\n4️⃣ Looking for model buttons...');
    const modelButtons = await page.locator('button:has-text("codebrewRouter"), button:has-text("local-model"), button:has-text("gemma")').all();
    console.log(`  Found ${modelButtons.length} model-related buttons`);

    if (modelButtons.length > 0) {
      console.log('  ✅ Found model button, checking which models are available...');
      for (const btn of modelButtons) {
        const text = await btn.textContent();
        console.log(`    - ${text}`);
      }
    }

    console.log('\n5️⃣ Trying to find and click the first model option...');
    const firstModelOption = await page.locator('[role="option"]').first();
    const optionText = await firstModelOption.textContent().catch(() => null);
    if (optionText) {
      console.log(`  Found option: ${optionText}`);
      await firstModelOption.click().catch(() => console.log('  Could not click option'));
    }

    console.log('\n6️⃣ Looking for chat input field...');
    const chatInputs = [
      await page.$('textarea'),
      await page.$('[contenteditable="true"]'),
      await page.$('input[type="text"]')
    ];
    
    let inputField = chatInputs.find(x => x);
    if (inputField) {
      console.log('  ✅ Found chat input');
      
      console.log('\n7️⃣ Sending test message...');
      await inputField.fill('Hello from Playwright test');
      console.log('  ✅ Entered: "Hello from Playwright test"');
      
      console.log('\n8️⃣ Looking for send button...');
      const sendButtons = await page.locator('button[type="submit"], button:has-text("Send"), [data-testid="send-button"]').all();
      console.log(`  Found ${sendButtons.length} potential send buttons`);
      
      if (sendButtons.length > 0) {
        console.log('  Clicking send button...');
        await sendButtons[0].click();
        console.log('  ✅ Clicked send');
        
        console.log('\n⏳ Waiting for response (10 seconds)...');
        await page.waitForTimeout(10000);
        
        console.log('✅ Test complete');
      } else {
        console.log('  ❌ Could not find send button');
      }
    } else {
      console.log('  ❌ Could not find chat input');
    }
    
    console.log('\n📸 Taking final screenshot...');
    await page.screenshot({ path: 'webui-chat-test.png', fullPage: true });
    console.log('✅ Screenshot saved to webui-chat-test.png');
    
    await page.waitForTimeout(5000); // Keep browser open briefly

  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: 'webui-chat-error.png' }).catch(() => {});
  } finally {
    await browser.close();
  }
})();
