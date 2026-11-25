---
name: cloudflare-apo
description: Guidance on Cloudflare Automatic Platform Optimization (APO). Use when troubleshooting edge caching of WordPress HTML or resolving APO detection issues.
---

# Cloudflare Automatic Platform Optimization (APO)

APO allows Cloudflare to cache the actual HTML of a WordPress site at their edge network, not just static assets (images, CSS, JS).

## Configuration Requirements
- APO requires the Cloudflare WordPress plugin to be installed and connected.
- It is a paid add-on ($5/mo) for Free Cloudflare plans, but included in Pro and Business plans.

## Troubleshooting APO Not Detecting Plugin
If Cloudflare reports that it cannot detect the WordPress plugin:
1. Go to the Cloudflare WordPress plugin settings.
2. Disable APO in the card, then re-enable it.
3. Clear any third-party server cache (like WP Rocket or server-side Varnish).
4. Verify that the origin server is returning the response header: `cf-edge-cache: cache,platform=wordpress`.

## Subdomains
APO supports subdomains, but ensure the Cloudflare plugin is active and authenticated on the specific subdomain installation of WordPress.
