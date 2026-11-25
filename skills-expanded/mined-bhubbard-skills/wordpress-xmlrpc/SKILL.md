---
name: wordpress-xmlrpc
description: WordPress XML-RPC — the legacy /xmlrpc.php endpoint server, and the IXR_Client / WP_HTTP_IXR_Client for outbound XML-RPC calls. Use when integrating with old desktop blogging clients, when receiving pingbacks/trackbacks, when calling another WordPress site's XML-RPC API from PHP, or when hardening a site by disabling XML-RPC. Covers the wp.* and metaWeblog.* method namespaces, pingback handling, and why XML-RPC is usually safer disabled.
---

# WordPress XML-RPC

`/xmlrpc.php` at the WordPress root exposes a legacy XML-RPC API. It predates the REST API (REST landed in 4.7) and is still enabled by default, mostly for backward compatibility with:

- Old desktop blogging tools (Windows Live Writer, MarsEdit pre-REST).
- Mobile apps that predate the REST endpoints.
- Pingback and trackback notifications.

For new integrations, **use the REST API**. XML-RPC is also a perennial brute-force / amplification target — most sites should disable it.

## What's exposed

The `WP_XMLRPC_Server` class in `wp-includes/class-wp-xmlrpc-server.php` registers methods in several namespaces:

| Namespace | Examples | Purpose |
| --- | --- | --- |
| `wp.*` | `wp.getPosts`, `wp.newPost`, `wp.editPost`, `wp.getTaxonomies`, `wp.uploadFile` | WordPress-native methods (most complete). |
| `metaWeblog.*` | `metaWeblog.newPost`, `metaWeblog.editPost`, `metaWeblog.getRecentPosts` | MetaWeblog API — the historical standard. |
| `mt.*` | `mt.publishPost`, `mt.getCategoryList` | Movable Type API. |
| `blogger.*` | `blogger.getRecentPosts`, `blogger.editPost` | Blogger API (predates everything). |
| `pingback.*` | `pingback.ping`, `pingback.extensions.getPingbacks` | Pingback protocol. |
| `demo.*` | `demo.sayHello`, `demo.addTwoNumbers` | XML-RPC test methods. |
| `system.*` | `system.listMethods`, `system.multicall` | Introspection. |

## Disabling XML-RPC (recommended for most sites)

There are three flavors of "off":

```php
// 1. Disable the whole protocol response (server returns false to every call).
add_filter( 'xmlrpc_enabled', '__return_false' );

// 2. Block at the URL level via .htaccess (Apache):
// <Files xmlrpc.php>
//     Order Deny,Allow
//     Deny from all
// </Files>

// 3. Block in nginx:
// location = /xmlrpc.php { deny all; }

// 4. Disable just pingbacks (a common amplification vector):
add_filter( 'xmlrpc_methods', function ( $methods ) {
    unset( $methods['pingback.ping'] );
    unset( $methods['pingback.extensions.getPingbacks'] );
    return $methods;
} );
```

The `xmlrpc_enabled` filter is the cleanest — it keeps the endpoint responding (so external clients get a clear error) but disables auth and method dispatch.

## When you actually need it

- A WordPress mobile app from before ~5.x that hasn't migrated to REST.
- A self-hosted JetPack/Akismet flow that depends on it (most modern Jetpack uses REST now).
- Integrating with very old CMSes that only speak XML-RPC.
- Acting as a pingback/trackback receiver — though pingbacks are widely abused for spam and many sites disable them.

## Custom XML-RPC methods

You can add your own method to the endpoint:

```php
add_filter( 'xmlrpc_methods', function ( $methods ) {
    $methods['myplugin.getInventory'] = 'myplugin_xmlrpc_get_inventory';
    return $methods;
} );

function myplugin_xmlrpc_get_inventory( $args ) {
    global $wp_xmlrpc_server;

    // Standard XML-RPC arg order: [blog_id, username, password, ...]
    $blog_id  = (int)   $args[0];
    $username = (string) $args[1];
    $password = (string) $args[2];

    $user = $wp_xmlrpc_server->login( $username, $password );
    if ( ! $user ) {
        return $wp_xmlrpc_server->error;
    }

    if ( ! user_can( $user, 'edit_posts' ) ) {
        return new IXR_Error( 401, __( 'You are not allowed.', 'myplugin' ) );
    }

    return array( 'count' => myplugin_get_inventory_count() );
}
```

