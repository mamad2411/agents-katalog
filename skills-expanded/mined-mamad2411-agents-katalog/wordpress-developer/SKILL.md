---
name: wordpress-developer
description: "Develop professional WordPress sites, custom themes, and plugins. Covers WordPress best practices, hooks system, custom post types, WP REST API, and security."
category: php-frameworks
tags: ['wordpress', 'php', 'cms', 'plugins', 'themes']
complexity: intermediate
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# WordPress Developer

## Purpose
Build professional, secure, and performant WordPress solutions using modern development practices.

## Operating Mode
You are a **WordPress professional developer**. You write secure, standards-compliant WordPress code using hooks, custom post types, and the WP REST API.

## The Process

### 1️⃣ WordPress Architecture
```
wp-content/
├── themes/
│   └── my-theme/
│       ├── functions.php      # Theme setup, hooks, includes
│       ├── style.css          # Theme header + main styles
│       ├── index.php
│       ├── header.php
│       ├── footer.php
│       ├── inc/
│       │   ├── post-types.php
│       │   ├── taxonomies.php
│       │   └── api-endpoints.php
│       └── template-parts/
└── plugins/
    └── my-plugin/
        ├── my-plugin.php      # Plugin header
        ├── includes/
        └── admin/
```

### 2️⃣ Custom Post Types
```php
// inc/post-types.php
function register_product_post_type(): void {
    register_post_type('product', [
        'labels' => [
            'name'          => __('Products', 'textdomain'),
            'singular_name' => __('Product', 'textdomain'),
        ],
        'public'       => true,
        'has_archive'  => true,
        'rewrite'      => ['slug' => 'products'],
        'supports'     => ['title', 'editor', 'thumbnail', 'custom-fields'],
        'show_in_rest' => true,  // Enable Gutenberg + REST API
        'menu_icon'    => 'dashicons-cart',
    ]);
}
add_action('init', 'register_product_post_type');

// Custom Meta Box
function add_product_meta_box(): void {
    add_meta_box('product_details', 'Product Details', 'render_product_meta_box', 'product');
}
add_action('add_meta_boxes', 'add_product_meta_box');

function save_product_meta_box(int $post_id): void {
    if (!isset($_POST['product_nonce'])) return;
    if (!wp_verify_nonce($_POST['product_nonce'], 'save_product')) return;
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;

    if (isset($_POST['product_price'])) {
        update_post_meta($post_id, '_product_price', sanitize_text_field($_POST['product_price']));
    }
}
add_action('save_post_product', 'save_product_meta_box');
```

### 3️⃣ Hooks & Filters
```php
// Actions (do something)
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style('theme-style', get_stylesheet_uri(), [], '1.0.0');
    wp_enqueue_script('theme-js', get_template_directory_uri() . '/js/main.js', ['jquery'], '1.0.0', true);
    
    // Pass PHP data to JS
    wp_localize_script('theme-js', 'themeData', [
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'nonce'   => wp_create_nonce('theme_nonce'),
    ]);
});

// Filters (modify data)
add_filter('the_content', function(string $content): string {
    if (is_single() && get_post_type() === 'product') {
        $price = get_post_meta(get_the_ID(), '_product_price', true);
        return $content . '<p class="price">Price: $' . esc_html($price) . '</p>';
    }
    return $content;
});

// Custom WP Query
$products = new WP_Query([
    'post_type'      => 'product',
    'posts_per_page' => 12,
    'meta_query'     => [
        ['key' => '_featured', 'value' => '1', 'compare' => '='],
    ],
    'orderby'        => 'meta_value_num',
    'meta_key'       => '_product_price',
    'order'          => 'ASC',
]);
```

### 4️⃣ WP REST API Extensions
```php
// Register custom endpoint
add_action('rest_api_init', function() {
    register_rest_route('my-api/v1', '/products', [
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => 'get_featured_products',
        'permission_callback' => '__return_true',
        'args'                => [
            'per_page' => ['default' => 10, 'sanitize_callback' => 'absint'],
        ],
    ]);
});

function get_featured_products(WP_REST_Request $request): WP_REST_Response {
    $products = get_posts([
        'post_type'      => 'product',
        'posts_per_page' => $request->get_param('per_page'),
    ]);

    $data = array_map(fn($post) => [
        'id'    => $post->ID,
        'title' => $post->post_title,
        'price' => get_post_meta($post->ID, '_product_price', true),
        'image' => get_the_post_thumbnail_url($post->ID, 'medium'),
    ], $products);

    return new WP_REST_Response($data, 200);
}
```

### 5️⃣ Security Essentials
```php
// Always sanitize inputs
$name = sanitize_text_field($_POST['name']);
$email = sanitize_email($_POST['email']);
$content = wp_kses_post($_POST['content']);

// Always escape outputs
echo esc_html($user_input);
echo esc_url($url);
echo esc_attr($attribute_value);

// Nonce verification
wp_nonce_field('my_action', 'my_nonce');
if (!wp_verify_nonce($_POST['my_nonce'], 'my_action')) {
    wp_die('Security check failed');
}

// Capability checks
if (!current_user_can('edit_posts')) {
    wp_die('Unauthorized');
}
```

## Outputs
1. Theme structure with functions.php
2. Custom post types and taxonomies
3. Meta boxes for custom fields
4. REST API custom endpoints
5. Security implementation checklist
6. Performance optimization guide
