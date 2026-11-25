---
name: wp-importer-filters
description: Utilizing developer filters to control the WordPress Importer's behavior. Use when customizing user creation, attachment fetching, or file size limits during import.
---

# WordPress Importer: Developer Filters

The WordPress Importer provides several filters to customize its behavior programmatically without editing the core plugin files.

## Preventing User Creation
If you want to force the importer to map content only to *existing* users, preventing it from creating new user accounts based on the XML data:
```php
add_filter( 'import_allow_create_users', '__return_false' );
```

## Disabling Attachment Fetching
If you are importing post content but want to skip downloading all the attached images (which speeds up the import significantly):
```php
add_filter( 'import_allow_fetch_attachments', '__return_false' );
```

## Limiting Attachment File Size
To prevent massive files from being downloaded and clogging up the server during import, you can set a maximum byte limit:
```php
// Limit imported attachments to 2MB
add_filter( 'import_attachment_size_limit', function() {
    return 2 * 1024 * 1024; 
} );
```

## Lifecycle Hooks
- `import_start`: Fires after the file is uploaded but before processing begins.
- `import_end`: Fires when the entire import process is complete. Useful for running cleanup tasks or triggering cache purges.
