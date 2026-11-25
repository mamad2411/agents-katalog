---
name: communications-master
description: >-
  Master hub for Communications — real-time chat, WhatsApp, voice/SMS, push, support/helpdesk,
  omnichannel AI inbox, and advanced email. Use to build production WebSocket/SSE chat, WhatsApp
  Business (Cloud API), SMS/voice (Twilio, A2P 10DLC), cross-platform push (Web Push/FCM v1/APNs),
  a Zendesk-grade helpdesk (tickets/SLA/CSAT), an omnichannel inbox with a RAG chatbot + human
  handoff, and advanced email (deliverability SPF/DKIM/DMARC, inbound parse, two-way sync,
  email-to-ticket). Bundles 7 specialized skills (in skills/<name>/GUIDE.md). Use for any chat,
  messaging, voice, push, support, or email task.
---

# Communications — Master Hub

Build chat, WhatsApp, SMS/voice, push, customer support, an omnichannel inbox + AI chatbot, and
advanced email — at staff/principal depth, with real APIs and 2026-current compliance.

## How to use this hub

This single skill bundles **all 7 communications skills**. Each bundled skill's full instructions
live in `skills/<name>/GUIDE.md` — **read the relevant `GUIDE.md` before acting**, then combine
them: a real support product spans chat + WhatsApp + SMS + push + email + helpdesk + bot.

**Workflow**
1. Match the request to one or more skills below; open its `GUIDE.md` first.
2. Compose. The cross-cutting invariants repeat across every channel — apply them everywhere:
   - **Verify every inbound webhook** (signatures: WhatsApp `X-Hub-Signature-256`, Twilio
     `X-Twilio-Signature`, ESP signing) before doing anything.
   - **Idempotent + at-least-once**: dedupe by provider message id; every channel redelivers.
   - **Consent/opt-in** is mandatory (WhatsApp opt-in, TCPA STOP, email one-click unsubscribe, push permission).
   - **i18n/RTL Arabic**: localize at send time, `dir="auto"`, ICU plurals, per-locale templates.

## Bundled skills

- **realtime-chat-messaging** — Production real-time chat: stateless WebSocket gateway + Redis
  Pub/Sub backplane, server-assigned total ordering, idempotent send, delivery/read receipts,
  presence, reconnect+replay, fan-out scaling, backpressure, and per-conversation authz.  
  → `skills/realtime-chat-messaging/GUIDE.md`
- **whatsapp-business-integration** — WhatsApp Cloud API (Graph v25.0): the 24h window vs approved
  templates (HSM), per-message pricing (post-2025), interactive buttons/lists/Flows, signed webhooks,
  status receipts, opt-in/quality, BSP abstraction, idempotent intake.  
  → `skills/whatsapp-business-integration/GUIDE.md`
- **voice-sms-telephony** — Programmable SMS/MMS + voice (Twilio et al.): US A2P 10DLC + TCPA
  compliance, `X-Twilio-Signature` validation, inbound + STOP/HELP, status callbacks, TwiML IVR,
  and real-time AI voice via Media Streams.  
  → `skills/voice-sms-telephony/GUIDE.md`
- **push-notifications-advanced** — Cross-platform push + in-app: Web Push (VAPID), FCM HTTP v1
  (legacy retired 2024), APNs token-based auth (.p8 JWT/HTTP2), token pruning, and an orchestration
  layer with preferences, quiet hours, dedupe/digest, and email/SMS fallback.  
  → `skills/push-notifications-advanced/GUIDE.md`
- **support-helpdesk-system** — Zendesk/Intercom-grade helpdesk: ticket state machine + event log,
  omnichannel intake, an SLA engine computed in **business hours** with pause-on-pending + breach
  escalation, routing (round-robin/load/skills), macros/automations, KB/deflection, CSAT/CES/NPS.  
  → `skills/support-helpdesk-system/GUIDE.md`
- **omnichannel-inbox-chatbot** — Unify chat/WhatsApp/SMS/email/social into one inbox + AI agent:
  channel adapters, identity resolution, RAG over the KB (grounded + cited), tool-calling with
  guardrails, and confidence-gated human handoff with full context + agent-assist.  
  → `skills/omnichannel-inbox-chatbot/GUIDE.md`
- **email-integration-advanced** — Advanced email: ESP send (Resend/SendGrid/SES), deliverability
  (SPF/DKIM/DMARC/BIMI + RFC 8058 one-click unsub + Gmail/Yahoo/Microsoft 2024–2025 rules),
  MJML/React Email, inbound parse, IMAP/Gmail/Graph two-way sync, threading, email-to-ticket,
  bounce/complaint suppression.  
  → `skills/email-integration-advanced/GUIDE.md`

## Typical compositions
- **Support platform**: omnichannel-inbox-chatbot (brain) + support-helpdesk-system (tickets/SLA) +
  realtime-chat-messaging (web chat) + whatsapp/voice-sms/email (channels) + push (agent/customer alerts).
- **Transactional comms**: email (receipts) + whatsapp (utility templates) + voice-sms (OTP) + push,
  all behind one preference/consent layer.

## Pairs well with
`ai-mcp-master` (prompt-engineering-advanced, mcp-builder for the chatbot/voice brain),
`business-master` (crm-builder for customer-360), `backend-api-master` (integrations-pro webhooks,
auth/MFA), `analytics-master` (engagement/deliverability), and `ui-master` (chat widget + dashboards).

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are
`GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant
`GUIDE.md` on demand.
