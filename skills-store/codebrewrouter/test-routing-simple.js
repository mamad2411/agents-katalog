const { chromium } = require('playwright');
const fs = require('fs');

async function testRouting() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('\n🎯 Testing LM Studio (.56) Routing\n');
  
  // Quick creative prompt - should route to LM Studio
  console.log('📤 Sending CREATIVE writing prompt...');
  console.log('   Prompt: "Tell a creative sci-fi story in 50 words"');
  
  try {
    const response = await page.request.post('http://localhost:5022/v1/chat/completions', {
      data: JSON.stringify({
        model: "codebrewRouter",
        messages: [
          { role: "system", content: "Be creative and imaginative." },
          { role: "user", content: "Tell a creative sci-fi story in exactly 50 words about AI learning to dream." }
        ],
        max_tokens: 60,
        temperature: 0.8
      }),
      headers: { 'Content-Type': 'application/json' }
    });
    
    const data = await response.json();
    console.log('\n📥 Response received!');
    console.log(`   Model: ${data.model}`);
    console.log(`   Content: ${data.choices[0].message.content}`);
    console.log(`   Tokens used: ${data.usage?.total_tokens || 'unknown'}\n`);
  } catch (e) {
    console.error(`Error: ${e.message}`);
  }
  
  // Test models endpoint to show both Ollama and LM Studio are available
  console.log('📊 Checking available models...');
  try {
    const modelsResponse = await page.request.get('http://localhost:5022/v1/models');
    const modelsData = await modelsResponse.json();
    console.log('   Available models:');
    modelsData.data.forEach(m => {
      console.log(`     • ${m.id}`);
    });
  } catch (e) {
    console.log(`   Error: ${e.message}`);
  }
  
  // Screenshot Scalar UI
  console.log('\n📸 Capturing Scalar UI screenshot...');
  await page.goto('http://localhost:5022/scalar', { waitUntil: 'load', timeout: 10000 });
  await page.screenshot({ path: 'screenshots/scalar-routing-demo.png', fullPage: true });
  console.log('   ✓ Screenshot saved: scalar-routing-demo.png');
  
  // Screenshot landing page
  console.log('\n📸 Capturing API landing page...');
  await page.goto('http://localhost:5022', { waitUntil: 'load', timeout: 10000 });
  await page.screenshot({ path: 'screenshots/api-landing.png', fullPage: true });
  console.log('   ✓ Screenshot saved: api-landing.png\n');
  
  console.log('✅ Test completed!');
  console.log('\n📋 Routing Configuration:');
  console.log('   Ollama Router (.12/.53):');
  console.log('     • Primary: http://192.168.16.12:11434');
  console.log('     • Fallback: https://codellama.local.codebrewco.net');
  console.log('   LM Studio (.56): http://192.168.16.56:1234/v1');
  console.log('   codebrewRouter: Routes tasks to appropriate provider\n');
  
  await browser.close();
}

testRouting().catch(console.error);
