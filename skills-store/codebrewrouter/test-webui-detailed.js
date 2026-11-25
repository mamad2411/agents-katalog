const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Intercept network requests to see what's being sent
  await page.on('response', response => {
    if (response.url().includes('chat') || response.url().includes('completions')) {
      console.log(`🌐 ${response.status()} ${response.url()}`);
    }
  });

  try {
    console.log('🌐 Opening Open WebUI...');
    await page.goto('http://localhost:8080/', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    console.log('📝 Sending "Tell me a dad joke" to codebrewRouter...\n');
    
    const inputField = await page.$('#chat-input');
    if (!inputField) throw new Error('Input field not found');
    
    await inputField.click();
    await inputField.type('Tell me a dad joke', { delay: 50 });
    
    console.log('📤 Pressing Enter...\n');
    const startTime = Date.now();
    await inputField.press('Enter');
    
    // Wait and capture chat messages
    console.log('⏳ Monitoring for response...\n');
    let lastLength = 0;
    
    for (let i = 0; i < 15; i++) {
      await page.waitForTimeout(1000);
      
      const elapsed = Date.now() - startTime;
      
      // Get all chat messages
      const chatContent = await page.evaluate(() => {
        const messages = [];
        document.querySelectorAll('[class*="message"], [class*="chat-message"]').forEach(el => {
          const text = el.innerText?.trim();
          if (text && text.length > 0) messages.push(text);
        });
        return messages;
      });
      
      const totalChars = chatContent.join('').length;
      
      // Also get the whole page content
      const pageText = await page.evaluate(() => document.body.innerText);
      
      // Find new content since last check
      if (totalChars > lastLength) {
        console.log(`[${elapsed}ms] 📝 Chat content updated (+${totalChars - lastLength} chars)`);
        lastLength = totalChars;
        
        // Show recent additions
        const lines = pageText.split('\n').slice(-5);
        lines.forEach(line => {
          if (line.trim().length > 0 && !line.includes('codebrewRouter')) {
            console.log(`    "${line.substring(0, 80)}"`);
          }
        });
      } else if (i % 3 === 0) {
        console.log(`[${elapsed}ms] ⏳ Waiting...`);
      }
      
      // Check for error indicators
      if (pageText.toLowerCase().includes('error') || pageText.toLowerCase().includes('failed')) {
        console.log(`[${elapsed}ms] ⚠️ ERROR found on page`);
        const errorLines = pageText.split('\n').filter(l => l.toLowerCase().includes('error'));
        errorLines.forEach(line => console.log(`    ERROR: ${line}`));
      }
      
      // Check for "thinking" or "loading"
      if (pageText.includes('thinking') || pageText.includes('⏳') || pageText.includes('...')) {
        // Model is thinking
      }
    }
    
    console.log('\n✅ Test complete - monitoring stopped after 15 seconds');
    
    // Final capture of page state
    const finalText = await page.evaluate(() => {
      const text = [];
      document.querySelectorAll('[class*="message"], [role="article"], [role="region"]').forEach(el => {
        const content = el.innerText?.trim();
        if (content && content.length > 10) text.push(content);
      });
      return text;
    });
    
    console.log('\n📋 Final message content:');
    finalText.slice(-3).forEach((msg, i) => {
      console.log(`  Message ${i + 1}: ${msg.substring(0, 200)}...`);
    });
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
  } finally {
    await browser.close();
  }
})();
