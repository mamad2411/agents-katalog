---
name: jetpack-ads
description: Working with Jetpack Ads (WordAds). Use when configuring ad placements, troubleshooting missing ads, or managing ads.txt.
---

# Jetpack Ads (WordAds)

Jetpack allows users to monetize their site using Automattic's WordAds program.

## Ad Placements
Ads can be placed automatically at the Top of each page, Bottom of each post, or Below the Header.
To place an ad programmatically within a theme:
```php
if ( function_exists( 'wordads_display_ad' ) ) {
    wordads_display_ad();
}
```

## Troubleshooting Missing Ads
- **Traffic Minimums**: WordAds requires a certain level of traffic to populate effectively.
- **Ads.txt**: The user must ensure their `ads.txt` file is properly configured. Jetpack usually handles this, but custom firewall rules might block access to it.
- **Site Status**: Ensure the site is Public (not marked as "Discourage search engines").

## Disabling Ads on Specific Pages
You can hide ads on specific posts or pages using a filter:
```php
add_filter( 'wordads_condition_is_active', function( $active ) {
    if ( is_page( 'checkout' ) ) {
        return false;
    }
    return $active;
} );
```
