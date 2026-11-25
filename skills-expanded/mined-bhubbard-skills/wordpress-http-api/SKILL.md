---
name: wordpress-http-api
description: WordPress HTTP API for making outbound HTTP/HTTPS requests — wp_remote_get, wp_remote_post, wp_remote_request, wp_safe_remote_*, response retrieval helpers, transports (cURL via WP_Http_Curl, PHP streams via WP_Http_Streams), proxy support (WP_PROXY_HOST etc.), cookies (WP_Http_Cookie), and SSRF protection via wp_http_validate_url. Use when a plugin/theme needs to call an external API, talk to webhooks, fetch remote JSON, or proxy through corporate firewalls.
---

# WordPress HTTP API

The HTTP API is WordPress's wrapper around outbound HTTP requests. It picks a transport at runtime (cURL preferred, PHP streams as fallback), handles redirects, cookies, gzip, chunked encoding, and proxies — so plugin code can stay simple.

**Never** reach for `file_get_contents( $url )`, raw `curl_init`, or `fopen` on URLs. The HTTP API integrates with WordPress filters, respects proxies, and handles SSRF protection — none of which the PHP primitives do.

## The four entry points

```php
// GET — most common.
$response = wp_remote_get( 'https://api.example.com/users', array(
    'timeout'     => 10,
    'redirection' => 5,
    'user-agent'  => 'MyPlugin/1.0 (+https://example.com)',
    'headers'     => array(
        'Accept'        => 'application/json',
        'Authorization' => 'Bearer ' . $token,
    ),
) );

// POST — body is JSON-encoded for you when you pass an array via 'body'.
$response = wp_remote_post( 'https://api.example.com/users', array(
    'headers' => array( 'Content-Type' => 'application/json' ),
    'body'    => wp_json_encode( array( 'name' => 'Alice' ) ),
    'timeout' => 15,
) );

// HEAD — just headers, no body. Cheap for existence checks.
$response = wp_remote_head( $url );

// General — for PUT/DELETE/PATCH or anything else.
$response = wp_remote_request( $url, array( 'method' => 'PUT', 'body' => $body ) );
```

Every call returns either an **array** with `headers`, `body`, `response`, `cookies`, `filename` keys, **or** a `WP_Error` on transport failure. The HTTP status comes back in `$response['response']['code']` — a 4xx or 5xx is still a *successful* request as far as `is_wp_error` is concerned.

```php
if ( is_wp_error( $response ) ) {
    error_log( 'HTTP failed: ' . $response->get_error_message() );
    return;
}
$code = wp_remote_retrieve_response_code( $response );
$body = wp_remote_retrieve_body( $response );
if ( 200 !== $code ) {
    error_log( "Bad status $code: $body" );
    return;
}
$data = json_decode( $body, true );
```

## The `wp_safe_remote_*` variants — use them for any user-supplied URL

`wp_remote_get` will happily fetch `http://localhost:6379/`, `http://169.254.169.254/` (cloud metadata), or `http://10.0.0.5/`. That's **SSRF** waiting to happen.

`wp_safe_remote_get` / `_post` / `_request` / `_head` pass through `wp_http_validate_url()`, which:

- Blocks anything except `http` / `https`.
- Resolves DNS and rejects RFC 1918 private ranges, loopback, link-local.
- Validates redirects every hop, not just the first URL.

```php
// User submitted this URL in a form — always use the safe variant.
$webhook = sanitize_url( $_POST['webhook'] );
$response = wp_safe_remote_post( $webhook, array(
    'body'    => wp_json_encode( $payload ),
    'headers' => array( 'Content-Type' => 'application/json' ),
) );
```

The non-`safe` variant is fine when the URL is hardcoded or built from trusted config.

## Response retrieval helpers

Always go through these — they handle the case where `$response` is unexpectedly malformed:

