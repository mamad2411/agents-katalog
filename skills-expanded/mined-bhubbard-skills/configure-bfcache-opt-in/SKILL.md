---
name: configure-bfcache-opt-in
description: Configure or disable the Remember Me opt-in behavior for the Instant Back/Forward (nocache-bfcache) WordPress plugin.
---

# Configure BFCache Opt-In

When using the Instant Back/Forward plugin, by default it only enables bfcache if the user checks the "Remember Me" checkbox when logging in. This skill provides instructions on how to disable this opt-in behavior so that all logged-in users receive the bfcache benefit.

## Instructions

1. Use the `nocache_bfcache_use_remember_me_as_opt_in` filter.
2. Add the following code to a custom plugin or your theme's `functions.php`:

```php
add_filter( 'nocache_bfcache_use_remember_me_as_opt_in', '__return_false' );
```

This will bypass the "Remember Me" requirement and remove the `no-store` Cache-Control directive for all authenticated users with JavaScript enabled.
