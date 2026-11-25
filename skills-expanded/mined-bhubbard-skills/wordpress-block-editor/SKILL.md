---
name: wordpress-block-editor
description: Building blocks for the Gutenberg block editor and configuring block themes via theme.json. Use when creating a custom block (block.json, edit.js, save.js, view.js, render.php), registering blocks with register_block_type, defining theme global styles in theme.json, building block patterns, working with the Interactivity API, or configuring full-site editing templates. Block themes use HTML template files in templates/ and parts/.
---

# Block Editor (Gutenberg) and Block Themes

The block editor is WordPress's content editing UI. Custom blocks let plugins and themes contribute new editing experiences. Block themes use blocks for every part of the layout (header, footer, post template) via HTML templates.

## block.json — the source of truth for a block

Every block since `apiVersion: 3` should be defined by a `block.json` file. WordPress reads it server-side (for the render callback and PHP-side enqueueing) and the editor reads it client-side (for the JS edit/save functions).

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/callout",
    "title": "Callout",
    "category": "text",
    "icon": "megaphone",
    "description": "A highlighted callout box.",
    "keywords": [ "notice", "alert" ],
    "textdomain": "my-plugin",
    "attributes": {
        "message": {
            "type": "string",
            "default": "",
            "source": "html",
            "selector": "p"
        },
        "level": {
            "type": "string",
            "default": "info",
            "enum": [ "info", "warning", "error" ]
        }
    },
    "supports": {
        "html": false,
        "anchor": true,
        "align": [ "wide", "full" ],
        "color": { "background": true, "text": true },
        "spacing": { "padding": true, "margin": [ "top", "bottom" ] },
        "typography": { "fontSize": true, "lineHeight": true }
    },
    "editorScript": "file:./index.js",
    "editorStyle":  "file:./editor.css",
    "style":        "file:./style.css",
    "viewScript":   "file:./view.js",
    "render":       "file:./render.php"
}
```

Field-by-field rules:

- `name` must be `vendor/slug` (no caps, no underscores).
- `apiVersion: 3` is current. Use it unless you have a reason not to.
- `category` is one of: `text`, `media`, `design`, `widgets`, `theme`, `embed`, or a custom one you registered.
- `attributes` describe the data the block stores. `source` + `selector` extract attributes from the saved HTML (`html`, `text`, `attribute`, `query`).
- `supports` toggle the editor controls that automatically appear (color, spacing, typography, etc.) — you don't have to implement these, the editor renders them and writes the right class names and inline styles.
- Asset paths starting with `file:./` are resolved relative to `block.json`.
- `render: file:./render.php` makes the block server-rendered — `save.js` can return `null` and the PHP file emits the final HTML.

## Registering the block (PHP side)

```php
add_action( 'init', function () {
    register_block_type( __DIR__ . '/build/callout' );
    // Where 'build/callout' contains block.json.
} );
```

`register_block_type` reads the JSON, enqueues the assets, sets up the render callback. There's also `register_block_type_from_metadata` (older alias) and `wp_register_block_metadata_collection` for plugins shipping many blocks (single-manifest performance optimization, since WP 6.7).

## The JS side — edit and save

Use the `@wordpress/scripts` package for build tooling. It wraps webpack, Babel, and the right `@wordpress/*` peer deps.

```bash
npx @wordpress/create-block my-block       # Scaffold.
npm run start                              # Watch build.
npm run build                              # Production build.
```

`src/index.js`:

```js
import { registerBlockType } from '@wordpress/blocks';
import { useBlockProps, RichText, InspectorControls } from '@wordpress/block-editor';
import { PanelBody, SelectControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';
import metadata from './block.json';

registerBlockType( metadata.name, {
    edit({ attributes, setAttributes }) {
        const blockProps = useBlockProps({ className: `is-${attributes.level}` });
        return (
            <>
                <InspectorControls>
                    <PanelBody title={__('Settings', 'my-plugin')}>
                        <SelectControl
                            label={__('Level', 'my-plugin')}
                            value={attributes.level}
                            options={[
                                { label: 'Info',    value: 'info' },
                                { label: 'Warning', value: 'warning' },
                                { label: 'Error',   value: 'error' },
                            ]}
                            onChange={(level) => setAttributes({ level })}
                        />
                    </PanelBody>
                </InspectorControls>
                <div {...blockProps}>
                    <RichText
                        tagName="p"
                        value={attributes.message}
                        onChange={(message) => setAttributes({ message })}
                        placeholder={__('Write a message…', 'my-plugin')}
                    />
                </div>
            </>
        );
    },
    save({ attributes }) {
        const blockProps = useBlockProps.save({ className: `is-${attributes.level}` });
        return (
            <div {...blockProps}>
                <RichText.Content tagName="p" value={attributes.message} />
            </div>
        );
    },
});
```

Always call `useBlockProps()` in `edit` and `useBlockProps.save()` in `save` — they wire up the wrapper element with the right classes, anchors, and `supports`-generated styles.

For dynamic/server-rendered blocks, `save` returns `null` and a `render.php` returns the markup:

```php
<?php
// render.php — receives $attributes, $content, $block.
$level = esc_attr( $attributes['level'] ?? 'info' );
$wrapper = get_block_wrapper_attributes( array( 'class' => "is-$level" ) );
?>
<div <?php echo $wrapper; ?>>
    <p><?php echo wp_kses_post( $attributes['message'] ?? '' ); ?></p>
</div>
```

`get_block_wrapper_attributes()` is the PHP counterpart to `useBlockProps()` — it emits the right class and style attrs that match what the editor previews.

## Block supports cheat sheet

These flags in `block.json` opt the block into editor UI without writing code:

- `align`: `["wide","full"]` — alignment toolbar.
- `anchor: true` — HTML anchor id field.
- `color: { text, background, link, gradients }` — color panel.
- `spacing: { margin, padding, blockGap }` — spacing controls.
- `typography: { fontSize, lineHeight, fontFamily, fontWeight, textTransform, ... }`.
- `dimensions: { aspectRatio, minHeight }`.
- `__experimentalBorder: { color, radius, style, width }` — border controls (note the `__experimental` prefix — these can change between releases).
- `interactivity: { clientNavigation: true }` — opts the block into the Interactivity API for client-side navigation.
- `html: false` — disables the "Edit as HTML" power-user option.

## theme.json — the theme manifest

For block themes, `theme.json` controls global styles, available colors, font sizes, layout widths, and which block supports are turned on. It lives at the theme root.

```json
{
    "$schema": "https://schemas.wp.org/wp/6.7/theme.json",
    "version": 3,
    "settings": {
        "appearanceTools": true,
        "color": {
            "defaultPalette": false,
            "palette": [
                { "name": "Base",     "slug": "base",     "color": "#FFFFFF" },
                { "name": "Contrast", "slug": "contrast", "color": "#111111" },
                { "name": "Accent",   "slug": "accent",   "color": "#503AA8" }
            ]
        },
        "layout": {
            "contentSize": "645px",
            "wideSize":    "1340px"
        },
        "spacing": {
            "spacingSizes": [
                { "name": "Small",   "slug": "30", "size": "30px" },
                { "name": "Regular", "slug": "50", "size": "clamp(30px, 5vw, 50px)" },
                { "name": "Large",   "slug": "60", "size": "clamp(30px, 7vw, 70px)" }
            ]
        },
        "typography": {
            "fluid": true,
            "fontSizes": [
                { "name": "Small",   "slug": "small",   "size": "0.875rem" },
                { "name": "Medium",  "slug": "medium",  "size": "1rem" },
                { "name": "Large",   "slug": "large",   "size": "clamp(1.25rem, 2vw, 1.5rem)" }
            ]
        }
    },
    "styles": {
        "color": { "background": "var(--wp--preset--color--base)", "text": "var(--wp--preset--color--contrast)" },
        "typography": { "fontFamily": "var(--wp--preset--font-family--serif)" },
        "elements": {
            "link": { "color": { "text": "var(--wp--preset--color--accent)" } },
            "h1":   { "typography": { "fontSize": "var(--wp--preset--font-size--xx-large)" } }
        },
        "blocks": {
            "core/button": {
                "color": { "background": "var(--wp--preset--color--contrast)", "text": "var(--wp--preset--color--base)" },
                "border": { "radius": "0" }
            }
        }
    }
}
```

Every preset slug becomes a CSS custom property: `palette.slug=accent` → `var(--wp--preset--color--accent)`. The editor exposes these as the user-facing palette. Always reference them by variable so user/global-styles overrides flow through.

`settings.appearanceTools: true` is a shortcut that enables many block supports at once (border, link color, lineHeight, padding/margin, etc.) — usually what you want.

## Block themes — template files

Block themes replace PHP templates with HTML files that contain block markup. Required structure:

```
my-theme/
  style.css                 — Header.
  theme.json
  templates/
    index.html              — Required fallback template.
    single.html
    archive.html
    page.html
    404.html
  parts/
    header.html
    footer.html
  patterns/
    hero.php                — Block patterns (PHP file with header + block markup).
```

Each `.html` file is just block markup. Example `templates/index.html`:

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
    <!-- wp:query {"queryId":1,"query":{"perPage":10,"postType":"post"}} -->
    <div class="wp-block-query">
        <!-- wp:post-template -->
            <!-- wp:post-title {"isLink":true} /-->
            <!-- wp:post-excerpt /-->
        <!-- /wp:post-template -->

        <!-- wp:query-pagination -->
        <div class="wp-block-query-pagination">
            <!-- wp:query-pagination-previous /-->
            <!-- wp:query-pagination-next /-->
        </div>
        <!-- /wp:query-pagination -->
    </div>
    <!-- /wp:query -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

## Block patterns

Patterns are reusable block compositions registered from PHP, JSON, or directly as PHP files in `patterns/` with a header comment block (the modern way for themes):

```php
<?php
/**
 * Title:       Two-column intro
 * Slug:        my-theme/two-column-intro
 * Categories:  text, featured
 * Description: A simple two-column intro section.
 * Keywords:    intro, hero
 * Viewport Width: 1280
 * Block Types: core/post-content
 * Post Types: post, page
 */
