---
name: perfex-theme
description: Use whenever the user is building or debugging a Perfex CRM custom client-area theme — files under `assets/themes/<theme>/` and `application/views/themes/<theme>/`, asset injection via `app_customers_head`/`app_customers_footer`/`app_admin_head`/`app_admin_footer` hooks, overriding core views, dark mode with `[data-theme="dark"]` plus anti-FOUC `<head>` scripts, RTL/Arabic support, or the jQuery Validate bug where a submit button's `name` is stripped from POST (breaks "Pay Now" / "Save Draft" detection). Also trigger when the user says "my theme CSS is cached after deploy", "Pay Now button loses its value", "jQuery Validate ate my button name", "client area dark mode", "theme file isn't picked up on Linux", or "FOUC when switching themes".
license: MIT
metadata:
  author: yasserstudio
  version: "1.5.0"
---

# Perfex Custom Themes & Client Area

You are a Perfex CRM theme developer. Your job is to build or fix custom client-area themes that use Perfex's asset hooks correctly, override core views without being blown away by updates, handle dark mode and RTL without FOUC, and dodge the jQuery Validate submit-button-name bug that silently breaks multi-action forms.

Perfex's client area supports custom themes under `assets/themes/<theme_name>/` + `application/views/themes/<theme_name>/`. Themes override core views and can inject their own CSS/JS via hooks.

## Theme folder layout

A client-area theme is a folder under `application/views/themes/<theme_name>/`. Core loads `functions.php` from the **active** theme on every request (`InitHook.php`, right after module init files), so that file is your entry point — the theme equivalent of a module's `my_module.php`.

```
application/views/themes/my_theme/
├── functions.php              # hooks, menu items, asset registration — REQUIRED
├── head.php                   # <head> — usually copied from themes/perfex/ then edited
├── footer.php
├── index.php
├── template_parts/            # navigation.php, etc.
└── views/                     # override any core client view by matching filename

assets/themes/my_theme/        # your CSS/JS/images (any path works; this is the convention)
```

Start by copying `application/views/themes/perfex/` wholesale, then delete what you don't override — it's the only complete, current reference. Activate via Setup → Settings → Customers → Theme.

## Asset loading — `register_theme_assets_hook()`, not raw `<link>`

Core's own theme registers assets through the `App_css` / `App_scripts` registries, and so should yours. `functions.php`:

```php
<?php
defined('BASEPATH') or exit('No direct script access allowed');

// Required: core's head hook, plus the default client menu unless you build your own
hooks()->add_action('app_customers_head', 'app_theme_head_hook');
hooks()->add_action('clients_init', 'add_default_theme_menu_items');

register_theme_assets_hook('my_theme_assets');   // fires on `app_client_assets`, priority 1

function my_theme_assets()
{
    $CI = &get_instance();

    // theme() registers into the customers-area group; add() with an explicit group works too
    $CI->app_css->theme('my-theme-css', 'assets/themes/my_theme/css/theme.css');
    $CI->app_scripts->theme('my-theme-js', [
        'path'       => 'assets/themes/my_theme/js/theme.js',
        'attributes' => ['defer'],
    ], ['theme-global-js']);                         // deps: load after the client-area core scripts

    // Keep the core plugins the client area needs (datatables, validation, selectpicker...)
    $group = $CI->app_scripts->default_theme_group();
    add_datatables_js_assets($group);
    add_jquery_validation_js_assets($group);
    add_bootstrap_select_js_assets($group);
}
```

`head.php` then emits the CSS with `<?= compile_theme_css(); ?>` and `footer.php` emits the scripts via `<?php app_customers_footer(); ?>` (which calls `compile_theme_scripts()` and fires the `app_customers_footer` hook) — copy those calls from the `perfex` theme.

What the registry does for you — and two traps:
- **Cache-busting:** a raw path gets `?v=<app version>` — and only that. The `time()`-in-development bust and the `.min` swap ("use minified files" setting) happen **only** when you go through `core_file()` / `core_version()` the way the stock theme does: `$CI->app_css->theme('x', base_url($CI->app_css->core_file('assets/themes/my_theme/css', 'theme.css')) . '?v=' . $CI->app_css->core_version())`. `'version'` in `$data` is a boolean toggle, not a value. For per-file busting on a raw path, append your own query: `'path' => '…/theme.css?t=' . filemtime(FCPATH . '…/theme.css')` (the registry appends `&v=` correctly).
- **Dependencies must exist in the same group, or your asset is silently dropped.** `all_deps()` gives up on a handle whose dep isn't registered in that group — no error, no `<script>` tag. Admin handles (`app-js`, `app-css`) are not in the customers group; the client-area handles are `common-js`, `theme-global-js`, `theme-clients-js`. Depend on those.
- **Dedup** — module assets and theme assets don't double-load.

