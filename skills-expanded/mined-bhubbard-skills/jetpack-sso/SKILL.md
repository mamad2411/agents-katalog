---
name: jetpack-sso
description: Implementing and customizing WordPress.com Single Sign-On for self-hosted sites. Use when a user wants to force SSO, match accounts automatically, or customize the login screen.
---

# Jetpack SSO (Single Sign-On) Implementation

Jetpack SSO allows users to log into a self-hosted WordPress site using their WordPress.com credentials.

## Forcing SSO
To bypass the default WordPress login form and force users directly to WordPress.com to authenticate:
```php
add_filter( 'jetpack_sso_bypass_login_forward_wpcom', '__return_true' );
```

## Automatically Matching Users
If you want Jetpack to automatically log a user in if their WordPress.com email matches a local user email (without them having to link accounts explicitly beforehand):
```php
add_filter( 'jetpack_sso_match_by_email', '__return_true' );
```

## Customizing the Login Form
You can hide the default WordPress login form so only the SSO button is visible.
```php
add_filter( 'jetpack_remove_login_form', '__return_true' );
```

## Preventing New User Registration
By default, if an unknown WordPress.com user logs in via SSO, they might be rejected if registration is closed. You can allow SSO to create accounts even if global registration is closed:
```php
add_filter( 'jetpack_sso_default_role', function() {
    return 'subscriber'; // Return the role to assign to new SSO users
} );
```
