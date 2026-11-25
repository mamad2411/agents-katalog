---
name: redirection-conditional
description: Configuring conditional redirects. Use when setting up redirects based on user login status, capabilities, browsers, or cookies.
---

# Redirection: Conditional Redirects

Instead of redirecting every visitor indiscriminately, the Redirection plugin allows you to trigger redirects only when specific conditions are met.

## Available Conditions
When creating a redirect, you can click the gear icon to expose conditional logic:
- **Login Status**: Redirect only if logged in or logged out (useful for hiding pages from public view).
- **Capability**: Redirect based on WordPress user role capabilities (e.g., `edit_posts`).
- **Referrer**: Redirect users who clicked a link from a specific external site.
- **Cookies**: Trigger a redirect if a specific tracking or session cookie is set.
- **Custom Filter**: Trigger based on your own PHP filter hook.

## Troubleshooting Conditions
If a conditional redirect isn't working:
1. Ensure full-page caching (like WP Rocket, Cloudflare APO, or Varnish) isn't serving a cached version of the page before the Redirection plugin's PHP executes. Conditional redirects often fail behind edge caches.
