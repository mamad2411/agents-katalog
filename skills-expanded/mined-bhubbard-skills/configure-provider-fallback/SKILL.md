---
name: configure-provider-fallback
description: Handle provider fallbacks using the Vercel AI Gateway in WordPress.
---

# Configure Provider Fallbacks

The Vercel AI Gateway supports automatic fallbacks during provider outages.

## Guidelines
- When building requests using `wp_ai_client_prompt`, you can supply multiple model preferences using `using_model_preference()`.
- The gateway will attempt to resolve the prompt using the first available and functioning provider/model combination in your list.

Example:
```php
$result = wp_ai_client_prompt( 'Generate a summary.' )
    ->using_model_preference( 'primary-model', 'fallback-model-1', 'fallback-model-2' )
    ->generate_text_result();
```
