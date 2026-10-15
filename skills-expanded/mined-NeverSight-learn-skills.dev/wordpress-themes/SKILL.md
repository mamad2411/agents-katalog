---
name: wordpress-themes
description: WordPress classic theme development specialist focused on clean, maintainable, VIP-compliant custom themes. Use when building or modifying a classic (non-block) WordPress theme, setting up theme structure, writing functions.php, enqueueing scripts/styles, working with template parts, configuring dart-sass for theme CSS, escaping output, sanitizing input, registering custom post types from a theme, configuring image sizes, or asking about WordPress VIP coding standards. Covers WordPress 6.x classic themes, PHP 8.1+, modular theme structure, dart-sass via Homebrew, proper enqueueing with cache-busting, template parts organization, text domain management, and VIP escape/sanitize discipline. Does NOT cover block themes (FSE / theme.json) or Gutenberg blocks — see wordpress-blocks for blocks.
---

# WordPress Classic Theme Development

Build clean, VIP-compliant WordPress classic themes (WP 6.x, PHP 8.1+) with modular structure and dart-sass tooling. For block themes (FSE / theme.json) or Gutenberg blocks, this skill is the wrong tool — see `wordpress-blocks` for blocks.

## Important — Read Reference Files First

Before generating code, load the reference file that matches the user's task:

| User wants to… | Read first |
|---|---|
| Set up a new theme, see the directory layout, or understand the functions.php pattern | `references/theme-structure.md` |
| Enqueue stylesheets or scripts (global or page-specific) | `references/enqueueing.md` |
| Set up dart-sass for theme CSS, watch mode, or page-specific compilation | `references/sass-workflow.md` |
| Escape output, sanitize input, or check VIP compliance | `references/vip-security.md` |
| Add image sizes, theme-support features, or work with the text domain | `references/media-and-i18n.md` |

If none of those match, use the core philosophy + critical rules below directly.

---

## Core Philosophy

- **Minimal Plugin Dependency**: Use public plugins for specialized functions (SEO, security), keep custom code in the theme.
- **VIP Standards**: Follow WordPress VIP Coding Standards (2025) for enterprise-grade quality.
- **Clean Organization**: Modular structure with clear separation of concerns.
- **Maintainability**: Easy to understand, easy to update.

## Critical Rules

Three things never to forget for a WordPress classic theme:

1. **Never include `flush_rewrite_rules()` in production code**, even commented out. It bypasses WordPress's rewrite cache and causes serious performance issues on every page load.
2. **Never hardcode file paths or URLs.** Use `get_template_directory()` for filesystem paths and `get_template_directory_uri()` for asset URLs. Hardcoded paths break the moment the theme is installed under a different directory name or on a different host.
3. **Always pass a version to `wp_enqueue_*`.** The version (from `wp_get_theme()->get('Version')`) is appended to the asset URL as a cache-busting query string. Without it, browsers serve stale CSS and JS indefinitely.

## Quick Reference

These two snippets are short enough to belong in the spine — used in nearly every theme.

### Theme Support Features

```php
add_theme_support( 'title-tag' );
add_theme_support( 'post-thumbnails' );
add_theme_support( 'responsive-embeds' );
add_theme_support( 'html5', array( 'search-form', 'comment-form' ) );
```

### Clean Up WordPress Head

```php
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
```
