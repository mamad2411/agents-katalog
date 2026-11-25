---
name: unbounce-url-conflicts
description: Understanding URL routing precedence. Use when an Unbounce landing page is unexpectedly overriding a native WordPress page.
---

# Unbounce: URL Routing & Conflicts

The Unbounce plugin allows you to map custom landing pages created on their platform to specific URLs on your WordPress domain (e.g., `yourdomain.com/special-offer/`).

## URL Precedence
What happens if you have an Unbounce landing page set to `/special-offer/`, but you also create a standard WordPress Page in `wp-admin` with the exact same `/special-offer/` slug?

**The Unbounce plugin takes absolute precedence.**
When a visitor hits that URL, the plugin will intercept the request, fetch the landing page data from Unbounce's servers, and display the Unbounce page instead of the native WordPress page.

## Troubleshooting Missing Pages
If a client complains that they edited a WordPress page but the changes aren't showing on the frontend (or an entirely different design is showing), check `wp-admin > Unbounce Pages`. They likely have an active Unbounce route overriding that specific URL slug.
