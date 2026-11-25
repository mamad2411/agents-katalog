---
name: exclude-speculative-loading
description: Exclude specific URLs from being prefetched or prerendered using the Speculative Loading plugin.
---

# Exclude Speculative Loading

Use the `plsr_speculation_rules_href_exclude_paths` filter to prevent URLs from being prerendered or prefetched.

```php
add_filter(
    'plsr_speculation_rules_href_exclude_paths',
    function ( array $exclude_paths, string $mode ): array {
        if ( 'prerender' === $mode ) {
            $exclude_paths[] = '/products/*';
        }
        $exclude_paths[] = '/cart/*';
        return $exclude_paths;
    },
    10,
    2
);
```

You can also add the `no-prerender` CSS class or `rel="nofollow"` to `<a>` tags to exclude them.
