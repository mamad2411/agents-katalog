---
name: cloudflare-api-auth
description: Handling Cloudflare API Token authentication. Use when the plugin fails to connect or throws permission errors.
---

# Cloudflare API Authentication

To function, the Cloudflare WordPress plugin must be authenticated with the user's Cloudflare account.

## Global API Key vs. API Token
Historically, the plugin required the **Global API Key**, which gave the plugin full access to the user's entire Cloudflare account.
- **API Tokens** (Introduced later) are highly recommended. They allow scoping permissions specifically to the single domain the WordPress site operates on, and only granting necessary permissions (like Cache Purge).

## Required Token Permissions
If a user is creating a custom API token for the plugin, it needs the following permissions for the specific Zone:
- Zone.Zone: Read
- Zone.Cache Purge: Purge
- Zone.Zone Settings: Edit
- Zone.Page Rules: Edit (If managing rules via the plugin)

## Environmental Variables
For developers managing sites via code (e.g., Bedrock/Trellis setups), authentication can be hardcoded in `wp-config.php`:
```php
define( 'CLOUDFLARE_EMAIL', 'admin@example.com' );
define( 'CLOUDFLARE_API_KEY', 'your_global_api_key_here' );
```
