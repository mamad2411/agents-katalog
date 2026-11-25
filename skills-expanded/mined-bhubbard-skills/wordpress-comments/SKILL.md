---
name: wordpress-comments
description: WordPress comments — querying with WP_Comment_Query, inserting and moderating comments, the comments_template/wp_list_comments rendering helpers, custom comment walkers, disabling comments, spam handling. Use when implementing a custom comment form, moderating programmatically, exposing comment counts in a sidebar, restricting comments to certain post types, or building a non-default comment UI. Covers wp_new_comment, wp_insert_comment, wp_set_comment_status, and the comment query API.
---

# WordPress Comments

WordPress comments are stored in `wp_comments` (with optional `wp_commentmeta`). Each comment belongs to a post, has an author (registered user or guest), and a status (`approve`, `hold`, `spam`, `trash`, `0` = unapproved). Comments can be threaded via `comment_parent`.

The comment system is one of WordPress's oldest subsystems, and a frequent target for spam — most production sites use Akismet or disable comments outright.

## Querying comments

```php
$comments = get_comments( array(
    'post_id' => 42,
    'status'  => 'approve',
    'orderby' => 'comment_date_gmt',
    'order'   => 'ASC',
    'number'  => 20,
    'offset'  => 0,
    'type'    => 'comment',          // 'comment' | 'trackback' | 'pingback' | 'pings' | 'all'.
) );

// Or with a query object:
$query = new WP_Comment_Query( array(
    'post_status' => 'publish',
    'author__in'  => array( 1, 2, 3 ),
    'meta_query'  => array(
        array( 'key' => 'flagged', 'value' => '1' ),
    ),
    'fields'      => 'ids',          // Just IDs.
) );

$total = wp_count_comments();         // Returns object with approved/awaiting_moderation/spam/etc counts.
$total = wp_count_comments( $post_id );  // Per-post.

// Single comment:
$c = get_comment( $comment_id );      // WP_Comment object.
```

## Inserting and updating

```php
// Programmatic insert — bypasses spam checks, moderation, notifications.
$id = wp_insert_comment( array(
    'comment_post_ID'      => 42,
    'comment_author'       => 'Alice',
    'comment_author_email' => 'alice@example.com',
    'comment_content'      => 'Nice post!',
    'comment_approved'     => 1,
    'comment_type'         => 'comment',
    'user_id'              => 0,        // 0 = guest.
) );

// User-facing insert — runs spam checks, moderation, sends notification emails.
$result = wp_new_comment( array(
    'comment_post_ID' => 42,
    'comment_author'  => 'Alice',
    'comment_author_email' => 'alice@example.com',
    'comment_content' => 'Nice post!',
), $wp_error = true );

// Update:
wp_update_comment( array(
    'comment_ID'      => 99,
    'comment_content' => 'Edited content',
), $wp_error = true );

// Status changes:
wp_set_comment_status( 99, 'approve' );    // 'approve' | 'hold' | 'spam' | 'trash' | 'delete'.
wp_trash_comment( 99 );
wp_delete_comment( 99, $force = true );    // Bypass trash.

// Bulk count refresh (call after manual DB changes):
wp_update_comment_count( $post_id );
```

**Use `wp_new_comment` for anything user-supplied.** It runs `wp_check_comment_data`, `wp_check_comment_flood`, `wp_check_comment_disallowed_list`, and the moderation queue logic. `wp_insert_comment` skips all of that — only safe for known-trusted inserts (e.g., migrations).

## Rendering comments in templates

The classic theme pattern (`comments.php` in the theme):

```php
<?php
if ( comments_open() || get_comments_number() ) :
    if ( post_password_required() ) return;
?>

<h2><?php comments_number(); ?></h2>

<ol class="comment-list">
    <?php
    wp_list_comments( array(
        'style'        => 'ol',
        'short_ping'   => true,
        'avatar_size'  => 60,
        'walker'       => new MyTheme_Comment_Walker(),     // Optional custom walker.
        'callback'     => 'mytheme_comment_callback',       // Or a callable for full control.
    ) );
    ?>
</ol>

<?php paginate_comments_links(); ?>

<?php comment_form(); ?>

<?php endif; ?>
```

`comments_template( '/comments.php' )` is what `single.php` calls to include this file. `wp_list_comments` walks the comment tree and emits HTML using either a callback or `Walker_Comment` (default).

## comment_form() — the default comment form

```php
comment_form( array(
    'title_reply'         => __( 'Leave a Reply', 'mytheme' ),
    'label_submit'        => __( 'Post Comment', 'mytheme' ),
    'comment_notes_before'=> '',
    'comment_notes_after' => '',
    'class_form'          => 'comment-form',
    'fields'              => array(
        // Override individual fields, or remove with => false.
        'url' => false,
    ),
) );
```

This generates the entire form including nonce, hidden fields for parent comment (for threading), and the `<form action="<?php echo site_url('/wp-comments-post.php'); ?>" method="post">` wrapper. `wp-comments-post.php` (in WordPress root) is the handler.

## Disabling comments

