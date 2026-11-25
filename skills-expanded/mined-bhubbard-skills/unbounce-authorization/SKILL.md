---
name: unbounce-authorization
description: Guidance on the Unbounce authorization process. Use when troubleshooting connection issues or domain setup between WordPress and Unbounce.
---

# Unbounce: Authorization & Domains

To use the Unbounce plugin, you must link your WordPress site to an active Unbounce account.

## The Connection Process
1. **Domain Setup**: Before authorizing the plugin, you *must* add your exact WordPress domain (e.g., `www.example.com`) as a custom domain inside your Unbounce account dashboard.
2. **Authorization**: In WordPress (`wp-admin > Unbounce Pages`), click "Authorize With Unbounce".
3. **Login**: You must log in using an Unbounce account that has access to the specific Client/Domain you just set up.

## Troubleshooting
- If the plugin fails to fetch your landing pages, confirm that the domain string added in Unbounce exactly matches your WordPress Site Address URL (including `www.` if applicable).
- The plugin utilizes server-side fetching via cURL. Ensure your server runs at least cURL 7.34.0 and OpenSSL 1.0.1+.
