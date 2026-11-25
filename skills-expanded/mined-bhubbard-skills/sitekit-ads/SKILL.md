---
name: sitekit-ads
description: Configuring Google Ads conversion tracking via Site Kit. Use when addressing conversion tracking tags and snippet placement for paid search campaigns.
---

# Site Kit Google Ads

While AdSense is for *making* money from ads, the Google Ads module in Site Kit is for tracking conversions from ads the user is *buying*.

## Conversion ID Configuration
Site Kit requires the user to input their Google Ads Conversion ID (e.g., `AW-123456789`).
- Once provided, Site Kit automatically places the global site tag (`gtag.js`) required for Google Ads.

## Conflict with Analytics/Tag Manager
If the user already has Google Analytics 4 connected via Site Kit, the `gtag.js` is already loaded. Site Kit intelligently routes the Ads Conversion ID through the existing `gtag` implementation to prevent duplicate scripts.
- If a user is manually injecting a Google Ads conversion script alongside Site Kit, warn them that it will cause duplicate firing and skewed conversion metrics.

## E-commerce Conversions
Site Kit handles the base global tag. For specific event tracking (e.g., a "Purchase" event in WooCommerce), the user still needs a specialized eCommerce integration, as Site Kit's basic module only establishes the connection, not specific event triggers.
