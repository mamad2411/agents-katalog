---
name: elementor-woo-archives
description: Guidelines and best practices for creating WooCommerce Product Archive templates using Elementor Pro. Use this skill for shop pages, category pages, and tag archives.
---

# Elementor WooCommerce Archives Skill

## Overview
Product Archives are where users browse your catalog. This includes the main Shop page, Product Categories, and Product Tags. Elementor Pro allows complete control over these loops.

## Core Widget: Products / Archive Products
Use the `Archive Products` widget when building a template assigned to Product Archives via the Theme Builder.

## Best Practices for Product Grids
1. **Columns**: 3 or 4 columns work best for desktop, 2 for tablet, and 1 or 2 for mobile depending on thumbnail size.
2. **Card Design**: Ensure consistent image aspect ratios. Include essential information: Title, Price, Rating, and Add to Cart.
3. **Hover Effects**: Add subtle hover effects (like an image swap or shadow) to indicate interactivity.
4. **Pagination**: Always include pagination for large categories. Test AJAX loading if using third-party addons, but standard pagination is safest for SEO.

## Filtering and Navigation
- **WooCommerce Sidebar**: Product archives often require filtering (by price, attribute, rating).
- Use a two-column layout for the template (e.g., 25% sidebar, 75% products).
- Place standard WooCommerce filter widgets or Elementor Pro's new Loop Filter widgets in the sidebar.
- **Mobile Filters**: On mobile, consider hiding the sidebar behind a toggle or Off-Canvas widget to save screen space.

## Dynamic Conditions
When creating the template in Elementor Theme Builder, you can set granular display conditions:
- **All Product Archives**: Applies to the shop, all categories, and tags.
- **Specific Categories**: Create distinct designs for specific product lines.
- **Search Results**: Create a dedicated archive template for WooCommerce product searches.

## Customizing the Loop
For advanced designs, use Elementor's **Loop Builder**.
1. Create a "Loop Item" template for a single product card.
2. Use dynamic tags to pull in the image, title, price, etc.
3. Use the "Loop Grid" widget on the Archive template and select your custom item design. This provides infinite flexibility compared to the standard "Archive Products" widget.

## Troubleshooting
- **Archive not displaying**: Ensure the WooCommerce page settings (WooCommerce > Settings > Products) are correct, and the Elementor template conditions are explicitly set.
- **Filters not working**: If using standard Woo widgets, ensure they are placed within an archive that queries the main loop, not a custom query.
