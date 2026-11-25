---
name: enable-debug-bar
description: How to enable WP_DEBUG and SAVEQUERIES for the Debug Bar plugin.
---

# Enable Debug Bar

The Debug Bar plugin provides a debug menu in the admin bar. To get the most out of it, enable `WP_DEBUG` and `SAVEQUERIES` in your `wp-config.php`:

```php
define( 'WP_DEBUG', true );
define( 'SAVEQUERIES', true );
```

This allows Debug Bar to track PHP Warnings, Notices, and MySQL queries effectively.
