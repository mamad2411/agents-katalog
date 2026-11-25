---
name: wordpress-mail
description: Sending email from WordPress via wp_mail and customizing PHPMailer (the underlying SMTP/mail library). Use when sending transactional email, switching to SMTP, attaching files, sending HTML email with inline images (embeds), changing the From address, listening for delivery failures via wp_mail_failed, or replacing wp_mail entirely (it's a pluggable function). Covers WP 6.9+ embeds parameter and the wp_mail_* filters.
---

# WordPress Mail (wp_mail)

`wp_mail()` is WordPress's email entry point. It's a **pluggable function** — any plugin can replace it entirely — but the default implementation in `wp-includes/pluggable.php` wraps PHPMailer with WordPress-style filter hooks.

## The signature

```php
wp_mail(
    string|string[] $to,                     // Recipient(s). String or array of addresses.
    string          $subject,
    string          $message,
    string|string[] $headers     = '',       // Extra headers, string or string[].
    string|string[] $attachments = array(),  // Paths to files to attach.
    string|string[] $embeds      = array()   // Paths to files to embed (cid:). Since 6.9.0.
): bool                                       // True = handed to SMTP/sendmail without error.
```

**A `true` return does not mean the email was delivered.** It only means the transport accepted it. Bounce handling lives downstream.

## Basic sends

```php
// Plain text:
wp_mail( 'alice@example.com', 'Hello', 'A simple plain-text message.' );

// HTML — flip the content type via filter:
add_filter( 'wp_mail_content_type', fn() => 'text/html' );
wp_mail( 'alice@example.com', 'Welcome', '<h1>Welcome</h1><p>Hi <strong>Alice</strong>.</p>' );
remove_filter( 'wp_mail_content_type', '...' );    // Restore default for other emails.

// Multiple recipients (the To header):
wp_mail( array( 'alice@example.com', 'bob@example.com' ), 'Heads up', 'Notice for both.' );
```

The default content type is `text/plain`. Forgetting to set HTML is the #1 reason HTML emails arrive as raw markup.

## Headers — Cc, Bcc, Reply-To, From, custom

Headers can be a single string with `\r\n` between entries, or an array of header lines:

```php
$headers = array(
    'From: Acme <no-reply@acme.example>',
    'Reply-To: support@acme.example',
    'Cc: manager@acme.example',
    'Bcc: archive@acme.example',
    'Content-Type: text/html; charset=UTF-8',
    'X-Custom-Header: tracking-id-123',
);
wp_mail( 'alice@example.com', 'Subject', '<p>Body</p>', $headers );
```

Setting `From:` in headers takes precedence over the `wp_mail_from` filter. If neither is set, WordPress uses `wordpress@<your-domain>`, which is usually flagged as spam by SPF/DMARC. **Always set a From address that's on the site's domain.**

## Attachments and embeds

Attachments are files served as downloadable parts. Embeds (since WP 6.9) are inline content referenced from HTML via `cid:`.

```php
wp_mail(
    'alice@example.com',
    'Your receipt',
    '<p>See attached PDF. Logo below:</p><img src="cid:logo" alt="Logo">',
    array( 'Content-Type: text/html; charset=UTF-8' ),
    array( WP_CONTENT_DIR . '/uploads/2026/05/receipt-123.pdf' ),     // Attachments.
    array( 'logo' => WP_CONTENT_DIR . '/themes/mytheme/img/logo.png' ) // Embeds: key becomes cid.
);
```

Embed CIDs default to the array key. To override, use the `wp_mail_embed_args` filter. Use embeds (not attachments) for logos and inline images so they render in the body without being separately downloadable.

## The filters — change anything without overriding wp_mail

| Filter | What you can change |
| --- | --- |
| `wp_mail` | The whole args array (`to`, `subject`, `message`, `headers`, `attachments`, `embeds`) before processing. |
| `wp_mail_from` | The From address. |
| `wp_mail_from_name` | The From display name. |
| `wp_mail_content_type` | `text/plain` or `text/html`. |
| `wp_mail_charset` | Defaults to site charset (usually UTF-8). |
| `wp_mail_embed_args` | Per-embed Content-ID, filename, etc. |

```php
add_filter( 'wp_mail_from',      fn() => 'no-reply@example.com' );
add_filter( 'wp_mail_from_name', fn() => 'Acme Notifications' );
```

## The action hooks — observe sends

```php
// Fires right before PHPMailer->send(). You can mutate the $phpmailer instance directly.
add_action( 'phpmailer_init', function ( $phpmailer ) {
    $phpmailer->SMTPDebug = 2;       // For debugging only.
    $phpmailer->isSMTP();
    $phpmailer->Host       = 'smtp.example.com';
    $phpmailer->Port       = 587;
    $phpmailer->SMTPAuth   = true;
    $phpmailer->Username   = getenv( 'SMTP_USER' );
    $phpmailer->Password   = getenv( 'SMTP_PASS' );
    $phpmailer->SMTPSecure = 'tls';
} );

// Fires when sending fails. Receives a WP_Error.
add_action( 'wp_mail_failed', function ( WP_Error $error ) {
    error_log( 'Mail failed: ' . $error->get_error_message() );
    error_log( 'Context: ' . print_r( $error->get_error_data(), true ) );
} );

// Fires after a successful send (since WP 5.9).
add_action( 'wp_mail_succeeded', function ( array $mail_data ) {
    // $mail_data has the to/subject/headers/etc.
} );
```

## Switching to SMTP

WordPress uses PHP's `mail()` by default. On most hosts this works poorly — outbound mail gets flagged or silently dropped. Use an SMTP relay (SendGrid, Postmark, Mailgun, SES, etc.) via the `phpmailer_init` hook:

```php
add_action( 'phpmailer_init', function ( $phpmailer ) {
    $phpmailer->isSMTP();
    $phpmailer->Host       = 'smtp.postmarkapp.com';
    $phpmailer->Port       = 587;
    $phpmailer->SMTPAuth   = true;
    $phpmailer->Username   = MY_SMTP_USER;       // From wp-config.php constants.
    $phpmailer->Password   = MY_SMTP_PASS;
    $phpmailer->SMTPSecure = PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_STARTTLS;
    $phpmailer->From       = 'no-reply@example.com';
    $phpmailer->FromName   = 'Example';
} );
```

For DKIM signing, set `$phpmailer->DKIM_*` properties — see the PHPMailer docs.

## PHPMailer is a vendored library

WordPress ships PHPMailer at `wp-includes/PHPMailer/`. Always use it via the `phpmailer_init` hook — don't `require` it directly. The class is autoloaded into the global PHP namespace via `wp-includes/class-phpmailer.php` (a compatibility shim) and `wp-includes/class-wp-phpmailer.php` (WP's subclass that wires up the WP-specific filters).