```php
wp_remote_retrieve_body( $response );              // string
wp_remote_retrieve_response_code( $response );     // int (e.g., 200)
wp_remote_retrieve_response_message( $response );  // 'OK', 'Not Found'
wp_remote_retrieve_headers( $response );           // headers object (iterable)
wp_remote_retrieve_header( $response, 'etag' );    // single header value (case-insensitive)
wp_remote_retrieve_cookies( $response );           // WP_Http_Cookie[]
wp_remote_retrieve_cookie( $response, 'session' ); // WP_Http_Cookie or ''
wp_remote_retrieve_cookie_value( $response, 'session' );  // string
```

## All the request arguments

These are the defaults from `WP_Http::request()`:

```php
$args = array(
    'method'              => 'GET',
    'timeout'             => 5,           // Seconds. Bump for slow APIs.
    'redirection'         => 5,           // Max redirects to follow.
    'httpversion'         => '1.0',       // '1.0' or '1.1'.
    'user-agent'          => 'WordPress/' . $wp_version . '; ' . home_url(),
    'reject_unsafe_urls'  => false,        // True via wp_safe_remote_*.
    'blocking'            => true,         // false = fire-and-forget (no response).
    'headers'             => array(),
    'cookies'             => array(),
    'body'                => null,         // string OR array (form-encoded automatically).
    'compress'            => false,        // gzip the request body.
    'decompress'          => true,         // gunzip the response.
    'sslverify'           => true,         // NEVER set to false in production.
    'sslcertificates'     => ABSPATH . WPINC . '/certificates/ca-bundle.crt',
    'stream'              => false,        // Stream response to file (see below).
    'filename'            => null,         // Required if stream=true.
    'limit_response_size' => null,         // Bytes. Protects against huge responses.
);
```

### Streaming a download to disk

For large files, set `stream => true` and `filename => '/path/to/save'` — the body isn't held in memory:

```php
$tmp = wp_tempnam( 'download' );
$resp = wp_remote_get( $url, array(
    'stream'              => true,
    'filename'            => $tmp,
    'timeout'             => 300,
    'limit_response_size' => 100 * MB_IN_BYTES,
) );
if ( ! is_wp_error( $resp ) && 200 === wp_remote_retrieve_response_code( $resp ) ) {
    // The body is now in $tmp on disk; $resp['body'] is empty.
    rename( $tmp, $final_path );
}
```

### Non-blocking requests

`'blocking' => false` returns immediately with no response data — useful for fire-and-forget webhooks. The request still goes out, but you can't read the result.

## Transports — cURL vs Streams

WordPress picks one at request time. cURL is strongly preferred when available because:

- It supports HTTP/2 (some builds), proper chunked encoding, and connection pooling per-process.
- It implements `CURLOPT_FOLLOWLOCATION` natively.
- It supports request streaming both ways.

The Streams transport is the fallback for hosts without cURL. It uses PHP's stream wrappers and re-implements redirect/cookie handling in PHP.

You generally don't choose — but you can force or block one:

```php
// Disable cURL transport entirely.
add_filter( 'use_curl_transport', '__return_false' );

// Or block streams (rarely needed).
add_filter( 'use_streams_transport', '__return_false' );

// Probe which transports are available for a request:
if ( wp_http_supports( array( 'ssl' ) ) ) { /* ... */ }
if ( wp_http_supports( array( 'stream' ), $url ) ) { /* ... */ }
```

Both transports are in `wp-includes/class-wp-http-curl.php` and `class-wp-http-streams.php`. Their `test()` static methods are what `WP_Http` calls to decide.

## Proxy support — define in wp-config.php

If the WP host sits behind a corporate proxy, define these in `wp-config.php`:

```php
define( 'WP_PROXY_HOST',         '192.168.84.101' );
define( 'WP_PROXY_PORT',         '8080' );
define( 'WP_PROXY_USERNAME',     'user' );          // Optional, basic auth only.
define( 'WP_PROXY_PASSWORD',     'pass' );
define( 'WP_PROXY_BYPASS_HOSTS', 'localhost, *.internal.example.com' );  // Comma-separated, * wildcards.
```

