---
name: callrail-wp-troubleshooting
description: "Guidelines for troubleshooting performance issues and verifying DNI for the CallRail WordPress plugin."
---

# CallRail WordPress Plugin Troubleshooting

## Performance Issues

**First-Party vs Third-Party Scripts:**
Historically, the plugin offered an option to load `swap.js` as a "first-party script" through WordPress to bypass ad-blockers. However, this relies heavily on the WordPress REST API, specifically the `/wp-json/Calltrk/v1/store` endpoint. 

*   **Symptom:** Slow server response times, high CPU load, or degraded site performance.
*   **Cause:** Frequent hits to the `/Calltrk/v1/store` REST route.
*   **Resolution:** Disable the "Enable As First Party Script" feature (if available) or circumvent the plugin entirely by directly injecting the standard `swap.js` snippet (version 11 or later) into the site header via a custom hook or Google Tag Manager.

## Validating Swap.js

If phone numbers are not swapping dynamically:
1. Ensure there are no caching plugins stripping the CallRail HTML comments or deferring the `swap.js` script incorrectly.
2. Verify that the correct API Key is saved in the database.
3. Check that the End User IP Address detection is not being masked by a CDN like Cloudflare without proper `HTTP_X_FORWARDED_FOR` headers configured.
