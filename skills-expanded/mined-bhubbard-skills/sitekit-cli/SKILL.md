---
name: sitekit-cli
description: Using WP-CLI commands to manage Google Site Kit. Use when troubleshooting server-side connection issues or resetting the plugin.
---

# Site Kit CLI (WP-CLI)

Google Site Kit provides WP-CLI commands to assist developers with managing the plugin without needing the WordPress dashboard.

## Resetting Site Kit
If a site is stuck in a redirect loop or the OAuth token is hopelessly corrupted, the best option is a hard reset.
```bash
wp google-site-kit reset
```
*Note: This disconnects all users and removes all module settings. They will need to run the setup wizard again.*

## Viewing Status
To quickly check which modules are active and connected:
```bash
wp google-site-kit modules list
```

## Activating/Deactivating Modules
You can toggle specific modules on or off via CLI:
```bash
wp google-site-kit modules activate analytics
wp google-site-kit modules deactivate pagespeed-insights
```

## Troubleshooting
If a CLI command fails, ensure WP-CLI is running as the correct system user (`www-data` or the account owner) so it has permission to read the `wp-config.php` and database.
