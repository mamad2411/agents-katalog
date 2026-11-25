---
name: yoast-video-seo-api
description: "Forcing video re-indexing or retrieving video metadata programmatically."
---

# Yoast Video SEO API

The Yoast Video SEO plugin provides internal API methods to force indexing of videos or to fetch video metadata programmatically.

## Fetching Video Data
When a post is saved, Yoast attempts to extract video URLs and ping the relevant oEmbed endpoints (like YouTube or Vimeo) to fetch metadata (duration, thumbnails, titles). This data is stored in post meta.

### Reading Video Meta
You can read the cached video data from the post meta:
```php
// Returns an array of video data for the post
$video_data = get_post_meta( $post_id, '_wpseo_video_data', true );
```

## Programmatic Re-indexing
If you import posts in bulk using a script, the Video SEO plugin might not automatically trigger its video-discovery routine because `save_post` might be bypassed or fired without the correct context.

You can trigger the indexing manually using the plugin's classes (Note: internal class names may vary slightly across versions).

```php
if ( class_exists( 'WPSEO_Video_Index' ) ) {
    $video_index = new WPSEO_Video_Index();
    // Force the plugin to scan the post content for videos and cache the metadata
    $video_index->index_post( $post_id );
}
```

## Best Practices
- Avoid running the `index_post` routine synchronously during a bulk import of thousands of posts, as the external API calls to YouTube/Vimeo will cause severe performance issues or timeouts. Offload this to a background task or WP Cron job.
