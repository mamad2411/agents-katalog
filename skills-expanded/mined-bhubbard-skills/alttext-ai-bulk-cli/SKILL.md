---
name: alttext-ai-bulk-cli
description: Managing bulk alt text generation and advanced image formats. Use when retroactively adding alt text to a large media library via UI or WP-CLI.
---

# AltText.ai: Bulk Operations & WP-CLI

For existing websites with thousands of images missing alt text, AltText.ai offers powerful bulk generation tools.

## Bulk Generation (UI)
You can bulk generate alt text via the Media Library dropdown or the dedicated Bulk Update tool.
- **Resiliency**: The bulk tool automatically saves progress. If it gets interrupted or times out on a slow shared host, it will resume exactly where it left off.
- **Exclusions**: You can exclude specific Post Types from having their attached images processed during bulk operations.

## Advanced Image Formats (SVG / AVIF)
AltText.ai can generate text for modern formats like SVG and AVIF, but note that these advanced image formats cost **2 API credits** per image instead of the standard 1 credit.

## WP-CLI Commands
Developers managing large sites or agency networks can automate generation from the command line:
- `wp alttext generate`: Triggers the bulk generation process via CLI, avoiding browser timeouts entirely.
- `wp alttext status`: Checks the current configuration and auto-generation state.
