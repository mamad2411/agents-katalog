---
name: localwp-wp-cli
description: Best practices and commands for utilizing WP-CLI within LocalWP sites.
---

# LocalWP WP-CLI Guide

This skill provides advanced workflows for using WP-CLI in your LocalWP sites.

## Features
- Accessing the site shell via LocalWP.
- Managing themes, plugins, and users from the command line.
- Automating site setup tasks.

## Setup Instructions
1. Open the LocalWP application.
2. Right-click on your site and select **Open Site Shell**.
3. You will be dropped into a terminal with `wp-cli` available and pre-configured for that specific site.

## Useful Commands
- `wp plugin install query-monitor --activate`
- `wp theme list`
- `wp search-replace 'http://oldsite.local' 'http://newsite.local'`

## Best Practices
- Use `wp search-replace` carefully when migrating databases.
- Automate repetitive tasks using bash scripts that call WP-CLI commands.
