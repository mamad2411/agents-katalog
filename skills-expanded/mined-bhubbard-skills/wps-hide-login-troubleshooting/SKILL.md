---
name: wps-hide-login-troubleshooting
description: Troubleshooting steps for recovering from a forgotten login URL or getting locked out when using the WPS Hide Login plugin.
---

# WPS Hide Login Troubleshooting Guide

Use this skill when a user is locked out of their WordPress site or has forgotten their custom login URL configured by the WPS Hide Login plugin.

## I forgot my login url!
If the user forgot their login URL, they have two options:
1. **Database Recovery:** 
   - Access the MySQL database.
   - Look for the value of the `whl_page` option in the `wp_options` table. This contains the custom login slug.
   - *Note for Multisite:* On a multisite install, the `whl_page` option might be in the `wp_sitemeta` table if it is not in the options table.

2. **Plugin Removal:**
   - Access the site via FTP or File Manager.
   - Rename or remove the `wps-hide-login` folder located in the `wp-content/plugins/` directory.
   - This will deactivate the plugin and allow login through the default `wp-login.php`.
   - After logging in, reinstall the plugin and configure a new URL.

## I'm locked out!
If the user is locked out and the above steps don't work, the issue might be related to `.htaccess` modifications from other plugins or an old WordPress MU configuration.
- Check the `.htaccess` file and compare it to a default WordPress `.htaccess` file to see if the problem originates there.

## Registration and Lost Password URLs
The default WordPress URLs (`/wp-login.php?action=register` or `/wp-login.php?action=lostpassword`) are not redirected by the plugin to avoid exposing the admin URL. 
If needed, use the custom login URL with the action appended, e.g., `/custom-login?action=register` or `/custom-login?action=lostpassword`.
