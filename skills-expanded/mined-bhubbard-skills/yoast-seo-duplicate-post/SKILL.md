---
name: yoast-seo-duplicate-post
description: "Interacting with or extending the Yoast Duplicate Post plugin API."
---

# Yoast Duplicate Post

Yoast Duplicate Post is a widely used plugin (acquired by Yoast) that allows users to clone posts, pages, and custom post types, or copy them to drafts for further editing.

## Reference
[Duplicate Post Documentation](https://developer.yoast.com/duplicate-post/overview/)

## Core Hooks

When a post is cloned, you often need to ensure that specific post meta is NOT copied (like a unique invoice number or a generated UUID), or that specific actions occur after copying.

### `duplicate_post_blacklist_meta_keys`
Filters the list of meta keys that should NOT be copied.
```php
add_filter( 'duplicate_post_blacklist_meta_keys', 'exclude_my_meta_keys' );
function exclude_my_meta_keys( $blacklist ) {
    // Prevent the 'invoice_id' from being copied to the new clone
    $blacklist[] = 'invoice_id';
    return $blacklist;
}
```

### `dp_duplicate_post`
Fires immediately after a post has been successfully duplicated.
```php
add_action( 'dp_duplicate_post', 'action_after_duplication', 10, 3 );
function action_after_duplication( $new_post_id, $post, $status ) {
    // $new_post_id is the ID of the newly created clone
    // $post is the original post object
    
    // Example: Generate a new unique ID for the clone
    update_post_meta( $new_post_id, 'invoice_id', generate_new_invoice_id() );
}
```

### `dp_duplicate_page`
Similar to `dp_duplicate_post`, but fires for pages.

## Best Practices
- If your custom plugin heavily relies on unique post meta, always hook into `duplicate_post_blacklist_meta_keys` to ensure users don't break data integrity when they clone a post.
- The Yoast Duplicate Post settings UI also allows site admins to manually enter meta keys to exclude from copying. Programmatic blacklisting is best for hidden meta keys that start with an underscore (e.g., `_my_hidden_key`).
