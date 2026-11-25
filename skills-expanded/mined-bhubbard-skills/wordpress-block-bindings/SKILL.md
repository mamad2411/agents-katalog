---
name: wordpress-block-bindings
description: WordPress Block Bindings API (since 6.5) — bind a block attribute (paragraph content, image src, button URL, etc.) to a dynamic data source like post meta, taxonomy data, or a custom callback. Use when you want a block to display dynamic data without writing a custom block, when surfacing post meta in editor and frontend, when implementing pattern overrides, or when building a new binding source. Covers register_block_bindings_source and the four built-in sources.
---

# Block Bindings API (WP 6.5+)

Block Bindings let you connect block attributes — paragraph text, image URLs, button targets, etc. — to dynamic data sources without writing a new block. The classic use case: a Paragraph block whose content comes from a registered post meta key, editable inline in the block editor.

It's the modern replacement for many "shortcode in a paragraph" patterns and for many cases where you'd previously have written a custom dynamic block.

## The four core built-in sources

WordPress ships with these sources registered automatically:

| Source name | What it binds to |
| --- | --- |
| `core/post-meta` | Post meta on the current post. Meta key must be registered with `show_in_rest => true`. |
| `core/post-data` | Post object fields (title, excerpt, date, etc.). |
| `core/term-data` | Term object fields, when in a term context. |
| `core/pattern-overrides` | Synced pattern overrides — one editable region inside a synced pattern. |

The bindings live in the block's `metadata.bindings` attribute, set by the editor or in pattern markup:

```html
<!-- wp:paragraph {"metadata":{"bindings":{"content":{"source":"core/post-meta","args":{"key":"book_subtitle"}}}}} -->
<p>Default text if meta is empty.</p>
<!-- /wp:paragraph -->
```

When the block renders, WordPress calls the source's `get_value_callback`, replaces the attribute, and outputs the resolved value.

## Registering post meta for bindings

To bind to `core/post-meta`, the key MUST be registered with `show_in_rest => true`:

```php
add_action( 'init', function () {
    register_post_meta( 'book', 'book_subtitle', array(
        'type'              => 'string',
        'single'            => true,
        'show_in_rest'      => true,        // Required for bindings.
        'sanitize_callback' => 'sanitize_text_field',
    ) );
} );
```

Without `show_in_rest`, `_block_bindings_post_meta_get_value()` returns null — that's a deliberate authorization check (see the source in `wp-includes/block-bindings/post-meta.php`).

## Registering a custom binding source

For data that doesn't fit post meta — derived values, external APIs, computed strings:

```php
add_action( 'init', function () {
    register_block_bindings_source( 'myplugin/weather', array(
        'label'              => __( 'Live Weather', 'myplugin' ),
        'uses_context'       => array( 'postId' ),               // Block-context keys this source needs.
        'get_value_callback' => 'myplugin_weather_binding',
    ) );
} );

/**
 * @param array    $source_args   Args from the block's metadata.bindings entry.
 * @param WP_Block $block_instance The block instance (read $block_instance->context['postId'] etc.).
 * @param string   $attribute_name The attribute being bound (e.g., 'content', 'url').
 * @return mixed                  The value to substitute, or null to use the default.
 */
function myplugin_weather_binding( array $source_args, $block_instance, string $attribute_name ) {
    $city = $source_args['city'] ?? 'San Francisco';
    $unit = $source_args['unit'] ?? 'F';
    return get_transient( "weather:$city:$unit" ) ?: '—';
}
```

Then in a pattern or block markup:

```html
<!-- wp:paragraph {"metadata":{"bindings":{"content":{"source":"myplugin/weather","args":{"city":"Brooklyn","unit":"F"}}}}} -->
<p>Loading…</p>
<!-- /wp:paragraph -->
```

## Which attributes can be bound?

Each block type declares which of its attributes are bindable. As of 6.5+:

- `core/paragraph` — `content`.
- `core/heading` — `content`.
- `core/image` — `id`, `url`, `title`, `alt`.
- `core/button` — `url`, `text`, `linkTarget`, `rel`.

To see the full current list:

```php
$attrs = get_block_bindings_supported_attributes( $block_type );
```

If you try to bind an unsupported attribute, WordPress silently ignores it.

## Pattern Overrides — the special synced-pattern source

`core/pattern-overrides` is the source that powers "synced patterns with editable areas." In the pattern definition, mark a block as overridable (`templateLock: false` + a `metadata.name`), and instances of the pattern get per-instance editable values for just that block.

This is a single-purpose source — you don't typically register your own using its mechanism. Look at `wp-includes/block-bindings/pattern-overrides.php` for the implementation.

## Editor experience

The editor renders the bound value live (read-only for `core/post-meta` of unregistered keys; editable when the meta key is registered properly). Users see a small icon on bound attributes; the underlying value can be edited inline (writing back to post meta) when permissions allow.

For custom sources, the value displays read-only — there's no general UI for editing arbitrary sources from inside the block. If you need editability, register the data as post meta and bind to `core/post-meta`.

## Use cases — when this beats a custom block

- **CPT detail fields**: a "book" CPT with title, subtitle, ISBN — bind paragraphs to meta instead of building a `<book-details>` block.
- **Author bio**: bind a Paragraph to `core/post-data` for `the_author`.
- **Dynamic CTA URLs**: bind a Button's `url` to a custom source that returns a UTM-tagged link.
- **Per-language content swap**: a source that returns the post in the current locale.

Use a custom block instead when you need bespoke editor UI, multiple coordinated outputs, or block-supports integration (color, spacing).

## Where to look in this codebase

- `wp-includes/block-bindings.php` — function API: `register_block_bindings_source`, `unregister_block_bindings_source`, `get_all_registered_block_bindings_sources`, `get_block_bindings_source`, `get_block_bindings_supported_attributes`.
- `wp-includes/class-wp-block-bindings-registry.php` — the registry.
- `wp-includes/class-wp-block-bindings-source.php` — the source instance class.
- `wp-includes/block-bindings/post-meta.php` — `core/post-meta` source. Excellent reference — has the full permission/visibility check pattern.
- `wp-includes/block-bindings/post-data.php` — `core/post-data` source (handles title, excerpt, date, etc.).
- `wp-includes/block-bindings/term-data.php` — `core/term-data` source.
- `wp-includes/block-bindings/pattern-overrides.php` — `core/pattern-overrides`.

## Common pitfalls

- Binding `core/post-meta` to a meta key that isn't `show_in_rest => true`. The source returns null silently — looks like the binding doesn't work.
- Forgetting `uses_context` when your source needs block context like `postId`. The context array on the block instance will be empty.
- Trying to bind a block attribute that isn't on the supported list (e.g., paragraph `align`). Silently ignored.
- Returning HTML from a `get_value_callback`. The value is substituted as a string — for content like a Paragraph, it's escaped/sanitized as if a user typed it. Use a custom block if you need raw HTML.
- Heavy work in `get_value_callback` on every render. Cache aggressively (transient or `wp_cache_*`).
- Permission leaks. The built-in `core/post-meta` source checks post visibility, password protection, and `is_protected_meta`. Replicate those checks in custom sources that surface user-restricted data.
- Forgetting that bindings render at both editor and frontend. Test both — same callback runs in both contexts.
