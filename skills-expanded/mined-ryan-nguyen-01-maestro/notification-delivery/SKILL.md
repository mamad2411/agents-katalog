---
name: notification-delivery
description: Use when designing or modifying notification systems across email, SMS, push, in-app, webhook, message center, billing alerts, operational alerts, retries, templates, preferences, suppression lists, delivery status, or notification event pipelines.
category: backend
---

# Notification Delivery

Use this local skill as the mandatory architecture layer for notification work. Provider-specific skills such as resend, capacitor-push-notifications, unified-notifications-ops, email-ops, and messages-ops can be attached in addition to this skill.

## Activation evidence

Apply this skill when task or code mentions notification, notify, email, SMS, push, FCM, APNs, in-app message, message center, template, delivery status, resend, bounce, complaint, unsubscribe, suppression, preference center, webhook alert, billing alert, OTP, reminder, campaign, transactional email, queue, retry, DLQ, SNS, SES, EventBridge, SQS, Azure Service Bus, Azure Event Grid, or SignalR.

## Operating rules

- Separate notification intent from provider delivery attempt.
- Use durable queue/outbox for important notifications. Do not send critical notifications only inside a request transaction without retry path.
- Make delivery idempotent using event id, recipient id, channel, template, and business object id.
- Respect user preferences, unsubscribe, suppression lists, consent, quiet hours, locale, and rate limits.
- Do not log sensitive personal data, OTP values, access links, reset tokens, or private message content.
- Templates must be versioned or reviewed for compatibility with variables and locale rules.
- Track status lifecycle: queued, rendered, provider_accepted, delivered, bounced, complained, failed, suppressed, retried.
- Blocking notification failure must not corrupt the business transaction unless the task explicitly requires synchronous confirmation.
- Critical payment/security notifications must use provider signature validation and auditable event records.

## Required coder output

Coder agents using this skill must document:

- Notification channels changed: email, SMS, push, in-app, webhook, or ops alert.
- Event source and trigger conditions.
- Template variables and fallback behavior.
- Queue/outbox, retry, DLQ, and idempotency strategy.
- Preference, suppression, unsubscribe, privacy, and audit behavior.
- Manual or automated delivery verification performed in dev or sandbox.

## Skill composition

- Attach resend for Resend email platform work.
- Attach email-ops for operational email workflow work.
- Attach messages-ops for message workflow work; review carefully because installer marked Snyk High Risk.
- Attach unified-notifications-ops for cross-channel notification orchestration.
- Attach capacitor-push-notifications for mobile push notification work using Capacitor, Firebase, or APNs.
- Attach eventbridge, sqs, lambda, cloudwatch, or aws-cloud-services for AWS notification pipelines.
- Attach azure-functions, azure-cost, kql, cloud-solution-architect, or microsoft-docs for Azure notification pipelines.
- Attach payment-platform when notification is triggered by payment, invoice, refund, dispute, or subscription events.
