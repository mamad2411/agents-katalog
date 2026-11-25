---
name: yoast-seo-schema-markup
description: "Deep dive into the default Schema pieces and how plugins output them."
---

# Yoast SEO Schema Markup Output

Understanding how Yoast constructs its Schema graph is crucial before using the Schema API to modify it.

## Reference
[Schema Pieces Documentation](https://developer.yoast.com/features/schema/pieces/)

## The Schema Graph
Yoast outputs a single JSON-LD block wrapped in a `@graph` array. This connects the WebSite, WebPage, Organization/Person, Article, and ImageObject entities together using `@id` references.

Example flow on an Article page:
1. `Organization` (Publisher)
2. `WebSite` (References the Publisher)
3. `WebPage` (References the WebSite as `isPartOf`)
4. `Article` (References the WebPage as `mainEntityOfPage` and Organization as `publisher`)
5. `Person` (Author, referenced by Article)

## Key Entities Yoast Generates

- **Organization / Person**: Represents the entity behind the website (configured in Yoast SEO > Site Representation). `@id`: `https://example.com/#organization`
- **WebSite**: Represents the site itself. `@id`: `https://example.com/#website`
- **WebPage**: Represents the specific URL being viewed. `@id`: `https://example.com/path/#webpage`
- **Article**: Added on Posts. `@id`: `https://example.com/path/#article`
- **ImageObject**: Added for the primary image, featured image, logo, etc.

## Plugin Specific Outputs (Add-ons)
- **Yoast WooCommerce SEO**: Replaces the generic `WebPage` with `ItemPage` and injects robust `Product` schema tied to the WebPage.
- **Yoast Local SEO**: Injects `LocalBusiness` schema and connects it to the main Organization.
- **Yoast Video SEO**: Injects `VideoObject` schema.

## Best Practices
- **Do not output separate JSON-LD blocks on the page if you can avoid it.** If you have custom schema (e.g., a custom `Event` post type), use the `wpseo_schema_graph_pieces` filter (see `yoast-seo-schema-api` skill) to inject your `Event` object into Yoast's `@graph` array, setting `mainEntityOfPage` to the WebPage `@id`. This prevents disconnected schema islands which search engines penalize.