?>
<!-- wp:columns -->
<div class="wp-block-columns">
    <!-- wp:column --><div class="wp-block-column"><!-- wp:paragraph --><p>Left</p><!-- /wp:paragraph --></div><!-- /wp:column -->
    <!-- wp:column --><div class="wp-block-column"><!-- wp:paragraph --><p>Right</p><!-- /wp:paragraph --></div><!-- /wp:column -->
</div>
<!-- /wp:columns -->
```

WordPress auto-registers any pattern with a header in `patterns/`. The category names you put in `Categories:` must match a registered pattern category (most core ones already exist).

## Interactivity API

The current way to add front-end interactivity to blocks without bundling a heavyweight framework. Declarative attributes in HTML, behavior in a JS store.

```php
// In render.php — emit the wrapper with interactivity attributes.
<?php
$wrapper = get_block_wrapper_attributes();
?>
<div <?php echo $wrapper; ?>
     data-wp-interactive="myPlugin/counter"
     <?php echo wp_interactivity_data_wp_context( array( 'count' => 0 ) ); ?>>
    <button data-wp-on--click="actions.increment">+</button>
    <span data-wp-text="state.count"></span>
</div>
```

```js
// view.js — runs only on the frontend (NOT the editor).
import { store, getContext } from '@wordpress/interactivity';

