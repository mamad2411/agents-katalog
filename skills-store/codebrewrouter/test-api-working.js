const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });

  try {
    console.log('🚀 Testing API with direct curl commands and screenshots\n');

    // Test 1: Models endpoint
    console.log('Test 1: GET /v1/models');
    const modelsStart = Date.now();
    
    await page.evaluate(async () => {
      const res = await fetch('http://localhost:5000/v1/models');
      window.modelsData = await res.json();
    });
    
    const modelsDuration = Date.now() - modelsStart;
    const modelsData = await page.evaluate(() => window.modelsData);
    
    console.log(`✅ Responded in ${modelsDuration}ms`);
    console.log(`   Models: ${modelsData.data.length}`);
    modelsData.data.forEach(m => {
      console.log(`   - ${m.id} (${m.provider}) [${m.enabled ? 'enabled' : 'DISABLED'}]`);
    });

    // Test 2: Chat with codebrewRouter
    console.log('\nTest 2: POST /v1/chat/completions (codebrewRouter)');
    const chatStart = Date.now();
    
    let chatError = null;
    let chatChunks = 0;
    let chatText = '';

    try {
      const response = await page.evaluate(async () => {
        try {
          const res = await fetch('http://localhost:5000/v1/chat/completions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              model: 'codebrewRouter',
              messages: [{ role: 'user', content: 'Tell me a dad joke in one line' }],
              stream: true,
              max_tokens: 150,
              temperature: 0.7
            })
          });

          if (!res.ok) {
            return { error: `HTTP ${res.status}: ${res.statusText}`, text: '' };
          }

          const reader = res.body.getReader();
          const decoder = new TextDecoder();
          let text = '';

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            text += decoder.decode(value);
          }

          return { error: null, text };
        } catch (error) {
          return { error: error.message, text: '' };
        }
      });

      if (response.error) {
        chatError = response.error;
      } else {
        const lines = response.text.split('\n').filter(l => l.startsWith('data: '));
        chatChunks = lines.length;
        
        lines.forEach(line => {
          const data = line.replace('data: ', '').trim();
          if (data !== '[DONE]') {
            try {
              const json = JSON.parse(data);
              if (json.choices?.[0]?.delta?.content) {
                chatText += json.choices[0].delta.content;
              }
            } catch (e) {}
          }
        });
      }
    } catch (error) {
      chatError = error.message;
    }

    const chatDuration = Date.now() - chatStart;

    if (chatError) {
      console.log(`❌ Failed: ${chatError}`);
    } else {
      console.log(`✅ Responded in ${chatDuration}ms`);
      console.log(`   Chunks: ${chatChunks}`);
      console.log(`   Response: "${chatText.substring(0, 100)}..."`);
    }

    // Test 3: Scalar UI
    console.log('\nTest 3: Scalar UI');
    try {
      await page.goto('http://localhost:5000/scalar', { waitUntil: 'domcontentloaded', timeout: 10000 });
      console.log('✅ Scalar loaded');
      await page.screenshot({ path: 'scalar-ui-final.png', fullPage: false });
    } catch (error) {
      console.log(`⚠️ Scalar: ${error.message}`);
    }

    // Final summary screenshot
    console.log('\n📸 Taking final screenshot');
    await page.screenshot({ path: 'test-complete.png', fullPage: false });

    console.log('\n' + '='.repeat(60));
    if (!chatError) {
      console.log('✅✅✅ API IS WORKING ✅✅✅');
      console.log('Chat endpoint responsive and returning data');
    } else {
      console.log('❌ Chat endpoint needs fixing');
    }
    console.log('='.repeat(60));

    process.exit(chatError ? 1 : 0);

  } catch (error) {
    console.error('Error:', error.message);
    await page.screenshot({ path: 'test-error-final.png' });
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
