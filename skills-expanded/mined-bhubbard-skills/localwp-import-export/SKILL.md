---
name: localwp-import-export
description: Instructions for importing and exporting sites in LocalWP, including handling archives and file exclusions.
---

# LocalWP Import & Export

This skill outlines how to export existing LocalWP sites and import sites from archives or other environments.

## Exporting a Site
Exporting a site creates a `.zip` archive containing the site's database, files, and Local configuration.

1. Right-click on the site in the LocalWP sidebar.
2. Select **Export**.
3. Choose the export location.
4. Optionally, configure **File Exclusions**. Local will automatically exclude common unnecessary files (like `.DS_Store`, `.git`, or large backup directories), but you can add your own filters to keep the archive size small.
5. Click **Export Site**.

*What's inside the export?*
- `app/public/`: The standard WordPress files, including `wp-content`.
- `app/sql/`: Database dumps (usually `.sql` files).
- `local-site.json`: Metadata about the site's PHP version, server type, etc.

## Importing a Site
You can import a previously exported Local site or a generic WordPress archive.

1. **Drag and Drop**: Simply drag the `.zip` archive into the LocalWP window.
2. **File Menu**: Go to **File > Import Site** and select the archive.
3. Name your new site and follow the prompts to complete the setup. Local will automatically provision the environment, extract files, and import the database.

### Importing Non-Local Archives
If you are importing a `.zip` that wasn't created by Local (e.g., from a client or a backup plugin):
- The archive *must* contain at minimum the `wp-content` folder and a `.sql` database dump.
- Put both at the root of the `.zip` file or inside a single folder within the zip.
- When you import, Local will download a fresh copy of WordPress core and inject your `wp-content` and database.

## Using WP Migrate
For moving sites between a live server and LocalWP, the [WP Migrate plugin](https://deliciousbrains.com/wp-migrate-db-pro/) (or similar plugins like All-in-One WP Migration or Duplicator) is highly recommended.
LocalWP includes "Local Connect" features specifically designed to push/pull to WPEngine or Flywheel directly, bypassing the manual import/export process entirely.
