---
name: kinsta-wp-backups
description: Best practices and instructions for managing WordPress backups on Kinsta, including manual backups, automatic backups, and disaster recovery.
---

# Kinsta WordPress Backups Guide

Kinsta offers a robust backup system accessible via the MyKinsta dashboard. Understanding the different types of backups and how to use them is essential for disaster recovery and safe development practices.

## Backup Types on Kinsta

1. **Automatic Daily Backups:** Kinsta automatically backs up your WordPress site every day. These are kept for 14 days on standard plans (up to 30 days on higher plans).
2. **Manual Backups:** You can create up to 5 manual backups at any time. These are kept for 14 days. It is highly recommended to take a manual backup before updating plugins, themes, or core WordPress files.
3. **System Generated Backups:** Created automatically when certain events occur, such as a search and replace operation or pushing from staging to live.
4. **Downloadable Backups:** You can generate a `.zip` archive of your entire site (files and database) once per week.
5. **Hourly Backups (Add-on):** For highly dynamic sites, you can purchase an add-on to back up the site every 6 hours or every hour.
6. **External Backups (Add-on):** Automatically send your backups to Amazon S3 or Google Cloud Storage.

## Managing Backups in MyKinsta

Navigate to **WordPress Sites > [Site Name] > Backups** in MyKinsta to access all backup options.

### Creating a Manual Backup
1. Go to the **Manual** tab under Backups.
2. Click **Back up now**.
3. Add a descriptive note (e.g., "Before WooCommerce update") and confirm.

### Restoring a Backup
1. Find the desired backup in the list (Daily, Manual, or System generated).
2. Click the **Restore to** button next to it.
3. You can choose to restore to your **Live** environment or a **Staging** environment.
   - **Tip:** Restoring to a staging environment is safer if you are unsure of the backup's contents or simply want to retrieve a specific deleted file or database table without overwriting the live site.

### Downloading a Backup
1. Go to the **Download** tab.
2. Click **Create backup now**. It will take some time to compile the `.zip` file.
3. Once ready, you'll receive an email and a download link will appear in the dashboard. The link expires after 24 hours.

## Disaster Recovery Best Practices
- Never rely entirely on your host for backups. Use the Downloadable or External backups features to keep off-site copies.
- If your site is hacked or severely broken, restoring the latest daily backup is usually the fastest path to recovery.
