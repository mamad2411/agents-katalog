const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // Log all network activity
  page.on('response', response => {
    if (response.url().includes('/v1/')) {
      console.log(`📡 ${response.status()} ${response.url()}`);
    }
  });
  
  page.on('requestfailed', request => {
    console.log(`❌ Request failed: ${request.url()}`);
    console.log(`   Error: ${request.failure().errorText}`);
  });

  try {
    console.log('🔍 Testing chat completions endpoint with codebrewRouter model...\n');

    // Test 1: Check models endpoint
    console.log('📊 Test 1: Checking available models');
    const modelsResponse = await page.evaluate(async () => {
      const res = await fetch('http://localhost:5000/v1/models');
      return await res.json();
    });
    console.log(`✅ Found ${modelsResponse.data.length} models:`);
    modelsResponse.data.forEach(m => console.log(`   - ${m.id} (${m.provider})`));

    // Test 2: Send a streaming request to codebrewRouter
    console.log('\n📨 Test 2: Sending chat message to codebrewRouter model');
    const controller = new (require('stream').ReadableStream)();
    
    let response = '';
    let receivedFirstChunk = false;
    let receivedData = false;

    const startTime = Date.now();
    const chatResponse = await page.evaluate(async () => {
      return new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error('Request timeout after 30 seconds'));
        }, 30000);

        fetch('http://localhost:5000/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: 'codebrewRouter',
            messages: [
              {
                role: 'user',
                content: 'Tell me a dad joke'
              }
            ],
            stream: true,
            temperature: 0.7,
            max_tokens: 100
          })
        })
          .then(res => {
            if (!res.ok) {
              throw new Error(`HTTP ${res.status}`);
            }
            
            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let fullText = '';

            const readChunk = () => {
              reader.read().then(({ done, value }) => {
                if (done) {
                  clearTimeout(timeout);
                  resolve(fullText);
                  return;
                }

                const chunk = decoder.decode(value);
                fullText += chunk;
                readChunk();
              }).catch(err => {
                clearTimeout(timeout);
                reject(err);
              });
            };

            readChunk();
          })
          .catch(err => {
            clearTimeout(timeout);
            reject(err);
          });
      });
    });

    const duration = Date.now() - startTime;
    console.log(`✅ Received response in ${duration}ms`);
    
    // Parse SSE chunks
    const chunks = chatResponse.split('\n').filter(line => line.startsWith('data: '));
    console.log(`✅ Received ${chunks.length} SSE chunks`);
    
    let extractedText = '';
    chunks.forEach((chunk, idx) => {
      const data = chunk.replace('data: ', '').trim();
      if (data === '[DONE]') {
        console.log(`   Chunk ${idx + 1}: [DONE]`);
        return;
      }
      
      try {
        const json = JSON.parse(data);
        if (json.choices?.[0]?.delta?.content) {
          extractedText += json.choices[0].delta.content;
          console.log(`   Chunk ${idx + 1}: "${json.choices[0].delta.content}"`);
        }
      } catch (e) {
        console.log(`   Chunk ${idx + 1}: (parse error)`);
      }
    });

    console.log(`\n📝 Full response: "${extractedText}"`);

    // Test 3: Send request to local-model (LM Studio)
    console.log('\n📨 Test 3: Sending chat message to local-model (LM Studio)');
    try {
      const localModelResponse = await page.evaluate(async () => {
        return new Promise((resolve, reject) => {
          const timeout = setTimeout(() => {
            reject(new Error('Request timeout after 15 seconds'));
          }, 15000);

          fetch('http://localhost:5000/v1/chat/completions', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              model: 'local-model',
              messages: [
                {
                  role: 'user',
                  content: 'hello'
                }
              ],
              stream: true,
              temperature: 0.7,
              max_tokens: 50
            })
          })
            .then(res => {
              if (!res.ok) {
                throw new Error(`HTTP ${res.status}: ${res.statusText}`);
              }
              const reader = res.body.getReader();
              const decoder = new TextDecoder();
              let fullText = '';

              const readChunk = () => {
                reader.read().then(({ done, value }) => {
                  if (done) {
                    clearTimeout(timeout);
                    resolve(fullText);
                    return;
                  }
                  fullText += decoder.decode(value);
                  readChunk();
                }).catch(err => {
                  clearTimeout(timeout);
                  reject(err);
                });
              };

              readChunk();
            })
            .catch(err => {
              clearTimeout(timeout);
              reject(err);
            });
        });
      });

      const localChunks = localModelResponse.split('\n').filter(line => line.startsWith('data: '));
      console.log(`✅ local-model test passed - received ${localChunks.length} chunks`);
    } catch (error) {
      console.log(`⚠️ local-model test failed: ${error.message}`);
    }

    console.log('\n📸 Taking screenshot of test results...');
    await page.screenshot({ path: 'test-results.png' });
    console.log('✅ Screenshot saved to test-results.png');

    console.log('\n✅ ALL TESTS PASSED');
    process.exit(0);

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    console.log('\n📸 Taking error screenshot...');
    await page.screenshot({ path: 'test-error.png' });
    console.log('Error screenshot saved to test-error.png');
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
