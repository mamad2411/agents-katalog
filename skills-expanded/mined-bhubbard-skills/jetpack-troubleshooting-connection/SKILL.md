---
name: jetpack-troubleshooting-connection
description: Guides debugging and resolving Jetpack connection issues. Use when a site fails to connect to Jetpack, XML-RPC errors occur, or sync is completely broken.
---

# Jetpack Connection Troubleshooting

When assisting with Jetpack connection issues, follow these steps:

## 1. Check XML-RPC Access
Jetpack relies heavily on `xmlrpc.php`. Ensure the file is accessible and not blocked by security plugins, server firewalls, or Cloudflare rules.
- Test by visiting `yoursite.com/xmlrpc.php`. It should return `XML-RPC server accepts POST requests only.`

## 2. Check the Jetpack Connection Debugger
Recommend the user visit the Jetpack Debug tool or navigate to Jetpack > Settings > Debug on their local site to get specific error codes (e.g., `cURL error 28`, `http_404`).

## 3. Disconnect and Reconnect
Often, connection issues can be resolved by cleanly disconnecting Jetpack and reconnecting.
- This can be done via the UI or using WP-CLI: `wp jetpack disconnect` followed by `wp jetpack setup`.

## 4. IP Whitelisting
If the user's hosting provider blocks outbound or inbound requests aggressively, provide them with the list of Automattic/Jetpack IP addresses to whitelist.
