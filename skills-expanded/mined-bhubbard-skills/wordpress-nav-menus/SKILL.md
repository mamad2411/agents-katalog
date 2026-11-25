---
name: wordpress-nav-menus
description: WordPress navigation menus (classic) — register_nav_menus, wp_nav_menu, menu locations, custom walkers, programmatic menu creation. Use when adding menu locations to a classic theme, rendering menus in templates, customizing menu HTML via a Walker_Nav_Menu subclass, querying menu items programmatically, or working with menu item meta. Block themes use the core/navigation block instead of these APIs.
---

# WordPress Navigation Menus

The classic Nav Menus system (since 3.0) lets users build menus in Appearance → Menus and assign them to **menu locations** registered by the theme. The theme calls `wp_nav_menu()` in a template, passing the location, and gets back rendered `<ul>` markup.

For **block themes**, this whole system is replaced by the `core/navigation` block (with its own block-specific menu storage). For **classic themes** and many existing block themes that still use header/footer.php, the API below is the canonical way.

## Registering locations

```php
add_action( 'after_setup_theme', function () {
    register_nav_menus( array(
        'primary'   => __( 'Primary Menu',  'mytheme' ),
        'footer'    => __( 'Footer Menu',   'mytheme' ),
        'social'    => __( 'Social Links',  'mytheme' ),
    ) );
} );
```

This makes those slots appear in Appearance → Menus → "Menu Settings" → "Display location" checkboxes. The admin assigns an existing menu to each location.

## Rendering a menu in a template

```php
<?php if ( has_nav_menu( 'primary' ) ) : ?>
    <nav class="primary-nav" aria-label="<?php esc_attr_e( 'Main navigation', 'mytheme' ); ?>">
        <?php
        wp_nav_menu( array(
            'theme_location'  => 'primary',
            'menu_id'         => 'primary-menu',
            'menu_class'      => 'nav-list',
            'container'       => false,        // Wrap each menu in a div? false = no wrapper.
            'depth'           => 2,            // Max nesting depth. 0 = unlimited.
            'fallback_cb'     => 'mytheme_no_menu_fallback',  // What to show if no menu is assigned.
            'walker'          => new MyTheme_Nav_Walker(),    // Optional custom walker.
        ) );
        ?>
    </nav>
<?php endif; ?>
```

`has_nav_menu( 'primary' )` returns true only when a menu has been **assigned to that location** in the admin (not just that the location was registered).

## All wp_nav_menu args

```php
$defaults = array(
    'menu'                 => '',         // Menu ID, slug, or name.
    'menu_class'           => 'menu',     // CSS class on the <ul>.
    'menu_id'              => '',         // ID on the <ul>. Defaults to <slug>-menu.
    'container'            => 'div',      // Outer tag, or false for none.
    'container_class'      => '',
    'container_id'         => '',
    'container_aria_label' => '',
    'fallback_cb'          => 'wp_page_menu',   // What to call if no menu assigned.
    'before'               => '',         // Before each <a>.
    'after'                => '',         // After each <a>.
    'link_before'          => '',         // Before <a> text.
    'link_after'           => '',         // After <a> text.
    'echo'                 => true,       // Echo vs return string.
    'depth'                => 0,          // 0 = unlimited.
    'walker'               => '',         // Walker_Nav_Menu instance.
    'theme_location'       => '',         // The registered location slug.
    'items_wrap'           => '<ul id="%1$s" class="%2$s">%3$s</ul>',
    'item_spacing'         => 'preserve', // 'preserve' or 'discard' whitespace between items.
);
```

The `items_wrap` tokens are: `%1$s` = id, `%2$s` = class, `%3$s` = the `<li>` items.

## Querying menu items programmatically

Menus are stored as a custom taxonomy (`nav_menu`) and menu items are a CPT (`nav_menu_item`) — making `wp_get_nav_menu_items` the canonical query:

```php
$location_name = 'primary';
$locations     = get_nav_menu_locations();
if ( isset( $locations[ $location_name ] ) ) {
    $menu_id    = $locations[ $location_name ];
    $menu_items = wp_get_nav_menu_items( $menu_id );

    foreach ( $menu_items as $item ) {
        // $item is a WP_Post-like stdClass with menu_item_parent, type, object_id, url, title, ...
    }
}
```

Each item has:

- `ID` — menu item post ID.
- `menu_item_parent` — parent menu item ID (0 = top-level).
- `type` — `'post_type'` | `'taxonomy'` | `'custom'`.
- `object` — post type name, taxonomy name, or `'custom'`.
- `object_id` — the linked post/term ID.
- `url`, `title`, `description`, `target`, `xfn`, `classes`, `attr_title`.

## Creating menus programmatically