```php
// Site-wide via filters:
add_filter( 'comments_open',  '__return_false', 20, 2 );
add_filter( 'pings_open',     '__return_false', 20, 2 );
add_filter( 'comments_array', '__return_empty_array', 10, 2 );

// Disable for a specific post type:
add_action( 'init', function () {
    remove_post_type_support( 'page', 'comments' );
    remove_post_type_support( 'page', 'trackbacks' );
} );

// Hide the menu in admin:
add_action( 'admin_menu', function () {
    remove_menu_page( 'edit-comments.php' );
} );

// Remove the comment count from the admin bar:
add_action( 'wp_before_admin_bar_render', function () {
    global $wp_admin_bar;
    $wp_admin_bar->remove_menu( 'comments' );
} );
```

For brand-new sites, the cleanest option is to set `Settings → Discussion → Allow people to submit comments on new posts` off. For existing sites with comment history, the filters above are the way.

## Moderation pipeline

When `wp_new_comment` runs:

1. `wp_check_comment_data_max_lengths` — length limits.
2. `wp_check_comment_disallowed_list` — blocklist regex match against author/email/url/content/IP/UA.
3. `wp_check_comment_flood` (filter) — flood control (same IP/email posting rapidly).
4. `pre_comment_approved` filter — final decision: `0` (hold for moderation), `1` (approved), `'spam'`, `'trash'`.
5. `comment_post` action — fired after insert.
6. `wp_new_comment_notify_moderator` — if held, email site admin.
7. `wp_new_comment_notify_postauthor` — if approved, email post author.

Customize the held-vs-approved decision:

```php
add_filter( 'pre_comment_approved', function ( $approved, $commentdata ) {
    // Auto-approve if the author has a previous approved comment AND the content is short.
    if ( strlen( $commentdata['comment_content'] ) < 500
         && did_author_previously_comment( $commentdata['comment_author_email'] ) ) {
        return 1;
    }
    return $approved;
}, 10, 2 );
```

## Spam — Akismet and friends

Without anti-spam, public WordPress sites get hammered. Akismet (bundled) is the standard. Alternatives: Antispam Bee, Cleantalk, FAQ-style honeypot plugins.

If rolling your own:

```php
// Honeypot field — bots fill every field; real users won't see this one.
add_action( 'comment_form_after_fields', function () {
    echo '<p style="display:none"><input name="please_leave_blank" /></p>';
} );

add_filter( 'preprocess_comment', function ( $commentdata ) {
    if ( ! empty( $_POST['please_leave_blank'] ) ) {
        wp_die( 'Spam detected.' );
    }
    return $commentdata;
} );
```

## Custom comment walker

When you want fully custom HTML per comment, subclass `Walker_Comment`:

```php
class MyTheme_Comment_Walker extends Walker_Comment {
    protected function html5_comment( $comment, $depth, $args ) {
        $tag = ( 'div' === $args['style'] ) ? 'div' : 'li';
        ?>
        <<?php echo $tag; ?> id="comment-<?php comment_ID(); ?>" <?php comment_class( $this->has_children ? 'parent' : '', $comment ); ?>>
            <article>
                <header>
                    <?php echo get_avatar( $comment, $args['avatar_size'] ); ?>
                    <b><?php comment_author_link( $comment ); ?></b>
                    <time><?php comment_date(); ?></time>
                </header>
                <div class="comment-body"><?php comment_text(); ?></div>
                <?php comment_reply_link( array_merge( $args, array(
                    'depth'     => $depth,
                    'max_depth' => $args['max_depth'],
                ) ) ); ?>
            </article>
        <?php
    }
}

wp_list_comments( array( 'walker' => new MyTheme_Comment_Walker() ) );
```

(See the `wordpress-walker` skill for the walker pattern in depth.)

## Where to look in this codebase

- `wp-includes/comment.php` — function API: `get_comment`, `wp_insert_comment`, `wp_new_comment`, `wp_update_comment`, `wp_delete_comment`, `wp_trash_comment`, `wp_set_comment_status`, `wp_check_comment_data`, `wp_count_comments`.
- `wp-includes/comment-template.php` — template helpers: `comments_template`, `wp_list_comments`, `comment_form`, `comment_author`, `comment_text`, `paginate_comments_links`.
- `wp-includes/class-wp-comment.php` — `WP_Comment`.
- `wp-includes/class-wp-comment-query.php` — `WP_Comment_Query`.
- `wp-includes/class-walker-comment.php` — the default walker.
- `wp-comments-post.php` (WordPress root) — the form handler for `<form action="...wp-comments-post.php">`.

## Common pitfalls

- Calling `wp_insert_comment` for user-submitted data and bypassing all spam checks. Use `wp_new_comment`.
- Echoing `comment_text()` without `esc_*`. The default applies `the_content` filter which allows HTML — but for partial-trust contexts (e.g., admin tables) escape with `esc_html` or `wp_kses`.
- Threading depth — `Settings → Discussion → Enable threaded comments` controls whether `comment_parent` is honored. Themes that don't pass `max_depth` to `wp_list_comments` get unexpected nesting.
- `get_comments_number()` vs `wp_count_comments()` — the former is per-post (uses cached `comment_count` on the post row); the latter is site-wide.
- Forgetting `wp_update_comment_count` after manual DB changes — the post's `comment_count` column gets stale.
- Letting the default Akismet "delete spam after 15 days" policy run while also relying on spam comments for analytics. Configure it intentionally.
- Believing trackbacks/pingbacks are useful in 2026. They're almost entirely spam. Disable in `Settings → Discussion`.
- Using `Settings → Discussion → Show avatars` for performance-critical sites without caching — Gravatar's free CDN can be slow. Use `get_avatar_url` and cache the result.
