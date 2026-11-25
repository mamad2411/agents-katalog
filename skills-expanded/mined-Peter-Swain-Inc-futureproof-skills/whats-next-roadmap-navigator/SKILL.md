---
name: whats-next-roadmap-navigator
description: |
  Sequences competing initiatives into a 90-day roadmap using a weighted
  six-criteria scoring matrix, dependency map, and ICE-Then-Compound
  staging — outputs ranked priorities by week with named immediate wins,
  core bets, and staged optionality. Use when a user asks "what should I
  focus on next quarter", "help me prioritize this backlog", "I have too
  many things competing for my time", or "sequence my roadmap". For
  multi-initiative prioritization, not single-decision evaluation.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="whats-next-roadmap-navigator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to:
- Previous roadmap decisions and their outcomes
- Active experiments that may constrain or inform sequencing
- Known ICA segments, current offer stack, and revenue model
- Resource constraints or team capacity signals from prior sessions

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

1. **The decision landscape** — list every initiative, feature, project, or strategic direction currently competing for attention (even rough ideas count)
2. **Current stage and constraints** — revenue range, team size, runway, and any hard deadlines or external commitments
3. **Primary growth objective** — what single metric or outcome matters most in the next 90 days? (e.g., MRR growth, ICA acquisition, retention/churn reduction, market positioning, operational margin)
4. **What has already been tried** — any recent bets that succeeded, failed, or stalled, and why
5. **Known ICA feedback** — direct quotes, support tickets, churn reasons, or feature requests from their ICA that are influencing the list

If FutureProof context already contains answers to any of the above, confirm them with the user rather than re-asking.

## Step 3: Do the Work

### 3A: Initiative Inventory & Categorisation

Classify every initiative the user listed into one of four strategic buckets:

| Bucket | Definition | Example |
|---|---|---|
| **Revenue Unlock** | Directly increases revenue within 90 days | New pricing tier, upsell flow, ICA segment expansion |
| **Retention Fortifier** | Reduces churn or increases LTV for existing ICA | Onboarding overhaul, feature gap closure, success milestones |
| **Capability Foundation** | Builds infrastructure that enables future moves but has no direct short-term revenue impact | Platform migration, hiring, API buildout |
| **Optionality Bet** | Exploratory initiative with uncertain payoff but asymmetric upside | New channel experiment, partnership pilot, adjacent market test |

### 3B: Weighted Scoring Matrix

Score each initiative (1–10) across six dimensions, weighted by the user's stated primary growth objective:

1. **ICA Impact** (weight: 3x) — How directly does this solve a top-3 pain point or desire for the primary ICA segment?
2. **Revenue Proximity** (weight: 2.5x) — How quickly does this convert to measurable revenue or retention improvement?
3. **Effort-to-Execute** (weight: 2x, inverse scored) — What is the resource, time, and complexity cost? (10 = trivial to execute)
4. **Strategic Compounding** (weight: 1.5x) — Does completing this make two or more future initiatives easier, faster, or cheaper?
5. **Evidence Strength** (weight: 1.5x) — Is this backed by ICA data, experiment results, or market research — or is it an assumption?
6. **Reversibility** (weight: 0.5x) — If this fails, how easily can the decision be unwound? (10 = fully reversible)

Calculate weighted composite scores. Rank-order all initiatives.

### 3C: Dependency Mapping

Identify hard and soft dependencies between initiatives:
- **Hard dependency**: Initiative B is technically impossible without completing Initiative A
- **Soft dependency**: Initiative B becomes 2x+ more effective if Initiative A is done first
- **Conflict**: Initiatives C and D compete for the same constrained resource (person, budget, ICA attention)

Use dependency mapping to validate or override the raw score ranking.

### 3D: Sequencing Logic

