---
name: wordpress-customizer
description: The Theme Customizer (WP_Customize_Manager) — live-preview UI for theme settings. Use when adding theme options that need live preview (colors, fonts, header text, layout switches), when working in classic (non-block) themes that need a settings UI, when implementing selective refresh for performance, or when migrating Customizer settings to theme.json. Covers panels, sections, controls, settings, transports (refresh vs postMessage), and partial/selective refresh.
---

# WordPress Customizer (WP_Customize_Manager)

The Customizer at `/wp-admin/customize.php` is WordPress's live-preview settings UI. It hierarchy: **Panels** contain **Sections** contain **Controls**. Controls are bound to **Settings** (what gets saved). When the user drags a slider or types, the preview iframe updates live.

The Customizer is the primary settings UI for **classic themes**. Block themes mostly replace it with the Site Editor + `theme.json`, so for new block themes you generally don't add Customizer code. For classic themes (still ~half of all WordPress themes), it's the right tool.

## The shape of a Customizer registration

Everything happens on the `customize_register` action, which receives a `WP_Customize_Manager` instance:

```php
add_action( 'customize_register', function ( WP_Customize_Manager $wp_customize ) {

    // 1. (Optional) A panel groups related sections.
    $wp_customize->add_panel( 'mytheme_layout', array(
        'title'       => __( 'Layout', 'mytheme' ),
        'description' => __( 'Adjust the overall layout.', 'mytheme' ),
        'priority'    => 30,
    ) );

    // 2. A section groups related controls. (Panels are optional; sections aren't.)
    $wp_customize->add_section( 'mytheme_header_section', array(
        'title'    => __( 'Header', 'mytheme' ),
        'panel'    => 'mytheme_layout',
        'priority' => 10,
    ) );

    // 3. A setting is what gets stored. Bind it to an option or a theme_mod.
    $wp_customize->add_setting( 'mytheme_tagline_color', array(
        'default'           => '#333333',
        'type'              => 'theme_mod',           // 'theme_mod' (recommended) or 'option'.
        'capability'        => 'edit_theme_options',
        'sanitize_callback' => 'sanitize_hex_color',
        'transport'         => 'postMessage',          // 'refresh' (default) or 'postMessage' for live.
    ) );

    // 4. A control is the UI widget. It points to a setting.
    $wp_customize->add_control( new WP_Customize_Color_Control(
        $wp_customize,
        'mytheme_tagline_color',                       // Control ID — match setting ID for 1:1.
        array(
            'label'    => __( 'Tagline Color', 'mytheme' ),
            'section'  => 'mytheme_header_section',
            'settings' => 'mytheme_tagline_color',
        )
    ) );
} );
```

Use the value:

```php
$color = get_theme_mod( 'mytheme_tagline_color', '#333333' );
// Or for 'option' type:
$color = get_option( 'mytheme_tagline_color', '#333333' );
```

## theme_mod vs option

