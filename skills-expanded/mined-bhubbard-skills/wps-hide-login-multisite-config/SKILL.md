---
name: wps-hide-login-multisite-config
description: Instructions for configuring WPS Hide Login on WordPress Multisite networks.
---

# WPS Hide Login Multisite Configuration

Use this skill when a user is setting up or configuring the WPS Hide Login plugin on a WordPress Multisite network.

## Multisite Compatibility
WPS Hide Login is fully compatible with WordPress Multisite environments, including both subdomains and subfolders configurations.

## Configuration Options
1. **Network Activation:** 
   - Activating the plugin for the entire network allows the Super Admin to set a network-wide default login URL.
   
2. **Individual Site Settings:**
   - Even with a network-wide default set, individual site administrators can still override the setting and rename their specific site's login page to something else.

## Database Considerations
When troubleshooting or looking up the custom login URL directly in the database on a Multisite network:
- The `whl_page` option will be located in the `wp_sitemeta` table if a network-wide default is set and there is no specific option override in the individual site's options table.
