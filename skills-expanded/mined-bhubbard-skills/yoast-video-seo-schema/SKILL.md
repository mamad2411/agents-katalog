---
name: yoast-video-seo-schema
description: "Customizing the VideoObject schema output."
---

# Yoast Video SEO Schema

The Yoast Video SEO plugin injects `VideoObject` schema into the main Yoast Schema `@graph` whenever a video is detected on a page. This tells search engines exactly what the video is about without relying solely on the sitemap.

## Reference
[VideoObject Schema Documentation](https://developer.yoast.com/features/schema/plugins/#yoast-video-seo)

## Core Schema Injection

The plugin maps the video data (fetched from YouTube/Vimeo APIs or entered manually in the meta box) into the `VideoObject` schema piece.

### Modifying the VideoObject Output
You can use the piece-specific filter to alter the schema output for videos.
```php
add_filter( 'wpseo_schema_videoobject', 'modify_yoast_video_schema' );
function modify_yoast_video_schema( $data ) {
    // Example: Add a custom property
    if ( isset( $data['name'] ) && strpos( $data['name'], 'Tutorial' ) !== false ) {
        $data['learningResourceType'] = 'tutorial';
    }
    return $data;
}
```

### Interaction with the Graph
The `VideoObject` is typically referenced by the `WebPage` or `Article` piece in the `@graph` array via the `video` property.

## Best Practices
- Ensure that the video title, description, and tags are properly set in the Yoast Video SEO meta box on the post editor if the automatic API fetch from the video host doesn't pull in optimized metadata. The schema relies heavily on this data.