- **`theme_mod`** (recommended) — value is stored per-theme. Switching themes hides the value (it'll come back if the user returns). Use for theme-specific settings.
- **`option`** — value is stored in `wp_options` and persists across themes. Use for settings that span themes (analytics ID, business hours).

## Transports — refresh vs postMessage

The `transport` argument decides how the preview updates:

- **`refresh`** (default) — the preview iframe reloads when this setting changes. Easy but slow.
- **`postMessage`** — the change is broadcast to the preview JS, which updates the DOM live. Fast but you must write the JS.

```php
$wp_customize->add_setting( 'mytheme_tagline_color', array(
    /* ... */
    'transport' => 'postMessage',
) );

// Then enqueue a preview script that listens:
add_action( 'customize_preview_init', function () {
    wp_enqueue_script(
        'mytheme-customize-preview',
        get_template_directory_uri() . '/js/customize-preview.js',
        array( 'customize-preview' ),
        '1.0',
        true
    );
} );
```

`js/customize-preview.js`:

```js
(function ($) {
    wp.customize('mytheme_tagline_color', function (value) {
        value.bind(function (newval) {
            $('.site-tagline').css('color', newval);
        });
    });
})(jQuery);
```

## Selective refresh — the best of both

Selective refresh re-renders **just one region** of the preview when a setting changes, server-side, so the markup stays consistent without a full reload. Register a "partial":

```php
add_action( 'customize_register', function ( $wp_customize ) {
    if ( isset( $wp_customize->selective_refresh ) ) {
        $wp_customize->selective_refresh->add_partial( 'blogname', array(
            'selector'        => '.site-title a',
            'render_callback' => fn() => get_bloginfo( 'name', 'display' ),
        ) );
    }
} );
```

When the `blogname` setting changes, the Customizer asks the server to re-render `.site-title a` only.

## Built-in control types

`WP_Customize_Control` is the base. Concrete subclasses:

- `WP_Customize_Color_Control` — color picker.
- `WP_Customize_Media_Control`, `WP_Customize_Image_Control`, `WP_Customize_Cropped_Image_Control` — file uploads with media library.
- `WP_Customize_Code_Editor_Control` — CodeMirror for HTML/CSS/JS.
- `WP_Customize_Date_Time_Control` — date+time picker.
- `WP_Customize_Background_Image_Control`, `WP_Customize_Header_Image_Control` — built-in header/background.
- `WP_Customize_Nav_Menu_*` — menu management.
- `WP_Customize_New_Menu_Control`, `WP_Customize_Theme_Control`, etc.

For simple controls (`text`, `textarea`, `radio`, `select`, `checkbox`, `range`, `hidden`, `email`, `url`, `number`, `tel`, `date`), you pass `type` in the args instead of instantiating a class:

```php
$wp_customize->add_control( 'mytheme_layout_width', array(
    'type'    => 'range',
    'label'   => __( 'Layout width (px)', 'mytheme' ),
    'section' => 'mytheme_header_section',
    'input_attrs' => array( 'min' => 800, 'max' => 1600, 'step' => 50 ),
) );
```

## Sanitization is required

`sanitize_callback` on every setting. WordPress will save raw input otherwise — which is fine if the value never reaches HTML, but easy to get wrong:

```php
// String:        'sanitize_text_field'
// Email:         'sanitize_email'
// URL:           'esc_url_raw'
// Hex color:     'sanitize_hex_color'
// Integer:       'absint'
// Checkbox/bool: function ( $v ) { return (bool) $v; }
// Enum/select:   function ( $v, $setting ) {
//                    $valid = array( 'left', 'right' );
//                    return in_array( $v, $valid, true ) ? $v : $setting->default;
//                }
```

`sanitize_callback` runs on save; `validate_callback` (since 4.6) runs on the preview side and can reject input with a `WP_Error`.

## Capability

Controls require a capability to be visible. The default is `edit_theme_options`. Override per-setting for finer-grained access:

```php
'capability' => 'manage_options',
```

## Customizer for non-theme settings

Plugins can register Customizer settings too — they don't have to be theme-bound. The convention: register on `customize_register`, namespace your IDs (`myplugin_*`), and use `option` type so the value survives a theme switch.

## When to use Customizer vs Settings API vs theme.json

| Need | Use |
| --- | --- |
| Theme styling that benefits from live preview | Customizer with `theme_mod` |
| Block theme global colors/fonts/layout | `theme.json` |
| Plugin admin settings without live preview | Settings API (`register_setting`, `add_settings_field`) |
| Plugin settings that change frontend rendering | Customizer with `option` |
| Per-post settings | Post meta + meta boxes / block sidebar |

For block themes, prefer `theme.json` and Site Editor patterns. Adding Customizer panels to a block theme is rare and usually a mistake.

## Where to look in this codebase

- `wp-includes/class-wp-customize-manager.php` — the core controller, including `add_setting`, `add_section`, `add_panel`, `add_control`, `register_dynamic_settings`.
- `wp-includes/class-wp-customize-setting.php` — the setting class.
- `wp-includes/class-wp-customize-section.php`, `class-wp-customize-panel.php` — section/panel containers.
- `wp-includes/class-wp-customize-control.php` — base control class.
- `wp-includes/customize/` — all built-in control and setting subclasses.
- `wp-includes/class-wp-customize-nav-menus.php` — the nav menu integration.
- `wp-includes/class-wp-customize-widgets.php` — widget management in the Customizer.
- `wp-admin/customize.php` — the Customizer admin page.
- `wp-includes/customize-controls.php`, `customize-preview.js` — front-end JS for the parent frame and the preview iframe respectively.

## Common pitfalls

- Forgetting to provide a `sanitize_callback`. Saves still happen but with raw input — security exposure if the value is ever echoed.
- Using `transport => 'postMessage'` without writing the matching preview JS. The save works but the live preview never updates until a manual refresh.
- Mixing `theme_mod` and `option` for the same logical setting in different versions — old values get orphaned.
- Adding hundreds of controls. The Customizer JS slows down noticeably past ~50. Group with panels/sections, or split work to a dedicated settings page.
- Doing heavy work in `render_callback` for a selective-refresh partial — it runs on every interaction. Cache or short-circuit.
- Investing in the Customizer for a brand-new block theme. The block editor + theme.json + global styles is the modern path.
