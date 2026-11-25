---
name: yoast-seo-analysis
description: "Understanding how the content analysis works and how to add custom analysis checks."
---

# Yoast SEO Content Analysis

Yoast SEO runs a sophisticated content analysis engine in JavaScript (via the `yoastseo` npm package) directly in the browser when editing a post.

## Reference
[Analysis Documentation](https://developer.yoast.com/features/analysis/overview/)

## Core Concepts
The analysis evaluates text for readability (Flesch reading ease, transition words, sentence length) and SEO (keyword density, exact matches, alt tags, link count).

## Adding Custom Analysis Checks
Currently, hooking into the JavaScript analysis engine to add custom rules (like "Does this post contain a specific shortcode?") requires writing JavaScript plugins that integrate with the `@yoast/app-components` or hooking into the internal Yoast Redux store.

Because the analysis runs entirely client-side, PHP filters do not affect the real-time score bullets in the editor.

### Modifying the Analyzed Text
You can, however, use PHP filters to modify the content *before* Yoast parses it for the initial database save or if you have custom fields whose content should count towards the SEO score.

Use the `wpseo_pre_analysis_post_content` filter:
```php
add_filter( 'wpseo_pre_analysis_post_content', 'add_custom_field_to_analysis', 10, 2 );
function add_custom_field_to_analysis( $content, $post ) {
    $custom_content = get_post_meta( $post->ID, 'my_custom_field', true );
    if ( ! empty( $custom_content ) ) {
        $content .= ' ' . $custom_content;
    }
    return $content;
}
```

## Best Practices
- If your theme uses Advanced Custom Fields (ACF) or Page Builders, those tools usually have their own bridging plugins (like ACF Content Analysis for Yoast) that pipe the custom field data into Yoast's JavaScript analyzer.
- Do not attempt to fake the SEO score via PHP. The red/orange/green bullets are generated purely in JavaScript based on the text present in the DOM editor and the content passed via localized scripts.
