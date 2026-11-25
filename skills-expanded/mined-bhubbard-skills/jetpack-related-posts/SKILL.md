---
name: jetpack-related-posts
description: Customizing the Jetpack Related Posts module. Use when a user wants to change how related posts look, filter the results, or move the related posts block.
---

# Jetpack Related Posts Customization

Jetpack's Related Posts module analyzes content to show contextual links at the bottom of posts.

## Changing the Number of Posts
To change the maximum number of related posts displayed (default is 3):
```php
add_filter( 'jetpack_relatedposts_filter_options', function( $options ) {
    $options['size'] = 6;
    return $options;
} );
```

## Excluding Specific Posts or Categories
You can prevent specific posts or categories from appearing in the related posts results.
```php
add_filter( 'jetpack_relatedposts_filter_exclude_post_ids', function( $exclude_post_ids, $post_id ) {
    $exclude_post_ids[] = 123; // Exclude post ID 123
    return $exclude_post_ids;
}, 10, 2 );
```

## Moving the Related Posts Block
If the user wants the related posts to appear somewhere other than the bottom of the content, you can remove the default filter and insert it manually.
```php
// Remove from bottom of content
function remove_jetpack_related_posts() {
    if ( class_exists( 'Jetpack_RelatedPosts' ) ) {
        $jprp = Jetpack_RelatedPosts::init();
        $callback = array( $jprp, 'filter_add_target_to_dom' );
        remove_filter( 'the_content', $callback, 40 );
    }
}
add_action( 'wp', 'remove_jetpack_related_posts', 20 );

// Use echo do_shortcode( '[jetpack-related-posts]' ); in a template file instead.
```
