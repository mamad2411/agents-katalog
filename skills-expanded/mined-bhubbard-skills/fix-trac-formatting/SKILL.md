---
name: fix-trac-formatting
description: Configure Theme Check to format output for Trac tickets during theme reviews.
---

# Format Theme Check Output for Trac

The Theme Review team uses Trac for tracking theme submissions. You can configure Theme Check to generate Trac-compatible markup.

## Configuration
Define the following constants in your `wp-config.php`:

```php
define( 'TC_PRE', 'Theme Review:[[br]]
- Themes should be reviewed using "define(\'WP_DEBUG\', true);" in wp-config.php[[br]]
- Themes should be reviewed using the test data from the Theme Checklists (TC)
-----
' );

define( 'TC_POST', 'Feel free to make use of the contact details below if you have any questions,
comments, or feedback:[[br]]
[[br]]
* Leave a comment on this ticket[[br]]
* Send an email to the Theme Review email list[[br]]
* Use the #wordpress-themes IRC channel on Freenode.' );
```

Once defined, a new Trac tickbox will appear next to the *Check it!* button, allowing you to easily copy the output for Trac tickets.
