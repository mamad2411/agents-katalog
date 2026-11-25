---
name: localwp-blueprints
description: Guide to creating, using, and managing Blueprints in LocalWP to streamline new site creation.
---

# LocalWP Blueprints

Blueprints allow you to save a snapshot of a site—including its active theme, plugins, and configuration—and use it as a template for quickly spinning up new sites.

## 1. When to Use Blueprints
- **Standardized Starter Kits**: If you always install the same 5 plugins and a specific starter theme, save that as a blueprint.
- **Client Base Sites**: Create a customized environment tailored for a specific client or project type.
- **Testing Environments**: Save a fresh install configured with dummy content (like the WP Theme Test Data) to easily reset your testing environment.

## 2. Creating a Blueprint
1. Set up a site in Local exactly how you want your template to be. Install your theme, configure settings, and install/activate plugins.
2. Ensure the site is **Running**.
3. Right-click the site in the left sidebar.
4. Select **Save as Blueprint**.
5. Give the blueprint a descriptive name (e.g., "WooCommerce Starter", "ACF + Tailwind Theme") and specify the PHP/MySQL versions.
6. Click **Save Blueprint**.

## 3. Creating a Site from a Blueprint
1. Click the **+** (Add Local Site) button in the bottom left corner.
2. Select **Create from a Blueprint**.
3. Choose the desired blueprint from the dropdown menu.
4. Proceed with naming the new site. Local will clone the blueprint's files and database into the new site environment.

## 4. Managing Blueprints
You can manage your existing blueprints in the Local Preferences.
1. Open **Preferences** (Local > Preferences or the hamburger menu).
2. Navigate to the **Blueprints** tab.
3. Here you can see all saved blueprints, view their PHP/server environment details, rename them, or delete ones you no longer need.

## 5. Updating a Blueprint
Blueprints are static snapshots. To "update" a blueprint (e.g., to update core or plugins):
1. Create a new site from the existing blueprint.
2. Perform the necessary updates on the new site.
3. Save the updated site as a new blueprint.
4. Delete the old blueprint from Preferences to keep things tidy.
