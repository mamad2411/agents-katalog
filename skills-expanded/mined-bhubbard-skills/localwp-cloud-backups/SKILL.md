---
name: localwp-cloud-backups
description: Instructions for setting up and managing LocalWP Cloud Backups to Google Drive or Dropbox.
---

# LocalWP Cloud Backups

This skill focuses on configuring and utilizing Cloud Backups in LocalWP to safely store backups of your local sites.

## Overview

LocalWP allows you to back up your local sites directly to cloud storage providers. This ensures your work is safe even if your local machine fails.

## Supported Providers

* Google Drive
* Dropbox

## Setup Instructions

1. **Connect Provider**: Go to the "Cloud Backups" add-on in LocalWP (ensure it is installed and enabled). Click "Connect" for your preferred provider and authorize Local.
2. **Configure Settings**: Choose the default backup frequency and retention policy.

## Performing Backups

### Manual Backups
You can trigger a backup at any time by selecting the site, navigating to the "Backups" tab, and clicking "Back up now".

### Restoring from a Backup
1. Go to the "Backups" tab for the specific site.
2. Select the backup you wish to restore.
3. Click "Restore to this site" or "Restore to new site".

## Best Practices

* **Regular Backups**: Get in the habit of backing up before making significant changes to a site (e.g., core updates, major plugin installations).
* **Storage Limits**: Be mindful of your cloud storage capacity, as multiple backups of large sites can consume space quickly. Use retention settings to prune old backups.
* **Test Restores**: Periodically test restoring a backup to a new site to ensure your backups are valid and complete.

## Troubleshooting

* **Authentication Issues**: If backups fail, try disconnecting and reconnecting your cloud provider account in Local.
* **Incomplete Backups**: Ensure your computer does not go to sleep during the backup process. Check the Local log files for specific error messages regarding file permissions or network timeouts.
