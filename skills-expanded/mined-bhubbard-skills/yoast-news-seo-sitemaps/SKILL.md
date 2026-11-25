---
name: yoast-news-seo-sitemaps
description: "Customize the Yoast News SEO Google News XML sitemap in WordPress — exclude categories, add custom post types, and follow Google's 48-hour rule. Use when working with Yoast News SEO, the wpseo_news_sitemap filters, a Google News sitemap, or configuring which posts get submitted to Google News."
---

# Yoast News SEO Sitemaps

The Yoast News SEO plugin generates a specialized XML sitemap designed specifically for Google News. By Google's rules, this sitemap must only contain articles published within the last 48 hours.

## Customizing the News Sitemap

### Excluding Specific Categories
If you have a news site but certain categories (e.g., "Sponsored" or "Press Releases") should not be submitted to Google News:
```php
add_filter( 'wpseo_news_sitemap_exclude_categories', 'exclude_categories_from_news' );
function exclude_categories_from_news( $excluded_categories ) {
    // Exclude category ID 15
    $excluded_categories[] = 15;
    return $excluded_categories;
}
```

### Modifying the Post Types
By default, it only includes standard `post` types. If you have a custom post type for news:
```php
add_filter( 'wpseo_news_post_types', 'add_cpt_to_news_sitemap' );
function add_cpt_to_news_sitemap( $post_types ) {
    $post_types[] = 'breaking_news';
    return $post_types;
}
```

## Best Practices
- Never attempt to force older posts (older than 48 hours) into the News sitemap using filters. Google explicitly forbids this and will flag the sitemap with errors in Google Search Console.
- Ensure the publication name in the Yoast News SEO settings exactly matches the name registered in the Google Publisher Center.
