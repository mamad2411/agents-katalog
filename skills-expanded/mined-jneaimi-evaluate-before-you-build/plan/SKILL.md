---
name: plan
description: >
  PM-focused planning skill based on Bloom's AI Collaboration model. Use when
  the user says /plan, wants to plan a project, build a roadmap, scope an
  initiative, set milestones, or break work into phases. Also trigger on
  phrases like "plan the work", "build a roadmap", "scope this project",
  "milestones", "RACI", "who owns what", "phase this out", or "PM plan".
  Heavier than /prebuild, tighter than /think — focused specifically on
  product/project planning discipline.
---

# Planning Checkpoint (/plan)

A structured planning skill for product and project managers. Evaluates the
initiative before committing to a roadmap — scope, stakeholders, constraints,
dependencies, milestones, and risks. Output is a phased plan with clear
owners and done-when criteria.

**Core principle:** A plan that wasn't evaluated isn't a plan — it's a wishlist.
Never produce a roadmap until the human has answered the 6 planning questions.

**Interaction model:** Use `AskUserQuestion` for all decision points. The AI
proposes informed options (based on any available project context), the human
confirms or adjusts. Same Bloom ladder as `/think` — tuned for PM work.

## How It Differs from /think and /prebuild

| | /plan | /think | /prebuild |
|---|-------|--------|-----------|
| **Focus** | Roadmap / execution plan | Any domain decision | Code generation |
| **Deliverable** | Phased plan + RACI + risk register | Domain-adapted doc | Working code |
| **Lens** | PM / delivery | Strategic / evaluative | Builder |
| **Answers from** | Human + AI-proposed options | Human provides substance | AI proposes, human picks |
| **Duration** | ~20 minutes | 30–60+ minutes | ~10 minutes |

Use `/plan` when the decision to do the thing is already made and you need
to sequence and scope the work. Use `/think` when you're still deciding *whether*
or *why*.

## Framework Reference

```
┌─────────────────────────────────────────┐
│  Level 5: Evaluate     HUMAN → AI      │  Scope, owners, constraints
│  Level 4: Analyze      HUMAN ↔ AI      │  Dependencies, sequencing
├─────────────────────────────────────────┤
│  Level 3: Apply        AI → HUMAN      │  Produce the plan doc
│  Level 2: Understand   AI → HUMAN      │  Walk through the plan
│  Level 1: Remember     AI alone        │  Save to project tracking
└─────────────────────────────────────────┘
```

## Commands

### /plan [initiative] — Start planning
Begin a new planning session for the described initiative.

### /plan continue — Resume
Resume from where a prior session left off.

### /plan summary — Show state
Display completed levels, confirmed decisions, and what's next.

### /plan save — Persist
Save the finalized plan to the vault or linked tracking system.

---

## Step 1: Detect the Initiative Shape (Silent)

Classify the initiative before asking questions:

- **Initiative type**: Product launch, feature delivery, migration, refactor,
  research spike, operational improvement, compliance/regulatory, content/campaign
- **Time horizon**: Sprint (≤2 weeks), Quarter (1–3 months), Multi-quarter (3+ months)
- **Team shape**: Solo, small team, multi-team

Output one line:

> **Detected:** [initiative type] — [brief description] ([horizon], [team shape])

---

## Step 2: Level 5 — Evaluate (6 Planning Questions)

Split into two rounds of 3 questions each (AskUserQuestion max 4 per call).

### Round 1: Outcome, Stakeholders, Constraints

```
AskUserQuestion (3 questions):

Question 1 — OUTCOME (header: "Outcome")
  "What specific outcome are we committing to?"
  Options — propose measurable framings:
    - "Business metric target" (e.g., revenue, conversion, retention)
    - "User outcome" (e.g., users can do X, users stop hitting Y)
    - "Learning outcome" (validated insight — even if we kill it)
    - "Delivery outcome" (thing exists, shipped, adopted internally)
  (User picks the closest; "Other" for custom)

Question 2 — STAKEHOLDERS (header: "Stakeholders")
  "Who owns, who's affected, who signs off?"
  Options — propose based on initiative type:
    - "Single owner, minimal cross-team impact"
    - "One team delivers, one team is downstream consumer"
    - "Multiple teams, needs exec alignment"
    - "External stakeholders involved (customers, vendors, regulators)"

Question 3 — CONSTRAINTS (header: "Fixed")
  "Of time / scope / quality / budget, which is fixed?"
  multiSelect: true (often 1–2 are fixed, the rest flex)
  Options:
    - "Time — hard deadline"
    - "Scope — must include X, Y, Z"
    - "Quality — cannot compromise (compliance, safety, brand)"
    - "Budget — fixed spend / headcount"
```

### Round 2: Dependencies, Milestones, Risks

```
AskUserQuestion (3 questions):

Question 4 — DEPENDENCIES (header: "Depends on")
  "What must be true / done / unblocked before we can start or ship?"
  multiSelect: true
  Options — propose categories:
    - "Upstream deliverable from another team"
    - "External vendor / API / contract"
    - "Hiring or capacity"
    - "Decision or approval still pending"
    - "No hard dependencies — we can start now"

Question 5 — MILESTONES (header: "Phasing")
  "How should the work phase?"
  Options — propose shapes based on horizon:
    - "Single sprint — one push, one demo"
    - "Phased — discovery → build → launch"
    - "Iterative — weekly slices shipped continuously"
    - "Gated — each phase requires sign-off to proceed"

Question 6 — RISK (header: "Top risks")
  "Which risks most threaten the outcome?"
  multiSelect: true
  Options — propose by initiative type (see risk table below):
    - "[Initiative-specific risk A]"
    - "[Initiative-specific risk B]"
    - "[Initiative-specific risk C]"
    - "[Initiative-specific risk D]"
```

