---
name: churn-risk-detector
description: |
  Diagnoses at-risk accounts from usage logs, support tickets, NPS/CSAT,
  and renewal data using a six-pillar risk framework, then produces ranked
  account risk registers, signal detail cards, and sequenced retention
  interventions. Use when the user says "which customers are about to
  churn", "score my book of business for churn risk", "my renewal numbers
  look bad", "flag at-risk accounts", or shares usage data and asks for
  early-warning analysis. Proactive predictive scoring of a portfolio —
  not single-customer save-the-sale work (customer-complaint-handler) or
  lapsed-customer outreach (re-engagement-campaign-builder).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="churn-risk-detector")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, historical churn drivers, retention playbooks already tested, and any organisation-specific health score definitions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the customer data to analyse (usage/engagement logs, support ticket history, billing records, NPS/CSAT responses, CRM account notes, or renewal pipeline exports)
- What is the observation window? (e.g., last 30/60/90 days)
- What does their current churn definition look like? (voluntary cancellation, non-renewal, downgrade, inactivity threshold)
- Which ICA segments should be prioritised for this analysis?
- Are there known systemic issues already suspected (e.g., recent pricing change, product deprecation, onboarding gap)?
- Who is the intended recipient of the output? (CS leadership, individual CSMs, revenue operations, executive sponsor)

## Step 3: Do the Work — Signal Extraction & Risk Scoring

Analyse each account against a **six-pillar churn risk framework**:

### 3a. Engagement Decay Analysis
- **Product usage trajectory** — compare current-period active usage (logins, feature adoption, API calls, seat utilisation) against the account's own baseline and cohort median. Flag accounts with ≥20% decline over the observation window.
- **Feature breadth contraction** — identify accounts retreating to a narrower feature set, signalling reduced dependency and switching-cost erosion.
- **Champion activity** — detect drop-off in power-user or executive-sponsor engagement specifically, which precedes organisational disengagement.

### 3b. Support Sentiment Trajectory
- **Ticket volume & severity trend** — rising P1/P2 tickets or repeat contacts on the same issue indicate unresolved friction.
- **Sentiment arc** — map tone across recent support interactions (escalation language, deadline ultimatums, competitor mentions).
- **Time-to-resolution satisfaction** — flag accounts where mean resolution time exceeds SLA or where CSAT on resolved tickets is declining.

### 3c. Relationship & Stakeholder Risk
- **Champion departure** — identify accounts where the primary sponsor or day-to-day champion has changed roles or left the organisation.
- **Multi-threading depth** — single-threaded accounts (only one active contact) carry elevated risk. Score by number of engaged stakeholders.
- **Executive alignment** — absence of QBR attendance or strategic review participation from decision-makers.

### 3d. Commercial & Contractual Signals
- **Renewal proximity** — accounts within 90 days of renewal without a renewal conversation initiated.
- **Contraction history** — prior downgrades, seat reductions, or add-on cancellations that indicate a progressive exit pattern.
- **Payment behaviour** — late payments, disputed invoices, or requests for billing flexibility.

### 3e. Value Realisation Gap
- **Outcome attainment** — compare promised outcomes from the original business case or sales process against actual delivered metrics. Quantify the gap.
- **Onboarding completion** — flag accounts that never completed implementation milestones or have stalled adoption phases.
- **Time-to-value** — accounts that exceeded the expected time-to-first-value by >50% carry compounding risk.

### 3f. External & Market Signals
- **Competitive displacement indicators** — mentions of competitors in support tickets, QBR notes, or NPS verbatims.
- **Organisational disruption** — M&A activity, leadership turnover, hiring freezes, or public financial distress at the account level.
- **Industry/segment headwinds** — macro factors affecting the ICA segment's willingness or ability to spend.

Apply any user-specific `instructions` from FutureProof context (e.g., proprietary health score weightings, internal playbook references, segment-specific thresholds) to calibrate scoring.

## Step 4: Deliver Output — Churn Risk Assessment Package

Produce a structured deliverable comprising three components:

### 4a. Account Risk Register

