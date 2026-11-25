---
name: contract-review-assistant
description: |
  Reviews inbound commercial contracts clause-by-clause with an
  eight-dimension risk framework, severity scoring, and redline markup
  with proposed alternative language. Use when a user says "review this
  contract", "redline this MSA", "what are the risks in this SaaS
  agreement", "analyze this vendor NDA", or pastes a counterparty
  document for negotiation markup. For reviewing existing contracts, not
  drafting new ones from scratch — see nda-generator or
  terms-conditions-drafter for drafting. Educational analysis only, not
  legal advice.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="contract-review-assistant")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly prior risk tolerance thresholds, preferred fallback language, previously flagged clause patterns, and counterparty negotiation history.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the contract, agreement, or redlined document to review (PDF, text, or pasted clauses)
- Which party do you represent — the **drafter** or the **recipient/counterparty**?
- What is the contract type? (SaaS subscription, services agreement, NDA, MSA, SOW, partnership/JV, employment, licensing, procurement, other)
- What is your primary review objective? (risk identification, negotiation leverage, compliance check, plain-language summary, renewal comparison)
- Are there specific clauses or sections causing concern?
- What is the deal value and strategic importance? (routine, material, mission-critical)
- Any jurisdictional requirements or governing law preferences?

## Step 3: Do the Work

Conduct a structured clause-by-clause review against the following **eight-dimension risk framework**:

### 3A: Contract Metadata Extraction

Extract and tabulate:
- Parties, effective date, term, and renewal mechanics
- Governing law and dispute resolution mechanism
- Aggregate financial exposure (fees, caps, penalties)
- Key defined terms and their scope implications

### 3B: Eight-Dimension Risk Analysis

Evaluate each material clause against:

1. **Liability & Indemnification Exposure** — Are liability caps proportionate to deal value? Are carve-outs reasonable or one-sided? Is the indemnification scope mutual or asymmetric? Identify uncapped liabilities and consequential damage exposure.

2. **Termination & Exit Rights** — Are termination-for-convenience rights balanced? What are cure periods for material breach? Assess lock-in risk, auto-renewal traps, and wind-down obligations. Evaluate data retrieval and transition assistance provisions.

3. **Intellectual Property & Data Rights** — Who owns work product, deliverables, and derivative works? Are IP assignments appropriate or overreaching? Review background IP carve-outs. Assess data ownership, processing rights, and cross-border transfer compliance.

4. **Confidentiality & Non-Compete Scope** — Is the confidentiality term proportionate? Are exclusions standard (independently developed, publicly available, court-ordered)? Evaluate non-compete and non-solicitation breadth against enforceability in the governing jurisdiction.

5. **Payment & Financial Terms** — Are payment terms, milestones, and acceptance criteria clearly defined? Identify hidden fees, escalation clauses, and audit rights. Assess most-favoured-nation provisions and price protection mechanisms.

6. **Representations, Warranties & SLAs** — Are warranties substantive or disclaimed to the maximum extent? Evaluate SLA commitments, measurement methodology, and remedy structure (credits vs. termination rights). Identify gaps between marketing promises and contractual commitments.

7. **Force Majeure & Change Control** — Does the force majeure clause capture relevant modern risks (pandemic, cyber-attack, sanctions, supply chain disruption)? Is there a formal change order process for scope modifications? Assess who bears the economic risk of unforeseen events.

8. **Compliance & Regulatory Alignment** — Evaluate against applicable regulatory frameworks (GDPR, CCPA, SOX, HIPAA, sector-specific regulations). Identify missing standard provisions (anti-bribery, sanctions, modern slavery, ESG where applicable). Assess audit and reporting obligations.

### 3C: Counterparty Leverage Assessment

Using FutureProof context on prior negotiations, ICA-specific deal patterns, and counterparty history:
- Flag clauses where the counterparty has historically conceded
- Identify non-negotiable positions based on prior session data
- Map each flagged clause to a **negotiate / accept / escalate** recommendation

### 3D: Apply User-Specific Instructions

Incorporate any organisational `instructions` from FutureProof context:
- Internal risk tolerance thresholds (e.g., "never accept uncapped indemnification above $500K deal value")
- Preferred fallback language and approved clause libraries
- Escalation rules (e.g., "any non-standard IP assignment requires General Counsel review")
- ICA-specific contracting standards and playbook positions

## Step 4: Deliver Output

Produce the following structured deliverables:

### Deliverable 1: Executive Risk Summary (1 page)

- **Overall Risk Rating**: Low / Moderate / Elevated / High / Critical
- **Deal-Breaker Flags**: clauses that require resolution before execution (if any)
- **Top 3 Negotiation Priorities**: ranked by financial exposure × likelihood of adverse outcome
- **Recommended Action**: Execute as-is / Execute with minor amendments / Negotiate material terms / Escalate to legal counsel / Do not execute

### Deliverable 2: Clause-by-Clause Scorecard

| # | Clause / Section | Risk Dimension | Severity (1–10) | Favours | Issue Summary | Recommended Action |
|---|-----------------|----------------|------------------|---------|---------------|-------------------|
| 1 | § X.X | Liability & Indemnification | 8 | Counterparty | Uncapped indemnity for third-party IP claims | Negotiate — propose aggregate cap at 2× annual fees |

Include all material clauses. Severity scoring methodology:
- **1–3**: Market-standard, no action required
- **4–6**: Acceptable with minor modification or documented risk acceptance
- **7–8**: Material risk requiring negotiation or internal escalation
- **9–10**: Deal-breaker or potential regulatory non-compliance

### Deliverable 3: Redline Markup with Proposed Alternative Language

For every clause scored 6 or above, provide:
- **Current Language**: exact text from the contract
- **Issue**: plain-language explanation of the risk
- **Proposed Revision**: specific alternative language ready for insertion (not vague guidance — full clause text)
- **Negotiation Rationale**: a one-sentence justification the user can present to the counterparty

### Deliverable 4: Missing Provisions Checklist

Identify standard provisions absent from the contract given its type and governing law:
- [ ] Provision name — why it matters — suggested insertion point

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
FutureProof:save_experiment(skill="contract-review-assistant", experiment={
  hypothesis: "Presenting the top 3 redline positions with pre-drafted fallback language increases counterparty acceptance rate versus presenting issues without proposed alternatives",
  variants: ["control: issue-flagging only with verbal negotiation", "variant: structured redline with primary + fallback language for each position"],
  measurement: "Percentage of flagged clauses resolved in user's favour across next 10 contract negotiations",
  expected_impact: "25% improvement in negotiation success rate on material terms"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="contract-review-assistant",
  query="Emerging contract risk patterns in 2024–2025: AI liability allocation clauses, updated force majeure standards post-pandemic, evolving data processing agreement requirements under EU AI Act and state-level US privacy laws",
  reason="Ensure clause library and risk scoring reflect current regulatory landscape and market-standard positions across jurisdictions"
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
FutureProof:save_session(skill="contract-review-assistant", session={
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