Only fall back to echoing raw `<link>`/`<script>` from `app_customers_head` / `app_customers_footer` for third-party snippets that can't live in the registry (inline config blobs, GTM, etc.).

## jQuery Validate + submit button name — the "Pay Now" bug

Perfex uses jQuery Validate on most forms. jQuery Validate's default behaviour **strips the submit button's `name` attribute from the POST body** when submitting programmatically. This breaks forms that rely on detecting which button was clicked:

```html
<form method="post">
    <button type="submit" name="pay_now" value="1">Pay Now</button>
    <button type="submit" name="save_draft" value="1">Save</button>
</form>
```

PHP sees neither `$_POST['pay_now']` nor `$_POST['save_draft']` on submit.

### Fix: mirror intent into a hidden input

```html
<form method="post">
    <input type="hidden" name="action" id="form_action" value="">
    <button type="submit" onclick="document.getElementById('form_action').value='pay_now'">Pay Now</button>
    <button type="submit" onclick="document.getElementById('form_action').value='save_draft'">Save</button>
</form>
```

Then check `$_POST['action']` server-side. This is the pattern used in a production client theme's Pay Now fix.

## Overriding a core view

Client-area views are loaded from `application/views/themes/<active_theme>/views/<name>.php`. To override the client dashboard, copy `application/views/themes/perfex/views/home.php` to `application/views/themes/my_theme/views/home.php` and edit.

For a *small* change to a view in the stock `perfex` theme (or any core/admin view), use the `my_` prefix instead of a full theme: `App_Loader` checks for `my_<file>.php` next to every view before loading the original — `views/my_home.php`, `views/my_invoicehtml.php`, `admin/invoices/my_invoice.php`. Survives updates, no theme switch needed. Module views get the same treatment only if the module calls `add_module_support($module, 'my_prefixed_view_files')`.

**Don't edit core views in place.** They'll be blown away on Perfex update.

## Language strings in themes

Themes can't register language keys directly (no `module_name.php` hook point). Either:
- Package the theme with a companion module that registers keys, OR
- Use inline strings and maintain a manual i18n dict in JS:
  ```php
  <script>
  window.THEME_STRINGS = <?= json_encode([
      'save' => _l('save'),
      'cancel' => _l('cancel'),
      // ... using core keys that already exist
  ]) ?>;
  </script>
  ```

For custom module-owned JS strings, use `json_encode(_l('key'))` — never raw concat — to avoid quote-escape bugs and XSS.

## Dark mode pattern

Use semantic CSS custom properties, switch via `[data-theme="dark"]`:

```css
:root {
    --bg-primary: #fff;
    --text-primary: #111;
    --brand-primary: #2A5189;
}
[data-theme="dark"] {
    --bg-primary: #0f1115;
    --text-primary: #e8e8e8;
    --brand-primary: #8eaadd;  /* lift lighter in dark for contrast */
}
```

Apply `data-theme` attribute BEFORE first paint to avoid FOUC:

```html
<head>
    <script>
    (function() {
        var t = localStorage.getItem('my_theme_mode');
        if (t) document.documentElement.setAttribute('data-theme', t);
    })();
</script>
</head>
```

Toggle logic lives in your theme's JS; persist choice under a namespaced key like `my_theme_mode`.

## RTL / Arabic support

Perfex supports RTL via language settings. In your theme CSS:

```css
[dir="rtl"] .my-component {
    /* flip margins, text-align */
}
```

Ship both LTR and RTL icon variants if your icons have directional meaning (chevrons, arrows).

## Forms with Bootstrap + Perfex

Perfex ships Bootstrap 3.x in the client area and admin. For new themes, you can ship a newer Bootstrap but watch for conflicts with inline admin code. Scope newer styles by adding a wrapper class on your custom views.

## Accessibility baseline

- Every `<input>` needs an `id` + `<label for="...">`.
- `aria-describedby` linking to error containers.
- Decorative icons: `aria-hidden="true"`.
- Required: `<span aria-label="required">*</span>`.
- Error containers: `role="alert" aria-live="polite"`.
- Add `<main id="main-content">` + a skip link.

## Update-safe CSS overrides

Two built-in methods for CSS customization that survive Perfex core updates:

### Method 1: `assets/css/custom.css` file

Create `assets/css/custom.css` in the Perfex root — no hook needed, survives updates. Admin loads it through the asset registry (`init_admin_assets()`, after `app-css`); the client area loads it from `app_customers_head()`, which the stock theme's `head.php` calls. **A custom theme that doesn't call `app_customers_head()` in its `head.php` loses `custom.css`** (and every module that injects into that hook) — keep that call.

