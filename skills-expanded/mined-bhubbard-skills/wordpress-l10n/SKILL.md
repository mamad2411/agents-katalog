---
name: wordpress-l10n
description: WordPress localization (l10n) and locale APIs — loading translations (.mo/.po), switching the active locale mid-request via switch_to_locale, working with WP_Locale (formatted dates, day/month names, currency), and per-user locales. Use when translating a plugin or theme, sending an email in the recipient's preferred locale, formatting localized dates and numbers, or building multi-language admin notices. Covers load_textdomain, switch_to_locale, determine_locale, get_locale, and WP_Locale_Switcher.
---

# WordPress Localization (l10n) and Locale Switching

WordPress has separate-but-related concepts:

- **i18n** (internationalization) — marking strings for translation (`__()`, `_e()`, `_n()`, etc.). Covered in the `wordpress-coding-standards` skill.
- **l10n** (localization) — loading and applying translations at runtime, switching locales, formatting locale-specific values like dates and numbers. This skill.

## The locale loading pipeline

When WordPress boots, it figures out which locale to use:

1. `WPLANG` constant (legacy) or the site's `WPLANG` option.
2. `locale` user meta of the current user (per-user setting since WP 4.7).
3. `WP_LANG_DIR` (default: `wp-content/languages/`) for the .mo file.
4. Fallback to `en_US` if no translations are present.

The active locale is what `get_locale()` returns. Use `determine_locale()` for the more nuanced value that respects per-user locale in admin contexts.

```php
$locale = get_locale();               // e.g., 'de_DE'.
$locale = determine_locale();         // Per-user-aware version. Use this in admin code.
```

## Loading translations for a plugin or theme

Since WP 4.6, WordPress automatically loads translations for plugins/themes hosted on .org. For custom or off-org:

```php
// Plugin:
add_action( 'init', function () {
    load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
} );

// Theme:
add_action( 'after_setup_theme', function () {
    load_theme_textdomain( 'my-theme', get_template_directory() . '/languages' );
} );
```

The path is to a directory containing `<textdomain>-<locale>.mo` files, e.g., `languages/my-plugin-de_DE.mo`.

For drop-in just-in-time translation (since WP 4.6), often no manual `load_*_textdomain` call is needed — WordPress loads translations lazily on the first `__()` for a given domain. But explicit loading is still useful when you need to ensure they're loaded before a specific operation.

## Switching locales mid-request

Common scenario: a German user clicks "send invitation" — the invitation email needs to go to a French recipient in French. `switch_to_locale` swaps WordPress's active locale temporarily:

```php
$locale = get_user_meta( $recipient_id, 'locale', true );    // The recipient's preferred locale.
if ( $locale && switch_to_locale( $locale ) ) {
    $subject = __( 'You have a new invitation', 'my-plugin' );
    $body    = __( 'Please click the link to accept...', 'my-plugin' );
    wp_mail( $recipient_email, $subject, $body );
    restore_previous_locale();
}
```

Or switch to a specific user's locale (preferred since WP 6.2 — properly handles users who haven't set a preference):

```php
if ( switch_to_user_locale( $user_id ) ) {
    // Strings translate in the user's locale.
    restore_previous_locale();
}
```

`restore_previous_locale()` pops one off the stack — locale switches nest. To unwind everything: `restore_current_locale()`.

`is_switched()` tells you if you're currently in a switched state.

## Per-user locale

Users can pick their own admin language at Edit Profile → Language. WordPress stores this in `user_meta` key `locale`. Read it with:

```php
$user_locale = get_user_meta( $user_id, 'locale', true );
```

The user-locale flow already applies in admin views — `determine_locale()` returns it. In frontend or cron contexts, you usually want `get_locale()` (site locale) unless you've explicitly switched.

## WP_Locale — formatted dates, days, months

`$GLOBALS['wp_locale']` (also `wp_locale()` since WP 6.4) is a `WP_Locale` instance with the current locale's translated weekday/month names, number formatting, etc.

```php
global $wp_locale;

// Full weekday names:
$days = $wp_locale->weekday;                  // [0 => 'Sunday', 1 => 'Monday', ...] (translated).

// Abbreviated weekday names:
$wp_locale->weekday_abbrev;
$wp_locale->weekday_initial;

// Month names:
$wp_locale->month;                            // [01 => 'January', ...].
$wp_locale->month_abbrev;

// Decimal/thousands separators:
$wp_locale->number_format['decimal_point'];
$wp_locale->number_format['thousands_sep'];

// Get the text direction:
$is_rtl = $wp_locale->is_rtl();               // True for Arabic, Hebrew, Persian, etc.
```

