---
name: twilio-conversations-classic-api
version: 1.0.0
description: Directly operate the Twilio Conversations REST API — create Conversations, add SMS/WhatsApp/chat participants, post messages, wire webhooks, and manage Conversation Services and autocreation.
author: matrixx0070
tags: [twilio, conversations, rest-api, webhooks, messaging]
capabilities: []
---

## When to use

Use this when you need the low-level wire calls: creating a Conversation (`CH...`), attaching SMS, WhatsApp, or chat participants with the correct binding, posting and listing messages, configuring scoped and global webhooks, provisioning a Conversation Service (`IS...`), or enabling autocreation via Address Configuration. This is the reference skill the higher-altitude skills route to when they need concrete endpoints and payloads.

**Not for:** designing the overall support system (use twilio-customer-support-architect), giving the agent cross-session memory (use twilio-conversation-memory), or building the RAG knowledge base (use twilio-enterprise-knowledge). Session/channel orchestration lives in twilio-conversation-orchestrator.

## Method

1. Authenticate. Use HTTP Basic auth with your Account SID and Auth Token (or an API Key `SK...` + secret). All calls hit `https://conversations.twilio.com/v1`.
2. Decide scope. Global (default) resources live under `/Conversations`; multi-tenant or isolated deployments should create a Conversation Service (`/Services`, SID `IS...`) and address resources under `/Services/{IS...}/Conversations`. Decision point: use a Service when you need separate webhooks, roles, or reachability config per tenant.
3. Create a Conversation. `POST /Conversations` (optionally `FriendlyName`, `Attributes` JSON, `UniqueName`). Capture the returned `CH...` SID.
4. Add participants. Decision point per channel:
   - SMS/WhatsApp: `POST /Conversations/{CH}/Participants` with `MessagingBinding.Address` (the customer's +E164, or `whatsapp:+E164`) and `MessagingBinding.ProxyAddress` (your Twilio number, or `whatsapp:` sender). Returns `MB...`.
   - Chat (app/SDK) user: send `Identity` instead of any `MessagingBinding`.
   Never mix `Identity` and `MessagingBinding` on the same participant.
5. Post messages. `POST /Conversations/{CH}/Messages` with `Author` and `Body` (and/or `MediaSid` for media). Returns `IM...`. List with `GET /Conversations/{CH}/Messages` (paginated).
6. Wire webhooks. Global conversation webhook is configured once at the account/service level and fires for all conversations. Scoped webhooks are `POST /Conversations/{CH}/Webhooks` with `Target=webhook`, `Configuration.Url`, `Configuration.Method`, and `Configuration.Filters` (e.g. `onMessageAdded`, `onConversationAdded`). Decision point: scoped for per-conversation routing, global for account-wide handlers.
7. Enable autocreation (optional). `POST /AddressConfigurations` maps an inbound Address (a Twilio number or WhatsApp sender) so an unknown inbound message auto-creates a Conversation and participant. Set `AutoCreation.Enabled=true`, `Type=webhook|studio|default`, and target.
8. Validate webhook authenticity. Verify the `X-Twilio-Signature` header on every inbound webhook before acting.

## Example

```bash
# 1. Create a conversation
curl -X POST https://conversations.twilio.com/v1/Conversations \
  --data-urlencode "FriendlyName=Support #4821" \
  -u "$ACCOUNT_SID:$AUTH_TOKEN"
# -> "sid": "CHxxxxxxxx..."

# 2. Add the customer over SMS (binding), your number as proxy
curl -X POST https://conversations.twilio.com/v1/Conversations/CHxxxx/Participants \
  --data-urlencode "MessagingBinding.Address=+15558675309" \
  --data-urlencode "MessagingBinding.ProxyAddress=+15551112222" \
  -u "$ACCOUNT_SID:$AUTH_TOKEN"
# -> "sid": "MBxxxxxxxx..."

# 3. Add an in-app agent as a chat participant (identity, no binding)
curl -X POST https://conversations.twilio.com/v1/Conversations/CHxxxx/Participants \
  --data-urlencode "Identity=agent_ada" \
  -u "$ACCOUNT_SID:$AUTH_TOKEN"

# 4. Post a message
curl -X POST https://conversations.twilio.com/v1/Conversations/CHxxxx/Messages \
  --data-urlencode "Author=agent_ada" \
  --data-urlencode "Body=Hi, how can I help?" \
  -u "$ACCOUNT_SID:$AUTH_TOKEN"
# -> "sid": "IMxxxxxxxx..."

# 5. Scoped webhook for message events
curl -X POST https://conversations.twilio.com/v1/Conversations/CHxxxx/Webhooks \
  --data-urlencode "Target=webhook" \
  --data-urlencode "Configuration.Url=https://api.example.com/twilio/hook" \
  --data-urlencode "Configuration.Method=POST" \
  --data-urlencode "Configuration.Filters=onMessageAdded" \
  -u "$ACCOUNT_SID:$AUTH_TOKEN"
```

## Pitfalls

- Sending both `Identity` and `MessagingBinding.Address` on one participant is rejected — a participant is either a chat identity or a channel binding, never both.
- Forgetting `MessagingBinding.ProxyAddress` for SMS/WhatsApp means Twilio has no sender to route replies through.
- WhatsApp addresses must be prefixed `whatsapp:` on both `Address` and `ProxyAddress`; a bare +E164 routes as SMS.
- Adding the same address to two open conversations under the same proxy causes routing ambiguity — one active address↔proxy pair maps to one conversation.
- Not verifying `X-Twilio-Signature` leaves your webhook forgeable.
- Message `Body` over 32KB is rejected; large payloads belong in media, not the body.
- Global and scoped webhooks both fire — deduplicate downstream if you configure both.

## Output format

Return the created resource SIDs and key fields as JSON, e.g. `{ "conversation_sid": "CH...", "participant_sids": ["MB...", ...], "message_sid": "IM...", "webhook_sid": "WH..." }`. For list calls, return the `meta` paging block plus the resource array. Surface any 4xx error `code` and `message` verbatim.

## Reference

- Base URL: `https://conversations.twilio.com/v1`. Auth: Basic (Account SID + Auth Token, or API Key `SK...`).
- Resources & SID prefixes: Conversation `CH`, Participant `MB`, Message `IM`, Webhook `WH`, Conversation Service `IS`. Also `/Users`, `/Roles`, `/AddressConfigurations`.
- Participant binding: `MessagingBinding.Address` (customer +E164 or `whatsapp:+E164`), `MessagingBinding.ProxyAddress` (your Twilio number / WhatsApp sender). Chat participants use `Identity`.
- Webhook event filters include `onMessageAdded`, `onMessageUpdated`, `onConversationAdded`, `onConversationStateUpdated`, `onParticipantAdded`, `onDeliveryUpdated`. Scoped webhooks live under `/Conversations/{sid}/Webhooks`; global/service webhooks are configured at the service level.
- Autocreation: `/AddressConfigurations` binds an inbound address to auto-create conversations (`AutoCreation.Enabled`, `AutoCreation.Type` = `webhook` | `studio` | `default`).
- Hard limits: message body 32KB; up to ~1000 participants per conversation. Media handled via the Media Content Service (MCS) — reference by `MediaSid`.
- Common errors: `401` auth failure, `404` unknown SID, `409` conflict (duplicate binding/unique name), `429` rate limited, `50xxx` Twilio error codes in the response `code` field. Validate inbound webhooks with the `X-Twilio-Signature` header.