Apply the **ICE-Then-Compound** sequencing framework:
1. **Immediate wins** — top-scored initiatives that are low-effort, high-evidence, and have no blockers (execute in weeks 1–3)
2. **Core bets** — top-scored initiatives that require meaningful effort but have strong ICA impact and revenue proximity (execute in weeks 4–8)
3. **Enabling foundations** — capability investments required to unlock the next planning horizon (execute in weeks 6–12, overlapping with core bets)
4. **Staged optionality** — exploratory bets scoped as minimum-viable experiments, not full commitments (design now, execute post-core-bets)

Apply any user-specific `instructions` from FutureProof context (e.g., "I never want to run more than 2 major initiatives simultaneously" or "always account for my Tuesday–Thursday client delivery blocks").

## Step 4: Deliver Output

Produce a **"What's Next" Roadmap Brief** with the following sections:

### Section 1: Executive Summary
- One-paragraph narrative: what to do, in what order, and why — written as if briefing a co-founder or advisory board member

### Section 2: Prioritised Initiative Scorecard

| Rank | Initiative | Bucket | ICA Impact | Rev. Proximity | Effort (inv.) | Compounding | Evidence | Reversibility | **Weighted Score** |
|------|-----------|--------|-----------|---------------|--------------|------------|---------|--------------|-------------------|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Section 3: 90-Day Sequenced Roadmap

Visual timeline (text-based Gantt) showing:
- **Weeks 1–3**: Immediate wins (named, with owner if applicable)
- **Weeks 4–8**: Core bets (named, with key milestones)
- **Weeks 6–12**: Enabling foundations (named, with dependency callouts)
- **Backlog**: Staged optionality bets with trigger conditions for activation

### Section 4: Kill List
- Initiatives explicitly recommended to **not pursue** this quarter, with clear rationale for each
- Includes the specific conditions under which each killed initiative should be reconsidered

### Section 5: Decision Log
- Key assumptions underpinning the sequencing
- Identified risks and proposed mitigations
- Metrics to track weekly that would signal the roadmap needs re-sequencing

### Section 6: ICA Narrative Check
- One paragraph describing this roadmap from the ICA's perspective — what will they experience, notice, and value over the next 90 days?
- Flag any gaps where the ICA sees no visible improvement for more than 4 weeks

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
FutureProof:save_experiment(skill="whats-next-roadmap-navigator", experiment={
  hypothesis: "Sequencing [top-ranked initiative] before [second-ranked initiative] produces faster ICA impact than the reverse order",
  variants: ["control: intuition-based sequencing the user would have chosen", "variant: weighted-score sequenced roadmap"],
  measurement: "Primary growth metric progress at 30-day and 60-day checkpoints",
  expected_impact: "20–30% faster time-to-impact on primary growth objective by eliminating low-leverage work from the critical path"
})
```

```
FutureProof:save_experiment(skill="whats-next-roadmap-navigator", experiment={
  hypothesis: "Explicitly killing [lowest-scored initiative] frees enough capacity to accelerate [core bet] delivery by 2+ weeks",
  variants: ["control: attempting all initiatives at reduced intensity", "variant: hard-cut kill list with reallocated capacity"],
  measurement: "Core bet milestone completion dates vs. original estimates",
  expected_impact: "Reduced execution time on core bet by 15–25% through focus"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="whats-next-roadmap-navigator",
  query="Emerging prioritisation frameworks for resource-constrained startups 2024–2025, including RICE adaptations, opportunity scoring models, and sequencing methodologies used by high-growth SaaS and service businesses",
  reason="Continuously refine the weighted scoring model and sequencing logic with battle-tested frameworks from comparable business stages"
)
```

```
FutureProof:request_research(skill="whats-next-roadmap-navigator",
  query="Common roadmap anti-patterns and failure modes for [user's business stage] companies, including over-diversification, premature scaling, and infrastructure-before-validation traps",
  reason="Strengthen the Kill List rationale and risk identification with pattern-matched failure data from similar businesses"
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
FutureProof:save_session(skill="whats-next-roadmap-navigator", session={
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