---
name: wordpress-woocommerce
description: "Customize and scale WooCommerce stores with custom checkout options, payment gateways, and subscription hooks."
category: backend
tags: [wordpress, woocommerce, e-commerce, php, checkout]
complexity: expert
risk: medium
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# WordPress WooCommerce Expert

## Purpose
Manage and implement WordPress WooCommerce Expert requirements efficiently within enterprise applications.

## Core Concepts
Detailed operational framework for WordPress WooCommerce Expert:

### 1️⃣ Overview and Strategy
Understanding boundaries, rules, and best practices for the wordpress-woocommerce feature domain.

### 2️⃣ Code Implementation Reference
```javascript
// Customize WooCommerce Add to Cart
add_filter('woocommerce_add_to_cart_redirect', 'custom_add_to_cart_redirect');
function custom_add_to_cart_redirect($url) {
    return wc_get_checkout_url();
}
```

### 3️⃣ Checklist & Validation Rules
- [ ] Integration validation checklist completed.
- [ ] Code conventions and naming rules followed.
- [ ] Strict type safety constraints verified.
- [ ] Security standards checked.

## Outputs
1. System integration pattern definitions.
2. Code templates and examples.
3. Test validation checklists.
