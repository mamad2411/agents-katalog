---
name: aql-performance-extensibility
description: Developer guidance on performance caching and filtering the block UI. Use when optimizing query speeds or hiding complex UI options from clients.
---

# Advanced Query Loop: Performance & Extensibility

## Performance Optimization
Complex database queries can slow down page loads.
- **Transient Caching**: Enable the caching toggle to store the query results in a transient for 1 hour, heavily reducing database hits on high-traffic pages. *(Note: Caching is disabled if the sort order is set to "Random".)*
- **Disable Pagination**: If you only need a static grid of X items, disable pagination entirely to reduce query overhead.

## Filtering Available Controls (Client Handover)
If you are building a site for a client and want to hide overwhelming UI controls, you can strip them out via PHP using the `aql_allowed_controls` filter:

```php
add_filter( 'aql_allowed_controls', function( $controls ) {
    // Remove complex controls to simplify the block inspector UI
    $to_exclude = array( 'post_meta_query', 'taxonomy_query_builder', 'date_query_dynamic_range' );
    
    return array_filter( $controls, function( $control ) use ( $to_exclude ) {
        return ! in_array( $control, $to_exclude, true );
    });
});
```
