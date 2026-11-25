---
name: alttext-ai-multilingual
description: Guidance on using AltText.ai in a multilingual environment. Use when configuring alt text generation for WPML or Polylang.
---

# AltText.ai: Multilingual Support

AltText.ai supports over 130 languages and integrates natively with major translation plugins like WPML and Polylang.

## How it works
When you generate alt text for an image that is part of a translated post or a translated media library entry, the plugin detects the target language (e.g., Spanish) and automatically generates the descriptive alt text in that specific language.
- It prevents double-processing (wasting API credits) on translated images during bulk generation.

## Regional Variants
For specific language sets, AltText.ai supports regional dialects. 
- **English**: American (en_US) vs British (en_GB) variants.
- **Portuguese**: Brazil (pt_BR) vs Portugal (pt_PT) variants.
- **Chinese**: Simplified (zh-Hans) vs Traditional (zh-Hant).
Ensure the correct variant is configured in `Settings > AltText.ai` so the AI outputs the correct locale formatting.
