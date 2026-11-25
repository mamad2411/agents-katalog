---
name: elementor-role-manager
description: Advanced setup and configuration guidelines for Elementor Role Manager.
---

# Elementor Role Manager Guide

## Overview
This skill provides advanced configuration guidelines for the Elementor Role Manager. The Role Manager is crucial for maintaining site integrity by restricting access to the Elementor editor and specific design features based on WordPress user roles.

## Core Concepts

The Elementor Role Manager allows administrators to define what different user roles (e.g., Editors, Authors, Contributors) can do within the Elementor environment.

### Access Levels
1.  **No Access:** The user cannot access the Elementor editor at all.
2.  **Access to Edit Content Only (Elementor Pro):** The user can edit text, images, and other content within existing widgets, but cannot add, delete, or move widgets, nor can they change styling.
3.  **Full Access:** The user has complete control over the design and content.

## Best Practices for Client Handoff

When configuring a site for a client, it is essential to restrict their access to prevent accidental design breakage.

1.  **Create a 'Client' Role or Use 'Editor':** Either use the built-in Editor role or create a custom role specifically for the client.
2.  **Restrict to 'Edit Content Only':** Navigate to *Elementor > Role Manager*. For the designated client role, check the box for **"Access to edit content only"**.
3.  **Hide Unnecessary UI:** Use supplementary code or plugins to hide complex WordPress dashboard menus (like Elementor settings, Theme Builder) from the client role, keeping their workspace clean.

## Advanced Configuration

### Working with Custom Post Types (CPTs)
Ensure that Elementor is enabled for relevant CPTs (*Elementor > Settings > General*). The Role Manager settings apply across all post types where Elementor is active.

### Granular Capability Control (Beyond the UI)
While the UI provides basic control, advanced scenarios might require modifying WordPress capabilities directly via code or an advanced role editor plugin (like User Role Editor).

Elementor introduces specific capabilities:
*   `edit_posts` (Standard WP capability, required for basic editor access)
*   `elementor_edit_design` (Controls whether a user can drag/drop widgets and change styles)

**Example: Programmatically altering a role's capability (use with caution):**
```php
// Add capability to a custom role
$role = get_role( 'custom_client_role' );
if ( $role ) {
    $role->add_cap( 'elementor_edit_design' ); // Grants full design access
    // OR
    $role->remove_cap( 'elementor_edit_design' ); // Restricts to content only (if Elementor Pro is active)
}
```

## Troubleshooting Access Issues
*   **User cannot see the "Edit with Elementor" button:** Check *Elementor > Settings > General* to ensure the post type is supported. Check the Role Manager to ensure the user's role has not been explicitly excluded.
*   **User can edit design when they shouldn't:** Ensure the "Access to edit content only" box is checked for their role. Note that this feature requires Elementor Pro. If Pro is disabled, the fallback is full access.
