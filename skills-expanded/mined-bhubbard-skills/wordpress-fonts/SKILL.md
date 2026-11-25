---
name: wordpress-fonts
description: WordPress Fonts API and Font Library (6.4 / 6.5+) — register font collections, generate @font-face CSS, manage uploaded fonts in /wp-content/fonts/. Use when shipping a theme with bundled fonts, registering a hosted font collection (e.g., Google Fonts mirror), generating @font-face rules from theme.json, working with the Font Library admin UI, or moving fonts off third-party CDNs for GDPR compliance.
---

# WordPress Fonts API and Font Library

WordPress has two related-but-distinct font systems:

- **Fonts API** (6.4+) — `wp_print_font_faces()` and theme.json's `typography.fontFamilies`. Generates `@font-face` CSS at render time.
- **Font Library** (6.5+) — admin UI under Appearance → Editor → Styles for uploading and managing fonts persistently. Stored as posts in `wp_font_family` and `wp_font_face` custom post types, with files in `/wp-content/fonts/`.

Both end up emitting `@font-face` rules. The Library is the user-facing way; the Fonts API is the programmatic way.

## Defining fonts in theme.json (the modern path)

```json
{
    "$schema": "https://schemas.wp.org/wp/6.7/theme.json",
    "version": 3,
    "settings": {
        "typography": {
            "fontFamilies": [
                {
                    "fontFamily": "\"Inter\", sans-serif",
                    "name": "Inter",
                    "slug": "inter",
                    "fontFace": [
                        {
                            "fontFamily": "Inter",
                            "fontStyle": "normal",
                            "fontWeight": "400",
                            "fontDisplay": "swap",
                            "src": [ "file:./assets/fonts/Inter-Regular.woff2" ]
                        },
                        {
                            "fontFamily": "Inter",
                            "fontStyle": "normal",
                            "fontWeight": "700",
                            "src": [ "file:./assets/fonts/Inter-Bold.woff2" ]
                        }
                    ]
                }
            ]
        }
    }
}
```

`file:./` is resolved relative to the theme root. WordPress calls `wp_print_font_faces_from_style_variations()` automatically on `wp_head` and `admin_print_styles`, so the `@font-face` rules emit without any PHP from you.

The slug (`inter`) becomes `var(--wp--preset--font-family--inter)`, which you can reference in `styles` or in any CSS via global styles.

## Generating @font-face rules programmatically

For non-theme.json scenarios — a plugin shipping fonts, or a CPT that has its own typography:

```php
add_action( 'wp_head', function () {
    wp_print_font_faces( array(
        'IBM Plex Mono' => array(
            array(
                'font-family' => 'IBM Plex Mono',
                'font-style'  => 'normal',
                'font-weight' => '400',
                'font-display'=> 'swap',
                'src'         => array(
                    'file:' . plugin_dir_path( __FILE__ ) . 'fonts/IBMPlexMono-Regular.woff2',
                ),
            ),
        ),
    ) );
} );
```

`wp_print_font_faces()` emits a `<style>` block with the assembled `@font-face` rules. Use `file:` prefixes for bundled files (WordPress resolves them); use absolute URLs for CDN fonts.

## Font Library — the admin UI

In WP 6.5+, Appearance → Editor → Styles → Typography → Font Library lets admins:

- Upload `.woff`, `.woff2`, `.ttf`, `.otf` files into `/wp-content/fonts/`.
- Add fonts from registered collections (default: Google Fonts).
- Activate/deactivate fonts per-site.

Uploaded fonts become posts: a `wp_font_family` parent with `wp_font_face` children. They're queried by the Font Library admin and the global styles system.

The default font directory is `/wp-content/fonts/`. Override via filter:

```php
add_filter( 'font_dir', function ( $defaults ) {
    $defaults['basedir'] = WP_CONTENT_DIR . '/uploads/fonts';
    $defaults['baseurl'] = content_url( 'uploads/fonts' );
    $defaults['path']    = $defaults['basedir'];
    $defaults['url']     = $defaults['baseurl'];
    return $defaults;
} );
```

Or use `wp_get_font_dir()` to read the resolved location.

## Registering a font collection

A collection is a curated list of available fonts that admins can browse and add. WordPress registers a default Google Fonts collection.

