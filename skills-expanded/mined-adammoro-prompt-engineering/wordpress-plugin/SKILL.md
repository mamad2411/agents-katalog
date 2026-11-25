---
name: wordpress-plugin
description: Scaffold and build a WordPress plugin. Use when the user wants to create a WordPress plugin, add functionality to a WordPress site through a plugin, or extend an existing plugin with hooks, shortcodes, blocks, admin pages, or settings.
---

# WordPress Plugin Builder

Build a working, secure WordPress plugin. Write the files, don't print a wall of
code for the user to assemble.

## Scope the plugin first

Ask only what you can't infer:

1. **What should it do?** Specifically — the user-visible behavior.
2. **Where does it surface?** Admin page, settings section, shortcode, block,
   widget, front-end hook, REST endpoint.
3. **Does it store data?** Options, post meta, custom post type, custom table.
   A custom table needs a real justification — options and post meta cover most
   cases and come with the platform's own upgrade handling.
4. **Who can use it?** Which capability gates each action.

Don't ask about naming conventions, file layout, or the header block. Pick
sensible defaults and say what you picked.

## Structure

```
plugin-name/
  plugin-name.php        # header, constants, activation/deactivation, bootstrap
  includes/              # classes, one per file
  admin/                 # admin-only code, loaded conditionally
  assets/                # css, js
  readme.txt             # WordPress.org format, if distributing
  uninstall.php          # clean up options and tables on delete
```

Prefix everything — functions, classes, options, hooks, globals — with a unique
slug. Collisions with other plugins are the most common cause of a site that
breaks only when two specific plugins are active.

## Non-negotiables

These are where plugins actually go wrong. Apply all of them.

**Escape on output, validate on input, sanitize on save.**
`esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses_post()` on the way out.
`sanitize_text_field()`, `absint()`, and friends on the way in. Escape at the
point of output, not earlier — a value escaped in one place and echoed in
another is a bug waiting to happen.

**Nonces on every state change.** `wp_nonce_field()` in the form,
`check_admin_referer()` or `wp_verify_nonce()` in the handler. Every form, every
AJAX action, every REST route.

**Capability checks on every privileged action.** `current_user_can()` with the
narrowest capability that fits. A nonce proves the request came from your form;
it does not prove the user is allowed to do the thing.

**`$wpdb->prepare()` for every query with a variable.** No exceptions, including
values you believe are safe.

**No direct file access.** `defined( 'ABSPATH' ) || exit;` at the top of every
PHP file.

**Text domain on every user-facing string.** `__()`, `_e()`, `esc_html__()`,
matching the plugin slug.

## Conventions

- WordPress coding standards: tabs, `snake_case` functions, `Class_Name`
  classes, Yoda conditions in comparisons.
- Hooks over direct calls. Register on `init`, `admin_menu`, `enqueue_scripts`
  rather than running at file load.
- Enqueue assets properly with `wp_enqueue_script`/`_style` and version
  constants. Never hardcode a `<script>` tag.
- Load admin code only in admin context.
- Bump a version constant and use it for cache busting.

## Finishing

- Write `uninstall.php` — delete options, drop custom tables, clear scheduled
  events. A plugin that leaves rows behind on delete is a bug.
- Check for PHP syntax errors: `php -l` on each file if PHP is available.
- If WP-CLI or a local WordPress is available, activate the plugin and confirm
  it loads without notices. Say whether you ran this or not.
- Write a short README covering what it does, how to install, and any settings.

## Report

State what you built, which files you created, what you verified and how, and
anything you left out. If you could not activate and test it, say so plainly
rather than implying it works.
