---
name: jetpack-akismet
description: Integrating and troubleshooting Akismet Anti-Spam. Use when handling comment spam, contact form spam, or custom form integration.
---

# Akismet Anti-Spam Integration

Akismet is Automattic's premier anti-spam service, tightly integrated with Jetpack.

## Protecting Custom Forms
If you are building a custom form, you can send the submission data to the Akismet API to determine if it's spam.

```php
$response = Akismet::http_post( $request_args, 'comment-check' );
if ( 'true' == $response[1] ) {
    // This is spam. Handle accordingly.
}
```
*Note: Ensure the `Akismet` class is available before calling its methods.*

## Contact Form 7 and Gravity Forms
Akismet natively integrates with many popular form plugins.
- **Contact Form 7**: Add `akismet:author`, `akismet:author_email`, etc., to the form fields.
- **Gravity Forms**: Enable the Akismet integration in the form settings.

## Debugging
If legitimate comments are being marked as spam (false positives), the user must find the comment in the Spam folder and mark it as "Not Spam" so the Akismet machine learning algorithm can adjust.
