---
name: jetpack-gravatar
description: Customizing Gravatar Hovercards. Use when adjusting the appearance or behavior of the popup profiles that appear over avatars.
---

# Jetpack Gravatar Hovercards

Hovercards display a small pop-up with a person's Gravatar profile when hovering over their avatar.

## Disabling Hovercards Programmatically
If a user wants to disable hovercards via code instead of the UI:
```php
add_filter( 'jetpack_module_hovercards', '__return_false' );
```

## Styling Hovercards
Hovercards are appended to the body of the document. You can style them via CSS by targeting the `.gprofiles` class. Note that they fetch data via an iframe/API from Gravatar, so modifying the internal structure is limited.
