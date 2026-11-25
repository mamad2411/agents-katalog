---
name: wordpress-widgets
description: WordPress classic widgets API — WP_Widget base class, register_sidebar, dynamic_sidebar, and the migration to block widgets. Use when adding a widget to a classic-PHP theme, registering custom sidebars, building a widget that pre-dates block widgets, or restoring the classic widget editor on a site that needs it. Block-based themes generally don't use widgets — they use template parts and block patterns instead.
---

# WordPress Widgets (Classic)

Widgets are reusable PHP-rendered components for sidebars: Recent Posts, Categories, custom HTML, third-party social feeds. The classic API (`WP_Widget` base class + `register_sidebar`) has been around since 2.8 and is still widely used despite WordPress 5.8's pivot to **block widgets**.

If you're working on a **block theme**, you usually don't deal with widgets at all — that role is filled by template parts, block patterns, and the Site Editor. For **classic themes** and existing widget areas, this is still the active API.

## The architecture

- A **widget** is a class extending `WP_Widget`. Multiple instances of the same widget can exist with different settings.
- A **sidebar** is a registered widget area where widgets can be placed (despite the name, they don't have to be on the side — a "sidebar" is just any drag-target).
- A theme calls `dynamic_sidebar( 'name' )` to render the contents of a sidebar in a template.

## Registering a sidebar

```php
add_action( 'widgets_init', function () {
    register_sidebar( array(
        'id'            => 'sidebar-main',
        'name'          => __( 'Main Sidebar', 'mytheme' ),
        'description'   => __( 'Shown on every page.', 'mytheme' ),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ) );

    register_sidebar( array( 'id' => 'footer-1', 'name' => __( 'Footer 1', 'mytheme' ) ) );
    register_sidebar( array( 'id' => 'footer-2', 'name' => __( 'Footer 2', 'mytheme' ) ) );
} );
```

`%1$s` becomes the widget's unique id; `%2$s` becomes the widget's CSS class. The defaults are sensible — only override if your markup needs to differ.

## Rendering in a template

```php
<?php if ( is_active_sidebar( 'sidebar-main' ) ) : ?>
    <aside class="sidebar-main">
        <?php dynamic_sidebar( 'sidebar-main' ); ?>
    </aside>
<?php endif; ?>
```

`is_active_sidebar` checks both that the sidebar is registered **and** has at least one widget assigned — common pattern so the `<aside>` doesn't render empty.

## Writing a widget — WP_Widget subclass

```php
class MyTheme_Recent_Posts_Widget extends WP_Widget {

    public function __construct() {
        parent::__construct(
            'mytheme_recent_posts',                   // ID base (unique per widget class).
            __( 'Recent Posts (MyTheme)', 'mytheme' ),
            array( 'description' => __( 'Recent posts with thumbnails.', 'mytheme' ) )
        );
    }

    // Frontend rendering for one instance.
    public function widget( $args, $instance ) {
        $title = ! empty( $instance['title'] ) ? $instance['title'] : __( 'Recent Posts', 'mytheme' );
        $count = isset( $instance['count'] ) ? (int) $instance['count'] : 5;

        echo $args['before_widget'];
        if ( $title ) {
            echo $args['before_title'] . esc_html( $title ) . $args['after_title'];
        }

        $posts = get_posts( array( 'posts_per_page' => $count ) );
        echo '<ul>';
        foreach ( $posts as $p ) {
            printf( '<li><a href="%s">%s</a></li>',
                esc_url( get_permalink( $p ) ),
                esc_html( get_the_title( $p ) )
            );
        }
        echo '</ul>';
        echo $args['after_widget'];
    }

    // Admin form.
    public function form( $instance ) {
        $title = $instance['title'] ?? '';
        $count = $instance['count'] ?? 5;
        ?>
        <p>
            <label for="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>">
                <?php esc_html_e( 'Title:', 'mytheme' ); ?>
            </label>
            <input type="text" class="widefat"
                id="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>"
                name="<?php echo esc_attr( $this->get_field_name( 'title' ) ); ?>"
                value="<?php echo esc_attr( $title ); ?>" />
        </p>
        <p>
            <label for="<?php echo esc_attr( $this->get_field_id( 'count' ) ); ?>">
                <?php esc_html_e( 'Number of posts:', 'mytheme' ); ?>
            </label>
            <input type="number" min="1" max="20"
                id="<?php echo esc_attr( $this->get_field_id( 'count' ) ); ?>"
                name="<?php echo esc_attr( $this->get_field_name( 'count' ) ); ?>"
                value="<?php echo esc_attr( $count ); ?>" />
        </p>
        <?php
    }

    // Save form values back into instance settings.
    public function update( $new_instance, $old_instance ) {
        return array(
            'title' => sanitize_text_field( $new_instance['title'] ?? '' ),
            'count' => max( 1, min( 20, (int) ( $new_instance['count'] ?? 5 ) ) ),
        );
    }
}

add_action( 'widgets_init', function () {
    register_widget( 'MyTheme_Recent_Posts_Widget' );
} );
```

Four methods to implement:

- `__construct` — register the ID base and name.
- `widget( $args, $instance )` — emit HTML for one instance.
- `form( $instance )` — admin settings form HTML.
- `update( $new_instance, $old_instance )` — sanitize and store settings.

`get_field_id()` and `get_field_name()` auto-generate prefixed `id`/`name` attrs so multiple instances don't collide.

## The 5.8 transition — block widgets

In WordPress 5.8, the Widgets admin screen and Customizer widgets panel were replaced with the **block editor**. Now:

- The "Appearance → Widgets" screen is a Gutenberg-style editor for placing **any block** (not just widgets) into sidebars.
- Legacy widgets still work — they're wrapped in a `core/legacy-widget` block.
- The Customizer widgets panel similarly uses blocks.

Most users barely notice. But for theme authors:

- Existing `WP_Widget` classes continue to function unchanged.
- New widget code should usually be **a block** instead. Same rendering, more flexibility, better authoring UX.
- Sidebars are still relevant — they're the drag targets for blocks.

## Restoring the classic widgets screen

For sites whose admins prefer the old UI:

```php
// Disable block-based widgets editor:
add_filter( 'use_widgets_block_editor', '__return_false' );

// Or specifically for the Customizer:
add_filter( 'gutenberg_use_widgets_block_editor', '__return_false' );  // Legacy filter, if Gutenberg plugin is active.
```

## Disabling widgets entirely

```php
// Hide the widgets admin menu:
add_action( 'admin_menu', function () {
    remove_submenu_page( 'themes.php', 'widgets.php' );
} );

// Unregister all sidebars:
add_action( 'widgets_init', function () {
    global $wp_registered_sidebars;
    foreach ( $wp_registered_sidebars as $sidebar_id => $sidebar ) {
        unregister_sidebar( $sidebar_id );
    }
}, 99 );
```

For block themes there's no widgets screen at all — themes that declare full-site editing don't register widget areas.

## Rendering a single widget outside a sidebar

```php
the_widget( 'MyTheme_Recent_Posts_Widget', array( 'count' => 3 ), array(
    'before_widget' => '<div class="card">',
    'after_widget'  => '</div>',
    'before_title'  => '<h3>',
    'after_title'   => '</h3>',
) );
```

Useful in custom page templates when you want widget-style components without a sidebar.

## Where to look in this codebase

- `wp-includes/widgets.php` — function API: `register_widget`, `unregister_widget`, `register_sidebar`, `register_sidebars`, `dynamic_sidebar`, `is_active_sidebar`, `is_active_widget`, `the_widget`.
- `wp-includes/class-wp-widget.php` — `WP_Widget` base class. The contract every widget implements.
- `wp-includes/class-wp-widget-factory.php` — registry of widget classes.
- `wp-includes/default-widgets.php` — bundles all the core widget classes (Search, Calendar, Recent Posts, Tag Cloud, etc.).
- `wp-includes/widgets/` — one file per built-in widget. Use as reference templates.
- `wp-admin/widgets.php` — the admin screen (which since 5.8 mostly bootstraps the block editor).

## Common pitfalls

- Echoing widget HTML without escaping the title/values. WordPress doesn't auto-escape — your `widget()` must.
- Forgetting `get_field_id()` / `get_field_name()` in `form()` — multiple instances of the same widget conflict.
- Returning `false` from `update()` to cancel a save — actually a useful feature (e.g., if validation fails), but undocumented and easy to do accidentally by forgetting the return.
- Building a new widget in 2026 when a block would do. New widget classes are mostly only needed for back-compat with users who still have widget areas configured.
- Reading user-submitted form values without sanitizing in `update()`. The values are stored raw in `wp_options`.
- Using legacy widgets inside a block theme. Block themes don't have widget areas — register a template part / block pattern instead.
- Defining sidebars with hardcoded class names that clash with block CSS (`widget`, `card`). Use namespaced classes.
- Calling `dynamic_sidebar` before `widgets_init` has fired. Always check `is_active_sidebar` first.
