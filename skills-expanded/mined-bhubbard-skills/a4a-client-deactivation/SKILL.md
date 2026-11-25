---
name: a4a-client-deactivation
description: Safely removing a site from the Automattic for Agencies dashboard. Use when handing over a site to a client or severing the agency connection.
---

# Automattic For Agencies: Deactivation & Removal

When an agency contract ends or a site is handed over completely to the client, the site should be removed from the agency's centralized A4A dashboard.

## The Removal Process
Removing a site from the agency dashboard is done directly from the client site's `wp-admin`, not from the A4A dashboard.

1. Log into the client's WordPress dashboard (`wp-admin`).
2. Navigate to **Plugins > Installed Plugins**.
3. Locate the **Automattic for Agencies Client** plugin and click **Deactivate**.
4. Confirm the prompt.

**Result**: Deactivating the plugin immediately severs the connection to WordPress.com and removes the site from the agency's A4A centralized management portal. The plugin can then be safely deleted.
