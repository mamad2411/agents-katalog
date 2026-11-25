---
name: wpcom-webhooks
description: Use this skill for implementing and handling WordPress.com webhooks and Store Licensing API integrations.
---

# WordPress.com Webhooks & Store Licensing API

This skill provides advanced developer guidance on working with Webhooks within the WordPress.com ecosystem. It is primarily focused on the Store Licensing API and general webhook integrations.

## Store Licensing API

For plugin and theme vendors selling through WordPress.com, the Store Licensing API heavily relies on webhooks to manage the lifecycle of product subscriptions.

### Webhook Events
WordPress.com sends webhooks to your registered URLs to notify you of the following subscription events:
- **Creation:** A new subscription is created.
- **Renewal:** A subscription is renewed.
- **Cancellation:** A subscription is canceled.
- **Refund:** A subscription is refunded.

### Handling Incoming Webhooks
1. **Payload:** The webhook payload contains event, site, product, and subscription details.
2. **Response:** You MUST acknowledge receipt of the webhook with a `200 OK` HTTP response.
3. **Action:** After acknowledging, perform the necessary actions on your end, such as provisioning a license, updating account limits, or revoking access.

### Testing Webhooks
Vendors should use the Webhook API to request test webhooks to verify their integration with test data before going live.

## General WordPress Webhook Implementations

When building custom webhooks or outgoing data pushes in WordPress:

- **Sending Data:** Use `wp_remote_post()` to send data to external services triggered by specific WordPress actions (hooks).
- **WooCommerce:** If working with WooCommerce, utilize its built-in REST API which supports creating and managing webhooks for store activity.
- **Reliability:** Implement robust logging and retry mechanisms, as standard WordPress webhook implementations may lack built-in delivery guarantees for critical data like payments.

## Reference
Always refer to the official [WordPress.com Developer Docs](https://developer.wordpress.com/docs/) for the most up-to-date API endpoints and payload schemas.
