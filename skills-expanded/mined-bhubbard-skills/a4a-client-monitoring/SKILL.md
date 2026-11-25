---
name: a4a-client-monitoring
description: Understanding the monitoring capabilities of the A4A client. Use when addressing questions about downtime alerts, plugin updates, and performance tracking.
---

# Automattic For Agencies: Monitoring & Updates

The A4A client is designed to be extremely lightweight. Unlike the full Jetpack plugin which adds numerous front-end features, the A4A client solely exists to facilitate remote management.

## Remote Management Features
Once connected, the agency can perform the following from their centralized A4A dashboard (not from the client's wp-admin):
- **Bulk Plugin Updates**: Trigger plugin updates across multiple client sites simultaneously in a few clicks.
- **Downtime Monitoring**: The WordPress.com infrastructure will ping the client site periodically. If the site fails to respond, an alert is immediately sent to the agency dashboard.
- **Security & Performance**: The connection allows Automattic to scan for known vulnerabilities or severe performance degradation and notify the agency.

## Data Syncing
The plugin only syncs the minimal amount of data necessary to provide these monitoring services to the WordPress.com servers. It does not bloat the client's database with tracking metrics.