For formatted dates use `date_i18n()` rather than PHP's `date()` — it goes through `WP_Locale` for month/day names:

```php
echo date_i18n( 'l, F j, Y', strtotime( '2026-05-20' ) );    // "Wednesday, May 20, 2026" or its translation.
```

`wp_date()` (since 5.3) is the modern version — accepts a DateTimeZone and returns the timezone-aware string.

## Number formatting

```php
number_format_i18n( 1234567.89, 2 );        // '1,234,567.89' in en_US, '1.234.567,89' in de_DE.
```

## Currency formatting — there's no built-in helper

WordPress doesn't ship a currency formatter (e-commerce plugins like WooCommerce do). Roll your own using `WP_Locale`'s separators or use PHP's `NumberFormatter`:

```php
$fmt = new NumberFormatter( get_locale(), NumberFormatter::CURRENCY );
echo $fmt->formatCurrency( 99.95, 'EUR' );    // '€99,95' or '€99.95' depending on locale.
```

## Plural rules and contexts

(Briefly — full coverage in `wordpress-coding-standards`.) Use `_n()` for plurals, `_x()` for context:

```php
sprintf( _n( '%d comment', '%d comments', $count, 'my-plugin' ), $count );
echo _x( 'Post', 'noun, an article', 'my-plugin' );
echo _x( 'Post', 'verb, to publish', 'my-plugin' );
```

## Just-in-time translation loading

Since WP 4.6, calling `__()` on a domain that isn't loaded triggers an automatic lookup in `WP_LANG_DIR/plugins/<textdomain>-<locale>.mo` or the theme equivalent. This means:

- For .org-hosted plugins, you typically don't need `load_plugin_textdomain` at all.
- For private/custom plugins, you must place translations in `wp-content/languages/plugins/<textdomain>-<locale>.mo` OR call `load_plugin_textdomain` pointing at your bundled `/languages/` directory.

To verify what's loaded:

```php
if ( is_textdomain_loaded( 'my-plugin' ) ) {
    // ...
}
```

## Compiling .po → .mo

```bash
# WP-CLI:
wp i18n make-mo my-plugin/languages/

# Or with msgfmt:
msgfmt my-plugin-de_DE.po -o my-plugin-de_DE.mo
```

WordPress reads `.mo` (compiled binary), not `.po` (source). The .po file is your editing source; .mo is what ships.

## Where to look in this codebase

- `wp-includes/l10n.php` — function API: `__`, `_e`, `_n`, `_x`, `_ex`, `_nx`, `load_textdomain`, `unload_textdomain`, `is_textdomain_loaded`, `load_plugin_textdomain`, `load_theme_textdomain`, `get_locale`, `determine_locale`, `switch_to_locale`, `restore_previous_locale`, `restore_current_locale`.
- `wp-includes/class-wp-locale.php` — `WP_Locale` (`weekday`, `month`, `number_format`, `is_rtl`, etc.).
- `wp-includes/class-wp-locale-switcher.php` — `WP_Locale_Switcher` (the stack-based locale switcher).
- `wp-includes/class-wp-textdomain-registry.php` — registry of loaded .mo files.
- `wp-includes/functions.php` — `date_i18n`, `wp_date`, `number_format_i18n`.
- `wp-includes/pomo/` — the gettext .po/.mo parsers (`PO`, `MO`, `Translation_Entry`, `Translations`).

## Common pitfalls

- Calling `__( $variable, 'my-plugin' )` instead of `__( 'literal', 'my-plugin' )`. Translation tools parse source code — variables can't be extracted. Use `sprintf` if you need composed strings.
- Hardcoding the textdomain as a variable. WPCS requires it to be a literal.
- Not calling `restore_previous_locale()` after `switch_to_locale()`. The site stays in the switched locale for the rest of the request.
- Loading the textdomain on the wrong hook. Plugins on `init`; themes on `after_setup_theme`. Calling earlier may silently miss the load because the locale isn't known yet.
- Using PHP's `date()` for user-facing dates. Use `date_i18n()` / `wp_date()` so month names translate.
- Forgetting that `_n()` requires the count both as the third argument *and* in the format string (the function picks singular/plural; you still have to `sprintf` the number in).
- Shipping a .po file but no .mo. WordPress reads only .mo at runtime.
- Per-user locale not applying to frontend rendering. By design — `determine_locale()` returns site locale on frontend. Use `switch_to_user_locale()` if you want it.
