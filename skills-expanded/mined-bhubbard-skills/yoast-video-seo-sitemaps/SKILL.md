---
name: yoast-video-seo-sitemaps
description: "Hooking into the Video XML sitemap generation to include, exclude, or modify video entries."
---

# Yoast Video SEO Sitemaps

The Yoast Video SEO plugin crawls your content to find embedded videos (YouTube, Vimeo, Wistia, etc.) and generates a dedicated `video-sitemap.xml` specifically formatted for Google Video search.

## Customizing the Video Sitemap

### Excluding Posts from the Video Sitemap
If you have a post that contains a video, but you explicitly do not want that video indexed in the video sitemap:
```php
add_filter( 'wpseo_video_sitemap_exclude_post_ids', 'exclude_videos_from_sitemap' );
function exclude_videos_from_sitemap( $post_ids ) {
    $post_ids[] = 123; // Exclude post ID 123
    return $post_ids;
}
```

### Excluding Specific Post Types
By default, the plugin scans all public post types. You can disable scanning for specific types:
```php
add_filter( 'wpseo_video_posttypes', 'limit_video_sitemap_posttypes' );
function limit_video_sitemap_posttypes( $post_types ) {
    // Only look for videos in 'post' and 'movie'
    return array( 'post', 'movie' );
}
```

### Forcing a Custom Thumbnail
Sometimes the plugin cannot fetch the video thumbnail automatically from the provider. You can force a thumbnail via filter:
```php
add_filter( 'wpseo_video_thumbnail', 'custom_video_thumbnail', 10, 2 );
function custom_video_thumbnail( $thumbnail_url, $post_id ) {
    if ( $post_id == 42 ) {
        return 'https://example.com/custom-video-thumb.jpg';
    }
    return $thumbnail_url;
}
```

## Best Practices
- If videos are not showing up in the sitemap, ensure they are embedded using standard oEmbed URLs or standard iframe formats supported by the plugin.
- The Video SEO plugin parses the `post_content` upon save to find videos. If a video is added via a highly customized page builder or shortcode that doesn't render in the backend, the plugin might not see it. In these cases, you might need to manually trigger indexing or use filters to tell the plugin where the video is.
