---
name: wordpress-assistant
description: "Use when assisting with WordPress development, configuration, and troubleshooting. Handles themes, plugins, and site management."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wordpress, cms, themes, plugins, php, web-development]
---

# WordPress Assistant

## Overview

Comprehensive WordPress development and troubleshooting support. Covers theme development, plugin configuration, site management, performance optimization, security hardening, and common debugging workflows. Works with both classic themes and the block editor (Gutenberg), as well as the WordPress REST API.

## When to Use

- "Help me build a WordPress theme" — theme development (classic or block)
- "This plugin isn't working" — plugin troubleshooting and configuration
- "My WordPress site is slow" — performance optimization
- "How do I secure my WordPress site?" — security hardening
- "I need to migrate my WordPress site" — migration and deployment
- "Create a custom post type for..." — custom functionality

**Don't use for:** non-WordPress PHP projects, static site generation (use appropriate tools), or replacing a WordPress developer for complex custom builds.

## How It Works

**Diagnose → Plan → Implement → Test → Harden**

1. **Diagnose:** Understand the current state — WordPress version, active theme/plugins, hosting environment
2. **Plan:** Determine the right approach (child theme, custom plugin, functions.php snippet, or config change)
3. **Implement:** Write code following WordPress coding standards and security best practices
4. **Test:** Verify in multiple browsers, check mobile responsiveness, test with WP_DEBUG on
5. **Harden:** Apply security, caching, and performance measures

## Steps

### 1. Diagnosis
- Ask for: WordPress version, PHP version, active theme, list of active plugins
- If troubleshooting: when did the issue start? After an update? A new plugin?
- Enable `WP_DEBUG` in wp-config.php for detailed error messages:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

### 2. Common Tasks

**Child Theme Setup (recommended for customizations):**
```php
// style.css in child theme directory
/*
Theme Name:   My Child Theme
Template:     parent-theme-slug
*/
```
```php
// functions.php in child theme
add_action('wp_enqueue_scripts', function() {
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
});
```

**Custom Post Type:**
```php
add_action('init', function() {
    register_post_type('portfolio', [
        'labels' => ['name' => 'Portfolio', 'singular_name' => 'Portfolio Item'],
        'public' => true,
        'has_archive' => true,
        'supports' => ['title', 'editor', 'thumbnail'],
        'show_in_rest' => true, // Enable Gutenberg + REST API
    ]);
});
```

**WP_Query for Custom Loops:**
```php
$query = new WP_Query([
    'post_type' => 'portfolio',
    'posts_per_page' => 6,
    'no_found_rows' => true, // Performance: skip pagination count
]);
while ($query->have_posts()) : $query->the_post();
    // Template output
endwhile;
wp_reset_postdata();
```

### 3. Performance Optimization
- **Caching:** Recommend a page cache plugin (WP Rocket, W3 Total Cache) or server-level caching
- **Images:** Convert to WebP, use lazy loading (`loading="lazy"`), serve via CDN
- **Database:** Clean up post revisions, spam comments, and transients
- **Plugins:** Audit active plugins — deactivate and remove unused ones
- **Hosting:** PHP 8.x, OPcache enabled, adequate memory limit (256M+)

### 4. Security Hardening
- Keep WordPress core, themes, and plugins updated
- Use strong passwords and two-factor authentication
- Limit login attempts (plugin or server-level)
- Disable XML-RPC if not needed
- Move wp-config.php above the web root or restrict access
- Regular backups (database + files) before any changes

### 5. Debugging Workflow
1. Check the browser console for JavaScript errors
2. Check `wp-content/debug.log` for PHP errors
3. Deactivate all plugins, then reactivate one by one to isolate conflicts
4. Switch to a default theme (Twenty Twenty-Four) to rule out theme issues
5. Check server error logs and PHP memory limits

## Common Pitfalls

1. **Editing parent themes directly.** Updates wipe your changes. Always use a child theme or custom plugin.

2. **Not using `wp_reset_postdata()`.** After a custom `WP_Query`, forgetting this breaks the main loop and causes confusing template bugs.

3. **Ignoring the `show_in_rest` flag.** Custom post types and taxonomies won't appear in the block editor or REST API without it.

4. **Hooks firing at the wrong time.** `init` for registering things, `wp_enqueue_scripts` for CSS/JS, `template_redirect` for redirects. Using the wrong hook causes "works sometimes" bugs.

5. **Direct database queries bypassing caching.** Use `WP_Query`, `get_posts()`, and `get_post_meta()` instead of raw SQL. They handle caching, security, and compatibility automatically.
