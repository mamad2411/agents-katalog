---
name: wpcom-ssh-wpcli
description: Assist users with enabling, connecting to, and using SSH and WP-CLI on WordPress.com plugin-enabled plans.
---

# WordPress.com SSH & WP-CLI

When assisting users with SSH and WP-CLI access on WordPress.com, follow these technical guidelines derived from the Developer Docs.

## Requirements

- **Plan Eligibility:** SSH and WP-CLI access are only available on plugin-enabled plans (Creator and Entrepreneur plans).
- **Activation:** SSH access must be explicitly enabled from the WordPress.com dashboard under *Settings > Hosting Configuration*.

## Connecting via SSH

1. **Locate Credentials:** Find the SSH username, hostname, and port in the *Hosting Configuration* settings.
2. **Terminal Command:** Use the standard SSH syntax:
   `ssh username@hostname -p port`
3. **Authentication:** It is highly recommended to add an SSH key to the WordPress.com dashboard for passwordless, secure authentication.

## Using WP-CLI

WordPress.com servers come pre-installed with WP-CLI, the command-line interface for WordPress.

- **Execution:** Once connected via SSH, type `wp` followed by the command (e.g., `wp plugin list`).
- **Environment Context:** Ensure commands are executed in the correct WordPress installation directory, typically `/htdocs` or `/wordpress`.
- **Permissions:** Commands should be run as the default SSH user provided by the platform. Avoid attempting root-level commands.
- **Limitations:** Some WP-CLI commands that require elevated server permissions or attempt to modify locked core files may be restricted on the managed WordPress.com environment.

## Troubleshooting

- If a connection times out, verify the port number (which may not be the standard port 22) and ensure the IP address isn't blocked.
- If WP-CLI returns memory errors, users may need to append `--memory-limit` or optimize the command execution.
