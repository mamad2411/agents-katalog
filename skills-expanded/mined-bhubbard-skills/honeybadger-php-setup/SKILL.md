---
name: honeybadger-php-setup
description: Setup and configure PHP error monitoring for the Honeybadger WordPress plugin.
---

# Honeybadger PHP Setup

This skill provides guidance on setting up and configuring PHP error monitoring using the Honeybadger WordPress plugin.

## Core Setup
1. Ensure the plugin is installed and activated.
2. In the WordPress admin, go to Settings -> Honeybadger.
3. Enter your Honeybadger PHP API Key.
4. Check the "PHP error reporting enabled" option.

## Advanced Configuration
Some advanced options like endpoint, environment name, and excluded exceptions need to be set manually.
Edit the file `src/honeybadger-application-monitoring.php` within the plugin directory to configure these additional parameters.

## Troubleshooting
- If errors are not reporting, ensure the API key is valid.
- Check that "PHP error reporting enabled" is checked.
- You can check the "Send test notification" option and click save to verify integration, but remember to uncheck it afterward.
