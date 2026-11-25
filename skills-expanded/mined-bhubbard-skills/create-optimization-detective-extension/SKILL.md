---
name: create-optimization-detective-extension
description: Scaffold an extension or hook into Optimization Detective's client-side module lifecycle.
---

# Create Optimization Detective Extension

Optimization Detective acts as a framework that collects data and relies on extensions (like Image Prioritizer or Embed Optimizer) to implement actual loading optimizations.

## Client-Side Extensions

Optimization Detective supports client-side extensions via script modules.

1. **Hooking into `od_init`**: Use the `od_init` action to enqueue your extension's logic alongside the detection module.
2. **JavaScript API**: Optimization Detective exposes lifecycle hooks such as `onTTFB`, `onFCP`, `onLCP`, `onINP`, and `onCLS` from `web-vitals.js` to extension JS modules via arguments in their `initialize` functions.

### Example Plugin Registration (PHP)

```php
add_action( 'od_init', function() {
    wp_enqueue_script_module(
        'my-od-extension',
        plugins_url( 'assets/extension.js', __FILE__ ),
        array( 'optimization-detective' ),
        '1.0.0'
    );
} );
```

### Example Extension (JS)

```javascript
export function initialize( { onLCP, isDebug, log } ) {
    onLCP( ( metric ) => {
        if ( isDebug ) {
            log( 'LCP Element:', metric.entries[0].element );
        }
        // Handle custom optimization data collection
    } );
}
```
