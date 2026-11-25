---
name: localwp-router-mode
description: Understanding and switching between Site Domains and Localhost Router Mode in LocalWP.
---

# LocalWP Router Mode Guide

This skill covers how Router Mode works in LocalWP and when to switch modes.

## Features
- **Site Domains Mode**: Uses a custom domain (e.g., `mysite.local`) and requires editing the hosts file and elevated privileges.
- **Localhost Mode**: Uses `localhost` and a random port (e.g., `localhost:10004`). Good for restrictive environments.

## Switching Modes
1. Open the LocalWP application.
2. Go to **Preferences** (or Settings).
3. Navigate to the **Advanced** tab.
4. Locate the **Router Mode** setting.
5. Choose either **Site Domains** or **Localhost**.
6. Apply changes. You may need to restart your sites.

## Best Practices
- Use Site Domains for a more realistic development environment and easier URL structures.
- Switch to Localhost Mode if you encounter continuous router errors, port conflicts, or lack administrative privileges to edit the `hosts` file.
