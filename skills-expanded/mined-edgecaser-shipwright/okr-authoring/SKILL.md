---
name: okr-authoring
description: "Guides the drafting of Objectives and Key Results using John Doerr's \"Measure What Matters\" methodology. Covers cascading OKRs from company to team to individual, alignment checking across teams, common anti-patterns, and mid-cycle check-ins."
category: planning
default_depth: standard
---

# OKR Authoring & Alignment

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Guides the drafting of Objectives and Key Results using John Doerr's "Measure What Matters" methodology. Covers cascading OKRs from company to team to individual, alignment checking across teams, common anti-patterns, and mid-cycle check-ins.

## When to Use

- Quarterly or annual OKR planning
- Aligning team OKRs with company-level objectives
- Reviewing and improving existing OKRs that feel stale or unmeasurable
- Coaching a team new to OKRs

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Single team drafting 1-2 objectives in a stable org | Step 1: Draft Objectives, Step 2: Draft Key Results |
| **Standard** | Quarterly planning with cross-team dependencies | All sections |
| **Deep** | Company-wide OKR cascade or first-time OKR rollout | All sections + per-KR instrumentation plan, dependency RACI across teams, OKR retrospective template from prior cycle |

**Omit rules:** At Light depth, skip Step 3: Alignment Check, Step 4: Anti-Pattern Detection, and Step 5: Scoring & Check-In Template. Produce only Objectives and Key Results with quality checklists passed.

## Key Concepts

- **Objective:** Qualitative, inspirational, time-bound. Answers "Where do we want to go?"
- **Key Result:** Quantitative, measurable, verifiable. Answers "How will we know we got there?"
- **Committed OKR:** We will hit this (1.0). Tied to business operations.
- **Aspirational OKR:** We aim to hit this (target: 0.7). Stretches the team.

## Framework

### Step 1: Draft Objectives

```markdown
## [Team / Individual] OKRs, [Quarter/Year]

### Objective 1: [Inspirational, qualitative goal]

**Quality checklist:**
- [ ] Inspirational, Would the team be excited to achieve this?
- [ ] Directional, Does this help decide what to work on (and what NOT to)?
- [ ] Time-bound, Clear quarter or timeframe
- [ ] Achievable-ish, Ambitious but not delusional
- [ ] No metrics in the Objective, Metrics belong in Key Results
- [ ] Starts with a verb, "Establish," "Deliver," "Transform," "Prove"
```

**Good Objectives:**
- "Become the trusted analytics partner for mid-market SaaS teams"
- "Prove that AI-powered onboarding dramatically accelerates time-to-value"
- "Establish a self-serve growth engine that reduces dependency on sales"

