---
name: imlazy-wordpress
description: WordPress + ACF (Advanced Custom Fields) development — themes, plugins, hooks, blocks, field groups, security, REST API, and the full ACF ecosystem
---

# WordPress + ACF Development Skill

Comprehensive guidance for WordPress theme/plugin development and ACF field management.

> This skill incorporates patterns from the official [WordPress Agent Skills](https://github.com/WordPress/agent-skills) — see their skills/ directory for deeper dives on specific topics.

Cross-reference: use `Skill(imlazy-php-review)` for PHP-level code review of any WordPress code encountered.

## When to Activate

- Building or modifying WordPress themes (classic or block)
- Creating or reviewing WordPress plugins
- Working with ACF field groups, blocks, or options pages
- Implementing custom REST API endpoints
- Enqueuing scripts/styles or registering blocks
- Performing WordPress security review
- Writing WP_Query loops or custom database queries

## WordPress Core

### 1. Theme Development

#### Template Hierarchy

WordPress resolves page templates in a strict order. Understand the file that will load:

```
single-{post-type}-{slug}.php  →  single-{post-type}.php  →  single.php  →  singular.php  →  index.php
page-{slug}.php               →  page-{id}.php            →  page.php    →  singular.php  →  index.php
category-{slug}.php           →  category-{id}.php        →  category.php →  archive.php   →  index.php
tag-{slug}.php                →  tag-{id}.php             →  tag.php     →  archive.php   →  index.php
taxonomy-{tax}-{term}.php     →  taxonomy-{tax}.php       →  taxonomy.php →  archive.php   →  index.php
archive-{post-type}.php       →  archive.php              →  index.php
```

Use `is_*()` conditionals in `index.php` as a fallback, not as a replacement for the hierarchy.

#### Block Themes (FSE)

```php
// theme.json — the heart of a block theme
{
  "version": 2,
  "settings": {
    "color": {
      "palette": [
        { "slug": "primary", "color": "#1d2327", "name": "Primary" },
        { "slug": "accent",  "color": "#007cba", "name": "Accent" }
      ]
    },
    "typography": {
      "fontSizes": [
        { "slug": "small", "size": "13px", "name": "Small" },
        { "slug": "medium", "size": "20px", "name": "Medium" }
      ]
    }
  },
  "templates": {
    "index": { "title": "Index", "postTypes": [ "page", "post" ] }
  }
}
```

#### Classic Theme Structure

```
themes/your-theme/
├── style.css              # Required: Theme header comment block
├── index.php              # Required: Main fallback template
├── functions.php          # Theme setup, enqueues, helpers
├── template-parts/        # Reusable partials (header, footer, loops)
├── page-templates/        # Custom page templates (full-width, landing, etc.)
└── assets/                # CSS, JS, images
```

Style.css header:

```css
/*
Theme Name: Your Theme
Theme URI:  https://example.com
Author:     You
Description: Description of your theme.
Version:    1.0.0
License:    GPL-2.0-or-later
Text Domain: your-theme
*/
```

### 2. Plugin Architecture

#### Main Plugin File

```php
<?php
/**
 * Plugin Name: Your Plugin
 * Plugin URI:  https://example.com
 * Description: Description of your plugin.
 * Version:     1.0.0
 * Author:      You
 * License:     GPL-2.0-or-later
 * Text Domain: your-plugin
 */

// Prevent direct access
defined('ABSPATH') or die('No direct access');
```

#### Activation / Deactivation Hooks

```php
register_activation_hook(__FILE__, 'your_plugin_activate');
function your_plugin_activate() {
    // Flush rewrite rules, set defaults, create tables
    // Do NOT output anything
    flush_rewrite_rules();
}

register_deactivation_hook(__FILE__, 'your_plugin_deactivate');
function your_plugin_deactivate() {
    // Clean up scheduled events, flush cache
    wp_clear_scheduled_hook('your_plugin_daily');
    flush_rewrite_rules();
}

// For one-time actions on activation (not every page load)
// Use a version option check in admin_init instead
```

### 3. Hooks System

#### Actions vs Filters

| Hook Type  | Purpose                          | Return Value         |
|------------|----------------------------------|----------------------|
| `do_action()` | Execute a task at a specific point | None (void)        |
| `apply_filters()` | Modify a value before use    | Modified value       |

```php
// PASS: ACTION — perform an operation
add_action('init', function () {
    register_post_type('book', /* ... */);
});

// PASS: FILTER — modify content
add_filter('the_title', function ($title) {
    return $title ?: 'Untitled';
});

// FAIL: Using a filter hook to perform side effects
add_filter('the_title', function ($title) {
    update_option('last_title_accessed', $title);  // SIDE EFFECT — use an action
    return $title;
});
```

#### Priority and Parameters

```php
// Priority (default 10), lower runs first. Accepted args (default 1).
add_action('init', 'my_late_registration', 20);
add_filter('the_content', 'my_filter', 10, 2);  // accepts 2 args

// Remove a hooked callback
remove_action('init', 'some_plugin_function', 10);
remove_filter('the_content', 'another_function');
```

#### Custom Hooks

```php
// In your plugin/theme
do_action('my_plugin_before_save', $post_id, $post_data);
$output = apply_filters('my_plugin_format_output', $output, $context);

// Document custom hooks with docblocks
/**
 * Fires before a post is saved by My Plugin.
 *
 * @param int   $post_id   The post ID.
 * @param array $post_data The post data being saved.
 */
do_action('my_plugin_before_save', $post_id, $post_data);
```

### 4. WP_Query & Database Queries

#### WP_Query (Preferred)

```php
// PASS: WP_Query with proper args
$query = new WP_Query([
    'post_type'      => 'book',
    'posts_per_page' => 10,
    'meta_key'       => 'rating',
    'orderby'        => 'meta_value_num',
    'order'          => 'DESC',
    'paged'          => get_query_var('paged', 1),
    'tax_query'      => [
        [
            'taxonomy' => 'genre',
            'field'    => 'slug',
            'terms'    => 'fiction',
        ],
    ],
]);

if ($query->have_posts()) :
    while ($query->have_posts()) : $query->the_post();
        the_title();
    endwhile;
    wp_reset_postdata();
endif;
```

#### WP_User_Query

```php
$user_query = new WP_User_Query([
    'role'    => 'subscriber',
    'number'  => 50,
    'orderby' => 'registered',
    'fields'  => ['ID', 'display_name', 'user_email'],
]);
$users = $user_query->get_results();
```

#### get_posts vs query_posts

```php
// PASS: get_posts() — returns array, no global state pollution
$posts = get_posts([
    'post_type'      => 'post',
    'posts_per_page' => 5,
    'meta_key'       => 'featured',
    'meta_value'     => '1',
]);

// FAIL: query_posts() — modifies main query, breaks pagination, pollutes global state
query_posts(['posts_per_page' => 1]);
// NEVER use query_posts(). Use pre_get_posts to alter the main query.
```

#### Pre-get_posts to Modify Main Queries

```php
// PASS: Modify main query via pre_get_posts
add_action('pre_get_posts', function (WP_Query $query) {
    if (!is_admin() && $query->is_main_query() && is_home()) {
        $query->set('posts_per_page', 20);
        $query->set('meta_key', 'featured');
        $query->set('meta_value', '1');
    }
});
```

### 5. REST API

#### Custom Endpoints

```php
// PASS: Register custom REST route
add_action('rest_api_init', function () {
    register_rest_route('my-plugin/v1', '/books/(?P<id>\d+)', [
        'methods'             => 'GET',
        'callback'            => 'my_plugin_get_book',
        'permission_callback' => function (WP_REST_Request $request) {
            return current_user_can('edit_posts');
        },
        'args' => [
            'id' => [
                'required'          => true,
                'validate_callback' => function ($param) {
                    return is_numeric($param);
                },
                'sanitize_callback' => 'absint',
            ],
        ],
    ]);
});

function my_plugin_get_book(WP_REST_Request $request) {
    $post = get_post($request['id']);

    if (!$post || $post->post_type !== 'book') {
        return new WP_Error('not_found', 'Book not found', ['status' => 404]);
    }

    return new WP_REST_Response([
        'id'    => $post->ID,
        'title' => $post->post_title,
        'meta'  => get_post_meta($post->ID),
    ], 200);
}
```

#### Authentication

```php
// Cookie authentication (logged-in users) — automatic for same-origin
// Application password authentication — use for external clients
add_filter('rest_authentication_errors', function ($errors) {
    if (!is_user_logged_in()) {
        return new WP_Error('rest_not_logged_in', 'Not authenticated', ['status' => 401]);
    }
    return $errors;
});

// OAuth / JWT — use a dedicated plugin (e.g., WP OAuth Server, JWT Auth)
```

#### Permissions Best Practices

```php
// Minimum capability mapping:
// GET    items  →  read / publish_posts
// POST   items  →  edit_posts
// PUT    items  →  edit_others_posts
// DELETE items  →  delete_posts

register_rest_route('my-plugin/v1', '/settings', [
    'methods'             => 'GET',
    'callback'            => 'my_plugin_get_settings',
    'permission_callback' => function () {
        return current_user_can('manage_options');  // Admin only
    },
]);
```

#### Controller Classes (WP_REST_Controller)

For non-trivial endpoints, subclass `WP_REST_Controller` for CRUD consistency:

```php
class My_Plugin_Books_Controller extends WP_REST_Controller {
    protected $namespace = 'my-plugin/v1';
    protected $rest_base = 'books';

    public function register_routes() {
        register_rest_route($this->namespace, "/{$this->rest_base}", [
            [
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => [$this, 'get_items'],
                'permission_callback' => [$this, 'get_items_permissions_check'],
            ],
            [
                'methods'             => WP_REST_Server::CREATABLE,
                'callback'            => [$this, 'create_item'],
                'permission_callback' => [$this, 'create_item_permissions_check'],
            ],
        ]);
        register_rest_route($this->namespace, "/{$this->rest_base}/(?P<id>\d+)", [
            [
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => [$this, 'get_item'],
                'permission_callback' => [$this, 'get_item_permissions_check'],
                'args'                => $this->get_endpoint_args_for_item_schema(false),
            ],
        ]);
    }

    public function get_items_permissions_check($request) {
        return current_user_can('edit_posts');
    }

    public function get_items($request) {
        $posts = get_posts([
            'post_type'      => 'book',
            'posts_per_page' => $request['per_page'] ?? 10,
            'paged'          => $request['page'] ?? 1,
        ]);

        $data = [];
        foreach ($posts as $post) {
            $data[] = $this->prepare_response_for_collection(
                $this->prepare_item_for_response($post, $request)
            );
        }

        return rest_ensure_response($data);
    }

    public function prepare_item_for_response($item, $request) {
        $post = $item instanceof WP_Post ? $item : get_post($item);
        $data = [
            'id'      => $post->ID,
            'title'   => $post->post_title,
            'content' => $post->post_content,
            'meta'    => get_post_meta($post->ID),
        ];
        return rest_ensure_response($data);
    }

    public function get_item_schema() {
        return [
            '$schema'    => 'http://json-schema.org/draft-04/schema#',
            'title'      => 'book',
            'type'       => 'object',
            'properties' => [
                'id'      => ['type' => 'integer'],
                'title'   => ['type' => 'string'],
                'content' => ['type' => 'string'],
            ],
        ];
    }
}

add_action('rest_api_init', function () {
    $controller = new My_Plugin_Books_Controller();
    $controller->register_routes();
});
```

#### Schema Validation & Discovery

```php
// Validate args against schema automatically
register_rest_route('my-plugin/v1', '/books', [
    'methods'             => 'GET',
    'callback'            => 'my_plugin_get_books',
    'permission_callback' => '__return_true',
    'args'                => [
        'category' => [
            'type'              => 'string',
            'validate_callback'  => function ($value) {
                return in_array($value, ['fiction', 'non-fiction', 'sci-fi']);
            },
        ],
        'per_page' => [
            'type'    => 'integer',
            'default' => 10,
            'minimum' => 1,
            'maximum' => 100,
        ],
        'page' => [
            'type'    => 'integer',
            'default' => 1,
            'minimum' => 1,
        ],
    ],
]);

// Pagination headers (set automatically when using WP_REST_Controller)
// Response headers: X-WP-Total, X-WP-TotalPages

// Discovery: ensure your namespace appears in the /wp-json/ index
// Use rest_get_route_for_post_type_items() for core-compatible route URLs
$route = rest_get_route_for_post_type_items('book');
// Returns: /wp/v2/books (when rest_base is set properly)

// Expose meta in REST responses
register_post_meta('book', 'isbn', [
    'show_in_rest'  => true,
    'type'          => 'string',
    'single'        => true,
    'auth_callback' => function () {
        return current_user_can('edit_posts');
    },
]);

// Support _fields for sparse responses
// GET /wp-json/my-plugin/v1/books?_fields=id,title
```

### 6. Block Editor / Gutenberg

#### block.json

```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "my-plugin/book-card",
  "title": "Book Card",
  "category": "widgets",
  "icon": "book",
  "description": "Display a book with cover, title, and author.",
  "keywords": ["book", "card", "library"],
  "version": "1.0.0",
  "textdomain": "my-plugin",
  "editorScript": "file:./index.js",
  "style": "file:./style-index.css",
  "render": "file:./render.php",
  "attributes": {
    "bookId": {
      "type": "number",
      "default": 0
    },
    "showRating": {
      "type": "boolean",
      "default": false
    }
  },
  "supports": {
    "align": ["wide", "full"],
    "color": {
      "background": true,
      "text": true
    }
  }
}
```

#### register_block_type

```php
// PASS: Register block from block.json metadata
add_action('init', function () {
    register_block_type(__DIR__ . '/build/book-card');
});

// Render callback in render.php (automatically loaded from block.json)
// <div <?php echo get_block_wrapper_attributes(); ?>>
//   <?php
//   $post = get_post($attributes['bookId']);
//   if ($post) : ?>
//     <h3><?php echo esc_html($post->post_title); ?></h3>
//     <p><?php echo esc_html(get_post_meta($post->ID, 'author', true)); ?></p>
//   <?php endif; ?>
// </div>

// Dynamic block with PHP render callback (alternative)
register_block_type('my-plugin/book-card', [
    'render_callback' => function ($attributes, $content, $block) {
        $post = get_post($attributes['bookId']);
        if (!$post) return '';

        ob_start();
        ?>
        <div <?php echo get_block_wrapper_attributes(); ?>>
            <h3><?php echo esc_html($post->post_title); ?></h3>
        </div>
        <?php
        return ob_get_clean();
    },
]);
```

### 7. Block Deprecations & Migrations

When you change a block's saved markup or attributes, existing posts with the old markup will show "This block contains unexpected or invalid content." Always add a `deprecated` entry before removing/changing the `save()` output.

#### Deprecated Entry Structure

```javascript
// blocks/book-card/edit.js — in registerBlockType
registerBlockType('my-plugin/book-card', {
  // ... current implementation
  edit,
  save,  // current save function

  deprecated: [
    {
      // Newest first, oldest last
      attributes: {
        bookId:  { type: 'number', default: 0 },
        layout:  { type: 'string', default: 'card' },
      },
      supports: { align: ['wide'] },
      save: function (props) {
        // The OLD save function (what this block used to output)
        return (
          <div className="book-card-legacy">
            <h3>{props.attributes.title}</h3>
          </div>
        );
      },
      migrate(attributes) {
        // Transform old attributes to new format
        return {
          ...attributes,
          layout: attributes.layout || 'card',
          version: 2,
        };
      },
    },
    {
      // Even older version
      attributes: { bookId: { type: 'number' } },
      save: function () {
        return <div class="book-old">...</div>;
      },
    },
  ],
});
```

#### PHP-Side Deprecations (Dynamic Blocks)

Dynamic blocks (`render.php`) don't save markup to post content, so they rarely need `deprecated`. However, if you change attributes, still add a `deprecated` entry with `save: () => null` and a `migrate` callback:

```javascript
deprecated: [
  {
    attributes: { oldAttr: { type: 'string' } },
    save: () => null,
    migrate(attributes) {
      return { newAttr: attributes.oldAttr };
    },
  },
],
```

#### Rules of Deprecation

- Never remove a deprecated entry that still exists in stored post content
- Each deprecation must include the exact old `save()` output and attribute shape
- Use `migrate()` to normalize old attribute values to new schema
- Test by creating a post with the old block, switching to the new code, and reloading
- List entries newest-first (WordPress tries them in order)

### 8. Interactivity API (data-wp-*)

For interactive frontend behavior without full React, use `viewScriptModule` with the `@wordpress/interactivity` API.

#### block.json Setup

```json
{
  "apiVersion": 3,
  "name": "my-plugin/like-button",
  "title": "Like Button",
  "viewScriptModule": "file:./view.js",
  "render": "file:./render.php",
  "attributes": {
    "postId": { "type": "number" },
    "likes":  { "type": "number", "default": 0 }
  }
}
```

#### view.js (Module Script)

```javascript
import { store, getContext, getElement } from '@wordpress/interactivity';

const { state } = store('my-plugin/like-button', {
  state: {
    get likes() {
      const context = getContext();
      return context.likes;
    },
    get isLiked() {
      const context = getContext();
      return context.isLiked;
    },
  },
  actions: {
    toggleLike() {
      const context = getContext();
      context.isLiked = !context.isLiked;
      context.likes += context.isLiked ? 1 : -1;
    },
  },
  callbacks: {
    logView() {
      console.log('Block viewed:', getContext().postId);
    },
  },
});
```

#### render.php

```php
<div
  <?php echo get_block_wrapper_attributes(); ?>
  data-wp-interactive="my-plugin/like-button"
  <?php echo wp_interactivity_data_wp_context([
    'postId'  => $attributes['postId'],
    'likes'   => $attributes['likes'],
    'isLiked' => false,
  ]); ?>
>
  <button data-wp-on--click="actions.toggleLike">
    <span data-wp-text="state.likes"></span> Likes
  </button>
  <span data-wp-bind--hidden="!state.isLiked">❤️ Liked!</span>
</div>
```

#### viewScript vs viewScriptModule

| Feature          | `viewScript`                    | `viewScriptModule`                    |
|------------------|----------------------------------|----------------------------------------|
| Module type      | Regular ES5 JS (IIFE)            | ES module (`type="module"`)            |
| Interactivity API| Manual store setup               | Built-in `@wordpress/interactivity`    |
| Dependencies     | `wp-interactivity` as dependency | No dependency array needed             |
| Browser support  | All browsers                     | Modern browsers (ES modules)           |
| Prefer when      | Simple scripts, legacy compat    | New development, Interactivity API     |

Use `viewScriptModule` for new development targeting WordPress 6.5+.

### 9. WP-CLI & Operations

WP-CLI is the command-line tool for WordPress management. Always confirm the environment (dev/staging/prod) before running write commands.

#### Essential Commands

```bash
# Cache
wp cache flush

# Rewrite rules
wp rewrite flush

# Database
wp db export backup.sql
wp db import backup.sql
wp db check
wp db optimize

# Search & Replace (URL migration)
wp search-replace 'http://old.dev' 'https://production.com' --dry-run
wp search-replace 'http://old.dev' 'https://production.com'           # After verifying
# For serialized data: --skip-tables=options (then fix with --all tables)

# Plugin Management
wp plugin list --status=active
wp plugin install wordpress-seo --activate
wp plugin update --all
wp plugin deactivate hello

# Theme Management
wp theme list
wp theme activate my-theme

# User Management
wp user list
wp user create editoruser editor@example.com --role=editor --display_name=Editor
wp user update 123 --display_name='New Name'

# Post/Content
wp post list --post_type=page --posts_per_page=10
wp post create --post_type=page --post_title='About' --post_status=publish
wp post meta list 123

# Cron
wp cron event list
wp cron event run wp_version_check
wp cron event schedule example_event hourly

# Multisite
wp site list
wp site create --slug=subsite --title="Subsite"

# Language
wp language core update
wp language plugin install my-plugin de_DE

# Option management
wp option get siteurl
wp option update my_plugin_setting 'value'
wp option list --search="my_plugin_*"
```

#### Safety & Automation

- Always use `--dry-run` before destructive operations
- Create a DB backup before search-replace: `wp db export`
- Use `--path=<wordpress-root>` to target the correct install
- For multisite: use `--url=<site-url>` to target a specific site
- Create `wp-cli.yml` in project root for defaults:
  ```yaml
  path: wp
  url: https://example.test
  ```
- For automation: use `WP_CLI_CONFIG_PATH` env var for custom config paths

### 10. Performance Optimization

#### Profiling (WP-CLI)

```bash
# Stage profiling — see time spent in bootstrap vs query vs template
wp profile stage

# Hook profiling — find slow callbacks
wp profile hook --order=avg

# Optional: target specific URL
wp profile hook --url=/books/
```

#### Autoloaded Options

Options autoloaded on every page load are the #1 performance foot-gun:

```bash
# Find largest autoloaded options
wp option list --autoload=yes --format=json | node -e "
  const opts = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  opts.sort((a,b) => parseInt(b.size) - parseInt(a.size)).slice(0,10)
    .forEach(o => console.log(o.option_name.padEnd(40), o.size + ' bytes'));
"

# Stop autoloading large blobs
wp option update my_large_option ''  # Or delete
# For persistent storage: use transients or custom DB table
```

#### Database Optimization

```sql
-- Find slow queries in query log (if enabled)
-- Check table sizes
SELECT TABLE_NAME, ROUND(DATA_LENGTH/1024/1024,2) AS size_mb
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'wordpress'
ORDER BY size_mb DESC;

-- Ensure proper indexes on postmeta (common N+1 hotspot)
-- WordPress core: CREATE INDEX meta_key_value ON wp_postmeta(meta_key, meta_value(100));
-- Only if your DB doesn't already have the index
```

#### Object Cache

```php
// Use wp_cache_* for heavy computations
function get_expensive_data() {
    $cached = wp_cache_get('my_expensive_key', 'my_group');
    if (false === $cached) {
        $cached = expensive_database_query();
        wp_cache_set('my_expensive_key', $cached, 'my_group', HOUR_IN_SECONDS);
    }
    return $cached;
}

// Install a persistent object cache (Redis/Memcached) for production
// Drop-in: wp-content/object-cache.php
// With Redis: install Redis + Redis Object Cache plugin
```

#### Server-Timing API (WordPress 6.2+)

```php
// Measure specific operations programmatically
add_action('init', function () {
    wp_server_timing()->register_metric('my_expensive_op', 'event');
    $start = microtime(true);
    // ... expensive operation ...
    wp_server_timing()->metric_trigger('my_expensive_op', (microtime(true) - $start) * 1000);
});
```

#### HTTP API Best Practices

```php
// Always set timeouts on remote requests
$response = wp_remote_get('https://api.example.com/data', [
    'timeout'   => 5,  // Max seconds
    'blocking'  => true,
]);

// Cache remote responses
$cached = get_transient('api_data');
if (false === $cached) {
    $response = wp_remote_get('https://api.example.com/data');
    if (200 === wp_remote_retrieve_response_code($response)) {
        set_transient('api_data', wp_remote_retrieve_body($response), HOUR_IN_SECONDS);
    }
}
```

### 11. WordPress Playground

WordPress Playground runs WordPress entirely in the browser via WebAssembly — no server setup needed.

#### Quick Start

```bash
# Spin up a disposable instance with your plugin/theme mounted
cd /path/to/plugin-or-theme
npx @wp-playground/cli@latest server --auto-mount
# Opens at http://localhost:9400

# Pin specific versions
npx @wp-playground/cli@latest server --auto-mount --wp=7.0 --php=8.3

# Run a Blueprint (scripted setup, no server UI)
npx @wp-playground/cli@latest run-blueprint \
  --blueprint=https://example.com/blueprint.json

# Build a reproducible snapshot
npx @wp-playground/cli@latest build-snapshot \
  --blueprint=./blueprint.json --outfile=./site.zip
```

#### Blueprint Example

```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "landingPage": "/wp-admin/admin.php?page=my-plugin",
  "preferredVersions": {
    "php": "8.3",
    "wp": "7.0"
  },
  "steps": [
    {
      "step": "installPlugin",
      "pluginZipFile": {
        "resource": "url",
        "url": "https://github.com/.../plugin.zip"
      },
      "options": {
        "activate": true
      }
    },
    {
      "step": "login",
      "username": "admin",
      "password": "password"
    },
    {
      "step": "runPHP",
      "code": "<?php update_option('my_plugin_setting', 'test_value'); ?>"
    }
  ]
}
```

#### Use Cases

- **Testing** a plugin/theme against different WP/PHP versions instantly
- **Debugging** with Xdebug (`--xdebug` flag)
- **CI validation** via `run-blueprint` in GitHub Actions
- **Bug reproduction** — build a snapshot ZIP to share with contributors
- **Onboarding** — give contributors a one-click Playground link

### 12. Security

#### Nonces

```php
// PASS: Verify nonce on form submissions
add_action('admin_post_my_action', function () {
    if (!isset($_POST['_wpnonce']) || !wp_verify_nonce($_POST['_wpnonce'], 'my_action_nonce')) {
        wp_die('Security check failed');
    }
    // Process form...
});

// FAIL: Missing nonce verification
add_action('admin_post_my_action', function () {
    update_option('my_setting', $_POST['value']);  // NO NONCE CHECK
});

// Generate nonce for forms
wp_nonce_field('my_action_nonce', '_wpnonce');
// Or for AJAX: wp_create_nonce('my_ajax_nonce')
```

#### Capability Checks

```php
// PASS: Check capabilities before actions
if (current_user_can('edit_others_posts')) {
    // Perform admin action
}

// FAIL: Relying on user ID or role strings
if (get_current_user_id() === 1) { /* ... */ }  // Fragile
if (in_array('administrator', wp_get_current_user()->roles)) { /* ... */ }  // Role rename breaks this

// PASS: Use capability checks, not role checks
if (current_user_can('manage_options')) { /* ... */ }
```

#### Data Escaping

| Function      | Context               | Example                                      |
|--------------|------------------------|----------------------------------------------|
| `esc_html()`  | Plain text in HTML    | `<p><?php echo esc_html($title); ?></p>`      |
| `esc_attr()`  | HTML attribute values | `<div class="<?php echo esc_attr($class); ?>">` |
| `esc_url()`   | URLs                  | `<a href="<?php echo esc_url($link); ?>">`    |
| `esc_textarea()` | Textarea content  | `<textarea><?php echo esc_textarea($text); ?></textarea>` |
| `esc_js()`    | Inline JavaScript     | `onclick="alert('<?php echo esc_js($msg); ?>')"` |
| `wp_kses()`   | Allowed HTML subset   | `echo wp_kses($content, $allowed_html);`      |

```php
// PASS: Escape everything on output
<h2><?php echo esc_html($title); ?></h2>
<a href="<?php echo esc_url($url); ?>"><?php echo esc_html($text); ?></a>

// FAIL: Unescaped output
<h2><?php echo $title; ?></h2>  // XSS vulnerability
```

### 13. Cron System

```php
// Schedule a recurring event (on plugin activation)
if (!wp_next_scheduled('my_plugin_daily_cleanup')) {
    wp_schedule_event(time(), 'daily', 'my_plugin_daily_cleanup');
}

add_action('my_plugin_daily_cleanup', 'my_plugin_do_cleanup');
function my_plugin_do_cleanup() {
    // Delete old transients, purge logs, etc.
    // Use WP_CRON constant check if needed
    if (defined('WP_CRON') && WP_CRON) {
        set_time_limit(0);
    }
}

// Single (one-time) event
wp_schedule_single_event(time() + HOUR_IN_SECONDS, 'my_plugin_delayed_action');

// Manual cron trigger: visiting /wp-cron.php?doing_wp_cron
// To disable WP-Cron and use system cron:
// define('DISABLE_WP_CRON', true);
// Then: * * * * * curl https://yoursite.com/wp-cron.php?doing_wp_cron > /dev/null 2>&1
```

### 14. Data APIs

#### Options API

```php
// Simple key-value storage (autoloaded by default)
update_option('my_plugin_setting', 'value');
$value = get_option('my_plugin_setting', 'default');
delete_option('my_plugin_setting');

// Autoload: pass false to prevent autoload on every page load
update_option('my_plugin_setting', 'value', false);
```

#### Transients (Cached Options)

```php
// Cached option with expiration
$cached = get_transient('my_plugin_data');
if (false === $cached) {
    $cached = expensive_computation();
    set_transient('my_plugin_data', $cached, HOUR_IN_SECONDS);
}

// Site-level transient (multisite-safe)
set_site_transient('my_plugin_global', $data, DAY_IN_SECONDS);
```

#### Post Meta

```php
// PASS: Use namespaced, single meta keys
update_post_meta($post_id, 'book_rating', 4.5);
$rating = get_post_meta($post_id, 'book_rating', true);  // single
$ratings = get_post_meta($post_id, 'book_rating', false); // array of all

// Register meta for REST API exposure
register_post_meta('book', 'book_rating', [
    'show_in_rest'  => true,
    'type'          => 'number',
    'single'        => true,
    'sanitize_callback' => 'absint',
    'auth_callback' => function () {
        return current_user_can('edit_posts');
    },
]);
```

#### User Meta

```php
update_user_meta($user_id, 'favorite_genre', 'fiction');
$genre = get_user_meta($user_id, 'favorite_genre', true);
```

### 15. WordPress Coding Standards

Follow the [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/):

```php
// Naming: lowercase with underscores (not camelCase)
function my_plugin_get_data() { }  // PASS
function myPluginGetData() { }  // FAIL

// Class names: uppercase with underscores prefixing
class My_Plugin_Helper { }  // PASS
class myPluginHelper { }  // FAIL

// Constants: uppercase with underscores
define('MY_PLUGIN_VERSION', '1.0.0');  // PASS

// Brace style: BSD/Allman for classes and functions
function my_plugin_function()        // PASS
{                                    // Brace on new line
    if (condition) {                 // Control structures: brace on same line
        // ...
    }
}

// Space after ! and before/after logical operators
if ( ! is_admin() ) { }  // WPCS requires spaces around !

// Yoda conditions
if (true === $value) { }         // PASS
if ($value === true) { }         // FAIL

// No PHP closing tag in pure PHP files
<?php
// ... code ...
// NO "?>" at the end
```

Use `phpcs` with the WordPress standard:
```bash
phpcs --standard=WordPress wp-content/plugins/my-plugin/
phpcbf --standard=WordPress wp-content/plugins/my-plugin/  # Auto-fix
```

### 16. Enqueuing Assets

```php
// PASS: Use wp_enqueue_* with proper dependencies and versioning
add_action('wp_enqueue_scripts', function () {
    // Styles
    wp_enqueue_style(
        'my-plugin-style',                     // Handle
        plugin_dir_url(__FILE__) . 'assets/style.css',
        ['wp-components'],                     // Dependencies
        '1.0.0',                               // Version
        'all'                                  // Media
    );

    // Scripts
    wp_enqueue_script(
        'my-plugin-script',
        plugin_dir_url(__FILE__) . 'assets/script.js',
        ['jquery', 'wp-api'],                  // Dependencies
        '1.0.0',
        ['in_footer' => true]                  // Load in footer
    );

    // Localize script for passing PHP data to JS
    wp_localize_script('my-plugin-script', 'myPluginData', [
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'nonce'   => wp_create_nonce('my_plugin_nonce'),
        'userId'  => get_current_user_id(),
    ]);
});

// FAIL: Hardcoding asset URLs
echo '<link rel="stylesheet" href="/path/to/style.css">';  // Breaks with plugins/migrations
echo '<script src="/path/to/script.js"></script>';

// Admin-specific enqueues
add_action('admin_enqueue_scripts', function ($hook) {
    if ('post.php' !== $hook && 'post-new.php' !== $hook) return;
    wp_enqueue_script('my-plugin-admin-js');
});
```

## ACF (Advanced Custom Fields)

### 1. Field Group Definitions

#### PHP Array Definition (Recommended for Version Control)

```php
// In functions.php or a dedicated ACF file
if (function_exists('acf_add_local_field_group')) {
    acf_add_local_field_group([
        'key'    => 'group_book_details',
        'title'  => 'Book Details',
        'fields' => [
            [
                'key'   => 'field_book_author',
                'label' => 'Author',
                'name'  => 'book_author',
                'type'  => 'text',
                'required' => 1,
            ],
            [
                'key'   => 'field_book_isbn',
                'label' => 'ISBN',
                'name'  => 'book_isbn',
                'type'  => 'text',
            ],
            [
                'key'   => 'field_book_rating',
                'label' => 'Rating',
                'name'  => 'book_rating',
                'type'  => 'number',
                'min'   => 1,
                'max'   => 5,
                'step'  => 0.5,
            ],
        ],
        'location' => [
            [
                [
                    'param'    => 'post_type',
                    'operator' => '==',
                    'value'    => 'book',
                ],
            ],
        ],
    ]);
}
```

#### ACF JSON Sync

```php
// In functions.php — set save/load points
add_filter('acf/settings/save_json', function ($path) {
    return get_stylesheet_directory() . '/acf-json';
});

add_filter('acf/settings/load_json', function ($paths) {
    $paths[] = get_stylesheet_directory() . '/acf-json';
    return $paths;
});

// ACF automatically saves field groups to acf-json/ when "Sync" is enabled
// Commit these JSON files to version control
// JSON files are read-only — edit in the admin UI, then sync via JSON
```

### 2. Field Types

```php
// Text
$title = get_field('book_subtitle');          // Returns string

// WYSIWYG
the_field('book_description');                // Echoes formatted HTML
$desc = get_field('book_description');        // Returns HTML string

// Image
$image = get_field('book_cover');             // Returns array
echo $image['url'];                           // Full URL
echo $image['sizes']['medium'];               // Specific size
echo $image['alt'];                           // Alt text
// or:
$image_id = get_field('book_cover', false, false);  // Returns ID only
echo wp_get_attachment_image($image_id, 'medium');

// Repeater
if (have_rows('book_chapters')) :
    while (have_rows('book_chapters')) : the_row();
        $title = get_sub_field('chapter_title');
        $pages = get_sub_field('page_count');
        echo "<li>$title ($pages pages)</li>";
    endwhile;
endif;

// Flexible Content
if (have_rows('page_sections')) :
    while (have_rows('page_sections')) : the_row();
        if (get_row_layout() === 'hero') :
            the_sub_field('headline');
        elseif (get_row_layout() === 'content_block') :
            the_sub_field('body_text');
        endif;
    endwhile;
endif;

// Relationship
$related = get_field('related_books');        // Returns array of WP_Post objects
foreach ($related as $post) :
    setup_postdata($post);
    the_title();
endforeach;
wp_reset_postdata();

// Gallery
$images = get_field('book_gallery');          // Returns array of image arrays
foreach ($images as $image) :
    echo wp_get_attachment_image($image['ID'], 'thumbnail');
endforeach;
```

### 3. ACF Blocks

#### block.json for ACF Block

```json
{
  "name": "acf/book-showcase",
  "title": "Book Showcase",
  "description": "Display featured books with cover, rating, and excerpt.",
  "category": "media",
  "icon": "book-alt",
  "keywords": ["book", "showcase", "featured"],
  "acf": {
    "mode": "preview",
    "renderTemplate": "block-book-showcase.php",
    "postTypes": ["page", "post"]
  },
  "supports": {
    "align": ["wide"],
    "anchor": true
  }
}
```

#### Block Template (renderTemplate)

```php
<?php
/**
 * Book Showcase Block Template
 *
 * @param array     $block      Block settings and attributes
 * @param string    $content    Block inner HTML (for dynamic blocks)
 * @param bool      $is_preview Whether in editor preview
 * @param int       $post_id    Current post ID
 */

$books = get_field('featured_books');  // ACF relationship field
$show_rating = get_field('show_rating');

if (!$books) :
    if ($is_preview) :
        echo '<p>Add featured books in the block settings.</p>';
    endif;
    return;
endif;
?>
<div <?php echo get_block_wrapper_attributes(); ?>>
    <div class="book-grid">
        <?php foreach ($books as $book) :
            $cover = get_field('book_cover', $book->ID);
        ?>
            <div class="book-card">
                <?php if ($cover) : ?>
                    <?php echo wp_get_attachment_image($cover['ID'], 'medium'); ?>
                <?php endif; ?>
                <h3><?php echo esc_html($book->post_title); ?></h3>
                <?php if ($show_rating) : ?>
                    <p>Rating: <?php echo esc_html(get_field('book_rating', $book->ID)); ?>/5</p>
                <?php endif; ?>
            </div>
        <?php endforeach; ?>
    </div>
</div>
```

### 4. ACF Options Pages

```php
// Register an options page
if (function_exists('acf_add_options_page')) {
    acf_add_options_page([
        'page_title' => 'Theme Settings',
        'menu_title' => 'Theme Settings',
        'menu_slug'  => 'theme-settings',
        'capability' => 'manage_options',
        'redirect'   => false,
        'icon_url'   => 'dashicons-admin-generic',
    ]);

    // Sub-pages
    acf_add_options_sub_page([
        'page_title' => 'Header Settings',
        'menu_title' => 'Header',
        'parent_slug' => 'theme-settings',
    ]);

    acf_add_options_sub_page([
        'page_title' => 'Footer Settings',
        'menu_title' => 'Footer',
        'parent_slug' => 'theme-settings',
    ]);
}

// Get values from options page
$site_phone = get_field('site_phone', 'option');
$footer_text = get_field('footer_copyright', 'option');
```

### 5. ACF Location Rules

```php
// Rules determine WHERE a field group appears
// Each rule group is an OR; rules within a group are AND
$field_group['location'] = [
    [   // Group 1: Show on Book post type
        [
            'param'    => 'post_type',
            'operator' => '==',
            'value'    => 'book',
        ],
        [
            'param'    => 'page_template',
            'operator' => '!=',
            'value'    => 'template-fullwidth.php',
        ],
    ],
    [   // Group 2: OR show on the settings page
        [
            'param'    => 'options_page',
            'operator' => '==',
            'value'    => 'theme-settings',
        ],
    ],
];

// Common params: post_type, page_template, taxonomy, post_category,
//                 post_format, user_role, block, page_type, page_parent
```

### 6. ACF Helper Functions

```php
// get_field($name, $post_id, $format_value) — returns value
$value = get_field('book_author', 123);            // For specific post
$value = get_field('book_author');                  // Inside the loop
$value = get_field('header_logo', 'option');        // Options page

// the_field() — echoes the value
the_field('book_author');

// have_rows() / the_row() — repeater/flexible loop
if (have_rows('chapters')) {
    while (have_rows('chapters')) {
        the_row();
        echo get_sub_field('title');
    }
}

// Sub-field helpers (use inside a repeater row)
$title = get_sub_field('chapter_title');
the_sub_field('chapter_title');

// ACF shortcode
// [acf field="book_author"]
// [acf field="book_author" post_id="123"]
// [acf field="site_phone" post_id="option"]

// Twig/Timber integration
// In a Twig template: {{ post.meta('book_author') }}
// Or with Timber:     {{ function('get_field', 'book_author', post.ID) }}
```

### 7. ACF Field Validation

```php
// PASS: ACF field validation via PHP
add_filter('acf/validate_value/key=field_book_isbn', function ($valid, $value, $field, $input) {
    if ($value && !preg_match('/^(?:\d{10}|\d{13})$/', $value)) {
        return 'ISBN must be 10 or 13 digits.';
    }
    return $valid;
}, 10, 4);

// PASS: Conditional required field
add_filter('acf/validate_value/name=book_publisher', function ($valid, $value, $field, $input) {
    $is_self_published = get_field('self_published');
    if ($is_self_published && empty($value)) {
        return 'Publisher is required for self-published books.';
    }
    return $valid;
}, 10, 4);

// FAIL: Not validating ACF fields before saving
// ACF does basic type validation, but custom business rules need hooks
```

## Cross-Reference: PHP Code Review

When writing WordPress code, always run `Skill(imlazy-php-review)` for PHP-level checks:

- WordPress Coding Standards (PSR-12 base + WP-specific rules)
- Proper escaping vs raw output
- Nonce verification on form submissions
- Capability checks vs role string checks
- WP_Query vs direct SQL queries
- ACF field existence checks before access

## Verification Checklist

- [ ] All user-facing output escaped (`esc_html`, `esc_attr`, `esc_url`)
- [ ] Nonces used on all forms and AJAX actions
- [ ] Capability checks (`current_user_can`) instead of role/ID checks
- [ ] `query_posts()` not used — use `WP_Query` or `pre_get_posts`
- [ ] `ABSPATH` guard in plugin files
- [ ] All REST endpoints have `permission_callback`
- [ ] Block `block.json` has `apiVersion: 3` and proper supports
- [ ] `deprecated` entries added when changing block `save()` output or attributes
- [ ] Interactivity API uses `viewScriptModule` (not `viewScript`) for new development
- [ ] WP-CLI `--dry-run` used before destructive operations
- [ ] Autoloaded options are minimal — no large blobs autoloaded on every page load
- [ ] ACF JSON sync configured and field group JSON files committed
- [ ] Repeater/flexible content loops check `have_rows()` before iterating
- [ ] Options page values use `'option'` as the post ID
- [ ] Transients have reasonable expiration times
- [ ] Cron hooks are cleared on plugin deactivation
- [ ] Assets enqueued through `wp_enqueue_*` with proper dependencies
- [ ] No `query_posts()` or direct SQL without `$wpdb->prepare()`
- [ ] ACF field values validated with custom `acf/validate_value` hooks
