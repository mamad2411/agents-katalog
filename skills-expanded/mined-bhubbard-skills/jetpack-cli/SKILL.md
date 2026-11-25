---
name: jetpack-cli
description: Guidance for using Jetpack's WP-CLI commands. Use when interacting with Jetpack via the terminal, troubleshooting connection status, managing modules, or running sync from the command line.
---

# Jetpack CLI (WP-CLI)

Jetpack comes with built-in support for WP-CLI, allowing you to manage connections, modules, and sync directly from the command line.

## Connection Management
- `wp jetpack status`: Displays the current connection status to WordPress.com.
- `wp jetpack setup`: Initiates the connection process. It can accept tokens or credentials for headless setup.
- `wp jetpack disconnect`: Safely disconnects the site from WordPress.com. (Often useful for resolving connection glitches).

## Module Management
You can easily toggle Jetpack features without accessing the WP Admin.
- `wp jetpack module list`: Lists all available modules and their status (active/inactive).
- `wp jetpack module activate <module_slug>`: Activates a specific module (e.g., `wp jetpack module activate stats`).
- `wp jetpack module deactivate <module_slug>`: Deactivates a specific module.

## Sync Management
When debugging Jetpack Sync, it's often helpful to trigger sync operations manually.
- `wp jetpack sync status`: Shows the current queue and sync health.
- `wp jetpack sync start`: Kicks off a manual sync of the current queue.
- `wp jetpack sync force`: Forces a full sync of all data (use with caution on large sites).

## Protect (Security)
Manage the Jetpack Protect whitelist via CLI:
- `wp jetpack protect whitelist list`: View whitelisted IPs.
- `wp jetpack protect whitelist add 1.2.3.4`: Add an IP to the whitelist so it is never blocked by brute force protection.
- `wp jetpack protect whitelist remove 1.2.3.4`: Remove an IP.

## General Options
You can read or update Jetpack specific options:
- `wp jetpack options list`: List Jetpack options.
- `wp jetpack options get <option_name>`
- `wp jetpack options update <option_name> <value>`
