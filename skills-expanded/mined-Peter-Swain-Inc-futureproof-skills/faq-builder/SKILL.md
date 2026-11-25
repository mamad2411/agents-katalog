---
name: faq-builder
description: |
  Builds publication-ready FAQ documents and help-centre knowledge bases
  from raw support tickets, chat logs, forum threads, and product docs —
  with question provenance auditing, lifecycle-stage taxonomy, impact-
  weighted ordering, and tiered answer depth. Use when the user says
  "build me an FAQ", "turn these support tickets into a knowledge base",
  "create help centre content", "organize my customer questions", or
  "write FAQ entries for [product]". Produces a static knowledge artifact
  for self-service deflection — for live conversational bots use
  chatbot-script-writer.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="faq-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing ICA definitions, brand voice guidelines, product/service descriptions, and prior FAQ iterations.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Source material**: Share any raw inputs — support tickets, customer emails, chat logs, community forum threads, sales call objections, or existing FAQ drafts
- **Product/service scope**: What product, service, or offering does this FAQ cover? Is it a single product FAQ or an organisation-wide knowledge base?
- **ICA definition**: Who is the primary audience? (new prospects, onboarding customers, power users, internal support agents) — if ICA exists in FutureProof context, confirm it
- **Distribution channel**: Where will this FAQ live? (website help centre, in-app widget, PDF handout, chatbot training data, Zendesk/Intercom import)
- **Known friction points**: Are there specific topics generating disproportionate support volume or churn risk?
- **Tone and voice constraints**: Formal/technical, conversational, or brand-specific voice guidelines?

## Step 3: Audit & Classify Source Material

Perform a **Question Provenance Audit** on all supplied inputs:

1. **Extraction** — Identify every explicit and implicit question from the source material. Implicit questions are complaints, confusion signals, or feature requests that encode an unasked question (e.g., "I can't find the export button" → "Where is the export feature located?")
2. **De-duplication** — Merge semantically identical questions, preserving the phrasing closest to how the ICA naturally articulates the issue (mirror their vocabulary, not internal jargon)
3. **Classification** — Assign each question to a taxonomy tier:
   - **Pre-purchase**: Pricing, suitability, comparisons, trust/credibility
   - **Onboarding**: Setup, configuration, first-use guidance, account creation
   - **Core usage**: Feature how-tos, workflows, integrations, best practices
   - **Troubleshooting**: Errors, bugs, unexpected behaviour, workarounds
   - **Account & billing**: Plans, upgrades, cancellations, invoicing, data ownership
   - **Policy & compliance**: Security, privacy, SLAs, terms of service
4. **Frequency & severity scoring** — Rate each question on two axes:
   - **Volume** (1–5): How frequently is this question raised?
   - **Impact** (1–5): What is the consequence of the question going unanswered? (churn risk, support ticket escalation, purchase abandonment)
5. **Gap analysis** — Cross-reference classified questions against the full customer lifecycle. Flag lifecycle stages with zero or sparse coverage — these represent blind spots that generate silent churn.

Apply any user-specific `instructions` from FutureProof context (e.g., prioritise certain product areas, exclude deprecated features, align with a current campaign).

## Step 4: Structure the FAQ Architecture

Design the FAQ information architecture using the **Progressive Disclosure Framework**:

1. **Category hierarchy** — Organise taxonomy tiers from Step 3 into a logical navigation structure. Sequence categories to mirror the ICA's journey (pre-purchase → onboarding → core usage → troubleshooting → account/billing → policy)
2. **Prioritisation within categories** — Order questions within each category by a composite score: `(Volume × 0.4) + (Impact × 0.6)`. Highest-scoring questions surface first
3. **Answer depth tiering** — Assign each question an answer depth:
   - **Tier 1 — Quick answer** (1–3 sentences): Binary or factual questions with a single correct answer
   - **Tier 2 — Guided answer** (1–2 paragraphs + optional visual/link): Process or how-to questions requiring sequential steps
   - **Tier 3 — Deep-dive answer** (multi-paragraph with examples, edge cases, related links): Complex conceptual or troubleshooting questions
