---
name: event-webhooks
description: Use this skill when the user wants to handle SendGrid Event Webhooks to track email delivery and engagement.
---

# SendGrid Event Webhooks

This skill provides guidelines for working with SendGrid Event Webhooks.

## Overview
SendGrid’s Event Webhook will notify a URL of your choice via HTTP POST with information about events that occur as SendGrid processes your emails.

## Types of Events
- **Delivery Events**: `processed`, `dropped`, `delivered`, `deferred`, `bounce`, `block`
- **Engagement Events**: `open`, `click`, `spamreport`, `unsubscribe`, `group_unsubscribe`, `group_resubscribe`

## Best Practices
- **Security**: Verify the signature of incoming webhooks to ensure they actually came from SendGrid. Use the Signature Verification feature.
- **Acknowledge Quickly**: Return a 2xx status code immediately upon receiving the webhook, and process the payload asynchronously to avoid timeouts.
- **Deduplication**: SendGrid guarantees at-least-once delivery, so your system must handle duplicate events gracefully using the `sg_event_id`.
- **Payload Handling**: The payload is an array of event objects. Be prepared to handle batches of events in a single POST request.

## Example Payload
```json
[
  {
    "email": "john.doe@sendgrid.com",
    "timestamp": 1337197600,
    "smtp-id": "<4FB4041F.6080505@sendgrid.com>",
    "event": "processed"
  }
]
```
