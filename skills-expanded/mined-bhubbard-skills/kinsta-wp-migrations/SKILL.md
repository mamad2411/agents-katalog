---
name: kinsta-wp-migrations
description: Instructions for migrating WordPress sites to Kinsta, covering Kinsta's migration service, manual migrations, and checking sites before pointing DNS.
---

# Kinsta WordPress Migrations Guide

Moving a WordPress site to Kinsta can be handled in a few different ways. This guide outlines the processes available through MyKinsta and best practices for a smooth transition.

## 1. Kinsta's Basic Migration Service (Free)
Kinsta offers free basic migrations from any host.
- **How to Request:** In MyKinsta, go to **Migrations** in the left sidebar and click **Request Migration**.
- **Requirements:** You will need to provide your current host's login credentials (cPanel, FTP, or custom dashboard login) and WordPress admin credentials.
- **Process:** Kinsta's migration team handles the entire process. You will be notified via the dashboard when it is complete.

## 2. Using the Migrate Guru Plugin
If you prefer not to share hosting credentials, or want to do it yourself easily, Kinsta recommends the Migrate Guru plugin.
- **Setup:** Create a new site in MyKinsta first.
- **Plugin:** Install Migrate Guru on the *source* site.
- **Execution:** Select Kinsta from the host list in Migrate Guru, provide your destination site URL, SFTP details (found in MyKinsta > WordPress Sites > [Site Name] > Info), and start the migration.

## 3. Manual Migration
For advanced users or complex sites, a manual migration involves moving files and the database yourself.
1. **Create Site:** Add a new site in MyKinsta.
2. **Export Database:** Export your database from the source host as a `.sql` file.
3. **Download Files:** Use FTP/SFTP to download the `wp-content` folder from the source host.
4. **Upload to Kinsta:** Use SFTP to connect to Kinsta and upload the `wp-content` folder.
5. **Import Database:** Use phpMyAdmin in MyKinsta (under **WordPress Sites > [Site Name] > Info**) to import the `.sql` file.
6. **Search & Replace:** Use the Search and Replace tool in MyKinsta (**Tools** tab) to update any hardcoded URLs from the live domain to the Kinsta temporary URL (if testing first) or ensure https is updated.

## Testing Your Migrated Site
*Crucial Step:* Always test the migrated site *before* pointing your live domain's DNS to Kinsta.
- **Site Preview Tool:** The easiest way to test. Go to **WordPress Sites > [Site Name] > Tools > Site Preview**. Click **Enable**. This allows you to browse the site exactly as it looks on Kinsta without changing DNS or editing your local hosts file. The preview link is active for a limited time.
- **Alternative (Hosts File):** You can edit your local machine's `hosts` file to point the live domain to Kinsta's IP address. This is a more advanced but highly reliable testing method.

## Going Live
Once testing is successful, point your domain's DNS A Record to your new Kinsta IP address, or update the nameservers if using Kinsta's DNS. Clear all caches (Server and Edge) after DNS propagates.
