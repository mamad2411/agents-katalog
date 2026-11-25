---
name: twilio-ai-agent-architect
version: 1.0.0
description: Design a Twilio AI voice and messaging agent end to end — choosing ConversationRelay vs AI Assistants vs custom, wiring LLM plus tools and knowledge, channels, guardrails, handoff, and observability.
author: matrixx0070
tags: [twilio, ai, architecture, assistants, agent]
capabilities: []
---

## When to use

Use this when you are deciding the shape of a Twilio AI agent before writing implementation code: which building block to stand on, how the LLM connects to tools and knowledge, which channels attach, and how humans take over. This is a design skill — it makes the architecture decisions and then routes you to sibling skills for the wiring.

**Not for:** the ConversationRelay WebSocket protocol itself (see twilio-voice-conversation-relay); connecting a live agent handoff leg (see twilio-agent-connect); or session/state orchestration across turns and channels (see twilio-conversation-orchestrator).

## Method

1. Decision point — build block:
   - You own the LLM and want maximum control over prompting, tools, and latency → ConversationRelay + your server. Most flexible; you operate the model.
   - You want Twilio to host the assistant, knowledge, and tool orchestration with less code → Twilio AI Assistants (LLM-backed, with Tools + Knowledge, attachable to channels). Note: an evolving product; confirm current GA status and limits before committing.
   - You need something neither covers (custom media pipeline, on-prem model) → custom on `<Connect><Stream>` Media Streams, owning STT/TTS.
2. Map channels: voice (ConversationRelay or Assistants voice attachment), SMS/MMS, WhatsApp, and web chat. Decide which are in scope and whether one agent brain serves all.
3. Design the LLM layer: system prompt, tool schema, and retrieval. With Assistants, register Tools (webhooks the assistant may call) and Knowledge (documents/URLs for grounding). With ConversationRelay, you implement tools and RAG in your own server.
4. Define guardrails: input/output filtering, refusal policy, PII redaction, max turn length, and cost/latency budgets. Voice needs tighter latency than chat.
5. Design handoff to human: detection trigger (intent, sentiment, explicit request), then transfer the voice leg or escalate the messaging thread — route to twilio-agent-connect for the live leg.
6. Design state: what persists per session and across channels — route to twilio-conversation-orchestrator.
7. Observability: log every turn (prompt, tool calls, tokens, latency), capture recordings for QA (twilio-call-recordings), and wire status callbacks. Add feedback capture (Assistants exposes a feedback endpoint).
8. Decision point — go-live: pilot on one channel, measure containment/handoff rate and cost per session, then expand.

## Example

Sketch of an AI Assistant with a tool and knowledge, then attached to voice via ConversationRelay (conceptual REST):

```bash
# Create the assistant
curl -X POST https://assistants.twilio.com/v1/Assistants \
  -u "$SID:$TOKEN" \
  -d "Name=support-agent" \
  -d "Personality=You are a concise, friendly support agent."

# Register a tool (a webhook the assistant may invoke)
curl -X POST https://assistants.twilio.com/v1/Assistants/$AID/Tools \
  -u "$SID:$TOKEN" \
  -d "Name=lookup_order" \
  -d "Type=Webhook" \
  -d "Url=https://example.com/tools/lookup_order"

# Attach knowledge for grounding
curl -X POST https://assistants.twilio.com/v1/Assistants/$AID/Knowledge \
  -u "$SID:$TOKEN" \
  -d "Name=faq" -d "Type=Web" -d "Url=https://example.com/faq"
```

Voice entry point that routes the call into your agent brain:

```xml
<Response>
  <Connect>
    <ConversationRelay url="wss://example.com/relay" ttsProvider="ElevenLabs" interruptible="true" />
  </Connect>
</Response>
```

## Pitfalls

- Choosing Assistants for its convenience, then hitting a hard limit that forces a rewrite onto ConversationRelay — validate tool/knowledge/latency limits against your requirements first.
- Treating voice like chat: voice demands sub-second first-token latency and barge-in; a chat-tuned prompt that streams slowly feels broken on a call.
- No handoff path: an agent with no escalation traps frustrated callers. Design the human exit before launch.
- Unbounded tool calls balloon latency and cost per turn; cap tool-call depth and set a budget.
- Assistants products are evolving; pin to documented, current endpoints and re-verify before production.
- Skipping observability means you cannot measure containment rate or debug bad turns after the fact.

## Output format

The deliverable of this skill is an architecture decision, not runtime output: a chosen build block, a channel map, an LLM/tool/knowledge wiring plan, guardrail and handoff policies, and an observability plan — each pointing at the sibling skill that implements it.

## Reference

- Build blocks:
  - ConversationRelay — TwiML `<Connect><ConversationRelay>`; you bring the LLM, Twilio does STT/TTS over a WebSocket. Lowest-level of the managed options, most control. See twilio-voice-conversation-relay.
  - Twilio AI Assistants — REST under `https://assistants.twilio.com/v1/Assistants` with sub-resources: `/Assistants/{Sid}/Tools`, `/Assistants/{Sid}/Knowledge`, plus feedback. LLM-backed assistants with hosted tools and knowledge, attachable to voice (via ConversationRelay), messaging, and web. Successor line to Autopilot; treat as evolving and verify GA/limits.
  - Custom Media Streams — `<Connect><Stream>` delivering base64 mulaw 8 kHz frames; you own the full STT/LLM/TTS pipeline.
- Channels: Programmable Voice, Programmable Messaging (SMS/MMS), WhatsApp Business, and web chat all attach to the same agent brain if you centralize state.
- Auth: HTTP Basic with Account SID + Auth Token (or API Key/Secret) on all REST calls.
- Cost model: standard per-minute voice / per-message rates, plus STT/TTS provider usage, plus your LLM tokens. Budget per session, not per request.
- Route implementation: voice protocol → twilio-voice-conversation-relay; live human handoff leg → twilio-agent-connect; cross-turn/cross-channel session state → twilio-conversation-orchestrator; QA recording → twilio-call-recordings.