**Bad Objectives:**
- "Increase revenue by 30%" (that's a Key Result, not an Objective)
- "Ship the new dashboard" (that's an output, not an outcome)
- "Be the best product" (too vague to be directional)

### Step 2: Draft Key Results

```markdown
### Key Results for Objective 1:

**KR1:** [Metric] from [baseline] to [target]
- Type: [Committed / Aspirational]
- Measurement: [How we'll measure, tool, query, method]
- Current baseline: [value as of today]
- Confidence (start of quarter): [X]%

**KR2:** [Metric] from [baseline] to [target]
- Type: [Committed / Aspirational]
- Measurement: [How we'll measure]
- Current baseline: [value]
- Confidence: [X]%

**KR3:** [Metric] from [baseline] to [target]
- Type: [Committed / Aspirational]
- Measurement: [How we'll measure]
- Current baseline: [value]
- Confidence: [X]%
```

**Key Result quality checklist:**
- [ ] Quantitative, Has a number
- [ ] Measurable, We can actually track this metric today (or will instrument it in week 1)
- [ ] Outcome-based, Measures results, not activities
- [ ] Has a baseline, We know where we're starting from
- [ ] Has a stretch target, Not sandbagged but not impossible
- [ ] 3-5 KRs per Objective, More than 5 means you're not focused enough
- [ ] Independent, Each KR measures something different

**Good Key Results:**
- "Increase trial-to-paid conversion from 8% to 14%"
- "Reduce median time-to-first-value from 4.2 days to 1.5 days"
- "Achieve NPS of 50+ among enterprise segment (currently 32)"

**Bad Key Results:**
- "Launch the onboarding redesign" (binary output, not a measurable outcome)
- "Ship 15 features" (activity metric, tells you nothing about impact)
- "Improve user experience" (not measurable)

### Step 3: Alignment Check

```markdown
## Alignment Matrix

### Vertical Alignment (Company → Team)
| Company Objective | Company KR | Team Objective | How It Connects |
|---|---|---|---|
| [Company Obj 1] | [Company KR 1.2] | [Team Obj 1] | [This team's work directly drives this company KR] |

### Horizontal Alignment (Team ↔ Team)
| Our Objective | Depends On | Other Team | Alignment Status |
|---|---|---|---|
| [Our Obj 1] | [Specific dependency] | [Team X] | [Aligned / Needs discussion / Conflict] |

### Coverage Check
| Company KR | Teams Contributing | Gap? |
|---|---|---|
| [Company KR 1] | [Team A, Team B] | [No gap / Gap: no team owns X] |

### Conflict Check
| Potential Conflict | Teams | Description | Resolution |
|---|---|---|---|
| [Conflict] | [Team A vs. Team B] | [How their OKRs might conflict] | [Proposed resolution] |
```

### Step 4: Anti-Pattern Detection

Run the OKRs through this anti-pattern checklist:

```markdown
## Anti-Pattern Audit

| Anti-Pattern | Detected? | Example | Fix |
|---|---|---|---|
| **Sandbagging**, KRs you'll definitely hit | [Y/N] | [which KR] | Increase target to 70% confidence |
| **Task masquerading as KR**, "Ship X" | [Y/N] | [which KR] | Rewrite as outcome: "X leads to [metric change]" |
| **Too many OKRs**, > 3 objectives or > 5 KRs each | [Y/N] | | Prioritize ruthlessly |
| **No baseline**, Can't measure starting point | [Y/N] | [which KR] | Instrument in week 1 or choose different metric |
| **Business-as-usual**, BAU work dressed as OKR | [Y/N] | [which KR] | OKRs are for change, not maintenance |
| **All committed, no aspirational**, No stretch | [Y/N] | | Add 1 aspirational objective |
| **Orphan OKR**, Doesn't connect to anything above | [Y/N] | [which] | Align to company/team OKR or question its value |
| **Metric without action**, Team can't influence it | [Y/N] | [which KR] | Choose a metric the team can directly move |
```

### Step 5: Scoring & Check-In Template

```markdown
## Mid-Quarter Check-In

| Objective / KR | Start | Current | Target | Score (0-1.0) | On Track? | Action Needed |
|---|---|---|---|---|---|---|
| **Obj 1:** [name] | | | | [avg of KRs] | | |
| KR1: [metric] | [baseline] | [current] | [target] | [0.X] | [Yes/At Risk/No] | [action] |
| KR2: [metric] | [baseline] | [current] | [target] | [0.X] | [Yes/At Risk/No] | [action] |

**Scoring guide:**
- 0.0-0.3: Failed to make meaningful progress
- 0.4-0.6: Made progress but fell short
- 0.7-0.8: Sweet spot for aspirational OKRs
- 0.9-1.0: Hit it (great for committed, means you sandbagged if aspirational)
```

## Minimum Evidence Bar

**Required inputs:** Company or team strategy context, the planning timeframe, and current baseline metrics for any proposed Key Results.

**Acceptable evidence:** Existing dashboards, analytics tools, prior-quarter OKR scores, product strategy docs, company-level OKRs to cascade from, user research findings that inform outcome targets.

**Insufficient evidence:** If a baseline metric cannot be sourced or estimated, produce a partial OKR document with affected Key Results marked `[TBD, requires: baseline instrumentation for <metric name> before target can be set]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Baselines, current scores, and alignment relationships to company OKRs must be grounded in data.
- **Hypotheses:** Targets and confidence levels are inherently forward-looking, label aspirational targets as such and note the assumptions behind stretch goals.

## Output Format

Produce an OKR Document with:
1. **Objectives**, 2-3 per team, with quality checklists passed
2. **Key Results**, 3-5 per objective, with baselines, targets, and measurement methods
3. **Alignment Matrix**, vertical and horizontal alignment verified
4. **Anti-Pattern Audit**, checklist results with fixes
5. **Check-In Template**, ready for mid-quarter scoring

**Shipwright Signature (required closing):**
6. **Decision Frame**, Key trade-offs in objective selection (what you're pursuing vs. what you're deferring), confidence in each target based on baseline data quality, OKR owner, cycle dates, revisit trigger
7. **Unknowns & Evidence Gaps**, KRs lacking baselines, metrics not yet instrumented, alignment relationships assumed but unconfirmed with partner teams
8. **Pass/Fail Readiness**, PASS if every KR has a measurable target with a known or planned baseline; FAIL if any KR is binary ("ship X") or has no measurement method. (At Light depth, company-level alignment is not evaluated since the Alignment Check is omitted.)
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **OKRs as task lists**, OKRs measure outcomes, not outputs. "Ship feature X" is a project, not an OKR
- **Setting and forgetting**, Check in weekly, score mid-quarter, retrospect end-of-quarter
- **All committed**, If every OKR is a 1.0 at end of quarter, you're not stretching
- **No alignment discussion**, Write OKRs in isolation and you'll have conflicting priorities across teams
- **Changing OKRs mid-quarter**, Resist the urge; OKRs are a commitment. If they need changing, it's a signal your planning needs work

## Weak vs. Strong Output

**Weak:**
> **KR2:** Improve onboarding completion rate (Committed)

No baseline, no target, no measurement method, impossible to score at end of quarter.

**Strong:**
> **KR2:** Increase onboarding completion rate from 34% to 55% (Committed). Measurement: Amplitude funnel "Signup → First Dashboard Created," baseline pulled 2026-03-20. Confidence: 72%.

Baseline sourced, target quantified, measurement tool named, confidence stated, can be scored objectively at check-in.
