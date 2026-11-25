---
name: localwp-xdebug
description: Instructions for configuring and troubleshooting Xdebug with LocalWP for advanced debugging.
---

# LocalWP Xdebug Guide

This skill provides guidance on setting up and utilizing Xdebug within LocalWP environments.

## Features
- Enabling Xdebug in LocalWP.
- Configuring IDEs (like VS Code, PhpStorm) to listen for Xdebug connections from LocalWP.
- Troubleshooting common connection issues.

## Setup Instructions
1. Open the LocalWP application.
2. Select the site you want to debug.
3. Navigate to the **Tools** tab.
4. Ensure **Xdebug** is enabled.
5. In your IDE, set up a PHP Debug configuration listening on the appropriate port (usually 9000 or 9003).

## Best Practices
- Keep Xdebug disabled when not actively debugging to improve site performance.
- Use path mappings in your IDE to ensure breakpoints hit correctly.
