---
name: enable-without-pretty-permalinks
description: Force speculative loading on sites without pretty permalinks.
---

# Enable Speculative Loading Without Pretty Permalinks

Speculative loading is disabled by default for sites without pretty permalinks. If you know there are no custom query parameters causing state changes, you can enable it:

```php
add_filter( 'plsr_enabled_without_pretty_permalinks', '__return_true' );
```

Note: By default, it is also disabled for logged-in users, but there are options in the UI to change this.
