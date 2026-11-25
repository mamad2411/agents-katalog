const http = require('http');

console.log('Testing CodebrewRouter chat completion...\n');

const requestData = JSON.stringify({
  model: 'codebrewRouter',
  messages: [
    {
      role: 'user',
      content: 'Say hello and tell me your name'
    }
  ],
  stream: true
});

const options = {
  hostname: 'localhost',
  port: 5022,
  path: '/v1/chat/completions',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': requestData.length,
    'Authorization': 'Bearer sk-test'
  }
};

const req = http.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  console.log(`Headers:`, res.headers);
  console.log('\n📡 Stream Response:\n');

  let totalData = '';
  res.on('data', (chunk) => {
    process.stdout.write(chunk.toString());
    totalData += chunk.toString();
  });

  res.on('end', () => {
    console.log('\n\n✅ Stream complete');
    
    // Try to parse chunks
    console.log('\n📊 Parsing SSE chunks:');
    const lines = totalData.split('\n').filter(line => line.trim());
    for (const line of lines.slice(0, 10)) {
      if (line.startsWith('data: ')) {
        const data = line.substring(6);
        if (data === '[DONE]') {
          console.log('  ✅ [DONE]');
        } else {
          try {
            const json = JSON.parse(data);
            const delta = json.choices?.[0]?.delta;
            if (delta?.content) {
              console.log(`  📝 "${delta.content}"`);
            } else {
              console.log(`  ${JSON.stringify(delta).substring(0, 100)}`);
            }
          } catch (e) {
            console.log(`  ⚠️ Could not parse: ${data.substring(0, 100)}`);
          }
        }
      }
    }
  });
});

req.on('error', (error) => {
  console.error('❌ Request error:', error.message);
  process.exit(1);
});

console.log('Sending request...\n');
req.write(requestData);
req.end();

// Timeout after 15 seconds
setTimeout(() => {
  console.log('\n⏱️ Request timeout');
  process.exit(0);
}, 15000);
