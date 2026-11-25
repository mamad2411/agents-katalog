---
name: cloudflare-ssl-redirects
description: Resolving Cloudflare SSL Redirect Loops. Use when encountering "Too Many Redirects" errors (ERR_TOO_MANY_REDIRECTS) after enabling Cloudflare.
---

# Cloudflare SSL Redirect Loops

One of the most common issues when activating Cloudflare is a redirect loop on the WordPress site.

## The Cause
This happens when Cloudflare is set to "Flexible" SSL in the Cloudflare Dashboard, but WordPress is configured to use HTTPS.
1. The browser connects to Cloudflare via HTTPS.
2. Cloudflare (using Flexible SSL) connects to the WordPress server via HTTP.
3. WordPress sees an HTTP request and redirects it to HTTPS.
4. Cloudflare receives the redirect and passes it to the browser. Loop begins.

## The Solution
The Cloudflare plugin provides a built-in header rewrite feature to resolve this. By activating the plugin and logging in, it automatically sets headers so WordPress knows the original request was HTTPS.

**Alternative (Dashboard Fix)**:
Advise the user to log into `cloudflare.com` > **SSL/TLS** > **Overview** and change the encryption mode from **Flexible** to **Full (strict)**, provided their server has a valid SSL certificate.
