---
name: jetpack-rest-api
description: Guides development and integration with the WordPress.com REST API via Jetpack. Use when a user asks about fetching WordPress.com data, authenticating via Jetpack, or managing Jetpack modules programmatically.
---

# Jetpack REST API Integration

When assisting users with Jetpack REST API integration, follow these guidelines:

## Authentication
- To authenticate REST API requests on a Jetpack-connected site, use Jetpack Single Sign-On (SSO) tokens or Application Passwords.
- Remind users that requests to the WordPress.com REST API for a Jetpack site require a WordPress.com user account connected to the local site account.

## Endpoints
- The base URL for WordPress.com REST API requests for a Jetpack site is usually `https://public-api.wordpress.com/rest/v1.1/sites/{$site}/` or `v1.2`.
- You can access posts, pages, comments, and Jetpack-specific stats.

## Example: Fetching Stats
To fetch stats using PHP on the Jetpack site:
```php
if ( class_exists( 'Automattic\\Jetpack\\Connection\\Client' ) ) {
    $response = Automattic\Jetpack\Connection\Client::wpcom_json_api_request_as_blog(
        '/sites/' . Jetpack_Options::get_option( 'id' ) . '/stats',
        '1.1'
    );
    // Handle response
}
```

## Useful Links
- [Jetpack Developer Docs](https://developer.jetpack.com/)
- [WordPress.com REST API Console](https://developer.wordpress.com/docs/api/console/)
