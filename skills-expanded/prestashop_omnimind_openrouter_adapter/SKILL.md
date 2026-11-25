# OpenRouter Adapter for OmniMind

Specific implementation guide for adding OpenRouter as an AI provider in the `ecom_omnimind` module.

## 1. Class Structure (`OpenRouterAdapter.php`)

Create the file in `classes/AI/OpenRouterAdapter.php`.

```php
namespace Ecom\Omnimind\AI;

use Configuration;

class OpenRouterAdapter implements AiAdapterInterface
{
    private $api_key;
    private $model;
    private $context;
    private $base_url = 'https://openrouter.ai/api/v1/chat/completions';

    public function __construct($api_key, $model, \Context $context)
    {
        $this->context = $context;
        $idShop = (int) (isset($this->context->shop->id) ? $this->context->shop->id : Configuration::get('PS_SHOP_DEFAULT')) ?: 1;
        $this->api_key = $api_key ?: Configuration::get('ECOM_OMNIMIND_OPENROUTER_KEY', null, null, $idShop);
        $this->model = $model ?: Configuration::get('ECOM_OMNIMIND_OPENROUTER_MODEL', null, null, $idShop);
    }

    public function getProviderName() { return 'OpenRouter'; }
    public function isConfigured() { return !empty($this->api_key); }
    public function getModel() { return $this->model; }

    public function sendPrompt($prompt, array $options = [])
    {
        if (!$this->isConfigured()) {
            return ['success' => false, 'error' => 'OpenRouter API Key not configured'];
        }

        // Standard OmniMind logic for Spanish enforcement
        $spanishRule = "IMPORTANTE: RESPONDE SIEMPRE EN CASTELLANO.\n";
        $prompt = $spanishRule . $prompt;

        $payload = [
            'model' => $this->model,
            'messages' => [['role' => 'user', 'content' => $prompt]],
            'temperature' => (float) ($options['temperature'] ?? 0.7),
        ];

        $response = $this->makeRequest($payload);

        if (isset($response['choices'][0]['message']['content'])) {
            $text = $response['choices'][0]['message']['content'];
            
            // Token usage logging
            if (isset($response['usage'])) {
                \Ecom\Omnimind\Catalog\TokenUsageService::logUsage(
                    'openrouter', 
                    $this->model, 
                    $response['usage']['prompt_tokens'], 
                    $response['usage']['completion_tokens']
                );
            }

            return [
                'success' => true, 
                'data' => (isset($options['raw']) && $options['raw']) ? $text : AiAdapterFactory::cleanJson($text)
            ];
        }

        return ['success' => false, 'error' => $response['error']['message'] ?? 'Unknown OpenRouter error'];
    }

    private function makeRequest($payload)
    {
        $ch = curl_init($this->base_url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode($payload),
            CURLOPT_HTTPHEADER => [
                'Authorization: Bearer ' . $this->api_key,
                'HTTP-Referer: ' . \Tools::getHttpHost(true),
                'X-OpenRouter-Title: ' . \Configuration::get('PS_SHOP_NAME'),
                'Content-Type: application/json'
            ],
            CURLOPT_TIMEOUT => 300
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true) ?: ['error' => ['message' => 'Invalid JSON']];
    }
}
```

## 2. Factory Registration (`AiAdapterFactory.php`)

Add the case for `openrouter` in the `getAdapter` method:

```php
case 'openrouter':
    return new OpenRouterAdapter($api_key, $model, $context);
```

## 3. Configuration Fields

Ensure the module configuration (normally in `ecom_omnimind.php` or a dedicated helper) includes:
- `ECOM_OMNIMIND_OPENROUTER_KEY`
- `ECOM_OMNIMIND_OPENROUTER_MODEL`

## 4. Models supported

OpenRouter allows using any model string. It is recommended to suggest common ones like:
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro-1.5`
- `meta-llama/llama-3.1-405b`
- `openai/gpt-4o`