```php
add_action( 'init', function () {
    wp_register_font_collection( 'my-foundry', array(
        'name'          => __( 'My Foundry Fonts', 'myplugin' ),
        'description'   => __( 'Curated typefaces from My Foundry.', 'myplugin' ),
        'font_families' => array(
            array(
                'font_family_settings' => array(
                    'fontFamily' => '"Acme Sans", sans-serif',
                    'slug'       => 'acme-sans',
                    'name'       => 'Acme Sans',
                    'fontFace'   => array(
                        array(
                            'fontFamily' => 'Acme Sans',
                            'fontStyle'  => 'normal',
                            'fontWeight' => '400',
                            'src'        => 'https://my-foundry.example.com/acme-sans-400.woff2',
                        ),
                    ),
                ),
                'categories' => array( 'sans-serif' ),
            ),
        ),
        'categories' => array(
            array( 'name' => 'Sans-Serif', 'slug' => 'sans-serif' ),
        ),
    ) );
} );

// Or point to a JSON manifest hosted elsewhere:
wp_register_font_collection( 'my-foundry', array(
    'name'        => 'My Foundry Fonts',
    'description' => 'Curated typefaces from My Foundry.',
    'src'         => 'https://my-foundry.example.com/collection.json',
) );
```

To remove the default Google Fonts collection (privacy, GDPR):

```php
add_action( 'init', function () {
    wp_unregister_font_collection( 'google-fonts' );
}, 11 );    // After 6.5's default registration on init priority 10.
```

## Disabling the Font Library entirely

```php
add_filter( 'block_editor_settings_all', function ( $settings ) {
    $settings['fontLibraryEnabled'] = false;
    return $settings;
} );
```

Useful if you want to lock typography to whatever the theme ships.

## Hosting your own Google Fonts mirror (GDPR pattern)

Modern WordPress sites often want to avoid Google Fonts CDN calls. Two common patterns:

1. **Download once, bundle in theme**: download the woff2 files, reference them via `file:` in theme.json. Zero external requests.
2. **Custom collection from your own CDN**: register a collection with `src` pointing to a JSON manifest on your own infrastructure. Admins still browse fonts but they load from your domain.

## Where to look in this codebase

- `wp-includes/fonts.php` — function API: `wp_print_font_faces`, `wp_print_font_faces_from_style_variations`, `wp_register_font_collection`, `wp_unregister_font_collection`, `wp_get_font_dir`, `wp_font_dir`.
- `wp-includes/fonts/class-wp-font-library.php` — `WP_Font_Library` (`register_font_collection`, `get_font_collections`).
- `wp-includes/fonts/class-wp-font-collection.php` — `WP_Font_Collection`.
- `wp-includes/fonts/class-wp-font-face.php` — `WP_Font_Face` (the `@font-face` CSS generator).
- `wp-includes/fonts/class-wp-font-face-resolver.php` — resolves font references in theme.json/global styles to concrete files.
- `wp-includes/fonts/class-wp-font-utils.php` — formatting helpers.
- `wp-includes/post.php` — `wp_font_family` and `wp_font_face` post types are registered around the typical CPT location.
- `wp-includes/rest-api/endpoints/class-wp-rest-font-collections-controller.php`, `class-wp-rest-font-families-controller.php`, `class-wp-rest-font-faces-controller.php` — REST endpoints powering the Font Library UI.

## Common pitfalls

- Referencing a file path that doesn't exist. WordPress silently omits the `@font-face` rule — no rendering error, just no font.
- Mixing relative `file:./` and absolute URLs in the same family. Pick one source style per family.
- Forgetting `font-display: swap`. With `auto` (default), browsers may show invisible text for 3+ seconds while fetching. `swap` shows fallback text immediately, then swaps.
- Loading multiple weights of the same family via separate `@font-face` rules with the same `font-family` string but different `font-weight`. **This is correct** — but some tools generate `font-family: 'Inter-Bold'` instead, which doesn't work for `<strong>` styling. Use one family name + multiple weights.
- Leaving the Google Fonts collection enabled while claiming GDPR compliance. Even just *registering* it doesn't leak data, but admins might add a font and trigger CDN calls. Unregister explicitly.
- Letting users upload font files without limits. Fonts can be many MB each and Font Library is unbounded by default.
