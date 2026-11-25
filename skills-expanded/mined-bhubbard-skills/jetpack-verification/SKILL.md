---
name: jetpack-verification
description: Handling Jetpack Site Verification Tools. Use when assisting users with adding Pinterest, Google, or Bing verification meta tags.
---

# Jetpack Site Verification Tools

This module allows users to easily add site verification meta tags for search engines and social networks (Google, Bing, Pinterest, Yandex).

## Filtering the Meta Tags
If you need to programmatically add a verification code, or modify an existing one, you can filter the output.

```php
add_filter( 'jetpack_site_verification_output', function( $html ) {
    // Append a custom verification tag
    $html .= '<meta name="custom-verify" content="12345" />';
    return $html;
} );
```

## Adding a Custom Service
You can hook into the Jetpack settings to add a new verification service to the UI, though this requires modifying the Jetpack UI arrays via `jetpack_site_verification_services`.

```php
add_filter( 'jetpack_site_verification_services', function( $services ) {
    $services['my_service'] = array(
        'name' => 'My Custom Service',
        'key'  => 'my_custom_service',
        'format' => '<meta name="my-verify" content="%s" />'
    );
    return $services;
} );
```
