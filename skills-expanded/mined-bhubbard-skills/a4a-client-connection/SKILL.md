---
name: a4a-client-connection
description: Guidance on connecting the Automattic for Agencies Client plugin. Use when troubleshooting connection errors, WordPress.com account linking, or "Identity Crisis" (IDC) issues.
---

# Automattic For Agencies: Connection Troubleshooting

The Automattic for Agencies (A4A) Client plugin acts as a bridge between the client's WordPress installation and the agency's centralized A4A dashboard.

## The Connection Process
Connection requires authenticating with a WordPress.com account.
**Crucial Requirement**: The user *must* authenticate using the exact primary WordPress.com account that was used to sign up for the Automattic for Agencies program. Using a secondary developer account will fail to link the site to the agency dashboard.

## "Linked to another user" Error
A very common issue occurs when the site was previously connected to WordPress.com/Jetpack under a different user account (e.g., the site owner's personal account).
- **The Fix**: The previous Jetpack/WP.com connection must be fully severed before the A4A client can securely take over the connection under the agency's account.

## Identity Crisis (IDC)
If the site URL changes (e.g., moving from staging to production), the plugin might trigger an Identity Crisis warning. The plugin includes an IDC revalidation tool to sync the new URL with the WordPress.com servers without losing the agency dashboard connection.
