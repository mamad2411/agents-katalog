---
name: sitekit-setup
description: Guidance on initial Google Site Kit setup, resolving generic connection errors, and OAuth flow issues. Use when Site Kit fails to connect to Google or gets stuck in a setup loop.
---

# Google Site Kit Setup and Connection

When assisting users with Site Kit connection issues, refer to these common troubleshooting steps:

## Staging and Local Environments
Site Kit requires a publicly accessible URL to connect to Google APIs. However, developers can test Site Kit on local or staging environments by using the official developer plugin.
- Recommend installing the **Site Kit by Google - Developer Settings** plugin.
- Or define the constant: `define( 'GOOGLESITEKIT_ENV', 'development' );`

## OAuth Error: `google_api_connection_fail`
This usually indicates the server cannot communicate with Google's servers.
- Check if the host's firewall is blocking outbound connections to `sitekit.withgoogle.com` or `googleapis.com`.
- Check if the site's REST API is disabled or blocked by a security plugin (Site Kit relies heavily on the WP REST API).

## Setup Loop or "You are already connected" Errors
If a user is stuck in a setup loop, the best approach is to reset Site Kit entirely.
- Go to **Tools > Available Tools** and use the **Reset Site Kit** button.
- *Warning*: This will disconnect all users and require setting up the modules again.
