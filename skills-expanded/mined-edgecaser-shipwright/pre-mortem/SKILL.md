---
name: pre-mortem
description: "Runs a structured \"imagine this already failed\" exercise to surface risks, assumptions, and failure modes before a launch or major initiative begins. Based on Gary Klein's prospective hindsight research."
category: execution
default_depth: standard
---

# Pre-Mortem Analysis

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Runs a structured "imagine this already failed" exercise to surface risks, assumptions, and failure modes before a launch or major initiative begins. Based on Gary Klein's prospective hindsight research.

## When to Use

- Before launching a new product or major feature
- Before committing to a large, irreversible initiative
- When the team seems overly confident or has groupthink
- Before signing a major partnership or platform migration

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Low-stakes feature with a single team | Set the Scene, Generate Failure Reasons (top 5 only), Assess & Prioritize Risks |
| **Standard** | Major feature launch or cross-team initiative | All sections |
| **Deep** | Irreversible bet, platform migration, or public-facing launch | All sections + stakeholder-specific failure interviews, second-order consequence mapping, historical failure audit of comparable initiatives |

**Omit rules:** At Light depth, skip Define Mitigations and Kill Criteria. Produce only a ranked risk list with likelihood and impact scores.

## Framework

### Step 1: Set the Scene

```markdown
## Pre-Mortem: [Initiative Name]

### The Scenario
It is [date 6 months from now]. We launched [initiative].
It has FAILED. Not a minor setback, a clear, undeniable failure.

### What "failure" means for this initiative:
- [Metric] is at [bad number] instead of [target]
- [Stakeholder] is [unhappy outcome]
- [Resource] was wasted on [outcome]
- The team feels [demoralized / burned out / confused]
```

### Step 2: Generate Failure Reasons

Ask: "Working backward from this failure, what went wrong?"

**Prompt each category:**

```markdown
## Failure Modes

### Customer & Market Failures
- [We built for the wrong persona]
- [The problem wasn't painful enough to change behavior]
- [Timing was wrong, market wasn't ready]
- [Competitors moved faster]

### Execution Failures
- [Scope crept and we shipped too late]
- [Quality was poor, too many bugs at launch]
- [Key dependency didn't deliver on time]
- [Team was under-resourced or burned out]

### Strategy & Business Failures
- [Business model assumptions were wrong]
- [Pricing was off, too high or too low]
- [Go-to-market didn't reach the right audience]
- [Internal stakeholder pulled support]

### Technical Failures
- [Architecture didn't scale]
- [Integration with X broke under real usage]
- [Data quality issues undermined the feature]
- [Security or compliance issue blocked launch]

### Unknown Unknowns
- [Something we haven't even considered yet]
```

### Step 3: Assess & Prioritize Risks

```markdown
## Risk Assessment

| # | Failure Mode | Likelihood | Impact | Detectability | Risk Score |
|---|---|---|---|---|---|
| 1 | [Description] | High/Med/Low | High/Med/Low | Early/Late/At launch | [H×I] |
| 2 | [Description] | ... | ... | ... | ... |

**Scoring:**
- Focus on High Likelihood × High Impact items first
- Pay special attention to "Late detectability" risks, these are the ones that blindside you
```

### Step 4: Define Mitigations

```markdown
## Mitigation Plan

### Risk 1: [Description]
**Prevention:** [What we can do now to reduce likelihood]
**Detection:** [Early warning signal to watch for]
**Contingency:** [What we'll do if it happens anyway]
**Owner:** [Who's responsible for this mitigation]
**Deadline:** [When the mitigation must be in place]

### Risk 2: [Description]
...
```

### Step 5: Kill Criteria

Define upfront what would cause you to stop or pivot:

```markdown
## Kill Criteria
If any of the following become true, we will pause and reassess:

1. [Metric] falls below [threshold] for [duration]
   - Decision: [Pivot / pause / kill]
   - Decision-maker: [Name]

2. [Cost] exceeds [budget] by [margin]
   - Decision: [Descope / kill]
   - Decision-maker: [Name]

3. [Dependency] is not delivered by [date]
   - Decision: [Descope / delay / alternative approach]
   - Decision-maker: [Name]
```

## Minimum Evidence Bar

**Required inputs:** A defined initiative with a stated objective, target metric, timeline, and at least a draft plan or PRD.

**Acceptable evidence:** PRD, project plan, architecture proposal, competitive landscape analysis, historical post-mortems from similar initiatives, or stakeholder risk interviews.

**Insufficient evidence:** If the initiative has no defined success metric or timeline, stop and recommend running PRD Development (`prd-development`) or completing the initiative brief before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Known dependencies, confirmed resource constraints, and past failure patterns from historical data must be grounded in evidence.
- **Hypotheses:** Failure mode likelihood ratings and impact estimates are informed speculation -- label them as such and flag which ones need validation through spikes or stakeholder review.

## Output Format

Produce a Pre-Mortem Report with:
1. **Failure Scenario**, vivid description of what failure looks like
2. **Failure Modes**, categorized list of what could go wrong
3. **Risk Assessment**, prioritized by likelihood × impact
4. **Mitigation Plan**, prevention, detection, and contingency for each top risk
5. **Kill Criteria**, pre-committed decision triggers

**Shipwright Signature (required closing):**
6. **Decision Frame**, go/no-go recommendation based on risk profile, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, failure modes with low-confidence likelihood ratings, risks that need spike investigation, missing historical baselines
8. **Pass/Fail Readiness**, PASS if material risks are ranked with likelihood and impact, and Standard/Deep risks have owned mitigations and kill criteria. Light may omit mitigation detail. FAIL if asserted risks have no rationale or material risks are left unassessed; do not invent risks to meet a count.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Being too polite**, The whole point is to imagine failure; encourage brutal honesty
- **Only listing obvious risks**, Push for the uncomfortable, politically sensitive failure modes
- **Mitigations without owners**, Unowned mitigations don't happen
- **No kill criteria**, Without pre-committed exit conditions, sunk cost fallacy takes over
- **Doing it once and forgetting**, Revisit the pre-mortem at milestones to check for emerging risks

## Weak vs. Strong Output

**Weak:**
> Risk: Something could go wrong with the integration. Likelihood: Medium. Mitigation: We'll handle it.

No specificity in the failure mode, no detection signal, no owner -- this mitigates nothing.

**Strong:**
> Risk: Payment provider API rate limits throttle checkout during Black Friday traffic (3x normal volume based on 2024 data). Likelihood: High. Detectability: At launch (no staging load test planned). **Mitigation:** Run load test at 4x peak by Nov 1 (Owner: Platform Lead). **Contingency:** Pre-negotiated burst rate agreement with provider; fallback to queued checkout if latency exceeds 2s.

Names the specific failure scenario with historical data, assigns an owner and deadline, and defines both prevention and contingency.
