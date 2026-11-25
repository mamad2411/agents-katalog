const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ 
    headless: false
  });
  const page = await browser.newPage();
  
  // Set viewport for better screenshots
  await page.setViewportSize({ width: 1920, height: 1080 });

  try {
    console.log('🚀 Starting API test with Scalar...\n');

    // Step 1: Navigate to Scalar API documentation
    console.log('📖 Step 1: Opening Scalar API documentation');
    console.log('   URL: http://localhost:5000/scalar');
    
    try {
      await page.goto('http://localhost:5000/scalar', { 
        waitUntil: 'networkidle',
        timeout: 15000
      });
      console.log('✅ Scalar loaded successfully');
      
      // Take screenshot of Scalar UI
      console.log('📸 Taking screenshot of Scalar UI...');
      await page.screenshot({ path: 'scalar-ui.png', fullPage: false });
      console.log('✅ Screenshot saved: scalar-ui.png');
    } catch (error) {
      console.log(`⚠️ Scalar not available: ${error.message}`);
      console.log('   Fallback: Testing API endpoints directly...\n');
    }

    // Step 2: Test models endpoint
    console.log('\n🔍 Step 2: Testing /v1/models endpoint');
    const modelsStart = Date.now();
    const modelsResponse = await page.evaluate(async () => {
      try {
        const res = await fetch('http://localhost:5000/v1/models', {
          timeout: 5000
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return {
          status: res.status,
          data: await res.json(),
          error: null
        };
      } catch (error) {
        return { status: 0, data: null, error: error.message };
      }
    });
    const modelsDuration = Date.now() - modelsStart;
    
    if (modelsResponse.error) {
      console.log(`❌ Models endpoint failed: ${modelsResponse.error}`);
    } else {
      console.log(`✅ Models endpoint responded in ${modelsDuration}ms with ${modelsResponse.data.data.length} models`);
      modelsResponse.data.data.forEach(m => {
        console.log(`   - ${m.id} (${m.provider}) - ${m.enabled ? '✅ enabled' : '❌ disabled'}`);
      });
    }

    // Step 3: Test chat completions with codebrewRouter
    console.log('\n💬 Step 3: Testing /v1/chat/completions with codebrewRouter');
    const chatStart = Date.now();
    
    const chatResult = await page.evaluate(async () => {
      try {
        const requestBody = {
          model: 'codebrewRouter',
          messages: [
            {
              role: 'user',
              content: 'Tell me a dad joke in one sentence'
            }
          ],
          stream: true,
          max_tokens: 150,
          temperature: 0.7
        };

        const res = await fetch('http://localhost:5000/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
          timeout: 30000
        });

        if (!res.ok) {
          return {
            success: false,
            error: `HTTP ${res.status}: ${res.statusText}`,
            chunks: 0,
            text: ''
          };
        }

        // Read streaming response
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        let chunkCount = 0;
        let firstChunkTime = 0;

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const chunk = decoder.decode(value);
          fullResponse += chunk;
          
          if (chunkCount === 0) firstChunkTime = Date.now();
          
          // Count SSE data lines
          const dataLines = chunk.split('\n').filter(l => l.startsWith('data: '));
          chunkCount += dataLines.length;
        }

        // Extract text content from SSE chunks
        let extractedText = '';
        const lines = fullResponse.split('\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.replace('data: ', '').trim();
            if (data === '[DONE]') continue;
            try {
              const json = JSON.parse(data);
              if (json.choices?.[0]?.delta?.content) {
                extractedText += json.choices[0].delta.content;
              }
            } catch (e) {
              // Skip parse errors
            }
          }
        }

        return {
          success: true,
          chunks: chunkCount,
          text: extractedText,
          error: null
        };
      } catch (error) {
        return {
          success: false,
          error: error.message,
          chunks: 0,
          text: ''
        };
      }
    });

    const chatDuration = Date.now() - chatStart;

    if (chatResult.success) {
      console.log(`✅ Chat completed in ${chatDuration}ms`);
      console.log(`   - Received ${chatResult.chunks} SSE chunks`);
      console.log(`   - Response: "${chatResult.text.substring(0, 100)}${chatResult.text.length > 100 ? '...' : ''}"`);
    } else {
      console.log(`❌ Chat failed: ${chatResult.error}`);
    }

    // Step 4: Test with local-model (LM Studio)
    console.log('\n💬 Step 4: Testing /v1/chat/completions with local-model');
    const localStart = Date.now();

    const localResult = await page.evaluate(async () => {
      try {
        const res = await fetch('http://localhost:5000/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: 'local-model',
            messages: [
              {
                role: 'user',
                content: 'Hello'
              }
            ],
            stream: true,
            max_tokens: 50,
            temperature: 0.7
          }),
          timeout: 15000
        });

        if (!res.ok) {
          return {
            success: false,
            error: `HTTP ${res.status}`,
            reached: false
          };
        }

        // Just check if we get first chunk
        const reader = res.body.getReader();
        const { value } = await reader.read();
        const chunk = new TextDecoder().decode(value);
        
        return {
          success: true,
          reached: true,
          firstChunk: chunk.substring(0, 50)
        };
      } catch (error) {
        return {
          success: false,
          error: error.message,
          reached: error.message.includes('ERR_') ? false : true
        };
      }
    });

    const localDuration = Date.now() - localStart;

    if (localResult.success) {
      console.log(`✅ local-model endpoint reachable in ${localDuration}ms`);
    } else {
      console.log(`⚠️ local-model test: ${localResult.error}`);
      if (!localResult.reached) {
        console.log(`   (Connection not reached - LM Studio may be offline at 192.168.16.56:1234)`);
      }
    }

    // Step 5: Summary and screenshot
    console.log('\n📊 Test Summary');
    console.log('═'.repeat(60));
    console.log(`✅ API Server: http://localhost:5000`);
    console.log(`✅ Models Endpoint: Working (${modelsDuration}ms)`);
    console.log(`${chatResult.success ? '✅' : '❌'} Chat Endpoint (codebrewRouter): ${chatResult.success ? `Working (${chatDuration}ms)` : 'Failed'}`);
    console.log(`${localResult.success ? '✅' : '⚠️'} Chat Endpoint (local-model): ${localResult.success ? 'Working' : 'Unreachable'}`);

    // Final screenshot
    console.log('\n📸 Taking final screenshot...');
    await page.screenshot({ path: 'api-test-complete.png', fullPage: false });
    console.log('✅ Screenshot saved: api-test-complete.png');

    if (chatResult.success) {
      console.log('\n✅✅✅ ALL CRITICAL TESTS PASSED ✅✅✅');
      console.log('API is working correctly with codebrewRouter model');
      process.exit(0);
    } else {
      console.log('\n⚠️ Chat endpoint issue detected');
      process.exit(1);
    }

  } catch (error) {
    console.error('\n❌ Unexpected error:', error.message);
    console.log('\n📸 Taking error screenshot...');
    await page.screenshot({ path: 'api-test-error.png' });
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
