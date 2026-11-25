---
name: wordpress-interactivity-api
description: WordPress Interactivity API (6.5+) — declarative, framework-light frontend interactivity for blocks. Use when adding client-side behavior to a block (counter, toggle, AJAX form, filter UI) without bundling React/Vue/Alpine, when working with data-wp-* HTML directives, when defining a server-rendered initial state via wp_interactivity_state, or when migrating jQuery sprinkles to a proper reactive system. Covers the JS store API and the PHP integration points.
---

# WordPress Interactivity API (6.5+)

The Interactivity API is WordPress's answer to "how do blocks add frontend interactivity without each plugin bundling its own React/Vue/Alpine?" It's a small reactive runtime (powered internally by Preact signals) wired to HTML via `data-wp-*` attributes, with a JS store API on the client and PHP helpers for server-rendering initial state.

Blocks opt in via `supports.interactivity: true` in `block.json` and ship a `viewScriptModule` that registers a store. The system handles hydration, event delegation, and signal-based reactivity.

## The shape of an interactive block

Three pieces:

1. **block.json** — opts the block into interactivity and declares the view module.
2. **render.php** — emits HTML with `data-wp-*` directives, plus initial state via PHP helpers.
3. **view.js** — registers the store (actions, callbacks, derived state).

### block.json

```json
{
    "apiVersion": 3,
    "name": "myplugin/counter",
    "supports": { "interactivity": true },
    "viewScriptModule": "file:./view.js",
    "render": "file:./render.php"
}
```

### render.php

```php
<?php
// Set the initial state for this store namespace.
wp_interactivity_state( 'myplugin/counter', array(
    'count'      => 0,
    'isOpen'     => false,
    'greeting'   => __( 'Hello!', 'myplugin' ),
) );

$wrapper = get_block_wrapper_attributes();
?>
<div
    <?php echo $wrapper; ?>
    data-wp-interactive="myplugin/counter"
    <?php echo wp_interactivity_data_wp_context( array( 'count' => 0, 'label' => 'Counter A' ) ); ?>
>
    <p data-wp-text="context.label"></p>
    <button data-wp-on--click="actions.increment">+</button>
    <button data-wp-on--click="actions.decrement">-</button>
    <span data-wp-text="context.count"></span>
    <p data-wp-text="state.greeting"></p>
</div>
```

### view.js

```js
import { store, getContext } from '@wordpress/interactivity';

store('myplugin/counter', {
    state: {
        get doubled() {
            const ctx = getContext();
            return ctx.count * 2;
        },
    },
    actions: {
        increment() {
            getContext().count += 1;
        },
        decrement() {
            getContext().count -= 1;
        },
        async sync() {
            const ctx = getContext();
            const r = await fetch('/wp-json/myplugin/v1/save?count=' + ctx.count);
            // ...
        },
    },
    callbacks: {
        log() {
            // Runs whenever this block hydrates.
            console.log('Counter mounted with', getContext().count);
        },
    },
});
```

That's a fully working interactive block. No React, no bundler-required, no jQuery.

## State vs context

Two scopes:

- **state** (`wp_interactivity_state` / `state.*`) — *global* per store namespace. Shared by every instance of the block on the page.
- **context** (`data-wp-context` / `context.*`) — *per-element*. Inherits down the DOM tree. Sibling blocks have separate contexts.

Rule of thumb: use `state` for things like a global modal-open flag or settings; use `context` for per-instance data (this specific counter's count, this specific toggle's open/closed).

`wp_interactivity_data_wp_context()` is the PHP helper for emitting the encoded attribute — it handles JSON-encoding and HTML-escaping correctly. Don't hand-roll it.

## The directives

| Directive | Effect |
| --- | --- |
| `data-wp-interactive="namespace"` | Marks the root of an interactive island and selects its store. |
| `data-wp-context='{"...": "..."}'` | Per-element context object. Inherits + overrides down the tree. |
| `data-wp-bind--<attr>="state.foo"` | Bind any HTML attribute to a reactive value. `data-wp-bind--src`, `data-wp-bind--href`, etc. |
| `data-wp-class--<name>="state.foo"` | Toggle class based on truthy value. |
| `data-wp-style--<prop>="state.color"` | Set inline style property. |
| `data-wp-text="state.msg"` | Set element text content. |
| `data-wp-on--<event>="actions.foo"` | Event handler (`click`, `submit`, `input`, any DOM event). |
| `data-wp-each="state.items"` | Render a list of children, one per item. |
| `data-wp-init="callbacks.foo"` | Run a callback on mount. |
| `data-wp-watch="callbacks.foo"` | Run when any signal the callback reads changes. |
| `data-wp-key="..."` | Stable key for `data-wp-each` items. |
| `data-wp-run="callbacks.foo"` | Run on hydration (similar to init). |

