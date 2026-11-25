---
name: configure-partytown
description: Use the plwwo_configuration filter to configure Partytown for Web Worker Offloading.
---

# Configure Partytown

You can customize the Partytown configuration using the `plwwo_configuration` filter.

```php
add_filter( 'plwwo_configuration', function ( $config ) {
    $config['mainWindowAccessors'][] = 'wp'; // Make the wp global available in the worker
    return $config;
} );
```

For functions (like `resolveUrl`), use an inline script:

```php
add_action( 'wp_enqueue_scripts', function () {
    wp_add_inline_script(
        'web-worker-offloading',
        "window.partytown = { ...(window.partytown || {}), resolveUrl: (url, location, type) => { return url; } };",
        'before'
    );
} );
```
