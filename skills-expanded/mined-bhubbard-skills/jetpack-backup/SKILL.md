---
name: jetpack-backup
description: Information about interacting with Jetpack Backup (formerly VaultPress). Use when addressing backup exclusions, backup states, or restoration hooks.
---

# Jetpack Backup (VaultPress)

Jetpack Backup provides real-time and daily backups.

## Excluding Files or Tables from Backup
To prevent certain files, directories, or database tables from being backed up (which saves storage and bandwidth), you can use the Jetpack Backup exclusion filters.

```php
add_filter( 'jetpack_backup_exclude_files', function( $files ) {
    $files[] = 'wp-content/uploads/cache'; // Exclude a specific folder
    return $files;
} );

add_filter( 'jetpack_backup_exclude_tables', function( $tables ) {
    $tables[] = 'wp_my_temporary_log_table'; // Exclude a specific table
    return $tables;
} );
```

## Checking Backup Status
Jetpack Backup operates via SSH/SFTP or direct API access from WordPress.com. If backups are failing, the most common issue is server firewalls blocking WordPress.com IP addresses or expired SSH credentials.
