---
name: twilio-customer-support-architect
version: 1.0.0
description: Design an AI-powered omnichannel customer support system on Twilio — deflection with AI Assistant plus Knowledge, Conversations intake, human handoff via Flex/TaskRouter, CSAT, and metrics.
author: matrixx0070
tags: [twilio, support, architecture, ai-assistant, handoff]
capabilities: []
---

## When to use

Use this at architecture altitude: you are laying out how an AI-first support experience fits together on Twilio — which channels feed intake, where the AI Assistant deflects, when and how a conversation escalates to a human agent, how you measure containment and CSAT, and where each responsibility lives. It decides structure and routes the concrete pieces to the sibling skills.

**Not for:** wire-level Conversations calls (route to twilio-conversations-classic-api), building/grounding the RAG knowledge base (route to twilio-enterprise-knowledge), or the agent's cross-session memory design (route to twilio-conversation-memory). Session/channel orchestration goes to twilio-conversation-orchestrator.

## Method

1. Map channels to intake. Enumerate entry points (SMS, WhatsApp, web chat, voice, email) and funnel messaging channels through Conversations so every thread is one uniform object. Decision point: use per-tenant Conversation Services (`IS...`) if you serve multiple brands/business units.
2. Define the deflection layer. Front the conversation with an AI Assistant grounded on Knowledge (RAG). The assistant answers FAQs and self-service intents with citations. Decision point: set a confidence/grounding threshold below which the assistant must not answer and instead escalates.
3. Design intent + routing. Classify each inbound turn (billing, tech, sales, account). Route resolvable intents to the assistant; route high-risk or low-confidence intents (payments disputes, cancellations, legal) straight to humans.
4. Specify escalation/handoff. On escalation, hand the live Conversation to Flex via TaskRouter: create a Task carrying the conversation SID plus a summary and captured facts, and add the selected agent as a participant. Decision point: warm handoff (assistant posts a summary, human joins the same thread) vs cold transfer (new thread) — prefer warm to preserve context.
5. Preserve continuity across the handoff. The human agent must see prior turns and known facts — source them from twilio-conversation-memory so the customer never repeats themselves.
6. Instrument metrics. Track containment/deflection rate, escalation rate, first-contact resolution, handle time, and grounding/citation coverage. Decision point: alert when deflection drops or escalation spikes — usually a stale Knowledge base (see twilio-enterprise-knowledge freshness).
7. Capture CSAT. After resolution, trigger a short survey (post-conversation message or Flex survey) and store the score against the conversation and agent/assistant that handled it.
8. Close the loop. Feed low-CSAT and frequent-escalation intents back into Knowledge and assistant prompt refinement.

## Example

```json
{
  "intake": {
    "channels": ["sms", "whatsapp", "webchat"],
    "unified_via": "twilio-conversations",
    "service_sid": "ISxxxxxxxx"
  },
  "deflection": {
    "assistant": "AI Assistant + Knowledge (RAG)",
    "answer_if": "grounding_confidence >= 0.7",
    "must_cite": true
  },
  "routing": {
    "auto_escalate_intents": ["cancel_subscription", "payment_dispute", "legal"],
    "classifier": "intent-model"
  },
  "handoff": {
    "engine": "taskrouter",
    "surface": "flex",
    "mode": "warm",
    "task_attributes": {
      "conversation_sid": "CHxxxxxxxx",
      "summary": "<assistant-generated>",
      "facts": {"plan": "pro", "open_ticket": "T-4821"}
    }
  },
  "metrics": ["deflection_rate", "escalation_rate", "fcr", "handle_time", "csat"],
  "csat": {"trigger": "on_resolved", "scale": "1-5"}
}
```

## Pitfalls

- Letting the assistant answer below its grounding threshold produces confident wrong answers; gate on grounding and escalate on low confidence.
- Cold transfers that drop context force customers to repeat themselves and tank CSAT. Design warm handoffs carrying a summary.
- Measuring deflection without measuring CSAT rewards silent failure (deflected but unresolved). Track both together.
- No stale-Knowledge alerting: deflection quietly degrades as the base ages. Tie metrics to Knowledge freshness.
- Treating each channel as a separate silo. Unify on Conversations so a thread is one object regardless of channel.
- Escalating without passing the conversation SID/facts to TaskRouter leaves the human agent blind.

## Output format

Produce an architecture spec (JSON or a labeled outline) covering: intake channels + unification, deflection layer + grounding threshold, intent/routing rules, handoff engine + mode + task attributes, metrics list, and CSAT trigger. For each component, name the sibling skill that owns implementation.

## Reference

- AI Assistants + Knowledge (RAG): base `https://assistants.twilio.com/v1`; Knowledge under `https://assistants.twilio.com/v1/Knowledge`. The assistant grounds answers on ingested sources and returns citations — the deflection engine.
- Conversations (omnichannel intake): `https://conversations.twilio.com/v1` — Conversations `CH`, Participants `MB` (SMS/WhatsApp bindings) / `Identity` (chat), Messages `IM`, Services `IS`. Full call details in twilio-conversations-classic-api.
- Human handoff: TaskRouter creates Tasks routed to Workers via Workflows and TaskQueues; Flex is the agent desktop surface. Warm handoff = post assistant summary into the Conversation, then add the human as a participant on the same `CH...` thread.
- Continuity across handoff: sourced from AI Assistant Sessions + your own memory store (see twilio-conversation-memory).
- Metrics to instrument: deflection/containment rate, escalation rate, first-contact resolution, average handle time, grounding/citation coverage, CSAT. Stale Knowledge is the usual root cause of falling deflection.
- Limits inherited from Conversations: 32KB message body, ~1000 participants per conversation, media via MCS.
