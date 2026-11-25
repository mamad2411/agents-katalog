---
name: perflab-instant-bfcache
description: Guidance on the Instant Back/Forward (bfcache) module. Use when troubleshooting pages failing to cache in the browser or back-button navigation delays.
---

# Performance Lab: Instant Back/Forward (bfcache)

This module optimizes the site to take advantage of the browser's Back/Forward Cache (bfcache), allowing instant loading when a user uses the back or forward buttons.

## Troubleshooting bfcache Failures
Browsers will refuse to use bfcache if certain headers or states exist. This module tries to eliminate those blockers.
- **`Cache-Control: no-store`**: If a page sends this header, bfcache is disabled.
- **Unload Events**: If a theme or plugin binds to the `unload` JavaScript event, bfcache is disabled. The module attempts to mitigate this, but developers should switch to the `pagehide` event instead.

## Site Health Check
The plugin adds a Site Health check to ensure the `Cache-Control: no-store` header is not inadvertently being sent on public pages.
