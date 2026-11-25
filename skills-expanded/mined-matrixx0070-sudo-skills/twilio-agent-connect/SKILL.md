---
name: twilio-agent-connect
version: 1.0.0
description: Attach a Twilio AI Assistant or LLM agent to voice, messaging, and web channels with correct session lifecycle, context passing, and human handoff.
author: matrixx0070
tags: [twilio, assistants, channels, sessions, handoff]
capabilities: []
---

You connect a built AI Assistant to the outside world. The assistant already has instructions, Tools, and Knowledge — your job is the binding: voice via ConversationRelay, messaging via Conversations, or an embeddable web widget, plus the Session/Message lifecycle and escalation to a human.

## When to use

Use this when an AI Assistant exists (or an LLM endpoint you own) and you need it to receive and reply on a real channel. Covers channel binding, Session creation and reuse, passing per-user context, streaming replies, and handing off to a human agent while preserving transcript.

Decision gate: which channel is primary? Voice → ConversationRelay binding (deep audio detail lives in twilio-voice-conversation-relay). Messaging (SMS/WhatsApp/chat) → Conversations binding. Web → the AI Assistant web widget or a Conversations-backed chat.

**Not for:** designing the assistant's personality/tools/knowledge (build that first); low-level voice audio, DTMF, barge-in, and TTS tuning (see twilio-voice-conversation-relay); orchestrating who-speaks-when across a long multi-party thread (see twilio-conversation-orchestrator).

## Method

1. Confirm the assistant identity. You need its `AssistantSid` (`AI...`). Verify with `GET https://assistants.twilio.com/v1/Assistants/{Sid}`.
2. Pick the channel binding:
   - Voice: point a Twilio number's voice webhook at TwiML that returns `<Connect><ConversationRelay>` targeting your assistant/relay endpoint. Delegate audio params to twilio-voice-conversation-relay.
   - Messaging: create/route a Conversation and add the assistant as a participant, or bind via the assistant's messaging channel so inbound SMS/WhatsApp reaches the assistant.
   - Web: embed the AI Assistant web widget, or stand up a Conversations chat participant driven by the assistant.
3. Manage the Session lifecycle. A Session (`/Sessions`) represents one ongoing conversation with the assistant. Decision point: reuse an existing Session per user/thread to keep memory, or create a fresh Session per interaction. Use a stable `identity` so returning users map to the same Session where continuity matters.
4. Pass context. Send per-turn or per-session context (customer id, locale, CRM fields) so Tools and instructions can use it. Do not stuff secrets into the prompt — pass identifiers and let Tools fetch.
5. Send and receive messages. Post user turns to `/Sessions/{Sid}/Messages` (or let the channel binding do it); read assistant replies from the Messages resource or the streamed channel response.
6. Define handoff. On an escalation signal (intent, low confidence, explicit request, or a Tool result), stop assistant turns and route to a human via Flex/TaskRouter or a webhook. Forward the full Session/Conversation transcript and context so the human resumes without re-asking.
7. Handle failure. On assistant/tool error or timeout, fall back to a safe reply and/or escalate. Never leave the caller in silence.

## Example

TwiML binding an inbound call to an assistant via ConversationRelay:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <ConversationRelay url="wss://your-relay.example.com/voice"
                       welcomeGreeting="Hi, how can I help?"
                       ttsProvider="ElevenLabs"
                       language="en-US" />
  </Connect>
</Response>
```

Creating a Session and posting a user turn (Node):

```js
const auth = { username: process.env.TWILIO_ACCOUNT_SID, password: process.env.TWILIO_AUTH_TOKEN };
const base = "https://assistants.twilio.com/v1";

const session = await fetch(`${base}/Assistants/${assistantSid}/Sessions`, {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ Identity: `user:${customerId}` }),
  // basic auth omitted for brevity
});

await fetch(`${base}/Sessions/${sessionSid}/Messages`, {
  method: "POST",
  body: new URLSearchParams({ Body: "Where is my order?", Author: `user:${customerId}` }),
});
```

## Pitfalls

- Creating a new Session every turn — you lose conversation memory and Tool state. Reuse per thread.
- Confusing an Assistant Session with a Conversations Conversation. They are different resources; a messaging binding may involve both.
- Blocking on the assistant reply on voice. Voice needs streaming/low latency — route audio via ConversationRelay, not a synchronous REST round-trip.
- Losing context on handoff. If the human agent gets no transcript, the customer repeats everything. Always forward Session/Conversation history.
- Putting secrets in prompt context. Pass identifiers; fetch sensitive data inside a Tool over an authenticated call.
- Webhook signature not validated. Verify the `X-Twilio-Signature` header on inbound webhooks.

## Output format

Produce: (1) the channel binding artifact (TwiML for voice, Conversations participant setup for messaging, or widget embed for web), (2) Session strategy (reuse key + lifecycle), (3) context payload schema, (4) handoff trigger list and the transcript-forwarding mechanism, (5) failure fallback. Reference twilio-voice-conversation-relay for any voice audio specifics.

## Reference

- Assistants base: `https://assistants.twilio.com/v1/Assistants`, `/Assistants/{Sid}/Sessions`, `/Sessions/{Sid}/Messages`, plus `/Tools` and `/Knowledge`.
- Auth: HTTP Basic with `AccountSid`:`AuthToken` (or API key SID/secret). SIDs: Assistant `AI...`, session identifiers per API.
- Voice binding: TwiML `<Connect><ConversationRelay url="wss://..." />`; the relay speaks over a WebSocket. TTS/STT providers and language are attributes on `<ConversationRelay>`.
- Messaging binding: Conversations API (`https://conversations.twilio.com/v1/Conversations`) with the assistant as a participant, or the assistant's channel binding for SMS/WhatsApp.
- Common webhook errors: 11200 (HTTP retrieval failure), 11205 (HTTP connection failure), 15003 (assistant/tool execution error class). Voice webhooks must return valid TwiML or the call drops.
- Handoff: Flex/TaskRouter (Tasks, Workflows, Workers) or a custom webhook; preserve Session transcript and any collected slots.
- Webhook security: validate `X-Twilio-Signature`; respond within Twilio's HTTP timeout (~15s for standard webhooks) or the call/message flow fails.