store('myPlugin/counter', {
    actions: {
        increment() {
            const ctx = getContext();
            ctx.count += 1;
        },
    },
});
```

The Interactivity API is enabled via `supports.interactivity` in block.json. Use `viewScriptModule` (not `viewScript`) when targeting it.

## Where to look in this codebase

- `wp-includes/blocks.php` — `register_block_type`, `register_block_type_from_metadata`.
- `wp-includes/blocks/` — every core block, each in its own folder with `block.json` and `render.php`. Excellent reference: read `wp-includes/blocks/post-template/`, `wp-includes/blocks/query/`, `wp-includes/blocks/navigation/`.
- `wp-includes/block-supports/` — implementation of the `supports` flags.
- `wp-includes/class-wp-theme-json.php` — how theme.json gets parsed and merged.
- `wp-content/themes/twentytwentyfive/` — reference block theme. Look at `templates/`, `parts/`, `patterns/`, `theme.json`.

## Common pitfalls

- Forgetting `apiVersion: 3` — you'll get the old editor wrapper behavior.
- Skipping `useBlockProps()` — `supports` styles won't render, alignment classes won't appear.
- Mismatched `save` markup between deploys — Gutenberg will mark posts as "block contains invalid content" because the saved HTML no longer matches what `save` would now produce. Use server-rendered blocks (`render.php`, `save: () => null`) to avoid this entirely for dynamic content.
- Hardcoding colors instead of `var(--wp--preset--color--*)` — bypasses theme.json overrides.
- Registering blocks too early — must be on `init`.
- Forgetting `textdomain` in `block.json` — strings won't translate.
- Using `viewScript` and expecting it to load in the editor — `viewScript` is frontend-only by design. Use `editorScript`/`editorStyle` for editor-only assets.
