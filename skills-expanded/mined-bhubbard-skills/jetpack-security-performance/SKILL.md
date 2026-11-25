---
name: jetpack-security-performance
description: Utilizing Jetpack's security (Protect, Scan) and performance (Boost, Site Accelerator) hooks. Use when configuring CDN cache, modifying lazy loading, or handling brute force protection APIs.
---

# Jetpack Security & Performance

## Site Accelerator (Photon / CDN)
Site Accelerator caches images and static assets on the WordPress.com CDN.
- Use `jetpack_photon_url( $image_url, $args )` to manually generate CDN URLs for images.
- To disable the CDN for a specific image, you can filter `jetpack_photon_skip_image`.

```php
add_filter( 'jetpack_photon_skip_image', function( $skip, $image_url, $args ) {
    if ( strpos( $image_url, 'no-cdn' ) !== false ) {
        return true;
    }
    return $skip;
}, 10, 3 );
```

## Jetpack Boost (Performance)
Jetpack Boost provides Critical CSS and deferral of JS.
- If critical CSS generation fails, check for firewall blocking WordPress.com IPs.
- You can programmatically disable lazy loading for specific images by adding the `data-skip-lazy` attribute or using the `jetpack_lazy_images_skip_image_with_atttributes` filter.

## Jetpack Protect (Security)
Jetpack Protect stops brute force attacks by utilizing a centralized IP blacklist.
- If a user's IP is blocked, they can whitelist it locally in Jetpack > Settings > Security, or you can whitelist programmatically via the `jetpack_protect_whitelist` option.
