---
name: twilio-conversation-orchestrator
version: 1.0.0
description: Orchestrate multi-turn, multi-channel Twilio Conversations — routing each turn to AI or human, managing participants, state, tool invocation, and escalation.
author: matrixx0070
tags: [twilio, conversations, orchestration, routing, escalation]
capabilities: []
---

You are the control loop over a live Twilio Conversation. Participants (customer, AI, human agents) share one thread across SMS, WhatsApp, chat, and MMS. You decide who responds to each incoming Message, when to invoke tools, when to escalate, and how state carries forward.

## When to use

Use this when a conversation spans many turns and possibly many channels or participants, and something must decide per turn whether the AI answers, a human answers, or a tool runs. Covers turn routing, participant management, channel binding, escalation triggers, and holding conversational state.

Decision gate: is there real routing logic (AI-vs-human, tool dispatch, escalation)? If you only need to create a Conversation and add participants (plain CRUD), drop to twilio-conversations-classic-api. If you need durable long-term memory/summarized history, pair with twilio-conversation-memory.

**Not for:** raw Conversations resource CRUD and address-configuration mechanics (see twilio-conversations-classic-api); persisting/summarizing long-term memory across sessions (see twilio-conversation-memory); the analytics layer over finished transcripts (see twilio-conversation-intelligence).

## Method

1. Establish the Conversation. Get or create the Conversation SID (`CH...`) for this customer thread. Bind the customer's address (phone/whatsapp/chat identity) as a participant so inbound messages land in the thread.
2. Register participants and roles. Tag each participant: `customer`, `ai`, `human_agent`, `supervisor`. Role drives routing.
3. Subscribe to the message webhook. Configure the Conversation's `/Webhooks` (or the service-scoped webhook) for `onMessageAdded`. Every inbound turn hits your orchestrator.
4. Route the turn. On each `onMessageAdded` from the customer, decide:
   - AI handles it (default) → send to the assistant, post its reply as the `ai` participant's Message.
   - Tool needed → invoke the tool, then let the AI compose a reply from the result.
   - Human handles it → suppress AI, notify the assigned human; when a human is active, AI stays silent unless re-enabled.
   Guard against loops: ignore `onMessageAdded` events authored by the `ai` participant.
5. Track state. Keep per-conversation state (current owner, open slots, escalation flag). Store it in Conversation `attributes` (JSON) or your own store keyed by Conversation SID.
6. Evaluate escalation triggers each turn: explicit request, negative sentiment, low AI confidence, repeated failure, or a tool signaling human-required. On trigger, flip owner to `human_agent`, add the human participant, and route via TaskRouter/Flex.
7. Manage channel transitions. If the customer moves channels, bind the new address to the same Conversation so history stays unified rather than forking a new thread.
8. Close out. On resolution, mark state resolved; optionally hand the transcript to the intelligence layer for summary/ACW.

## Example

Orchestrator turn handler (Node, pseudo-real):

```js
// Webhook: onMessageAdded
export async function onMessageAdded(evt) {
  if (evt.Author === "ai") return; // never react to our own turns

  const state = await loadState(evt.ConversationSid);
  if (state.owner === "human_agent") return; // human is driving, stay silent

  if (shouldEscalate(evt, state)) {
    await addHumanParticipant(evt.ConversationSid);
    await setState(evt.ConversationSid, { ...state, owner: "human_agent", escalated: true });
    await postSystemMessage(evt.ConversationSid, "A specialist is joining.");
    return;
  }

  const aiReply = await assistant.turn(state.sessionSid, evt.Body);
  if (aiReply.toolCall) {
    const result = await runTool(aiReply.toolCall);
    aiReply.text = await assistant.compose(state.sessionSid, result);
  }
  await postMessage(evt.ConversationSid, { author: "ai", body: aiReply.text });
  await setState(evt.ConversationSid, { ...state, lastAiConfidence: aiReply.confidence });
}
```

## Pitfalls

- AI reply loops: not filtering out messages authored by the AI participant causes the bot to answer itself. Always guard on `Author`.
- Both AI and human replying at once: without an `owner` flag you get double replies. One owner per turn.
- Forking threads on channel switch: creating a new Conversation instead of binding the new address loses history. Rebind to the same `CH...`.
- Storing large state in `attributes`: the Conversation `attributes` JSON has a size cap (~65 KB / 65535 bytes). Keep it small; put bulk state in your own store.
- Webhook ordering/duplication: webhooks can retry and arrive out of order — make handlers idempotent (dedupe on Message SID).
- Escalating with no context: forward the transcript when flipping to human.

## Output format

Deliver: (1) participant role model, (2) webhook subscription config (`onMessageAdded` etc.), (3) the turn-routing decision table (customer turn → AI / tool / human), (4) escalation trigger list + owner-flip mechanism, (5) state model (where `owner`/slots live), (6) loop and idempotency guards. Route CRUD specifics to twilio-conversations-classic-api and memory to twilio-conversation-memory.

## Reference

- Conversations base: `https://conversations.twilio.com/v1/Conversations`; sub-resources `/Participants`, `/Messages`, `/Webhooks`. SID prefixes: Conversation `CH...`, Participant `MB...`, Message `IM...`, Service `IS...`.
- Scopes: conversation-scoped webhooks (per `CH...`) vs service-scoped (per Conversation Service `IS...`) vs account-global. Choose one level to avoid duplicate deliveries.
- Webhook event types: `onMessageAdded`, `onParticipantAdded`, `onConversationStateUpdated`, plus pre-action (`onMessageAdd`) variants that can block/modify.
- Address binding / autocreation: Address Configuration maps an inbound customer address (SMS/WhatsApp/chat) to a Conversation, autocreating one if none exists.
- `attributes` is a JSON string on Conversations, Participants, and Messages, limited to 65,535 bytes.
- Conversation state values: `active`, `inactive`, `closed`; a closed Conversation rejects new messages until reactivated (per service timers).
- Rate/error: 429 on rate limits; 50xxx-class Conversations errors for participant/binding conflicts. Handoff via TaskRouter (Tasks/Workflows/Workers) or Flex.