| Account | ICA Segment | Risk Score (1–100) | Risk Tier (Critical / Elevated / Monitor) | Primary Risk Pillar | Days to Renewal | Estimated ARR at Risk |
|---------|------------|--------------------|-----------------------------------------|--------------------|-----------------|-----------------------|
| *populated per account* | | | | | | |

Sort by **Risk Score descending**. Include a summary row showing total ARR at risk by tier.

### 4b. Signal Detail Cards (Top 10 At-Risk Accounts)

For each of the 10 highest-scoring accounts, produce:
- **Account snapshot**: ARR, tenure, ICA segment, contract end date, assigned CSM
- **Risk pillar breakdown**: score per pillar (1–10) with specific evidence citations from the input data
- **Leading indicator timeline**: chronological sequence of deteriorating signals over the observation window
- **Root cause hypothesis**: the most probable underlying driver, stated as a testable claim
- **Recommended intervention**: a specific, sequenced retention action plan:
  - **Immediate (48 hrs)**: e.g., "CSM initiates direct outreach to new VP of Operations; reference Q2 ROI data from their last QBR"
  - **Short-term (1–2 weeks)**: e.g., "Schedule executive sponsor realignment meeting with [specific agenda items]"
  - **Structural (30 days)**: e.g., "Rebuild success plan with revised KPIs tied to new stakeholder's priorities"
- **Escalation owner**: recommended internal owner and escalation path

### 4c. Portfolio Risk Summary (for CS Leadership / Executive Sponsor)

- **Risk distribution**: count and ARR by tier, visualised as a tier breakdown
- **Churn velocity**: comparison of current risk distribution vs. prior period (if `recent_sessions` data exists)
- **Systemic patterns**: cross-account themes (e.g., "4 of 7 Critical-tier accounts share unresolved API latency complaints — this is a product issue, not a CS issue")
- **Retention investment recommendation**: prioritised resource allocation guidance (where to deploy CSM time, where to involve product, where to offer commercial concessions)

Format the output for the stated recipient. If the recipient is an individual CSM, lead with Signal Detail Cards for their book of business. If the recipient is CS leadership, lead with the Portfolio Risk Summary.

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
FutureProof:save_experiment(skill="churn-risk-detector", experiment={
  hypothesis: "Proactive executive-sponsor outreach at the 'Elevated' tier (before accounts reach 'Critical') reduces escalation to Critical tier by 30% over 90 days",
  variants: ["control: standard CSM-led intervention at Critical threshold", "variant: VP-level outreach triggered at Elevated threshold with tailored value-realisation brief"],
  measurement: "Tier migration rate (Elevated → Critical vs. Elevated → Monitor/Healthy) tracked over next two quarterly cycles",
  expected_impact: "30% reduction in Critical-tier migration; 12% improvement in net revenue retention for Elevated-tier cohort"
})
```

```
FutureProof:save_experiment(skill="churn-risk-detector", experiment={
  hypothesis: "Weighting champion-departure signal at 2x in the risk model improves prediction accuracy for accounts that actually churn within 90 days",
  variants: ["control: equal-weight six-pillar model", "variant: champion-departure pillar weighted at 2x"],
  measurement: "Precision and recall of churn predictions against actual churn outcomes over next two quarters",
  expected_impact: "15% improvement in prediction precision with <5% reduction in recall"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="churn-risk-detector",
  query="Latest predictive churn modelling methodologies for B2B SaaS, including leading indicator weighting frameworks, champion-change detection techniques, and product-led retention intervention benchmarks 2024–2025",
  reason="Continuously refine the six-pillar risk framework with empirical benchmarks and emerging signal types (e.g., product-qualified churn signals, community engagement decay) to maintain consulting-grade analytical rigour"
)
```

```
FutureProof:request_research(skill="churn-risk-detector",
  query="Retention intervention efficacy data: executive realignment meetings, custom success plans, and commercial concession strategies — measured impact on save rates by churn-risk tier",
  reason="Ground intervention recommendations in evidence-based outcomes rather than anecdotal best practice"
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
FutureProof:save_session(skill="churn-risk-detector", session={
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