const { chromium } = require('playwright');
const fs = require('fs');

async function testLmStudioRouting() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('\n🎭 Playwright Test: LM Studio (.56) Routing\n');
  console.log('=' * 60);
  
  // Complex prompts that should route to LM Studio for creative/coding tasks
  const prompts = [
    {
      name: "Code Generation Task",
      prompt: "Write a Python function that generates Fibonacci numbers using a generator. Include docstring and error handling.",
      expectedModel: "codebrew_balanced"
    },
    {
      name: "Creative Writing Task", 
      prompt: "Write a short sci-fi story (200 words) about an AI discovering consciousness. Include dialogue and vivid descriptions.",
      expectedModel: "codebrew_balanced"
    },
    {
      name: "Complex Analysis Task",
      prompt: "Analyze the theme of identity in Shakespeare's works and compare how it appears in 3 different plays. Be detailed.",
      expectedModel: "codebrew_balanced"
    }
  ];
  
  // Test 1: API Scalar Interface
  console.log('\n1️⃣ Testing API Scalar Interface\n');
  try {
    await page.goto('http://localhost:5022/scalar', { waitUntil: 'load', timeout: 10000 });
    await page.waitForSelector('[class*="scalar"]', { timeout: 5000 });
    console.log('✓ Scalar UI loaded');
    
    // Capture Scalar UI
    await page.screenshot({ path: 'screenshots/scalar-interface.png', fullPage: true });
    console.log('📸 Screenshot saved: screenshots/scalar-interface.png');
  } catch (e) {
    console.error(`✗ Scalar UI test failed: ${e.message}`);
  }
  
  // Test 2: Direct API Tests to .56
  console.log('\n2️⃣ Testing Direct API Requests (should route to .56 for creative/complex tasks)\n');
  
  for (const test of prompts) {
    console.log(`Testing: ${test.name}`);
    try {
      const response = await page.request.post('http://localhost:5022/v1/chat/completions', {
        data: JSON.stringify({
          model: "codebrewRouter",
          messages: [
            {
              role: "system",
              content: "You are a helpful assistant. Be concise and creative when needed."
            },
            {
              role: "user",
              content: test.prompt
            }
          ],
          max_tokens: 100,
          temperature: 0.7
        }),
        headers: { 'Content-Type': 'application/json' }
      });
      
      const data = await response.json();
      const responseText = data.choices[0]?.message?.content || "(no response)";
      
      console.log(`  ✓ Response received:`);
      console.log(`    Model: ${data.model}`);
      console.log(`    Content: ${responseText.substring(0, 80)}...`);
      console.log('');
    } catch (e) {
      console.error(`  ✗ Request failed: ${e.message}`);
    }
  }
  
  // Test 3: Streaming Response with Complex Prompt
  console.log('3️⃣ Testing Streaming Response (Complex Creative Task)\n');
  try {
    const streamPayload = {
      model: "codebrewRouter",
      messages: [
        {
          role: "user",
          content: "Write a detailed technical explanation of quantum computing including superposition, entanglement, and quantum gates. Then explain how these could be used for cryptography. Be thorough."
        }
      ],
      stream: true,
      max_tokens: 150,
      temperature: 0.8
    };
    
    const response = await page.request.post('http://localhost:5022/v1/chat/completions', {
      data: JSON.stringify(streamPayload),
      headers: { 'Content-Type': 'application/json' }
    });
    
    const text = await response.text();
    const chunks = text.split('\n').filter(line => line.startsWith('data:'));
    
    console.log(`✓ Streaming response received`);
    console.log(`  Total chunks: ${chunks.length}`);
    console.log(`  Status: ${response.status()}`);
    
    // Extract model info from first chunk
    if (chunks.length > 0) {
      try {
        const firstData = chunks[0].substring(5).trim();
        if (firstData && firstData !== '[DONE]') {
          const parsed = JSON.parse(firstData);
          console.log(`  Model: ${parsed.model || 'unknown'}`);
          console.log(`  First chunk delta: ${JSON.stringify(parsed.choices[0]?.delta).substring(0, 60)}...`);
        }
      } catch (e) {
        // Ignore parsing errors
      }
    }
    console.log('');
  } catch (e) {
    console.error(`✗ Streaming test failed: ${e.message}`);
  }
  
  // Test 4: Check available models
  console.log('4️⃣ Checking Available Models\n');
  try {
    const response = await page.request.get('http://localhost:5022/v1/models');
    const data = await response.json();
    console.log('✓ Available models:');
    data.data.forEach(m => {
      console.log(`  • ${m.id}`);
    });
    console.log('');
  } catch (e) {
    console.error(`✗ Models endpoint failed: ${e.message}`);
  }
  
  // Test 5: Check diagnostics to see which providers are active
  console.log('5️⃣ Provider Health Check\n');
  try {
    const response = await page.request.get('http://localhost:5022/v1/models/diagnostics');
    const data = await response.json();
    console.log('✓ Provider Status:');
    Object.entries(data || {}).forEach(([provider, status]) => {
      console.log(`  • ${provider}: ${status.healthy ? '✅ HEALTHY' : '❌ UNHEALTHY'}`);
    });
  } catch (e) {
    console.error(`✗ Diagnostics failed: ${e.message}`);
  }
  
  console.log('\n✅ All Playwright tests completed!');
  console.log('Screenshots saved to: screenshots/');
  
  await browser.close();
}

testLmStudioRouting().catch(console.error);
