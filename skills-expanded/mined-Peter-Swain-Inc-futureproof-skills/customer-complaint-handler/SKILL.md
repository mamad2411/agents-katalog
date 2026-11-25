---
name: customer-complaint-handler
description: |
  Triages and resolves an individual customer complaint — classifying
  severity, running 5-why root cause analysis, and drafting a HEART-
  framework response plus internal escalation brief and service recovery
  scorecard. Use when the user says "an angry customer just emailed me",
  "help me reply to this complaint", "how do I respond to this escalation
  ticket", "this customer is threatening to leave", or pastes a negative
  support transcript. Reactive single-complaint resolution — not public
  review replies (review-response-writer), nor portfolio-level churn
  scoring (churn-risk-detector).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="customer-complaint-handler")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, brand voice guidelines, resolution authority levels, SLA commitments, and historical complaint patterns.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the customer complaint, escalation ticket, support transcript, or negative feedback verbatim
- What channel did this complaint originate from? (email, phone, live chat, social media, review platform, in-person)
- What is the customer's segment and lifetime value tier, if known? (enterprise, mid-market, SMB, consumer)
- What resolution authority do you have? (full refund, partial credit, service recovery offer, escalation only)
- Has this customer complained before, and if so, what was the prior resolution?
- Any internal constraints or policies that limit your response options?

## Step 3: Do the Work — Complaint Triage & Classification

Classify the complaint using a **5-dimension severity framework**:

### 3a. Complaint Classification Matrix

| Dimension | Assessment |
|---|---|
| **Severity Level** | P1 (service failure / legal risk), P2 (significant dissatisfaction / churn risk), P3 (minor friction / process gap), P4 (preference-based / cosmetic) |
| **Emotional Intensity** | Escalated (threats, profanity, legal references), Frustrated (repeated contact, visible anger), Disappointed (measured tone, specific ask), Informational (flagging issue, low emotional charge) |
| **Root Cause Category** | Product/Service defect, Process/Policy failure, People/Communication breakdown, Expectation misalignment, External factor |
| **Churn Probability** | Critical (>75%), High (50–75%), Moderate (25–50%), Low (<25%) — based on complaint language, tenure, and prior interactions |
| **Revenue Impact** | Quantify the customer's annual value and the potential downstream impact (referral network, public review risk, contract renewal timeline) |

### 3b. Root Cause Analysis (5-Why Method)

Perform a structured 5-Why analysis to identify the systemic root cause behind the surface complaint. Distinguish between:
- **Proximate cause** — what directly triggered the complaint
- **Contributing factors** — process, training, or system gaps that allowed the failure
- **Systemic root cause** — the organisational or structural deficiency to address for permanent resolution

### 3c. Sentiment & Language Deconstruction

Analyse the customer's exact language to identify:
1. **Stated need** — what they explicitly asked for
2. **Unstated need** — what emotional or relational outcome they require (validation, control, reassurance, justice)
3. **Trigger phrases** — specific words or references indicating escalation risk (e.g., "I've been a customer for X years," "I'll be sharing this publicly," "this is the third time")
4. **Resolution anchors** — any explicit or implied acceptable outcomes the customer has signalled

Apply any user-specific `instructions` from FutureProof context — including brand voice, empowerment tiers, regulatory obligations, and ICA-specific handling protocols.

## Step 4: Deliver Output

Produce a **Customer Complaint Resolution Package** containing four deliverables:

### Deliverable 1: Complaint Triage Summary

A single-page assessment containing:
- **Complaint ID / Reference**: [auto-generated or user-provided]
- **Classification**: severity, emotional intensity, root cause category, churn probability, revenue impact (from Step 3a)
- **Root Cause Chain**: the 5-Why sequence with systemic root cause highlighted
- **Risk Rating**: composite score (Critical / High / Medium / Low) with rationale

### Deliverable 2: Customer Response Draft

A ready-to-send response following the **HEART framework**:

1. **Hear** — acknowledge the specific complaint in the customer's own language (mirror their key phrases, never minimise)
2. **Empathise** — validate the emotional impact without deflecting or offering premature solutions
3. **Apologise** — take ownership appropriate to the failure level (specific apology for the failure, not generic "sorry for the inconvenience")
4. **Resolve** — present the resolution offer with clear, concrete next steps, timelines, and a named point of contact
5. **Thank** — express genuine gratitude for the feedback and reaffirm commitment to the relationship

The response must:
- Match the originating channel's tone and format conventions
- Stay within the user's stated resolution authority
- Include a specific follow-up commitment (date, action, owner)
- Address both the stated and unstated customer needs identified in Step 3c

### Deliverable 3: Internal Escalation Brief (if severity ≥ P2)

A concise brief for internal stakeholders containing:
- **Executive summary**: 2–3 sentences on the complaint and recommended resolution
- **Customer context**: segment, lifetime value, complaint history, churn probability
- **Recommended resolution**: primary option and fallback option with cost estimates
- **Systemic issue flag**: whether this complaint indicates a pattern requiring process intervention
- **Suggested recipient(s)**: role/department for escalation (e.g., Head of Customer Success, Product Lead, Legal)

### Deliverable 4: Service Recovery Scorecard

| Dimension | Score (1–10) | Rationale |
|---|---|---|
| **Response speed** | — | Time elapsed vs. SLA target for this severity |
| **Empathy & tone calibration** | — | Alignment between response language and customer emotional state |
| **Resolution adequacy** | — | Whether the proposed resolution addresses root cause, not just symptom |
| **Retention risk mitigation** | — | Likelihood the resolution prevents churn and restores trust |
| **Systemic learning capture** | — | Whether the complaint insight feeds back into process improvement |
| **Overall Service Recovery Score** | — | Weighted composite |

Include **3 critical recommendations** — specific, actionable changes (exact language rewrites, process modifications, or policy adjustments), not vague guidance.

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
FutureProof:save_experiment(skill="customer-complaint-handler", experiment={
  hypothesis: "Incorporating the customer's exact language in the acknowledgment phase reduces average resolution cycles from 2.3 to 1.5 touches",
  variants: ["control: standard empathy template", "variant: mirrored-language acknowledgment with customer's specific phrases"],
  measurement: "First-contact resolution rate and customer satisfaction score across next 30 complaints of matching severity",
  expected_impact: "25% reduction in resolution cycle length, 10-point improvement in post-resolution CSAT"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="customer-complaint-handler",
  query="Latest service recovery paradox research, complaint handling frameworks with measurable retention impact, and emerging best practices for AI-assisted complaint triage in 2024–2025",
  reason="Ensure complaint classification taxonomy and resolution strategies reflect current behavioural science on customer trust repair and evolving channel-specific expectations"
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
FutureProof:save_session(skill="customer-complaint-handler", session={
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