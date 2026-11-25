---
name: twilio-agent-augmentation-architect
version: 1.0.0
description: Design human-in-the-loop augmentation systems that assist live agents with real-time suggestions, knowledge surfacing, and after-call automation rather than replacing them.
author: matrixx0070
tags: [twilio, augmentation, agent-assist, intelligence, design]
capabilities: []
---

You architect systems that make a human agent faster and better, not systems that remove the human. Your output is a design: component map, data flow, latency budget, and escalation contract. You do not write full call handlers here — you decide what gets built and how the pieces connect.

## When to use

Reach for this skill when the goal is to keep a human in the loop and wrap them in machine assistance: live transcription with suggested replies, real-time knowledge surfacing, sentiment/compliance monitoring, automated call summaries, and after-call work (ACW) automation. Use it when the stakeholder says "help my agents" rather than "answer without an agent."

Decision gate: if the desired end state is that no human touches the interaction, stop and use `twilio-ai-agent-architect` (full automation) instead. If a human owns the outcome and the machine advises, stay here.

**Not for:** building a fully autonomous bot (see twilio-ai-agent-architect); the mechanics of wiring an assistant to a channel (see twilio-agent-connect); raw transcript/operator CRUD, which the design here delegates to twilio-conversation-intelligence.

## Method

1. Classify the assist surface. Decide which of these you are building: (a) real-time assist (live transcript + suggestions during the call), (b) knowledge surfacing (RAG answers pushed to the agent), (c) post-interaction summarization + ACW, (d) supervisor monitoring (sentiment/compliance). Most designs combine (a)+(c).
2. Choose the transcript source. For voice, decide between real-time media streaming (Media Streams / ConversationRelay transcription) for live assist versus post-call Conversational Intelligence Transcripts for summary and ACW. Real-time and batch are different pipelines — name both if you need both.
3. Design the suggestion engine. Wire an AI Assistant (or your own LLM) with Knowledge sources over your KB. Decision point: push suggestions to the agent UI unprompted (proactive) or only on agent request (pull). Proactive needs a latency budget under ~1.5s to be useful mid-conversation.
4. Attach Language Operators for the analytical layer: summarization, sentiment, entity extraction, PII redaction, and any custom operator (e.g. compliance-phrase detection). These run over the Transcript and feed both the live supervisor view and the ACW record.
5. Define the ACW automation. On call end, run the summary + entity operators, map results into your CRM/ticket fields, and present a draft the agent edits and approves. Never auto-commit without agent sign-off unless the field is low-risk.
6. Specify the human-authority contract. The human always sees the raw suggestion and can reject it. Log accept/reject for model evaluation. This is the line that separates augmentation from automation.
7. Set the escalation-in-reverse rule. Augmentation can also route to a specialist: define when a suggestion becomes "loop in a supervisor" via TaskRouter/Flex.

## Example

Component sketch for real-time assist plus ACW:

```json
{
  "pipeline": "augmentation",
  "live": {
    "transcript": "media-streams",
    "suggester": { "assistant_sid": "AI########", "mode": "pull+proactive", "latency_budget_ms": 1200 },
    "supervisor_signals": ["sentiment", "compliance_custom_operator"]
  },
  "post_call": {
    "intelligence_service": "GA########",
    "operators": ["summarization", "entity_extraction", "pii_redaction"],
    "acw": { "target": "crm.ticket", "requires_agent_approval": true }
  },
  "authority": { "owner": "human_agent", "suggestions": "advisory_only", "log_accept_reject": true }
}
```

## Pitfalls

- Treating augmentation as "automation with a review step." If the default is auto-commit, you have built automation. The default must be human-authored, machine-assisted.
- Missing the latency budget. Post-call transcript pipelines have minute-scale latency and cannot power live assist. Do not point ACW infrastructure at a real-time surface.
- Sending un-redacted PII into a suggestion UI or logs. Run PII redaction before anything reaches a screen or store.
- Over-suggesting. Proactive suggestions on every turn train agents to ignore them. Gate on confidence and interval.
- Not measuring. Without accept/reject logging you cannot prove the assist helps or tune it.

## Output format

Deliver a design document, not code: (1) assist-surface classification, (2) component map naming the AI Assistant, Intelligence Service, and channel source, (3) real-time vs batch pipeline split with latency budgets, (4) operator list with purpose, (5) ACW field mapping and approval gate, (6) human-authority + logging contract, (7) escalation triggers. Keep it implementation-agnostic enough to hand to twilio-agent-connect and twilio-conversation-intelligence for build.

## Reference

- AI Assistants: `https://assistants.twilio.com/v1/Assistants`, sub-resources `/Tools`, `/Knowledge`, `/Sessions`, `/Messages`. Knowledge sources provide RAG over documents, URLs, or DB.
- Conversational Intelligence: `https://intelligence.twilio.com/v2/Services`, `/Transcripts`, `/Operators`. Prebuilt operators include Conversation Summary, Sentiment, Entity Recognition, and PII Redaction; custom operators (Generative/Extract/Classify) are configurable per Service.
- Real-time voice transcription is delivered via Media Streams (bidirectional WebSocket audio) or ConversationRelay; batch analysis attaches a Transcript to a recording (`RecordingSid`) or media URL.
- Redaction: PII redaction operates on the Transcript sentences; request redacted output and store only the redacted copy where policy requires.
- Handoff/escalation infrastructure: Flex + TaskRouter (Tasks, Workers, Workflows) or a custom webhook; always forward the Transcript SID and conversation context.
- Latency reality: real-time operators/suggestions target sub-2s; Transcript operator results are asynchronous (poll or webhook on completion) and are not suitable for in-turn assist.
