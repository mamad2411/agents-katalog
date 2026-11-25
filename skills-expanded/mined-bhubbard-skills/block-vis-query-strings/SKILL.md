---
name: block-vis-query-strings
description: Guidance on using the Query String control. Use when configuring dynamic blocks for marketing campaigns, email links, or personalization.
---

# Block Visibility: Query Strings

The Query String visibility control allows site owners to display personalized blocks based on the URL parameters the visitor used to reach the page.

## Common Use Cases
- **Marketing Campaigns**: Show a specific promotional banner only if the user arrives from a newsletter link (e.g., `?utm_source=newsletter`).
- **Personalization**: Show a welcome message containing the user's name if passed in the URL (e.g., `?user=john`).

## Configuration
In the block's Visibility panel under "Query String":
1. Specify the **Key** (e.g., `utm_source`).
2. Specify the **Value** (e.g., `newsletter`).
3. If you want the block to show anytime the key is present regardless of the value, leave the Value field blank.

## Troubleshooting Cache Issues
If query string visibility isn't working for logged-out users, it is almost certainly due to server-side page caching (e.g., WP Rocket, Varnish). Many hosts strip query parameters to serve cached pages. Ensure the specific query string keys used by the plugin are excluded from the host's caching rules.
