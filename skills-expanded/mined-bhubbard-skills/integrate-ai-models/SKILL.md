---
name: integrate-ai-models
description: Use Vercel AI Gateway Provider plugin to interact with multiple AI models through wp_ai_client_prompt.
---

# Integrate AI Models using Vercel AI Gateway

When the Vercel AI Gateway Provider plugin is active, you can leverage it to access hundreds of models from over 40 providers using the built-in WordPress AI client.

## Usage

Use the `wp_ai_client_prompt` function to generate text, images, etc. You can explicitly target the gateway:

```php
$result = wp_ai_client_prompt( 'Hello, world!' )
    ->using_provider( 'ai_gateway' )
    ->generate_text_result();
```

Alternatively, you can specify model preferences and rely on the gateway dynamically:

```php
$result = wp_ai_client_prompt( 'Hello, world!' )
    ->using_model_preference( 'claude-opus-4.7', 'gemini-3.1-pro-preview', 'gpt-5.4' )
    ->generate_text_result();
```

## Best Practices
- Only use `using_provider( 'ai_gateway' )` if you explicitly require the Vercel AI Gateway, otherwise provide model preferences for better ecosystem compatibility.
