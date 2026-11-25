const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    console.log('🌐 Opening Open WebUI...');
    await page.goto('http://localhost:8080/', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    console.log('📝 Sending message to codebrewRouter...');
    
    // Click the input and type message
    const inputField = await page.$('#chat-input');
    if (!inputField) {
      throw new Error('Input field not found');
    }
    
    await inputField.click();
    await inputField.type('Tell me a dad joke', { delay: 50 });
    console.log('✅ Typed message');
    
    // Press Enter
    console.log('📤 Pressing Enter to send...');
    const start = Date.now();
    await inputField.press('Enter');
    
    // Wait and monitor for response
    console.log('⏳ Waiting for response...');
    let hasResponse = false;
    let waitTime = 0;
    
    for (let i = 0; i < 30; i++) {
      await page.waitForTimeout(1000);
      waitTime = Date.now() - start;
      
      // Check if there's a response in the chat
      const messages = await page.$$eval('[class*="message"], [class*="chat"]', els => 
        els.length
      );
      
      const pageText = await page.evaluate(() => document.body.innerText);
      
      // Look for any response
      if (pageText.includes('dad') || pageText.includes('joke') || pageText.includes('laugh') || pageText.includes('Why')) {
        hasResponse = true;
        console.log(`✅ Response detected after ${waitTime}ms!`);
        console.log('Response preview:', pageText.substring(pageText.lastIndexOf('codebrewRouter'), Math.min(pageText.length, pageText.lastIndexOf('codebrewRouter') + 500)));
        break;
      }
      
      // Look for loading/thinking indicator
      if (pageText.includes('thinking') || pageText.includes('waiting')) {
        console.log(`  ${i}s - Still processing...`);
      } else if (i % 5 === 0) {
        console.log(`  ${waitTime}ms elapsed...`);
      }
    }
    
    if (!hasResponse) {
      console.log(`❌ No response after 30 seconds`);
      const finalText = await page.evaluate(() => document.body.innerText);
      console.log('\nFinal page text (last 1000 chars):');
      console.log(finalText.substring(Math.max(0, finalText.length - 1000)));
    }
    
    console.log('📸 Final screenshot...');
    await page.screenshot({ path: 'webui-final.png', fullPage: true });
    
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
