---
name: wpcom-oauth2
description: Provides guidance on implementing OAuth2 authentication for WordPress.com applications. Trigger when users ask about authenticating, getting access tokens, or managing authorization flows for WP.com.
---
# WordPress.com OAuth2 Authentication

This skill covers the process of obtaining OAuth2 tokens to interact with the WordPress.com REST API on behalf of a user.

## OAuth2 Flow
WordPress.com supports standard OAuth2 flows, primarily the Authorization Code grant type for server-side apps and the Implicit grant type for client-side apps.

### 1. Register an Application
First, register your application at the WordPress.com Developer site to get a `client_id` and `client_secret`.

### 2. Request Authorization
Redirect the user to the WordPress.com authorization endpoint:
```
https://public-api.wordpress.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code
```
If using Implicit flow, use `response_type=token`.

### 3. Get Access Token
If using Authorization Code flow, the user is redirected to your `redirect_uri` with a `code` parameter. Exchange this code for an access token via a POST request:
```http
POST https://public-api.wordpress.com/oauth2/token
Content-Type: application/x-www-form-urlencoded

client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&redirect_uri=YOUR_REDIRECT_URI
&code=THE_CODE_RECEIVED
&grant_type=authorization_code
```

## Scopes
- **global**: Access to all endpoints the user has access to.
- **auth**: Allows using WordPress.com for sign-in (Single Sign-On).

## Best Practices
- Keep your `client_secret` secure. Never expose it in client-side code.
- Store the access token securely.
- Handle token revocation or expiration gracefully.

## Reference
Official documentation: https://developer.wordpress.com/docs/oauth2/