## PHP integration helpers

```php
// Set or extend the global state for a namespace:
wp_interactivity_state( 'myplugin/counter', array( 'count' => 0 ) );

// Set or extend configuration (read-only client-side, accessed via getConfig()):
wp_interactivity_config( 'myplugin/counter', array(
    'apiUrl' => rest_url( 'myplugin/v1/' ),
    'nonce'  => wp_create_nonce( 'wp_rest' ),
) );

// Emit a data-wp-context attribute safely:
echo wp_interactivity_data_wp_context(
    array( 'count' => 0, 'label' => 'A' ),
    'myplugin/counter'      // Namespace (optional).
);

// Server-side process directives in already-rendered HTML (useful for pre-rendering):
$html = wp_interactivity_process_directives( $html );

// Read current context from inside a server-side render callback that's processing children:
$ctx = wp_interactivity_get_context( 'myplugin/counter' );

// Get info about the element currently being processed (advanced):
$el = wp_interactivity_get_element();
```

The whole API surface is in `wp-includes/interactivity-api/interactivity-api.php`.

## Server-side rendering with initial state

The Interactivity API pre-resolves `data-wp-text`, `data-wp-bind`, `data-wp-class`, and `data-wp-style` directives **server-side** so the initial HTML is already correct. No FOUC, no JS-required for first paint.

This is why you pass initial state from PHP: WordPress walks the DOM, sees `data-wp-text="state.greeting"`, looks up `wp_interactivity_state` for that namespace, and substitutes the text before the response goes out.

Client-side, the runtime hydrates: it attaches event handlers, sets up reactivity, and from then on updates are JS-driven.

## Client-side navigation (the speed wow)

```php
// In block.json or via filter:
"supports": {
    "interactivity": {
        "clientNavigation": true
    }
}
```

When enabled, internal link clicks are intercepted: instead of a full page reload, the Interactivity API fetches the new page, diffs the DOM, and updates only what changed. Combined with view transitions, this gives single-page-app feel with zero JS framework lock-in.

## When to use this vs a custom React block

Use Interactivity API when:

- The interaction is simple-to-medium (toggles, counters, AJAX forms, filterable lists).
- You want it to work without a build step.
- You want server-rendered initial HTML.
- You're targeting front-end (not the editor — editor is React).

Use custom React (`@wordpress/element`) when:

- You're inside the block editor (`edit.js`).
- The UI is complex (a full data grid, a drag-drop builder).
- You need React-ecosystem libraries (charts, maps, etc.).

For frontend, the Interactivity API is now the recommended path for new blocks.

## Where to look in this codebase

- `wp-includes/interactivity-api/interactivity-api.php` — function API: `wp_interactivity`, `wp_interactivity_state`, `wp_interactivity_config`, `wp_interactivity_data_wp_context`, `wp_interactivity_get_context`, `wp_interactivity_get_element`, `wp_interactivity_process_directives`.
- `wp-includes/interactivity-api/class-wp-interactivity-api.php` — `WP_Interactivity_API` (the core processor; state/config storage; directive walking).
- `wp-includes/interactivity-api/class-wp-interactivity-api-directives-processor.php` — the HTML parser that walks tags and applies directives.
- `wp-includes/blocks/` — many core blocks (`query`, `navigation`, `search`, `image`) use the Interactivity API for client navigation, lightbox, dropdowns. Read their `render.php` and `view.js`.
- The JS runtime ships as the `@wordpress/interactivity` script module, registered in `script-loader.php`.

## Common pitfalls

- Setting state in PHP but forgetting to register the store in JS. Server pre-renders correctly, but actions/callbacks never run.
- Mismatching namespaces between `data-wp-interactive`, `wp_interactivity_state`, and `store(name, ...)`. All three must match exactly.
- Mutating arrays/objects by reassignment (`ctx.list = [...ctx.list, x]`) when the runtime expects in-place mutation. Signals track in-place mutations on arrays/objects; reassigning the whole value still works but loses reference equality elsewhere.
- Forgetting `data-wp-context` on the wrapper. Without context, `context.*` directives have nothing to read.
- Putting interactive directives outside a `data-wp-interactive` element. The runtime ignores them.
- Loading view.js as a classic script. It must be a module (`viewScriptModule` in block.json).
- Trying to use the Interactivity API in the block editor (the `edit` component). It's frontend-only — use React inside the editor.
- Relying on `localStorage` for state. Fine for persistence, but state itself is the runtime's responsibility — don't hand-roll a separate reactive layer.