Don't pin a specific PHPMailer version in your plugin — WordPress upgrades it.

## Replacing wp_mail entirely

Because `wp_mail` is pluggable, you can override it before WordPress loads its own:

```php
// In a mu-plugin so it loads before plugins:
if ( ! function_exists( 'wp_mail' ) ) {
    function wp_mail( $to, $subject, $message, $headers = '', $attachments = array() ) {
        // Send via an HTTP API instead of SMTP — e.g., Postmark.
        $resp = wp_remote_post( 'https://api.postmarkapp.com/email', array(
            'headers' => array(
                'X-Postmark-Server-Token' => POSTMARK_TOKEN,
                'Content-Type'            => 'application/json',
            ),
            'body' => wp_json_encode( array(
                'From'     => 'no-reply@example.com',
                'To'       => is_array( $to ) ? implode( ',', $to ) : $to,
                'Subject'  => $subject,
                'HtmlBody' => $message,
            ) ),
        ) );
        return ! is_wp_error( $resp ) && 200 === wp_remote_retrieve_response_code( $resp );
    }
}
```

But unless you specifically need to replace it, prefer the `phpmailer_init` SMTP route — you keep all the WP filters, attachments, embeds, multipart handling, etc.

## Testing email locally

Set up MailHog or Mailpit as an SMTP capture server (no real delivery, web UI to view sent mail):

```php
add_action( 'phpmailer_init', function ( $phpmailer ) {
    $phpmailer->isSMTP();
    $phpmailer->Host = 'mailhog';        // Or 'localhost'.
    $phpmailer->Port = 1025;
    $phpmailer->SMTPAuth = false;
    $phpmailer->SMTPSecure = '';
} );
```

Or short-circuit `wp_mail` entirely in tests:

```php
add_filter( 'pre_wp_mail', function ( $null, $atts ) {
    $GLOBALS['captured_mail'][] = $atts;
    return true;        // Skip actually sending. Returning a non-null short-circuits.
}, 10, 2 );
```

## Where to look in this codebase

- `wp-includes/pluggable.php` — the `wp_mail()` function itself (search for `function wp_mail`).
- `wp-includes/class-wp-phpmailer.php` — WP's PHPMailer subclass with WP-specific wiring.
- `wp-includes/class-phpmailer.php` — compatibility shim mapping `PHPMailer` to the namespaced class.
- `wp-includes/PHPMailer/` — the vendored library (`PHPMailer.php`, `SMTP.php`, `Exception.php`).
- `wp-includes/class-wp-recovery-mode-email-service.php` — example of WordPress's own recovery-email sending.

## Common pitfalls

- Treating a `true` return as proof of delivery. It isn't — it means accepted by the transport, not delivered.
- Sending HTML without setting `Content-Type: text/html`. Set it via header line *or* `wp_mail_content_type` filter — not both, or the filter will lose to the header.
- Leaving the default From (`wordpress@<host>`). SPF/DKIM/DMARC will mark it as spam. Always override.
- Re-adding a `wp_mail_content_type` filter and never removing it, then wondering why later plain-text emails arrive as HTML. Remove after the send, or scope it more tightly.
- Using `$phpmailer->Body` inside `phpmailer_init` to do find-replace. The body has already been set by then — use the `wp_mail` filter on `$atts['message']` to mutate before.
- Forgetting that `wp_mail_failed` only fires for exceptions thrown by PHPMailer, not for legitimate bounces (those happen days later at the receiving server).
- Hardcoding SMTP credentials in code. Put them in `wp-config.php` as constants or env vars.
