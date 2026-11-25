---
name: wordpress-script-modules
description: WordPress Script Modules API (6.5+) — native ES module enqueueing with import maps. Use when shipping modern JS as ES modules (import/export), enqueuing the Interactivity API's view modules, building blocks whose viewScriptModule is in block.json, or migrating off classic wp_enqueue_script for new code. Distinct from classic scripts — uses wp_register_script_module / wp_enqueue_script_module and emits a module-type script tag with an import map.
---

# WordPress Script Modules (6.5+)

Script Modules are a parallel-but-separate enqueueing system from classic `wp_enqueue_script`. They emit `<script type="module">` tags and a browser **import map** so ES module imports resolve to the right URLs.

This is the path forward for modern frontend JS in WordPress. The Interactivity API uses it for its view scripts. Block themes will increasingly use it for `viewScriptModule` entries in `block.json`.

## When to use modules vs classic scripts

- **Use script modules** when: shipping ES module source (`import`/`export`), the script targets a modern browser baseline, you want native browser dependency resolution.
- **Use classic scripts** when: integrating with existing jQuery/legacy code, your dep tree includes globals like `jquery`, you need IE/very-old-browser support (though IE is unsupported by WordPress core since 5.8).

The two systems can coexist on the same page. A block can have both `viewScript` (classic) and `viewScriptModule` (modules).

## Registering and enqueueing

```php
add_action( 'wp_enqueue_scripts', function () {
    wp_register_script_module(
        'myplugin/cart-widget',                        // Identifier (vendor/name).
        plugins_url( 'build/cart-widget.js', __FILE__ ),
        array(
            // Static dependency — always imported.
            '@wordpress/interactivity',
            // Or in full form with import type:
            array( 'id' => 'myplugin/api-client', 'import' => 'static' ),
            // Dynamic dependency — for import('...').then(...) only. Added to importmap but not preloaded.
            array( 'id' => 'myplugin/lazy-features', 'import' => 'dynamic' ),
        ),
        '1.0.0'
    );

    wp_enqueue_script_module( 'myplugin/cart-widget' );
} );
```

`wp_enqueue_script_module()` accepts the same args as `wp_register_script_module()`, so you can register-and-enqueue in one call when you don't need to share the registration.

## Inside the JS

Treat it as standard ES modules — the import map handles resolution:

```js
// build/cart-widget.js
import { store, getContext } from '@wordpress/interactivity';
import apiClient from 'myplugin/api-client';

store('myplugin/cart-widget', {
    actions: {
        async addItem() {
            const ctx = getContext();
            await apiClient.post('/cart/items', { id: ctx.itemId });
            ctx.itemCount += 1;
        },
    },
});
```

The bare identifier `@wordpress/interactivity` is resolved by the browser via the emitted import map — no bundler needed.

## What gets emitted

WordPress renders something like:

```html
<script type="importmap">
{
  "imports": {
    "@wordpress/interactivity": "https://example.com/wp-includes/js/dist/interactivity.min.js?ver=...",
    "myplugin/api-client":      "https://example.com/wp-content/plugins/myplugin/build/api-client.js?ver=1.0.0"
  }
}
</script>

<link rel="modulepreload" href=".../cart-widget.js" />
<link rel="modulepreload" href=".../api-client.js" />     <!-- static deps preloaded -->
<script type="module" src=".../cart-widget.js"></script>
```

Static deps get `<link rel="modulepreload">` for parallel fetch. Dynamic deps are only in the import map so `import('myplugin/lazy-features')` resolves when called.

## In block.json (the typical entry point)

A block opts into modules by declaring `viewScriptModule`:

```json
{
    "name":             "myplugin/cart-widget",
    "viewScriptModule": "file:./view.js",
    "supports":         { "interactivity": true }
}
```

`register_block_type` reads this and calls `wp_register_script_module` for the file behind the scenes. The block's `viewScriptModule` is enqueued automatically wherever the block renders.

`viewScript` (classic) and `viewScriptModule` are separate — a block can have one, the other, or both.

## Static vs dynamic imports

```js
// Static — always imported when this module loads. Preloaded by WordPress.
import { utils } from 'myplugin/utils';

// Dynamic — only fetched when the function runs.
async function loadFeatures() {
    const features = await import('myplugin/features');
    features.activate();
}
```

When you register the module, mark deps with the right `import` type:

```php
wp_register_script_module( 'myplugin/main', $url, array(
    array( 'id' => 'myplugin/utils',    'import' => 'static'  ),
    array( 'id' => 'myplugin/features', 'import' => 'dynamic' ),
) );
```

Static deps get `<link rel="modulepreload">`. Dynamic deps don't (the import is on-demand).

## Versions and cache busting

Same convention as classic scripts: pass a version string. WordPress appends `?ver=...` to the module URL and the import map entry.

```php
wp_register_script_module( 'myplugin/main', $url, $deps, '1.2.3' );
```

## fetchpriority

```php
wp_register_script_module( 'myplugin/main', $url, $deps, '1.0', array(
    'fetchpriority' => 'high',     // 'auto' (default) | 'low' | 'high'.
) );
```

Hints the browser about download priority for the `<link rel="modulepreload">` tag.

## Hooks for output ordering

`WP_Script_Modules` registers itself via `add_hooks()` on:

- `wp_head` priority 10 — prints `<link rel="modulepreload">` for static deps.
- `wp_footer` priority 10 — prints `<script type="module">` enqueues.
- `wp_head` priority 11 — prints the import map.
- `admin_print_footer_scripts` — for admin pages.

Generally you don't interact with these — but if you're debugging "my module shows up before its deps in the source," that's the hook order to inspect.

## Where to look in this codebase

- `wp-includes/class-wp-script-modules.php` — the entire `WP_Script_Modules` class. **Read this** to see exactly what's emitted, where, and in what order.
- `wp-includes/script-modules.php` (if present) or the helpers in `wp-includes/functions.wp-scripts.php` — function shims `wp_register_script_module`, `wp_enqueue_script_module`, `wp_dequeue_script_module`, `wp_deregister_script_module`.
- `wp-includes/script-loader.php` — registers core script modules (search for `wp_register_script_module`).
- `wp-includes/interactivity-api/interactivity-api.php` — uses script modules to register `@wordpress/interactivity`.

## Common pitfalls

- Mixing the classic `wp_enqueue_script` and `wp_enqueue_script_module` for the same identifier. They're separate registries — handles don't collide but you may load the same code twice.
- Registering a module with a bare URL but no `vendor/name` identifier convention. The identifier must work as an import specifier — namespaced names are required.
- Forgetting that the browser must support importmaps. All evergreen browsers do; very old ones don't. If you support pre-2023 browsers, ship a polyfill or use classic scripts.
- Using `import` syntax in a script registered with `wp_register_script` (classic). The browser will error — classic scripts are not modules. Either register as a module or transpile.
- Expecting `@wordpress/element` (React) to be importable as a module. As of 6.5+, most `@wordpress/*` packages are still classic-only. `@wordpress/interactivity` is the main module-native one. Check what's registered before depending on it.
- Forgetting to set `import => 'dynamic'` for runtime-imported modules. They get preloaded uselessly.
- Forgetting that `viewScriptModule` only loads on the frontend (where the block actually renders). The editor uses `editorScript`.
