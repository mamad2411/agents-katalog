---
name: sitekit-dashboard-sharing
description: Configuring and troubleshooting Site Kit Dashboard Sharing. Use when a user wants to give Editors or Authors access to Analytics or Search Console data without full admin rights.
---

# Site Kit Dashboard Sharing

Dashboard Sharing allows Site Kit administrators to share module data with other WordPress user roles.

## Enabling Sharing
By default, only Administrators can see the Site Kit dashboard.
- Admins can go to **Site Kit > Settings > Admin Settings > Dashboard Sharing** to manage which roles (e.g., Editor, Author, Contributor) can view data for specific modules (Analytics, Search Console, etc.).

## View-Only Access
When an Editor accesses the dashboard via sharing, they are in a "view-only" state. They cannot alter module settings, disconnect services, or change configurations.
- If an Editor complains they cannot see the data, the Admin must explicitly grant them view access for *each* specific module.

## Bypassing View-Only (Multiple Admins)
If there are multiple Administrators on a site, *each* Admin must authenticate with their own Google account to gain full management access, unless Dashboard Sharing is enabled, in which case the secondary admins can simply view the data the primary admin connected.
