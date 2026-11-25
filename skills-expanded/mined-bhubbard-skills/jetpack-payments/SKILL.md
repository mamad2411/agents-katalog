---
name: jetpack-payments
description: Guidance on Jetpack Payments and Pay with PayPal blocks. Use when assisting with recurring payments, donations, or simple block-based ecommerce.
---

# Jetpack Payments & PayPal

Jetpack provides blocks for processing simple payments (via Stripe) or taking PayPal donations.

## Pay with PayPal Block
This block inserts a simple button. If a user needs to track the payment on their site (e.g., updating a database when payment succeeds), advise them that the basic PayPal block does *not* offer complex IPN (Instant Payment Notification) webhooks. They would need a full eCommerce plugin like WooCommerce.

## Jetpack Payments (Stripe)
Jetpack Payments allows for one-time, recurring, or "pay what you want" donations via Stripe.
- **Styling**: The buttons can be styled using standard Gutenberg block styles.
- **Hooks**: You can hook into the payment success actions (which happen on WordPress.com infrastructure) via Jetpack Sync, but local verification hooks are limited because the transaction is processed securely off-site.

## Troubleshooting
If payments aren't working, ensure Jetpack is fully connected and that the user's Stripe/PayPal account is fully verified.
