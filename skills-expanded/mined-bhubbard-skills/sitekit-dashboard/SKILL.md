---
name: sitekit-dashboard
description: Troubleshooting issues within the Site Kit dashboard interface. Use when the dashboard fails to load, shows "Data error", or conflicts with other admin scripts.
---

# Site Kit Dashboard Troubleshooting

The Site Kit dashboard relies heavily on React and the WordPress REST API to fetch and display data.

## "Data error in Site Kit"
This error usually means the REST API request failed.
1. Check the browser's developer console for 403 Forbidden or 500 Internal Server Errors.
2. Ensure security plugins (like Wordfence or iThemes Security) aren't blocking `/wp-json/google-site-kit/`.
3. Check for overly aggressive caching that might be caching REST API responses.

## Blank Dashboard
A completely blank dashboard almost always indicates a JavaScript conflict in the WordPress admin.
- Another plugin might be loading an outdated version of React, conflicting with Site Kit's React bundle.
- Suggest using the **Health Check & Troubleshooting** plugin to disable all other plugins for the admin user to isolate the conflict.

## Dashboard Widgets
Site Kit registers its own dashboard widgets on the main WP admin dashboard. If a user wants to hide these to clean up the UI, they can use the standard WordPress "Screen Options" tab at the top right of the screen.
