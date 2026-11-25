# OpenRouter Integration for PrestaShop

Comprehensive guide to integrate OpenRouter API into PrestaShop modules, focusing on direct API calls using native PHP (cURL) to maintain compatibility and avoid external dependencies (no Guzzle/SDKs).

## API Configuration

- **Base URL:** `https://openrouter.ai/api/v1`
- **Main Endpoint:** `https://openrouter.ai/api/v1/chat/completions`
- **Auth:** Bearer Token via `Authorization` header.

## Required Headers

OpenRouter requires standard OpenAI headers plus optional but recommended identification headers for ranking:

```php
$headers = [
    'Authorization: Bearer ' . $api_key,
    'HTTP-Referer: ' . \Tools::getHttpHost(true), // Recommended site URL
    'X-OpenRouter-Title: ' . \Configuration::get('PS_SHOP_NAME'), // Recommended site title
    'Content-Type: application/json'
];
```

## Basic Implementation (PHP cURL)

Use this pattern to call OpenRouter without external libraries:

```php
public function callOpenRouter($model, $messages, $temperature = 0.7) {
    $api_key = \Configuration::get('OPENROUTER_API_KEY');
    $url = 'https://openrouter.ai/api/v1/chat/completions';
    
    $payload = [
        'model' => $model,
        'messages' => $messages,
        'temperature' => $temperature,
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $api_key,
        'HTTP-Referer: ' . \Tools::getHttpHost(true),
        'X-OpenRouter-Title: ' . \Configuration::get('PS_SHOP_NAME'),
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code !== 200) {
        // Handle error
        return null;
    }

    return json_decode($response, true);
}
```

## Integrating into OmniMind Adapter Pattern

To adapt OpenRouter into the existing `ecom_omnimind` architecture:

1. **Create Adapter:** `OpenRouterAdapter.php` in `classes/AI/`.
2. **Implement Interface:** Must extend/implement the standard `AiAdapter` pattern used in the module.
3. **Register Adapter:** Add to `AiAdapterFactory`.
4. **Configuration:** Add `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` fields to the module configuration.

## Key Features of OpenRouter

- **Unified API:** One endpoint for hundreds of models (Llama, GPT-4, Claude, etc.).
- **Fallback Logic:** OpenRouter handles model routing if specific providers are down.
- **Cost Tracking:** OpenRouter provides detailed usage stats via their dashboard.

## Best Practices

- **Timeout:** Always set a generous timeout (60s+) as some models through OpenRouter might have high latency.
- **Error Handling:** Check for both HTTP errors and JSON error messages from the API.
- **Model Names:** Use the full model ID (e.g., `openai/gpt-4o`, `anthropic/claude-3-opus`).
