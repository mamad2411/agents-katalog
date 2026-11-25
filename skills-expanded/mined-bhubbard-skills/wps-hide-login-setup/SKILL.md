---
name: wps-hide-login-setup
description: Instructions for installing, configuring, and safely changing the WordPress login URL using the WPS Hide Login plugin.
---

# WPS Hide Login Setup Guide

Use this skill when a user wants to install or configure the WPS Hide Login plugin to change their default WordPress login URL.

## Features
- **WPS Hide Login** is a lightweight plugin that lets you easily and safely change the URL of the login form page.
- It does not literally rename or change files in core, nor does it add rewrite rules.
- It intercepts page requests, making the `wp-admin` directory and `wp-login.php` page inaccessible.

## Setup Instructions
1. Install and activate the **WPS Hide Login** plugin from the WordPress plugin repository.
2. Go to **Settings > WPS Hide Login**.
3. Enter the desired new login slug in the **Login url** field.
4. Save the changes.
5. **CRITICAL:** Advise the user to immediately bookmark or securely store the new login URL, as the default `wp-admin` and `wp-login.php` will no longer work.

## Compatibility Notes
- Works seamlessly with BuddyPress, bbPress, Jetpack, and WPS Limit Login.
- If using a page caching plugin (other than WP Rocket), the new login URL slug MUST be added to the list of pages not to cache. WP Rocket is automatically compatible.
