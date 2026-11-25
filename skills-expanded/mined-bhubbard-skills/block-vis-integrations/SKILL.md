---
name: block-vis-integrations
description: Guidance on using Block Visibility integrations. Use when configuring visibility based on WooCommerce, EDD, ACF, or WP Fusion data.
---

# Block Visibility: Integrations

Block Visibility includes native integrations for popular ecosystem plugins, allowing blocks to be rendered based on deep contextual data.

## Advanced Custom Fields (ACF)
You can show or hide a block based on the value of an ACF field attached to the current post, user, or even ACF Options pages. Supports advanced operators (`>`, `<`, `==`, `!=`) for numeric and date fields.

## WooCommerce & Easy Digital Downloads (EDD)
E-commerce integrations allow for highly personalized shopping experiences.
- **Cart Contents**: Show an upsell block if a specific product is currently in the user's cart.
- **Purchase History**: Hide promotional blocks if the logged-in customer has already purchased the product in the past.
- **Time Since Order**: Show a special discount block if it's been exactly X days since their last order.

## WP Fusion
Integrates with CRM/Marketing platforms via WP Fusion to show/hide blocks based on the user's assigned CRM tags.
