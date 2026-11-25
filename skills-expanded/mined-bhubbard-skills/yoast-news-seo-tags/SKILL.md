---
name: yoast-news-seo-tags
description: "Modifying specific News meta tags like news_keywords and standalone robots tags."
---

# Yoast News SEO Tags

While `news_keywords` is largely deprecated by Google, the Yoast News SEO plugin still manages specific metadata output for news articles, including specific robots directives for Google News.

## Key Filters

### Google News Robots
Sometimes you want an article indexed in regular Google Search, but explicitly blocked from Google News. The plugin outputs a `<meta name="Googlebot-News">` tag.

```php
add_filter( 'wpseo_news_robots', 'modify_news_robots' );
function modify_news_robots( $robots ) {
    // Block a specific category from Google News
    if ( has_category( 'internal-updates' ) ) {
        return 'noindex, nofollow';
    }
    return $robots;
}
```

### Stock Tickers
If your news site covers finance, the plugin allows tagging articles with stock tickers. You can filter this array programmatically.
```php
add_filter( 'wpseo_news_stock_tickers', 'add_custom_stock_tickers' );
function add_custom_stock_tickers( $tickers ) {
    $tickers[] = 'NASDAQ:GOOGL';
    return $tickers;
}
```

## Best Practices
- Focus efforts on Schema (`NewsArticle`) rather than legacy meta tags like `news_keywords`. Google relies heavily on structured data for the Top Stories carousel.
