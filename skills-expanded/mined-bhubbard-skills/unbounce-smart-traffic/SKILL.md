---
name: unbounce-smart-traffic
description: Troubleshooting Unbounce Smart Traffic on WordPress. Use when AI-driven A/B testing stats fail to track conversions or load variants properly.
---

# Unbounce: Smart Traffic Tracking

Smart Traffic is Unbounce's AI-powered routing system that sends visitors to the landing page variant where they are most likely to convert.

## Compatibility with WordPress
Smart Traffic is fully compatible with WordPress domains connected via the Unbounce plugin, but it is highly susceptible to interference from WordPress performance optimization tools.

## Troubleshooting Smart Traffic
If Smart Traffic is enabled but conversions aren't tracking or the AI isn't learning:
1. **JavaScript Minification**: Ensure plugins like Autoptimize or WP Rocket are not aggressively minifying or deferring Unbounce's proprietary tracking scripts.
2. **Caching**: As with standard A/B testing, aggressive HTML caching on the server or via a plugin will prevent Smart Traffic from dynamically routing visitors. You must add the `X-Unbounce-Plugin` header to your cache exclusion list.
3. **Cookie Blockers**: Smart Traffic relies on cookies to track visitor variant exposure. Strict GDPR/cookie banner plugins that aggressively block all cookies by default may break the AI routing.
