---
name: unbounce-ssl-certificates
description: Managing SSL certificates for Unbounce pages. Use when an Unbounce landing page displays a "Not Secure" warning despite the WordPress site having SSL.
---

# Unbounce: SSL Certificates & Security

When an Unbounce page is published to a WordPress domain via the plugin, it relies on the WordPress server's security configurations.

## The "Not Secure" Warning
If a user visits an Unbounce landing page and the browser flags it as "Not Secure":
1. **WordPress SSL Status**: The Unbounce plugin acts as a proxy, fetching the page from Unbounce and serving it through WordPress. Therefore, the WordPress server *must* have a valid SSL certificate installed for the domain. Unbounce's own SSL certificates do not automatically cover pages served through the WordPress plugin.
2. **Mixed Content Errors**: If the WP domain has a valid SSL certificate, but the page still shows "Not Secure" or a broken padlock, inspect the page for mixed content. This occurs when an Unbounce page (served over HTTPS) loads an asset (like an image, custom web font, or third-party script) over an insecure HTTP connection. All assets referenced in the Unbounce builder must use HTTPS URLs.
