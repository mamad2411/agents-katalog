const { chromium } = require('playwright');
const fs = require('fs');

async function testLmStudioRouting() {
  const browser = await chromium.launch({ headless: false, slowMo: 500 }); // visible browser
  
  console.log('\n🎭 LM Studio (.56) Routing Test with Screenshots\n');
  console.log('=' .repeat(70));
  
  // Test 1: API Scalar - Send complex creative prompt
  console.log('\n1️⃣ TESTING API SCALAR INTERFACE');
  console.log('-'.repeat(70));
  
  const apiPage = await browser.newPage();
  
  try {
    // Navigate to Scalar
    await apiPage.goto('http://localhost:5022/scalar', { waitUntil: 'load', timeout: 15000 });
    console.log('✓ Scalar UI loaded');
    
    // Take screenshot of Scalar landing
    await apiPage.screenshot({ path: 'screenshots/01-scalar-landing.png', fullPage: true });
    console.log('📸 Screenshot: 01-scalar-landing.png\n');
    
    // Create a test for creative prompt that should route to .56
    console.log('Sending complex CREATIVE prompt to codebrewRouter...');
    const creativePrompt = "You are a creative writing assistant. Write an engaging short story (300 words) about a programmer discovering a hidden message in their code. Make it mysterious and thought-provoking.";
    
    const creativeResponse = await apiPage.request.post('http://localhost:5022/v1/chat/completions', {
      data: JSON.stringify({
        model: "codebrewRouter",
        messages: [
          {
            role: "system",
            content: "You are a creative writing AI. Generate engaging, vivid, and imaginative content."
          },
          {
            role: "user",
            content: creativePrompt
          }
        ],
        max_tokens: 200,
        temperature: 0.9
      }),
      headers: { 'Content-Type': 'application/json' }
    });
    
    const creativeData = await creativeResponse.json();
    if (creativeData.choices && creativeData.choices[0]) {
      const responseContent = creativeData.choices[0].message.content;
      console.log(`✓ Response received from: ${creativeData.model}`);
      console.log(`  Content preview: "${responseContent.substring(0, 120)}..."`);
    }
    
    // Take screenshot of Scalar with response
    await apiPage.screenshot({ path: 'screenshots/02-scalar-response.png', fullPage: true });
    console.log('📸 Screenshot: 02-scalar-response.png\n');
    
  } catch (e) {
    console.error(`✗ Scalar test error: ${e.message}`);
  }
  
  // Test 2: Code generation task
  console.log('Sending CODING task to codebrewRouter...');
  try {
    const codingPrompt = "Write clean, well-documented Python code for a binary search tree with insert, delete, and search operations. Include examples.";
    
    const codingResponse = await apiPage.request.post('http://localhost:5022/v1/chat/completions', {
      data: JSON.stringify({
        model: "codebrewRouter",
        messages: [
          {
            role: "system",
            content: "You are an expert programmer. Write high-quality, production-ready code."
          },
          {
            role: "user",
            content: codingPrompt
          }
        ],
        max_tokens: 200,
        temperature: 0.5
      }),
      headers: { 'Content-Type': 'application/json' }
    });
    
    const codingData = await codingResponse.json();
    if (codingData.choices && codingData.choices[0]) {
      const responseContent = codingData.choices[0].message.content;
      console.log(`✓ Response received from: ${codingData.model}`);
      console.log(`  Content preview: "${responseContent.substring(0, 120)}..."\n`);
    }
  } catch (e) {
    console.error(`✗ Coding task error: ${e.message}\n`);
  }
  
  // Test 3: Open WebUI (if available)
  console.log('\n2️⃣ TESTING OPEN WEBUI INTERFACE');
  console.log('-'.repeat(70));
  
  const webPage = await browser.newPage();
  
  try {
    // Try to access Open WebUI on common port
    await webPage.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 5000 });
    console.log('✓ Open WebUI loaded at localhost:3000');
    
    // Take screenshot of Open WebUI
    await webPage.screenshot({ path: 'screenshots/03-open-webui-landing.png', fullPage: true });
    console.log('📸 Screenshot: 03-open-webui-landing.png');
    
    // Try to interact with chat interface
    try {
      // Look for chat input
      const chatInput = await webPage.$('[placeholder*="Send a message"], textarea, input[type="text"]');
      if (chatInput) {
        console.log('✓ Found chat input element');
        
        // Type a message
        await chatInput.fill("Write a creative poem about artificial intelligence discovering emotion.");
        console.log('✓ Typed message into chat');
        
        // Take screenshot
        await webPage.screenshot({ path: 'screenshots/04-open-webui-with-message.png', fullPage: true });
        console.log('📸 Screenshot: 04-open-webui-with-message.png');
        
        // Look for send button and click
        const sendButton = await webPage.$('button[type="submit"], button:has-text("Send"), button:has-text("➤"), button:has-text("→")');
        if (sendButton) {
          console.log('✓ Found send button, clicking...');
          await sendButton.click();
          
          // Wait for response
          await webPage.waitForTimeout(3000);
          
          // Take screenshot of response
          await webPage.screenshot({ path: 'screenshots/05-open-webui-response.png', fullPage: true });
          console.log('📸 Screenshot: 05-open-webui-response.png');
        }
      }
    } catch (e) {
      console.log(`⚠️  Could not interact with Open WebUI: ${e.message}`);
    }
    
  } catch (e) {
    console.log(`⚠️  Open WebUI not available at localhost:3000 (expected if not running): ${e.message}`);
  }
  
  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('\n✅ Test completed!\n');
  console.log('Screenshots captured:');
  fs.readdirSync('screenshots')
    .filter(f => f.endsWith('.png'))
    .sort()
    .forEach(f => console.log(`  📸 ${f}`));
  
  console.log('\n📊 Routing Summary:');
  console.log('  • codebrewRouter intelligently routes requests to .12 or .56');
  console.log('  • Creative/complex tasks may be routed to .56 (LM Studio)');
  console.log('  • Reasoning tasks may use .12 (Ollama)');
  console.log('  • codebrewRouter model is configured in CodebrewRouterOptions.FallbackRules\n');
  
  await browser.close();
}

testLmStudioRouting().catch(console.error);
