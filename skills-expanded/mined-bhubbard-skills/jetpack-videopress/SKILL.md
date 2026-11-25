---
name: jetpack-videopress
description: Guidance for customizing VideoPress embeds and APIs. Use when a user needs to modify video player parameters, handle video shortcodes, or interact with the VideoPress API.
---

# VideoPress Customization

VideoPress is Jetpack's ad-free video hosting and playback module.

## Modifying Embed Parameters
You can filter the default parameters passed to the VideoPress player.
```php
add_filter( 'videopress_shortcode_options', function( $options ) {
    $options['autoplay'] = true; // Auto-play videos by default
    $options['controls'] = false; // Hide player controls
    return $options;
} );
```

## Extracting Video Data
If you need to retrieve raw video information (like the direct MP4 URL or poster image) given a VideoPress GUID:
```php
if ( function_exists( 'videopress_get_video_details' ) ) {
    $video_info = videopress_get_video_details( 'video_guid_here' );
    $poster_url = $video_info->poster;
}
```

## Responsive Layouts
VideoPress embeds are automatically responsive. If the user experiences layout issues, advise them to check their theme's `.wp-video` and `.videopress-placeholder` CSS classes.
