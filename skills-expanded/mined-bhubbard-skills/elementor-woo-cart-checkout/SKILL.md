---
name: elementor-woo-cart-checkout
description: Guidelines and best practices for customizing WooCommerce Cart and Checkout pages using Elementor Pro. Use this skill when optimizing the checkout funnel.
---

# Elementor WooCommerce Cart & Checkout Skill

## Overview
The Cart and Checkout pages are the most critical steps in an eCommerce funnel. This skill outlines how to build and optimize these pages using Elementor Pro.

## Cart Page Guidelines
### Core Widget: Cart
Elementor Pro provides a dedicated `Cart` widget that replaces the default `[woocommerce_cart]` shortcode.

### Best Practices
- **Layout**: Choose between a one-column or two-column layout. A two-column layout (cart items on the left, totals on the right) is highly recommended for desktop.
- **Distraction-Free**: Remove unnecessary navigation links or footer widgets that might lead users away from the cart.
- **Cross-sells**: Utilize the cross-sells feature within the Cart widget to increase Average Order Value (AOV).

## Checkout Page Guidelines
### Core Widget: Checkout
The `Checkout` widget replaces the `[woocommerce_checkout]` shortcode.

### Best Practices
- **Multi-step vs. One-page**: Elementor doesn't natively do multi-step without addons, but you can style the sections clearly. Keep the form fields minimal.
- **Order Summary Visibility**: The order review and payment methods should always be highly visible. Consider making the order summary column sticky on desktop.
- **Trust Badges**: Add an Image widget near the payment options to display accepted credit cards, SSL certificates, or money-back guarantees.
- **Form Styling**: Ensure input fields have adequate padding, clear borders, and readable text sizes for accessibility.

## Customization Limits
- Elementor's native widgets control the *styling* of the cart and checkout. Modifying the *functional logic* (e.g., adding custom checkout fields, complex conditional shipping) typically requires dedicated plugins like Checkout Field Editor or custom PHP snippets using WooCommerce hooks (`woocommerce_checkout_fields`).

## Troubleshooting
- **Payment gateways not showing**: Ensure shipping methods are configured and SSL is active. Some gateways require an HTTPS connection to load.
- **AJAX update issues**: If changing quantities doesn't update totals, check for JS conflicts or theme overrides interfering with WooCommerce AJAX.
