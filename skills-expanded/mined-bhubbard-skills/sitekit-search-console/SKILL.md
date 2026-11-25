---
name: sitekit-search-console
description: Utilizing Google Search Console within Site Kit. Use when resolving site verification failures or property mismatch errors.
---

# Site Kit Search Console

Search Console is the foundational module of Site Kit. It must be connected before any other module.

## Verification Failures
Site Kit attempts to verify site ownership automatically via an HTML file or Meta tag placed via the REST API.
- If verification fails, it is usually due to caching plugins caching the homepage without the verification tag, or security plugins blocking the REST API.
- **Solution**: Clear all page caches and temporarily disable security plugins during setup.

## Property Mismatches
Search Console is strict about URLs. `http://example.com` and `https://example.com` are different properties.
- Ensure the WordPress Address (URL) and Site Address (URL) in WP Settings exactly match the connected Search Console property.
- If the user recently migrated to HTTPS, they must add the new HTTPS property in Search Console and reconnect Site Kit.