### Risk options by initiative type

| Initiative Type | Propose These Risks |
|----------------|---------------------|
| Product launch | Market timing, GTM readiness, Adoption gap, Competitive response |
| Feature delivery | Scope creep, Integration breakage, Perf regression, Usability miss |
| Migration | Data loss, Rollback complexity, Downtime, Parallel-run cost |
| Refactor | Hidden coupling, Test coverage gap, Freeze conflicts, Velocity dip |
| Research spike | Inconclusive result, Over-scoping the spike, Not decision-actionable |
| Compliance | Deadline miss, Audit finding, Scope misinterpretation, Evidence gap |
| Content/campaign | Platform rule change, Tone miss, Timing collision, Asset readiness |

---

## Step 3: Compile Level 5 Summary

After both rounds, display the compiled evaluation:

```
## Level 5 Summary

- **Outcome:** [compiled]
- **Stakeholders:** [compiled + implied RACI hints]
- **Fixed constraints:** [compiled]
- **Dependencies:** [compiled list]
- **Phasing approach:** [compiled]
- **Top risks:** [compiled list]

Moving to Level 4: Analyze...
```

---

## Step 4: Level 4 — Analyze (Sequencing & Capacity)

Translate Level 5 answers into a draft timeline. Analyze:

1. **Dependency graph** — which items unblock which. Propose the critical path.
2. **Capacity check** — given the team shape, is the phasing realistic?
3. **Risk-adjusted buffer** — where should slack live based on top risks?
4. **Decision gaps** — any milestone that has an unmade decision behind it?

**IMPORTANT:** If analysis surfaces a new decision (e.g., "Phase 2 depends on
Option A or B from another team — which?"), RETURN TO LEVEL 5 and ask via
`AskUserQuestion`. Don't assume.

---

## Step 5: Level 3 — Produce the Plan

Produce a structured plan document. Match the level of detail to the horizon:

### Sprint plan (≤2 weeks)
- Goal (1 line), scope (bulleted), out of scope (bulleted)
- Daily/milestone breakdown
- Done-when checklist
- Single owner

### Quarterly plan (1–3 months)
- Outcome statement
- Phases with entry/exit criteria
- RACI table
- Dependency list (with owner and needed-by date)
- Risk register (risk, likelihood, impact, mitigation, owner)
- Success metrics (leading + lagging indicators)

### Multi-quarter plan (3+ months)
- Vision + outcome statement
- Quarterly themes with milestones
- Cross-team dependencies and coordination plan
- Review cadence (monthly / quarterly gates)
- Risk register with escalation paths
- Success metrics + review dates

### Template skeleton

```markdown
# Plan: [Initiative Name]

## Outcome
[From Q1 — measurable]

## Scope
**In:** [bulleted]
**Out:** [bulleted]

## Fixed constraints
[From Q3]

## Phases

### Phase 1 — [Name] ([dates])
- Entry: [criteria]
- Work: [bullets]
- Exit / Done-when: [criteria]
- Owner: [role/name]

### Phase 2 — [Name] ([dates])
...

## RACI
| Activity | R | A | C | I |
|----------|---|---|---|---|
| ...      |   |   |   |   |

## Dependencies
| Depends on | Owner | Needed by | Status |
|------------|-------|-----------|--------|
| ...        |       |           |        |

## Risks
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| ...  |           |        |            |       |

## Success metrics
- Leading: [indicators tracked weekly]
- Lagging: [outcome metrics tracked at end]

## Review cadence
[When/who reviews progress]
```

---

## Step 6: Level 2 — Walk Through the Plan

After producing the plan, explain:
- Why phasing is shaped this way (tie back to constraints from Q3)
- Where the critical path lives (from Level 4 analysis)
- Which risks have active mitigations vs. which are just watched
- What the first concrete action is ("By end of week, [owner] does [thing]")

Tailor depth to the human:
- **Senior PM:** Highlights of non-obvious sequencing choices
- **New to PM:** Section-by-section walkthrough

---

## Step 7: Level 1 — Save the Plan

Use `AskUserQuestion` to confirm destination:

```
AskUserQuestion (1 question):

Question: "Where should we save this plan?"
Header: "Save to"
Options:
  - "Vault: ~/SecondBrain/01-projects/[initiative]/plan.md" (Recommended)
  - "Linear / Jira / Notion — hand off for tracking"
  - "Don't save — this was exploratory"
```

Always include:
- Frontmatter (type: plan, created: YYYY-MM-DD, status, owner, tags)
- Review date in frontmatter (e.g., `review: 2026-05-01`)
- Cross-links to related decisions or research in the vault

---

## When NOT to Use

- **Decision still open** — Use `/think` first.
- **Code-only task with no multi-phase shape** — Use `/prebuild`.
- **One-person, one-day task** — Plans add overhead with no benefit.
- **Continuous / steady-state work** — Plans are for bounded initiatives.

---

## Rules

1. **NEVER produce a roadmap before Level 5 is complete.** Even if the human
   says "just give me the plan" — at minimum ask Q1 (Outcome), Q3 (Fixed
   constraint), and Q6 (Risks) before drafting.
2. **ALWAYS use AskUserQuestion** for the 6 questions — not a text dump.
3. **ALWAYS loop back to Level 5** when Level 4 surfaces a new decision.
   Don't guess sequencing.
4. **Every milestone must have a done-when criterion.** "Phase 1 complete"
   is not a criterion — "API deployed and 3 consumers integrated" is.
5. **Every risk must have a named owner and a mitigation.** Risks without
   owners are theater.
6. **Match detail to horizon.** Don't produce a quarterly template for a
   one-sprint task.
7. **Flag the critical path explicitly.** The human needs to know which
   item, if slipped, slips everything.
