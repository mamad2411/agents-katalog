const { chromium } = require('playwright');

async function test() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('🎭 Playwright Test Suite for HTTPS Fallback Configuration\n');
  
  // Test 1: API Gateway Landing Page
  console.log('1️⃣ Testing API Gateway Landing Page...');
  try {
    await page.goto('http://localhost:5022', { waitUntil: 'load', timeout: 10000 });
    const title = await page.title();
    console.log(`✓ Landing page loaded: ${title}`);
    const healthLink = await page.$eval('a[href="/health"]', el => el.textContent);
    console.log(`✓ Found health link: ${healthLink}`);
  } catch (e) {
    console.error(`✗ Landing page test failed: ${e.message}`);
  }
  
  // Test 2: Scalar API Documentation
  console.log('\n2️⃣ Testing Scalar API Documentation...');
  try {
    await page.goto('http://localhost:5022/scalar', { waitUntil: 'load', timeout: 10000 });
    await page.waitForSelector('[class*="scalar"]', { timeout: 5000 });
    console.log('✓ Scalar UI loaded');
  } catch (e) {
    console.error(`✗ Scalar UI test failed: ${e.message}`);
  }
  
  // Test 3: Direct API Request - /v1/models
  console.log('\n3️⃣ Testing /v1/models endpoint...');
  try {
    const response = await page.request.get('http://localhost:5022/v1/models');
    const data = await response.json();
    console.log(`✓ Models endpoint responding: ${response.status()}`);
    console.log(`✓ Available models: ${data.data.map(m => m.id).join(', ')}`);
  } catch (e) {
    console.error(`✗ Models endpoint test failed: ${e.message}`);
  }
  
  // Test 4: Chat Completion Request
  console.log('\n4️⃣ Testing /v1/chat/completions endpoint...');
  try {
    const payload = {
      model: 'codebrewRouter',
      messages: [{ role: 'user', content: 'What is the capital of France?' }],
      max_tokens: 50
    };
    
    const response = await page.request.post('http://localhost:5022/v1/chat/completions', {
      data: JSON.stringify(payload),
      headers: { 'Content-Type': 'application/json' }
    });
    
    const data = await response.json();
    console.log(`✓ Chat completion endpoint responding: ${response.status()}`);
    console.log(`✓ Model response: ${data.choices[0].message.content.substring(0, 80)}...`);
  } catch (e) {
    console.error(`✗ Chat completion test failed: ${e.message}`);
  }
  
  // Test 5: Streaming Chat Completion
  console.log('\n5️⃣ Testing streaming /v1/chat/completions...');
  try {
    const payload = {
      model: 'codebrewRouter',
      messages: [{ role: 'user', content: 'Count to 3' }],
      stream: true,
      max_tokens: 20
    };
    
    const response = await page.request.post('http://localhost:5022/v1/chat/completions', {
      data: JSON.stringify(payload),
      headers: { 'Content-Type': 'application/json' }
    });
    
    console.log(`✓ Streaming endpoint responding: ${response.status()}`);
    const text = await response.text();
    const chunks = text.split('\n').filter(line => line.startsWith('data:'));
    console.log(`✓ Received ${chunks.length} SSE chunks`);
    console.log(`✓ Final chunk: ${chunks[chunks.length - 2]}`);
  } catch (e) {
    console.error(`✗ Streaming test failed: ${e.message}`);
  }
  
  console.log('\n✅ All Playwright tests completed!');
  await browser.close();
}

test().catch(console.error);
