---
name: epic-breakdown
description: "Takes a large product initiative and decomposes it into shippable epics, each with a hypothesis statement, success metric, and estimated effort. Ensures each epic delivers independent value and can be shipped and measured on its own."
category: execution
default_depth: standard
---

# Epic Breakdown Advisor

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Takes a large product initiative and decomposes it into shippable epics, each with a hypothesis statement, success metric, and estimated effort. Ensures each epic delivers independent value and can be shipped and measured on its own.

## When to Use

- A PRD has been approved and needs to be broken into executable work
- An initiative is too large for a single sprint and needs phasing
- The team needs to agree on what "done" looks like for each increment
- Reducing delivery risk by shipping smaller, measurable chunks

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Single-team initiative with obvious slicing | Define the Initiative, Define Each Epic (hypothesis + scope only), Sequence the Epics |
| **Standard** | Cross-team initiative or multi-quarter effort | All sections |
| **Deep** | High-stakes platform bet or re-architecture | All sections + per-epic RACI, rollback plan per phase, dependency risk matrix with external teams |

**Omit rules:** At Light depth, skip Identify Value Slices analysis and Validate the Breakdown checklist. Produce only a numbered epic list with one-line hypotheses and a sequencing order.

## Framework

### Step 1: Define the Initiative

```markdown
## Initiative: [Name]
**Objective:** [What we're trying to achieve, outcome, not output]
**Success metric:** [Primary metric and target]
**Total estimated scope:** [T-shirt size or person-weeks range]
**Target completion:** [Quarter or date range]
```

### Step 2: Identify Value Slices

Think in terms of "what's the thinnest slice that delivers real value to a real user?"

**Slicing strategies (choose the best fit):**

| Strategy | When to Use | Example |
|---|---|---|
| By user journey step | Linear workflow | Onboarding → First action → Habit loop |
| By persona | Multiple user types | Admin features → Member features |
| By complexity | Progressive enhancement | Basic version → Advanced version |
| By risk | High-uncertainty initiative | Riskiest part first → Build on learnings |
| By data flow | System integration work | Ingest → Process → Display |

### Step 3: Define Each Epic

```markdown
### Epic [N]: [Name]

**Hypothesis:** We believe that [building X] will [result in Y] because [evidence/reasoning].

**Value delivered:** [What a user can do after this epic ships that they couldn't before]

**Success metric:**
- Primary: [metric + target]
- Leading indicator: [early signal this is working]

**Scope:**
- In: [What's included]
- Out: [What's explicitly excluded, moves to a later epic or is cut]

**Dependencies:**
- Requires: [Other epics or external work that must complete first]
- Enables: [What future epics this unblocks]

**Estimated effort:** [T-shirt size: S (1-2 weeks) / M (2-4 weeks) / L (4-8 weeks)]

**Key risks:**
- [Risk 1], Mitigation: [approach]
```

### Step 4: Sequence the Epics

```markdown
## Epic Sequence

### Phase 1: [Name, e.g., "Foundation"]
Timeline: [Sprints N-M]
- Epic 1: [name], [what it delivers]
- Epic 2: [name], [what it delivers]

Milestone: [What's true when Phase 1 is complete]

### Phase 2: [Name, e.g., "Core Experience"]
Timeline: [Sprints N-M]
Depends on: Phase 1
- Epic 3: [name]
- Epic 4: [name]

Milestone: [What's true when Phase 2 is complete]

### Phase 3: [Name, e.g., "Polish & Scale"]
Timeline: [Sprints N-M]
Depends on: Phase 2
- Epic 5: [name]

Milestone: [What's true when Phase 3 is complete]
```

### Step 5: Validate the Breakdown

Run through these checks:

```markdown
## Breakdown Validation Checklist
- [ ] Each epic delivers independent user value (can ship alone)
- [ ] Each epic has a measurable success metric
- [ ] No epic is larger than 4-8 weeks of work
- [ ] The riskiest assumptions are tested in the earliest epics
- [ ] Dependencies are explicit and minimized
- [ ] The sum of epics covers the full initiative scope
- [ ] Scope cuts are documented (items explicitly not included)
- [ ] Each epic has a clear hypothesis that could be proven wrong
```

## Minimum Evidence Bar

**Required inputs:** Approved PRD or initiative brief with a stated objective, success metric, and rough scope estimate.

**Acceptable evidence:** PRD, strategy document, stakeholder alignment deck, customer research summary, or recorded decision from a planning meeting.

**Insufficient evidence:** If no success metric or objective exists for the initiative, stop and recommend running PRD Development (`prd-development`) before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Initiative objective, dependencies on existing systems, and team capacity constraints must be grounded in evidence.
- **Hypotheses:** Per-epic success metrics and effort estimates are hypotheses until validated by engineering review and post-ship measurement -- label them as such.

## Output Format

Produce an Epic Breakdown Document with:
1. **Initiative Overview**, objective, metric, timeline
2. **Epic Definitions**, hypothesis, scope, metric, effort for each
3. **Sequence & Phases**, ordered delivery plan with milestones
4. **Dependency Map**, which epics depend on which
5. **Validation Checklist**, breakdown quality assessment

**Shipwright Signature (required closing):**
6. **Decision Frame**, recommended sequencing and slicing strategy, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, unvalidated effort estimates, untested hypotheses, unclear cross-team dependencies
8. **Pass/Fail Readiness**, PASS if every epic has independent value, a measurable hypothesis, and a sequenced delivery order (at Light depth: one-line hypothesis per epic and a sequencing order are sufficient; success metrics and validation checklist are not required); FAIL if any epic lacks a hypothesis or exceeds 8 weeks
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Epics without independent value**, "Set up infrastructure" isn't an epic; it's a task inside an epic
- **No hypothesis**, If there's no hypothesis, there's no way to learn from shipping
- **Too large**, If an epic takes more than 6-8 weeks, it needs further decomposition
- **Sequencing by comfort, not risk**, Ship the riskiest thing first, not the easiest
- **Scope creep across epics**, Each epic's "out of scope" must be clear and respected

## Weak vs. Strong Output

**Weak:**
> Epic 3: Dashboard Improvements. Build dashboard features. Success metric: Users like it.

No hypothesis, no measurable metric, no independent value statement -- this is a task bucket, not a shippable epic.

**Strong:**
> Epic 3: Self-Serve Reporting. **Hypothesis:** We believe that giving ops managers the ability to build their own reports will reduce ad-hoc data requests to the analytics team by 40%, because 68% of current requests follow 5 repeatable templates (source: Q3 support ticket analysis). **Success metric:** Ad-hoc data requests drop from 50/week to 30/week within 6 weeks of launch.

Testable hypothesis grounded in evidence, with a specific metric and timeframe that makes "did this work?" unambiguous.
