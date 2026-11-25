---
name: elementor-woo-single-product
description: Guidelines and best practices for creating and customizing WooCommerce Single Product templates using Elementor Pro. Use this skill when modifying product detail pages.
---

# Elementor WooCommerce Single Product Skill

## Overview
This skill provides best practices, common widgets, and layout strategies for designing WooCommerce Single Product templates using Elementor Pro. A well-designed single product page is crucial for conversions.

## Key Widgets
When building a Single Product template, utilize these core Elementor WooCommerce widgets:
- **Product Title**: Displays the product name dynamically.
- **Product Price**: Shows the current price, sale price, and formatting.
- **Product Images**: The main product gallery. Ensure zoom and lightbox settings are configured appropriately.
- **Add to Cart**: The primary call-to-action. Can be customized with variations and quantity selectors.
- **Product Meta**: Displays SKU, categories, and tags.
- **Product Content / Excerpt**: Shows the long and short descriptions.
- **Product Rating**: Displays star ratings based on reviews.
- **Product Related**: Shows related products to encourage cross-selling.

## Best Practices
1. **Clear Visual Hierarchy**: Ensure the Title, Price, and Add to Cart button are immediately visible above the fold.
2. **Mobile Responsiveness**: Stack elements logically on mobile. Images first, followed by title, price, and add to cart.
3. **Variations**: If using variable products, test the layout with multiple variations to ensure the dropdowns or swatches do not break the design.
4. **Trust Signals**: Include widgets for secure checkout badges or guarantees near the Add to Cart button.
5. **Dynamic Tags**: Use Elementor's Dynamic Tags to pull custom fields (ACF or native) into text widgets for additional product data.

## Common Hooks and Extensibility
If custom code is required, use these common WooCommerce hooks within Elementor's HTML widget or functions.php:
- `woocommerce_before_single_product_summary`
- `woocommerce_single_product_summary`
- `woocommerce_after_single_product_summary`

## Troubleshooting
- **Add to Cart Button not working**: Check for conflicting caching plugins or JavaScript errors in the console. Ensure the template is properly assigned to "Products" in Elementor Display Conditions.
- **Gallery Images not showing**: Ensure the theme supports WooCommerce gallery features if Elementor's widget is acting up.
