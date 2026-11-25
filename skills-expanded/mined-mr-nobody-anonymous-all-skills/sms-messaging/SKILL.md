---
name: sms-messaging
description: "Send SMS and WhatsApp messages programmatically: provider APIs, sender registration, opt-in and STOP handling, templating and delivery receipts."
type: procedural
category: communication
domain: communication
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: intermediate
triggers:
  - twilio sms integration
  - whatsapp business api template
  - sms opt out handling
  - sms delivery receipt
  - sender id registration
keywords:
  - sms
  - whatsapp
  - twilio
  - opt-in
  - delivery-receipt
  - messaging
source: custom
enabled: true
---

# SMS and WhatsApp Messaging

## Purpose

Send SMS and WhatsApp messages programmatically: provider APIs, sender registration, opt-in and STOP handling, templating and delivery receipts.

## When to Use

- Users must receive time-sensitive notifications by text.
- WhatsApp template messages need approval and variable mapping.
- Delivery receipts and opt-outs must be handled correctly.

## When NOT to Use

- The message is marketing without documented consent.
- Email or in-app notification would satisfy the need.
- The destination country forbids the sender type you plan to use.

## Capabilities

- Integrate a messaging API with sender registration and templates.
- Enforce opt-in capture and honour STOP/opt-out immediately.
- Handle delivery receipts, failures and retries within provider rules.
- Keep message content compliant with local regulation.

## Inputs

- The destination countries and their sender/registration requirements.
- The consent record and opt-out mechanism.
- The message types: OTP, alert, or templated WhatsApp notification.

## Workflow

1. Confirm consent exists and record where it came from.
2. Register the sender id or WhatsApp template before first send.
3. Send a single test to your own number and inspect the receipt.
4. Persist provider message ids so receipts can be reconciled.
5. Process opt-out keywords and suppress immediately.

## Tools

- Twilio (or another provider) API
- webhook receiver
- consent store

## Examples

- `allskills mcp install --harness claude --servers twilio`
- `curl -s -X POST https://api.twilio.com/2010-04-01/Accounts/$SID/Messages.json -u "$SID:$TOKEN" -d "To=+1..." -d "From=+1..." -d "Body=hi"`
- `allskills route "send OTP by sms"`

## Safety

- Sending without consent is illegal in most jurisdictions and can suspend the account.
- OTP messages must never include full account details.
- Retries can double-charge and spam recipients; use provider idempotency.

## Source

All-Skills canonical library (`skills/communication/sms-messaging`). First-party skill, maintained in this repository.

## Notes

- WhatsApp requires pre-approved templates with named variables.
- Long messages split into segments and multiply cost; keep them short.
- Pairs with: `communication/transactional-email`, `security/oauth2-oidc-integration`.
