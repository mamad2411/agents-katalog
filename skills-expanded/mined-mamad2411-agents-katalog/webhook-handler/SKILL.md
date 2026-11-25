---
name: webhook-handler
description: "Implement webhook handlers for processing incoming events from external services."
---

# Webhook Handler

## Overview
Webhooks enable external services to send real-time notifications to your application. This skill should be invoked when implementing handlers for incoming webhook events from services like Stripe, GitHub, or custom integrations.

## Core Principles
- **Verification**: Always verify webhook signatures
- **Idempotency**: Handle duplicate deliveries gracefully
- **Async Processing**: Process webhooks asynchronously
- **Response**: Return appropriate HTTP status quickly

## Preparation Checklist
- [ ] Identify webhook source
- [ ] Get webhook secret
- [ ] Plan event handling logic
- [ ] Design idempotency strategy

## Step-by-Step Process
1. **Verify**: Validate signature/secret
2. **Parse**: Extract event payload
3. **Acknowledge**: Return 200 quickly
4. **Process**: Handle event asynchronously
5. **Idempotency**: Check for duplicates
6. **Respond**: Update systems accordingly

## Do's and Don'ts
- ✅ **Do** verify webhook signatures
- ✅ **Do** respond quickly (< 5 seconds)
- ✅ **Do** implement idempotency
- ❌ **Don't** process synchronously
- ❌ **Don't** skip signature verification
- ❌ **Don't** assume valid payloads

## Anti-Patterns
- **No Verification**: Accepting webhooks without validation
- **Sync Processing**: Processing in request handler
- **No Idempotency**: Handling duplicates incorrectly
- **Timeout**: Taking too long to respond