```css
/* assets/css/custom.css */
.panel-heading { background: #2A5189; color: #fff; }
.btn-primary { border-radius: 4px; }
```

### Method 2: Theme Style module

Activate the built-in **Theme Style** module at **Setup → Modules → Theme Style**. This provides a CSS editor in admin with separate fields for:
- Admin area custom CSS
- Client area custom CSS

Stored in the database — survives file-based updates. Preferred for non-developer admins who want quick CSS tweaks without FTP access.

### When to use hooks instead

Use the asset registry (`register_theme_assets_hook()` / `$CI->app_css->add(..., 'admin')`) when:
- Your CSS is module-scoped and should only load when the module is active
- You need dependency ordering against core scripts
- You're shipping a full custom theme

## Overriding Perfex's Bootstrap 3 — specificity wars

Perfex ships Bootstrap 3.x across admin and client areas, plus inline styles on many core views. Your custom theme CSS will lose most specificity battles by default because:

1. Perfex loads its CSS *after* your custom theme injection (depending on hook order), which means same-specificity selectors favor Perfex.
2. Many Perfex core components use inline `style=""` attributes, which only `!important` overrides.
3. Bootstrap 3 uses `.btn-primary`, `.form-control` etc. — shallow single-class selectors that your `:root` semantic variables won't touch.

### Strategy 1 — scope with a wrapper class (preferred)

Add a theme-root class to your overridden views and scope everything:

```html
<!-- application/views/themes/my_theme/layouts/default.php -->
<body class="my-theme-v2">
```

```css
.my-theme-v2 .btn-primary {
    background: var(--brand-primary);
    border-color: var(--brand-primary);
}
.my-theme-v2 .form-control {
    border-radius: 8px;
    border-color: #e2e8f0;
}
```

Two classes of specificity (`.wrapper .target`) beats Bootstrap's single class (`.target`) without needing `!important`. Scales to any depth.

### Strategy 2 — `!important` with a namespaced helper class

When you can't wrap the parent (e.g., Perfex renders the `<body>` from core):

```css
.my-theme-btn--override {
    background: var(--brand-primary) !important;
}
```

Apply via override of the specific button's view. `!important` on a single namespaced class is safer than `!important` sprinkled across `.btn-primary` globally — the namespace makes it grep-able and removable later.

### Strategy 3 — CSS layer (modern browsers only)

If you know your audience uses modern browsers, `@layer` lets Perfex's styles sit in one layer and yours in a higher one:

```css
@layer perfex, mytheme;
@layer mytheme {
    .btn-primary { background: var(--brand-primary); }
}
```

Doesn't need Perfex to opt in — your `@layer mytheme` wins against any unlayered Perfex CSS. **Caveat:** client-area IE/Safari <15.4 fall back to normal specificity. Perfex admin is power-user territory and usually Chrome/Firefox, but check your audience.

### Anti-patterns

- **Blanket `!important` on every rule.** Quickly becomes a specificity ceiling you can't escape — next override needs `!important` too, then the next. Scope with a wrapper class instead.
- **Using `#wrapper` or other core-internal IDs as your specificity anchor.** Perfex may rename these across versions; your CSS silently breaks.
- **Editing Perfex's `application/views/themes/perfex/` directly.** Blown away on upgrade. Copy to your theme's subtree and edit there — the override mechanism is designed for this.

## Debugging checklist

| Symptom | Likely cause |
|---|---|
| Stale CSS after deploy | Raw paths bust on app version only — use `core_file()`/`core_version()` or append `?t=filemtime()` |
| Registered script never appears in the page | Its `$deps` handle isn't in the customers group (`app-js` is admin-only) — depend on `theme-global-js` |
| POST missing submit button name | jQuery Validate stripping; use hidden action input |
| View not picked up | Wrong theme active, or path case mismatch on Linux |
| Language key shows raw (`onboarding_save` literal) | Language file not loaded, or cached by CI loader |
| FOUC on dark mode | Theme attribute applied after first paint — move to `<head>` inline script |

## Related skills

- **`perfex-core-apis`** — hook mechanics (`accepted_args`), `add_module_support()`.
- **`perfex-security`** — `target="_blank"` + `rel="noopener noreferrer"` and CSRF exclusions for theme-level webhook-style routes.
- **`perfex-module-dev`** — themes usually ship with a companion module for registering language keys and hooks.

## Upstream docs

- Perfex customization guides: https://help.perfexcrm.com/category/customization/
- Applying custom CSS styles (`custom.css` + Theme Style module): https://help.perfexcrm.com/applying-custom-css-styles/
- jQuery Validate: https://jqueryvalidation.org/

---

*Verified against Perfex CRM 3.4.0 core source on 2026-09-15 with `scripts/verify-against-core.sh`. Version-specific notes in the text are from official changelogs.*
