---
name: alttext-ai-seo-integrations
description: Guidance on integrating AltText.ai with SEO plugins and WooCommerce. Use when optimizing image alt text with focus keywords or specific product names.
---

# AltText.ai: SEO & Ecommerce Integrations

AltText.ai's primary strength is its ability to generate contextually relevant text that benefits search engine optimization.

## SEO Plugin Integration
The plugin natively hooks into popular SEO plugins (Yoast, Rank Math, All in One SEO, SEOPress, etc.). 
- When generating alt text for an image attached to a post, the AI automatically analyzes the post's **focus keyphrase** (set via the SEO plugin) and seamlessly weaves it into the generated alt text using natural language processing.

## WooCommerce (Ecommerce Vision)
If an image is uploaded and attached to a WooCommerce product, AltText.ai switches to its "Ecommerce Vision" model. 
- It evaluates the image but *specifically* injects the actual WooCommerce product name into the alt text, vastly improving image search rankings for specific store inventory.

## Custom ChatGPT Prompts
If the default generation isn't fitting the site's tone, users can supply a custom ChatGPT prompt in the plugin settings to act as a modifier for all generated alt text (e.g., "Always write the description in a humorous tone").
