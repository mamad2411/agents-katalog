---
name: callrail-webhooks
description: Instructions for setting up and handling CallRail webhooks for real-time post-call events.
---

# CallRail Webhooks Guide

## Overview
Webhooks allow CallRail to send HTTP POST requests to your server when specific events occur, such as a call starting, ending, or a text message being received.

## Setup
You can configure webhooks in the CallRail dashboard under Settings > Integrations > Webhooks.

## Common Webhook Events
1. **Post-Call (Call End)**: Triggered when a call finishes. Useful for logging calls into an external CRM or database.
2. **Pre-Call (Call Start)**: Triggered right before the phone rings the destination number.
3. **SMS Received**: Triggered when an inbound text message is received.

## Payload Structure
The webhook payload will be sent as JSON or Form Encoded (depending on configuration). A typical JSON payload includes:
- `id`: The unique call ID.
- `company_id`: ID of the company.
- `customer_phone_number`: The caller's phone number.
- `tracking_phone_number`: The CallRail tracking number dialed.
- `duration`: Length of the call in seconds.

## Best Practices
- Always return a `200 OK` response quickly to acknowledge receipt. Do heavy processing asynchronously.
- Validate incoming webhooks if needed (e.g., checking query parameters or basic auth if you append them to the webhook URL).
- Store failed webhook events for retry processing.
