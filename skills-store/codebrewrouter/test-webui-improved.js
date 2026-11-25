const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    console.log('🌐 Opening Open WebUI at http://localhost:8080/');
    await page.goto('http://localhost:8080/', { waitUntil: 'domcontentloaded', timeout: 30000 });
    
    await page.waitForTimeout(2000);
    
    console.log('📸 Taking initial screenshot...');
    await page.screenshot({ path: 'webui-initial.png', fullPage: true });
    
    // Get all text content
    const bodyText = await page.evaluate(() => document.body.innerText);
    console.log('\n📄 Page text preview (first 500 chars):');
    console.log(bodyText.substring(0, 500));
    
    // Check for models
    console.log('\n🔍 Checking for model mentions:');
    if (bodyText.includes('codebrewRouter')) console.log('✅ Found codebrewRouter');
    if (bodyText.includes('local-model')) console.log('✅ Found local-model');
    if (bodyText.includes('gemma')) console.log('✅ Found gemma');
    
    // Find the input field
    console.log('\n📝 Looking for input field...');
    const inputs = await page.$$eval('[contenteditable="true"], textarea, input[type="text"]', els => 
      els.map(el => ({ tag: el.tagName, placeholder: el.placeholder, id: el.id, class: el.className }))
    );
    console.log('Found inputs:', inputs);
    
    // Find buttons
    console.log('\n🔘 Looking for buttons...');
    const buttons = await page.$$eval('button', buttons => 
      buttons.slice(0, 10).map(btn => ({ text: btn.innerText, class: btn.className }))
    );
    console.log('First 10 buttons:');
    buttons.forEach((btn, i) => console.log(`  ${i}: ${btn.text || '(empty)'} - ${btn.class}`));
    
    // Try to find and interact with input
    const inputField = await page.$('[contenteditable="true"]');
    if (inputField) {
      console.log('\n✏️ Clicking input field and typing message...');
      await inputField.click();
      await inputField.type('Tell me a dad joke');
      
      console.log('📸 Screenshot after typing...');
      await page.screenshot({ path: 'webui-after-typing.png', fullPage: true });
      
      // Look for button with send icon or text
      const sendBtn = await page.$('button[aria-label*="send"], button[title*="send"], button svg[data-icon="send"]');
      if (sendBtn) {
        console.log('✅ Found send button, clicking...');
        await sendBtn.click();
        
        console.log('⏳ Waiting for response (5 seconds)...');
        await page.waitForTimeout(5000);
        
        console.log('📸 Screenshot after sending...');
        await page.screenshot({ path: 'webui-after-send.png', fullPage: true });
      } else {
        console.log('❌ Could not find send button');
        // Try pressing Enter
        console.log('📤 Trying to press Enter...');
        await inputField.press('Enter');
        
        await page.waitForTimeout(3000);
        console.log('📸 Screenshot after Enter...');
        await page.screenshot({ path: 'webui-after-enter.png', fullPage: true });
      }
    } else {
      console.log('❌ Could not find input field');
    }
    
    // Check for errors or responses
    const finalText = await page.evaluate(() => document.body.innerText);
    if (finalText.includes('error') || finalText.includes('Error')) {
      console.log('\n⚠️ Error found on page');
    }
    
    console.log('\n✅ Test complete - check PNG files for screenshots');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    try {
      await page.screenshot({ path: 'webui-error.png', fullPage: true });
    } catch (e) {
      console.error('Could not save error screenshot:', e.message);
    }
  } finally {
    await browser.close();
  }
})();