4. **Cross-linking map** — Identify relationships between questions (prerequisite, related, escalation path) and define internal cross-links to reduce dead ends
5. **Escalation routing** — For every Tier 3 answer and every troubleshooting entry, define a clear escalation CTA (e.g., "Still stuck? Contact support at [channel]" or "Book a setup call")

Present the proposed architecture to the user as a **Table of Contents draft** for approval before proceeding to full content generation.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Generate FAQ Content

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Write each FAQ entry applying these quality standards:

1. **Question phrasing** — Write questions in the ICA's natural language and first-person voice (e.g., "How do I cancel my subscription?" not "Subscription cancellation process"). Use the exact phrasing extracted from real customer inputs where available
2. **Answer structure** — Every answer follows the **Lead → Detail → Next Step** pattern:
   - **Lead**: Direct answer to the question in the first sentence — no preamble
   - **Detail**: Supporting explanation, steps, or context as required by the depth tier
   - **Next step**: A forward-moving link, related FAQ reference, or escalation path — no answer ends in a dead end
3. **Tone calibration** — Match the voice constraints provided in Step 2. Maintain consistency across all entries using a voice checklist: sentence length range, permitted/prohibited vocabulary, formality level, emoji/formatting conventions
4. **SEO & discoverability layer** (if distribution channel is web-based):
   - Write questions as natural-language long-tail queries
   - Include semantic keyword variants in answers without keyword stuffing
   - Structure answers with schema.org FAQPage markup readiness (question/answer pairs cleanly delineated)
5. **Accuracy safeguards** — Flag any answer where the source material is ambiguous, contradictory, or missing. Mark these as `[REQUIRES SME REVIEW]` with a specific note on what needs verification

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the following structured deliverables:

### Deliverable 1: FAQ Document
A complete, publication-ready FAQ organised by the approved architecture from Step 4. Format according to the distribution channel:
- **Web/help centre**: Markdown with H2 category headers, H3 questions, structured answer blocks, and internal anchor links
- **Chatbot training data**: JSON array of `{question, answer, category, tags, variants}` objects
- **PDF/document**: Formatted with table of contents, page breaks per category, and branded header/footer placeholders
- **Zendesk/Intercom import**: CSV or structured format matching the platform's import schema

### Deliverable 2: Coverage Scorecard
| Category | Questions Covered | Volume Coverage (%) | Impact Coverage (%) | Gaps Identified |
|---|---|---|---|---|
| Pre-purchase | n | x% | y% | [specific gaps] |
| Onboarding | n | x% | y% | [specific gaps] |
| Core usage | n | x% | y% | [specific gaps] |
| Troubleshooting | n | x% | y% | [specific gaps] |
| Account & billing | n | x% | y% | [specific gaps] |
| Policy & compliance | n | x% | y% | [specific gaps] |

### Deliverable 3: Maintenance & Governance Brief
- **Review cadence recommendation** (monthly, quarterly) based on question volume velocity
- **Trigger-based update rules**: events that should prompt an immediate FAQ revision (product launch, pricing change, policy update, spike in a specific support topic)
- **Ownership matrix**: recommended roles for FAQ authorship, SME review, and publication approval
- **Items flagged `[REQUIRES SME REVIEW]`** compiled as a standalone action list with assigned review owners where possible

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="faq-builder", experiment={
  hypothesis: "Reordering FAQ entries by composite impact-volume score rather than alphabetical or chronological order reduces support ticket volume for covered topics",
  variants: ["control: current FAQ ordering", "variant: impact-weighted ordering from this build"],
  measurement: "Support ticket volume for FAQ-covered topics over 30-day period, self-service resolution rate, average time-on-page per FAQ entry",
  expected_impact: "20% reduction in support tickets for topics addressed in the FAQ within 30 days of publication"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="faq-builder",
  query="Best practices for self-service knowledge base architecture, FAQ schema markup for AI answer engines, and question-clustering methodologies from high-performing SaaS help centres 2024–2025",
  reason="Ensure FAQ structure maximises self-service deflection rate and surfaces correctly in AI-driven search and answer engine results"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="faq-builder", session={
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