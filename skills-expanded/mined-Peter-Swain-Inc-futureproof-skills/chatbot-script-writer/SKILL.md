---
name: chatbot-script-writer
description: |
  Writes and optimizes full chatbot conversation scripts — intent
  taxonomies, slot-filling flows, escalation handoffs, and edge-case
  hardening — for web widgets, WhatsApp, SMS, IVR, and in-app support
  channels. Use when the user says "write a chatbot script", "build a
  support bot flow", "rewrite my Intercom/Zendesk bot", "improve
  containment rate", or "design intent handling for [use case]". This is
  the automated-bot scripting skill; for human-written replies to public
  reviews use review-response-writer, and for one-off complaint responses
  use customer-complaint-handler.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="chatbot-script-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, brand voice guidelines, prior chatbot performance data, and any established escalation protocols.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Channel & platform**: Where will this chatbot live? (web widget, WhatsApp, SMS, in-app, Facebook Messenger, voice IVR)
- **Use case scope**: What intents must the script handle? (e.g., order status, returns/refunds, billing inquiries, product troubleshooting, appointment scheduling, FAQ deflection)
- **ICA profile**: Who is the primary audience? (e.g., first-time buyers, enterprise account holders, subscription members — demographics, technical literacy, emotional state on entry)
- **Existing materials**: Share any current chatbot scripts, call centre scripts, FAQ documents, or CRM workflow diagrams to build from
- **Brand voice & tone constraints**: Formal, conversational, playful, empathetic? Any prohibited phrases or compliance language requirements?
- **Success metric**: What is the primary KPI? (containment rate, CSAT score, first-contact resolution, escalation reduction, average handle time)
- **Escalation rules**: When and how should the bot hand off to a live agent?

## Step 3: Do the Work

### 3A: Intent Architecture Mapping

Build a complete **Intent Taxonomy** by:
1. Categorising every in-scope intent into tiers — **Primary** (>60% of anticipated volume), **Secondary** (20–35%), and **Edge Case** (<5%)
2. Mapping each intent to a **resolution pathway** (self-serve deflection, guided troubleshooting, data lookup via API, or agent escalation)
3. Identifying **intent overlap zones** — ambiguous user inputs that could match multiple intents — and defining disambiguation logic

### 3B: Conversation Flow Design

For each intent, script the following nodes:

1. **Greeting & intent detection** — opening message that sets expectations (bot identity disclosure, scope of help available) and captures the user's need via quick-reply buttons, free-text parsing, or both
2. **Clarification & slot-filling** — progressive disclosure questions to collect required data (order number, account email, product SKU) with validation logic and error-recovery prompts
3. **Resolution delivery** — the answer, action confirmation, or next-step instruction written in language that mirrors the ICA's vocabulary and reading level
4. **Satisfaction check** — micro-survey ("Did this solve your issue?") with branching: positive → close, negative → secondary attempt or escalation
5. **Graceful escalation** — warm handoff script that transfers collected context to the live agent so the customer never repeats themselves
6. **Dead-end recovery** — fallback responses for unrecognised inputs, repeated failures, and silence timeouts

### 3C: Script Quality Audit

Evaluate every scripted node against six dimensions:

| Dimension | Standard |
|---|---|
| **ICA empathy alignment** | Language acknowledges the user's emotional state (frustration, urgency, confusion) before delivering procedural steps |
| **Cognitive load minimisation** | Each message ≤ 60 words; no more than one question per turn; buttons offered for predictable answers |
| **Resolution directness** | Bot reaches resolution or escalation within ≤ 5 turns for primary intents |
| **Error tolerance** | Misspellings, synonyms, and partial inputs are handled without dead-ending the conversation |
| **Compliance & disclosure** | Data collection prompts include purpose statements; bot identifies itself as automated where legally required |
| **Brand voice consistency** | Tone, terminology, and personality remain uniform across every node and intent path |

Apply any user-specific `instructions` from FutureProof context (e.g., mandatory legal disclaimers, preferred escalation thresholds, A/B test directives from prior experiments).

### 3D: Edge Case & Abuse Hardening

Script defensive paths for:
- **Profanity and abuse** — empathetic de-escalation response followed by escalation offer, not silence
- **Personally identifiable information volunteered unsolicited** — redaction advisory and secure-channel redirect
- **Looping behaviour** — detection of 3+ repeated identical inputs with circuit-breaker escalation
- **Multi-intent messages** — acknowledgement of both needs with sequential handling or triage prioritisation

## Step 4: Deliver Output

Produce a **Chatbot Script Package** containing:

### 4A: Intent Map (Visual)
A structured table or tree diagram listing every intent, its tier, resolution pathway, and estimated volume share.

### 4B: Full Conversation Scripts
For each intent, deliver:
- **Bot messages**: exact copy, including emoji/formatting if platform-appropriate
- **Quick-reply button labels**: character-limited, action-oriented
- **Conditional logic annotations**: branching rules in `IF/THEN` pseudocode for developer handoff
- **API call placeholders**: clearly marked points where the bot must query backend systems (e.g., `{{LOOKUP: order_status(order_id)}}`)
- **Agent handoff payload**: structured summary template passed to the live agent queue

### 4C: Score Card

| Dimension | Score (1–10) | Critical Gap |
|---|---|---|
| ICA empathy alignment | — | — |
| Cognitive load minimisation | — | — |
| Resolution directness | — | — |
| Error tolerance | — | — |
| Compliance & disclosure | — | — |
| Brand voice consistency | — | — |

### 4D: Critical Fixes
Top 3 highest-impact changes — each with the **original copy**, the **specific rewrite**, and the **rationale** tied to the target KPI.

### 4E: Implementation Checklist
Sequenced developer/ops handoff checklist: platform configuration, API integrations required, QA test scenarios, and go-live sign-off criteria.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="chatbot-script-writer", experiment={
  hypothesis: "Replacing the generic greeting with an intent-predictive opening based on page context reduces average turns-to-resolution by 20%",
  variants: ["control: generic greeting with open-ended 'How can I help?'", "variant: contextual greeting pre-selecting likely intent based on referral page or prior session"],
  measurement: "Average turns-to-resolution and containment rate across 1,000 conversations",
  expected_impact: "20% reduction in turns-to-resolution, 8% improvement in containment rate"
})
```

```
FutureProof:save_experiment(skill="chatbot-script-writer", experiment={
  hypothesis: "Adding an empathy acknowledgement turn before procedural instructions improves CSAT by 10%",
  variants: ["control: immediate procedural response", "variant: empathy statement ('I understand how frustrating that is — let me fix this now') followed by procedural response"],
  measurement: "Post-chat CSAT score and escalation rate over 2-week period",
  expected_impact: "10% CSAT improvement, 5% escalation reduction"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="chatbot-script-writer",
  query="Latest benchmarks for chatbot containment rates, CSAT scores, and first-contact resolution by industry vertical 2024–2025, including impact of generative AI hybrid approaches on deflection quality",
  reason="Calibrate score card thresholds and resolution-path design against current industry performance standards"
)
```

```
FutureProof:request_research(skill="chatbot-script-writer",
  query="Emerging compliance requirements for automated customer service bots including EU AI Act disclosure obligations, ADA/WCAG accessibility standards for conversational interfaces, and CCPA/GDPR data collection in chat",
  reason="Ensure script compliance guidance reflects current and forthcoming regulatory obligations"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="chatbot-script-writer", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```