```php
$menu_id = wp_create_nav_menu( 'My Menu' );

wp_update_nav_menu_item( $menu_id, 0, array(
    'menu-item-title'     => 'Home',
    'menu-item-url'       => home_url( '/' ),
    'menu-item-status'    => 'publish',
    'menu-item-type'      => 'custom',
) );

wp_update_nav_menu_item( $menu_id, 0, array(
    'menu-item-title'     => 'About',
    'menu-item-object'    => 'page',
    'menu-item-object-id' => $about_page_id,
    'menu-item-type'      => 'post_type',
    'menu-item-status'    => 'publish',
) );

// Assign to a location:
$locations = get_theme_mod( 'nav_menu_locations' );
$locations['primary'] = $menu_id;
set_theme_mod( 'nav_menu_locations', $locations );
```

Useful for theme demo content imports or migrations.

## Custom walker — the most common customization

To control the per-item HTML, subclass `Walker_Nav_Menu`:

```php
class MyTheme_Nav_Walker extends Walker_Nav_Menu {

    // Wrap each <li>.
    public function start_el( &$output, $item, $depth = 0, $args = null, $id = 0 ) {
        $classes = empty( $item->classes ) ? array() : (array) $item->classes;
        $classes[] = 'menu-item-' . $item->ID;

        $class_names = join( ' ', apply_filters( 'nav_menu_css_class', array_filter( $classes ), $item, $args, $depth ) );
        $class_attr  = $class_names ? ' class="' . esc_attr( $class_names ) . '"' : '';

        $output .= '<li' . $class_attr . '>';

        $atts = array(
            'title'  => ! empty( $item->attr_title ) ? $item->attr_title : '',
            'target' => ! empty( $item->target )     ? $item->target     : '',
            'rel'    => ! empty( $item->xfn )        ? $item->xfn        : '',
            'href'   => ! empty( $item->url )        ? $item->url        : '',
        );
        $atts = apply_filters( 'nav_menu_link_attributes', $atts, $item, $args, $depth );

        $attr_str = '';
        foreach ( $atts as $key => $val ) {
            if ( $val ) {
                $attr_str .= ' ' . $key . '="' . esc_attr( $val ) . '"';
            }
        }

        $output .= '<a' . $attr_str . '>';
        $output .= $args->link_before . esc_html( $item->title ) . $args->link_after;
        $output .= '</a>';
    }

    // Wrap each submenu <ul>.
    public function start_lvl( &$output, $depth = 0, $args = null ) {
        $indent  = str_repeat( "\t", $depth );
        $output .= "\n$indent<ul class=\"sub-menu depth-" . ( $depth + 1 ) . "\">\n";
    }
}
```

(See the `wordpress-walker` skill for more on the walker pattern.)

## Block themes — the navigation block

In a block theme, the typical pattern is:

```html
<!-- wp:navigation {"ref":42} /-->
```

Where `42` is a `wp_navigation` post type ID (a different storage layer from classic menus, just to be confusing). The `core/navigation` block has its own admin UI inside the Site Editor.

If you need to migrate classic menus to navigation blocks, look at `wp-includes/blocks/navigation/` and the `wp_navigation` post type registration. For most plugins, the classic API still works alongside.

## Where to look in this codebase

- `wp-includes/nav-menu.php` — function API: `register_nav_menus`, `register_nav_menu`, `has_nav_menu`, `wp_create_nav_menu`, `wp_update_nav_menu_item`, `wp_get_nav_menu_items`, `wp_delete_nav_menu`, `get_registered_nav_menus`, `get_nav_menu_locations`.
- `wp-includes/nav-menu-template.php` — `wp_nav_menu`, `wp_page_menu` (fallback for "no menu assigned"), filters around menu rendering.
- `wp-includes/class-walker-nav-menu.php` — `Walker_Nav_Menu` (the default walker).
- `wp-includes/class-wp-customize-nav-menus.php` and the various `class-wp-customize-nav-menu-*.php` — Customizer integration.
- `wp-includes/blocks/navigation/` — the block-theme replacement.

## Common pitfalls

- Calling `wp_nav_menu` without a fallback. If no menu is assigned, default fallback is `wp_page_menu` which lists every page on the site — often surprising.
- Using `register_nav_menu` (singular) and `register_nav_menus` (plural) — both work, but they take different arg shapes. The singular takes `(location, description)`, the plural takes `array( location => description )`.
- Forgetting that `theme_location` is a stable identifier; users can change which menu is at that location anytime. Never key code off menu ID directly.
- Custom walker that doesn't honor `walker_nav_menu_start_el` and related filters — third-party plugins (mega menus, badges) break.
- Querying menus via `WP_Query` on `nav_menu_item` post type and missing `nopaging => true` — get truncated results.
- Building a custom navigation block in 2026 instead of customizing the `core/navigation` block. Usually a mistake — the core block is extensible.
- Hardcoding menu IDs in templates. Always go through `get_nav_menu_locations()`.
- Letting menu item titles render unescaped because the admin can include HTML. Always `esc_html` in walker output.
