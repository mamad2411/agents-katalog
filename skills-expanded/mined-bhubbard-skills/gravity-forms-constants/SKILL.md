---
name: gravity-forms-constants
description: "Documentation on available constants in wp-config.php."
---

# Gravity Forms Constants

Gravity Forms supports several constants that can be defined in your site's `wp-config.php` file to customize behavior globally.

## Reference
[Constants Documentation](https://docs.gravityforms.com/category/developers/php-api/constants/)

## Important Constants

### Background Processing
By default, Gravity Forms processes notifications and add-on feeds in the background using `wp-cron` to speed up form submission times for the user.
```php
// Disable background processing entirely. Feeds and notifications process synchronously during submission.
define( 'GFORM_DISABLE_ASYNC', true );
```

### Logging
Gravity Forms has a robust logging add-on. Sometimes you need to force logging via configuration.
```php
// Enable logging programmatically
define( 'GF_LOGGING_ENABLED', true );
```

### Updates and Installation
```php
// Disable automatic background updates for Gravity Forms
define( 'GFORM_DISABLE_AUTO_UPDATE', true );
```

### Script Outputs
```php
// Prevent Gravity Forms from outputting CSS
define( 'GF_DISPLAY_DISABLE_CSS', true );
```

## Best Practices
- Use `GFORM_DISABLE_ASYNC` when debugging feeds or notifications that aren't firing. If they work synchronously but fail asynchronously, the server's cron configuration is likely the issue.
