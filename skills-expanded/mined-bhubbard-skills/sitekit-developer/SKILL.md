---
name: sitekit-developer
description: Guidance on using PHP filters and JS hooks provided by Site Kit. Use when extending or modifying the plugin's behavior via code.
---

# Site Kit Developer Hooks

Google Site Kit provides several PHP filters for developers to customize its behavior.

## Removing the Generator Tag
By default, Site Kit outputs a `<meta name="generator" content="Site Kit by Google ...">` tag.
```php
add_filter( 'googlesitekit_generator', '__return_empty_string' );
```

## Forcing Site Kit to bypass setup (Local/Staging)
```php
define( 'GOOGLESITEKIT_ENV', 'development' );
```

## Altering Script Loading
You can filter how Site Kit loads its frontend scripts (e.g., adding `defer` or `async` attributes, though Site Kit generally handles this optimally).
```php
add_filter( 'googlesitekit_script_attributes', function( $attributes, $handle ) {
    // Modify attributes based on the script $handle
    return $attributes;
}, 10, 2 );
```

## Useful Links
- [Site Kit GitHub Repository](https://github.com/google/site-kit-wp)
- Developers should reference the GitHub repo for a comprehensive list of up-to-date filters, as the plugin evolves rapidly.
