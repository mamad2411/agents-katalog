---
name: kinsta-wp-caching
description: Guides for managing and troubleshooting WordPress caching on Kinsta's platform, including Server Caching, Edge Caching, and Redis Caching.
---

# Kinsta WordPress Caching Guide

Kinsta provides a powerful, multi-layered caching architecture designed specifically for WordPress. Understanding and managing these caching layers through the MyKinsta dashboard is crucial for maintaining optimal site performance.

## 1. Server Caching (Page Caching)
Kinsta automatically caches full HTML pages at the server level (Nginx). This is the primary caching mechanism.
- **Clearing Cache in MyKinsta:** Go to **WordPress Sites > [Site Name] > Tools > Site Cache** and click **Clear Cache**.
- **Kinsta MU Plugin:** The Kinsta Must-Use (MU) plugin is installed by default on all Kinsta sites. It automatically purges the page cache when you update content (e.g., publishing a post). You can also clear the cache manually from the WordPress admin bar.

## 2. Edge Caching
Edge Caching leverages Cloudflare's global network to serve your site's cached pages from data centers closest to your visitors, drastically reducing Time to First Byte (TTFB).
- **Managing Edge Caching:** Go to **WordPress Sites > [Site Name] > Edge Caching**. Here you can enable, disable, and clear the Edge Cache.
- **Mobile Caching:** If your site generates different HTML for mobile devices, ensure Mobile Caching is enabled in the Edge Caching settings to prevent serving desktop cached pages to mobile users.

## 3. Object Caching (Redis)
For dynamic sites (e.g., WooCommerce, membership sites) where page caching is bypassed, Object Caching is essential. Kinsta offers Redis as an add-on.
- Redis stores the results of database queries in memory, so subsequent requests don't need to query the database again.
- **Enabling Redis:** This requires purchasing the Redis add-on via MyKinsta (**WordPress Sites > [Site Name] > Backups / Add-ons**). Once enabled, Kinsta support will configure it, and you'll typically use a plugin like WP Redis or Redis Object Cache.

## Troubleshooting Cache Issues
- **Bypassing Cache:** If you are seeing outdated content while logged out, the page might be cached. You can bypass Kinsta caching temporarily by appending `/?kcache=bypass` to the end of any URL.
- **Exclusions:** If certain dynamic pages (like carts or checkouts) are being improperly cached, you can request Kinsta Support to add specific URL paths or cookies to the cache exclusion list.

## Best Practices
- Avoid using third-party page caching plugins (like W3 Total Cache or WP Super Cache) as they conflict with Kinsta's server-level caching.
- Always clear the Edge Cache when making significant design or structural changes to the site.
