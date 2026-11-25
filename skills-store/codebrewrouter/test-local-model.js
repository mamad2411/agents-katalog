const fetch = require('node-fetch');

(async () => {
  console.log('Testing local-model (LM Studio) chat completion...');
  try {
    const response = await fetch('http://localhost:8080/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'local-model',
        messages: [{ role: 'user', content: 'Hello' }],
        stream: true
      }),
      timeout: 15000
    });

    console.log('Status:', response.status);
    let body = '';
    response.body.on('data', chunk => {
      body += chunk.toString();
      process.stdout.write('.');
    });
    
    response.body.on('end', () => {
      console.log('\nStream complete');
      console.log('First 500 chars:', body.substring(0, 500));
    });

    response.body.on('error', err => console.error('Stream error:', err));
  } catch (err) {
    console.error('Error:', err.message);
  }
})();
