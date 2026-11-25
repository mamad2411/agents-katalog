---
name: sitekit-consent-mode
description: Managing Google Consent Mode v2 within Site Kit. Use when integrating cookie banners, addressing data privacy (GDPR/CCPA), or working with the WP Consent API.
---

# Site Kit Consent Mode

Site Kit supports Google Consent Mode out-of-the-box, ensuring that Google tags (Analytics, Ads) adjust their behavior based on user consent status.

## Enabling Consent Mode
Site Kit does not provide a cookie banner itself. Instead, it relies on standard WordPress consent plugins (like WP Cookie Notice or Complianz) or the WP Consent API.
- If the user has a supported consent plugin, Site Kit detects it and automatically configures the tags to use Consent Mode.

## Troubleshooting Consent Issues
If Analytics data drops significantly, the consent banner might be incorrectly blocking all scripts instead of utilizing Consent Mode.
- Ensure the user's cookie plugin is fully compatible with Google Consent Mode v2.
- Site Kit outputs a snippet `window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);}` with the `default` consent states before other scripts load.

## Advanced Developer Hooks
Developers can filter the consent state using the WP Consent API hooks, and Site Kit will respect those states.
