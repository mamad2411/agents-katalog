---
name: resolve-common-warnings
description: Address common warnings raised by the Plugin Check tool.
---

# Resolve Common Warnings from Plugin Check

When reviewing a plugin with the Plugin Check tool, you may encounter several common errors and warnings.

## Common Issues
1. **Direct File Access**: Ensure proper security validation using `defined( 'ABSPATH' ) || exit;` at the top of PHP files.
2. **Internationalization (i18n)**: 
    - Do not use variables in translation strings.
    - Ensure your text domain matches the plugin slug.
3. **Escaping**: Always escape output using functions like `esc_html()`, `esc_attr()`, or `wp_kses_post()`.
4. **Readme Sync**: The "Tested up to" header in the plugin's main PHP file must match the `readme.txt` file.

Address these proactively to speed up the WordPress.org plugin directory review process.