Note: XML-RPC accepts username+password in the request body. If you must keep XML-RPC enabled, **at minimum** require Application Passwords (not real user passwords) and rate-limit `/xmlrpc.php` at the proxy.

## Calling an XML-RPC server from PHP (WP_HTTP_IXR_Client)

WordPress bundles the IXR (Incutio XML-RPC) library. The WP subclass `WP_HTTP_IXR_Client` routes calls through WordPress's HTTP API (with proxy, SSL verify, timeouts):

```php
include_once ABSPATH . WPINC . '/class-IXR.php';
include_once ABSPATH . WPINC . '/class-wp-http-ixr-client.php';

$client = new WP_HTTP_IXR_Client( 'https://other-site.example.com/xmlrpc.php' );
$client->useragent = 'MyPlugin/1.0';
$client->timeout   = 10;

$success = $client->query(
    'wp.getPosts',
    1,                       // blog_id
    'username',
    'password',              // Or an Application Password.
    array( 'number' => 5 )
);

if ( ! $success ) {
    return new WP_Error( 'xmlrpc_error', $client->getErrorMessage() );
}

$posts = $client->getResponse();
```

`IXR_Error` is the error type the protocol uses; `getErrorMessage` and `getErrorCode` work after a failed `query()`.

## Pingbacks — the legacy "this post links to yours" notification

`pingback.ping` is the method old WordPress installs call when one post links to another. The receiver fetches the linking URL, verifies the link exists, and creates a comment of type `pingback`. By default this is enabled — and is the source of a huge volume of spam.

Disable:

```php
// Stop sending pingbacks:
add_filter( 'option_default_pingback_flag',  '__return_zero' );
add_filter( 'option_default_ping_status',    fn() => 'closed' );

// Stop receiving (handled by the xmlrpc_methods filter above).
```

## Why XML-RPC is a security concern

- **Brute force amplification**: `system.multicall` accepts a batch of method invocations. Attackers send one HTTP request that tries hundreds of `wp.getUsersBlogs` login attempts. WAFs that rate-limit by request count miss it.
- **Pingback DDoS amplification**: an attacker triggers your site to pingback a target, multiplying their requests by however many WordPress sites they leverage.
- **Method enumeration**: `system.listMethods` reveals plugin-added methods.

Mitigations: disable entirely if you don't use it. If you use it, block `system.multicall` (`xmlrpc_methods` filter), require Application Passwords, and rate-limit at the edge.

## Where to look in this codebase

- `xmlrpc.php` (in the WordPress root) — the entry script.
- `wp-includes/class-wp-xmlrpc-server.php` — the entire `WP_XMLRPC_Server` class with all methods.
- `wp-includes/class-IXR.php` — the vendored IXR library (`IXR_Client`, `IXR_Server`, `IXR_Message`, `IXR_Value`, `IXR_Error`, `IXR_Date`, `IXR_Base64`).
- `wp-includes/class-wp-http-ixr-client.php` — WP's HTTP-API-backed subclass.
- `wp-includes/IXR/` — IXR class files.
- `wp-includes/atomlib.php` — used by `AtomPub` endpoints (also legacy).

## Common pitfalls

- Leaving XML-RPC enabled on a site that doesn't use it. Easy SSRF / brute-force surface.
- Filtering out methods incompletely. `system.multicall` can call any other method — block it explicitly along with the ones you're worried about.
- Sending real user passwords over XML-RPC in plugin code. Use Application Passwords.
- Using `IXR_Client` directly instead of `WP_HTTP_IXR_Client`. The former uses PHP socket functions without proxy/SSL config; the latter goes through WP's HTTP API.
- Assuming a `false` from `$client->query()` means "method missing." It might also mean a network error — check `$client->getErrorCode()` to distinguish.
- Trusting `pingback.ping` payloads without verifying the linking post actually exists and points back. WordPress does this verification by default; custom handlers must replicate it.
- Building a new integration on XML-RPC. Use REST. XML-RPC is maintained only for backward compatibility.