The HTTP API picks up these constants automatically via `WP_HTTP_Proxy` and routes every outbound request through them (except hosts in `WP_PROXY_BYPASS_HOSTS`). Only Basic auth works on most transports; cURL may support NTLM if compiled for it.

## Cookies

Set cookies on outbound requests via the `cookies` arg as `WP_Http_Cookie` instances or `name=value` strings:

```php
$response = wp_remote_get( 'https://example.com/api', array(
    'cookies' => array(
        new WP_Http_Cookie( array( 'name' => 'session', 'value' => $sid, 'domain' => 'example.com' ) ),
    ),
) );
```

Read response cookies via `wp_remote_retrieve_cookies()` or the singular helpers.

## Hosts allowlist for external requests

By default, all outbound requests are allowed. To restrict (e.g., for security or compliance):

```php
// Block ALL external requests:
define( 'WP_HTTP_BLOCK_EXTERNAL', true );

// Then allowlist specific hosts:
define( 'WP_ACCESSIBLE_HOSTS', 'api.wordpress.org, *.cloudflare.com, github.com' );
```

Plugins/themes can also filter via `pre_http_request` to short-circuit or `http_request_args` to mutate args.

## Useful filters

- `pre_http_request` — return non-`null` to short-circuit the entire request (great for stubbing in tests).
- `http_request_args` — last chance to mutate args (add headers, change timeout) before transport.
- `http_response` — modify the response array after a successful request.
- `http_request_redirection_count` — change the default 5 max redirects.
- `http_request_host_is_external` — control which hosts are considered external for the block-external setting.
- `https_local_ssl_verify` / `https_ssl_verify` — selectively disable SSL verify (development only).

## Testing pattern — stub out wp_remote_get

```php
// In tests, return a canned response without touching the network:
add_filter( 'pre_http_request', function ( $pre, $args, $url ) {
    if ( str_contains( $url, 'api.example.com/users' ) ) {
        return array(
            'headers'  => array(),
            'body'     => wp_json_encode( array( 'id' => 1, 'name' => 'Stub' ) ),
            'response' => array( 'code' => 200, 'message' => 'OK' ),
            'cookies'  => array(),
            'filename' => null,
        );
    }
    return $pre;
}, 10, 3 );
```

## Where to look in this codebase

- `wp-includes/http.php` — function-level API (`wp_remote_*`, `wp_safe_remote_*`, retrieval helpers, `wp_http_validate_url`, `wp_parse_url`).
- `wp-includes/class-http.php` and `class-wp-http.php` — the `WP_Http` class that dispatches transports.
- `wp-includes/class-wp-http-curl.php` — cURL transport (`request()`, `stream_headers`, `stream_body`, `test()`).
- `wp-includes/class-wp-http-streams.php` — PHP streams transport, plus `verify_ssl_certificate()` for SAN matching.
- `wp-includes/class-wp-http-proxy.php` — proxy logic; reads the `WP_PROXY_*` constants.
- `wp-includes/class-wp-http-cookie.php` — `WP_Http_Cookie` for in/out cookies.
- `wp-includes/class-wp-http-response.php` and `class-wp-http-requests-response.php` — the response shapes.
- `wp-includes/class-wp-http-encoding.php` — gzip/deflate.
- `wp-includes/Requests/` — vendored Requests library that underlies everything.

## Common pitfalls

- Treating a `WP_Error` and a 4xx/5xx the same. They aren't — `is_wp_error` only catches transport failures. Always also check `wp_remote_retrieve_response_code()`.
- Using `wp_remote_get` with user-supplied URLs. Use `wp_safe_remote_get` to avoid SSRF.
- Setting `sslverify => false` in production. Almost always wrong; if your CA bundle is the issue, ship the right bundle.
- Default `timeout => 5` is short. For LLM-style APIs that take 30s+, raise it explicitly.
- Sending a JSON body without setting `Content-Type: application/json`. The server will treat it as form-encoded and fail.
- Passing an associative array as `body` and expecting JSON. WP form-encodes arrays. Call `wp_json_encode()` yourself for JSON.
- Forgetting that `blocking => false` means no response — useful for true fire-and-forget only.
