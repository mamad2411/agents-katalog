---
name: plan-plus
classification: hybrid
classification-reason: Combines workflow automation with capability-dependent features
deprecation-risk: low
effort: high
description: |
  Brainstorming-enhanced PDCA planning with intent discovery and YAGNI review. For a single feature's plan use /plan-plus; for grouping multiple features under one scope/budget see /sprint master-plan (v2.1.13).
  Triggers: plan-plus, brainstorm, plan plus, intent
argument-hint: "[feature]"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - AskUserQuestion
imports:
  - ${PLUGIN_ROOT}/templates/plan-plus.template.md
next-skill: pdca design
pdca-phase: plan
task-template: "[Plan] {feature}"
---

# Plan Plus — Brainstorming-Enhanced PDCA Planning

> Combines brainstorming's intent discovery with bkit PDCA's structured planning to produce
> higher-quality Plan documents through collaborative dialogue.

## Overview

Plan Plus enhances the standard `/pdca plan` by adding 4 brainstorming phases before document
generation. This ensures that user intent is fully understood, alternatives are explored,
and unnecessary features are removed before any implementation begins.

**When to use Plan Plus instead of `/pdca plan`:**
- The feature has ambiguous or complex requirements
- Multiple implementation approaches are possible
- You want to ensure YAGNI compliance from the start
- The feature involves significant architectural decisions

## HARD-GATE

<HARD-GATE>
Do NOT write any code, scaffold any project, or invoke any implementation skill
until this entire process is complete and the user has approved the Plan document.
This applies to EVERY feature regardless of perceived simplicity.
A "simple" feature still goes through this process — the design can be short,
but you MUST present it and get approval.
</HARD-GATE>

## Process Flow

```
Phase 0: Context Exploration (automatic)
    ↓
Phase 1: Intent Discovery (1 question at a time)
    ↓
Phase 1.5: Premise Challenge (forcing questions, agreed premises)
    ↓
Phase 2: Alternatives Exploration (2-3 approaches, incl. "do nothing")
    ↓
Phase 3: Scope Mode + YAGNI Review (multiSelect verification)
    ↓
Phase 4: Incremental Design Validation (section-by-section, failure map)
    ↓
Phase 5: Plan Document Generation (plan-plus.template.md)
    ↓
Phase 6: Next Steps → /pdca design {feature}
```

## Phase Details

### Phase 0: Project Context Exploration (Automatic)

Before asking any questions, explore the current project state:

1. Read CLAUDE.md, package.json, pom.xml, etc. for project information
2. Check recent 5 git commits (understand current work direction)
3. Check existing `docs/01-plan/` documents (prevent duplication)
4. Check ongoing PDCA status — `getPdcaStatusView()` in `lib/pdca/status.js`.
   It reads `.bkit/state/pdca-status.json` and fills in any feature whose phase
   is only evidenced by its documents. `.bkit-memory.json` is NOT this store:
   after migration it is `.bkit/state/memory.json`, which holds the 9-phase
   pipeline status and nothing about PDCA phase.

> Share exploration results briefly: "I've reviewed the current project state: ..."

### Phase 1: Intent Discovery (Brainstorming Style)

**Principle: One question at a time, prefer multiple choice**

Use `AskUserQuestion` tool to discover the following in order:

#### Q1. Core Purpose
"What is the core problem this feature solves?"
- Provide 3-4 choices (inferred from project context)
- Always include a custom input option

#### Q2. Target Users
"Who will primarily use this feature?"
- Admin / End user / Developer / External system

#### Q3. Success Criteria
"What criteria would indicate this feature is successful?"
- Derive specific, measurable criteria

#### Q4. Constraints (only when needed)
Conflicts with existing systems, performance requirements, technical constraints, etc.

> **Important**: Minimize questions. Clear features need only Q1-Q2.
> Only proceed to Q3-Q4 for ambiguous features.

### Phase 1.5: Premise Challenge

Phase 1 records what the user wants. This phase tests whether it is worth
building in that shape. Ask one forcing question at a time with
`AskUserQuestion`, and push on vague answers once before moving on.

| # | Forcing question | A strong answer names |
|---|------------------|----------------------|
| F1 | **Demand** — Who would be genuinely upset if this did not exist next month? | A specific person or role, not a segment |
| F2 | **Status quo** — What do those users do today to get this done, even badly? | The current workaround and what it costs them |
| F3 | **Wedge** — What is the smallest version that someone would use this week? | One flow, not a feature list |
| F4 | **Do nothing** — What happens if we build nothing? | A concrete cost, or an admission that there is none |

Routing — ask only what the feature needs:
- New product or user-facing capability: F1-F4
- Internal tool or refactor: F2, F4
- Bug fix or small change: skip this phase and say so

**Stance rules**
- Take a position on every answer and state what evidence would change it.
  Do not reply with neutral filler ("That could work", "Interesting approach").
- Enthusiasm is not evidence of demand; a workaround the user already pays for is.
- If the user wants to move on, ask the single most important remaining question,
  then proceed. Do not ask a third time.

Close the phase by printing the agreed premises as a numbered list and asking
the user to confirm them:

```
PREMISES
1. {who needs this, and why now}
2. {what they do today}
3. {the smallest useful version}
```

If the user rejects a premise, revise it before Phase 2 — alternatives built on
a rejected premise are wasted work. Record the confirmed premises in the Plan
document's "Premise Challenge" section.

### Phase 2: Alternatives Exploration (Brainstorming Core)

**Always propose 2-3 approaches** with trade-offs for each. When Phase 1.5 ran,
one of them may be "do nothing / use the existing workaround" if F4 showed the
cost of inaction is low.

Format:
```
### Approach A: {name} — Recommended
- Pros: ...
- Cons: ...
- Best for: ...

### Approach B: {name}
- Pros: ...
- Cons: ...
- Best for: ...

### Approach C: {name} (optional)
- Pros: ...
- Cons: ...
```

> Present the recommended approach first with clear reasoning.
> Use AskUserQuestion to let the user choose.

### Phase 3: Scope Mode + YAGNI Review (Brainstorming Core)

First pick a scope mode for the selected approach. Recommend one, then let the
user confirm with `AskUserQuestion`:

| Mode | When to recommend | What it changes |
|------|-------------------|-----------------|
| **Expand** | Greenfield work where a small addition multiplies value | Propose up to 3 additions, each high value for low effort |
| **Selective** | A new capability on an existing product | Hold the core, offer additions one at a time |
| **Hold** | A fix, or a plan that is already well sized | No additions; challenge anything touching more than ~8 files or adding a service |
| **Reduce** | The plan spans more than ~15 files or several subsystems | Cut to the Phase 1.5 wedge and defer the rest |

Every proposed addition gets its own decision: add now, defer (record in
3.2 Deferred), or drop. Record the mode in the Plan document.

Then perform a YAGNI (You Ain't Gonna Need It) review on the selected approach:

Use AskUserQuestion with `multiSelect: true`:
"Select only what is essential for the first version:"

List all features and move unselected items to Out of Scope.

**Principle**: Don't abstract what can be done in 3 lines.
Don't design for hypothetical future requirements.

### Phase 4: Incremental Design Validation (Brainstorming Style)

Present the design section by section, getting approval after each:

1. Architecture overview → "Does this direction look right?"
2. Key components/modules → "Does this structure look right?"
3. Data flow → "Does this flow look right?"
4. Failure map → "Is anything here unacceptable to ship?"

For the failure map, list each new entry point (endpoint, command, job, UI
action) and trace what happens when its input is empty, invalid, or its
dependency fails:

| Entry point | What can go wrong | Handled? | What the user sees |
|-------------|-------------------|:--------:|--------------------|
| {entry} | {failure} | Yes/No | {message, retry, silent} |

Any row with "No" and a silent outcome must either get a handling decision or be
listed as an accepted risk in section 7. Keep this short for small features —
the point is that no failure is silent by accident.

> If the user says "no" to any section, revise only that section and re-present.

### Phase 5: Plan Document Generation

Generate the Plan document using `plan-plus.template.md` with results from Phases 0-4.

**Additional sections** (not in standard plan.template.md):
- **User Intent Discovery** — Core problem, target users, success criteria from Phase 1
- **Premise Challenge** — Forcing-question answers and confirmed premises from Phase 1.5
- **Alternatives Explored** — Approaches compared in Phase 2
- **YAGNI Review** — Scope mode and included/deferred/removed items from Phase 3
- **Failure Map** — Entry-point failure table from Phase 4 (in section 8)
- **Brainstorming Log** — Key decisions from Phases 1-4
- **Executive Summary** -- Auto-synthesize 4-perspective summary (Problem/Solution/Function UX Effect/Core Value) from Phases 1-4 results. Place at document top, before numbered sections.
- **Executive Summary Response** -- MANDATORY: After generating the Plan document, also output the Executive Summary table in your response so the user sees the summary immediately without opening the file.

**Output Path**: `docs/01-plan/features/{feature}.plan.md`

After document generation, the Stop hook records the phase: `scripts/plan-plus-stop.js`
writes `phase = "plan"` to `.bkit/state/pdca-status.json` and creates the Task
chain (`lib/task/creator.js`, which names each Task `<icon> [Plan] {feature}`).
Do not write the phase by hand, and do not write it to `.bkit-memory.json` —
that file is the pipeline store, not the PDCA one.

State the document path in your closing output. The hook recovers the feature
name from it, and without it the phase is recorded against whatever feature was
current before.

### Phase 6: Next Steps

After Plan document generation:
```
Plan Plus completed
Document: docs/01-plan/features/{feature}.plan.md
Next step: /pdca design {feature}
```

## Key Principles

| Principle | Origin | Application |
|-----------|--------|-------------|
| One question at a time | Brainstorming | Sequential questions via AskUserQuestion |
| Explore alternatives | Brainstorming | Mandatory 2-3 approaches in Phase 2 |
| YAGNI ruthlessly | Brainstorming | multiSelect verification in Phase 3 |
| Incremental validation | Brainstorming | Section-by-section approval in Phase 4 |
| HARD-GATE | Brainstorming | No code before approval (entire process) |
| Context first | Brainstorming | Automatic exploration in Phase 0 |
| Challenge the premise | gstack `/office-hours` | Forcing questions and confirmed premises in Phase 1.5 |
| Choose a scope mode | gstack `/plan-ceo-review` | Expand / Selective / Hold / Reduce in Phase 3 |
| No silent failures | gstack `/plan-ceo-review` | Failure map in Phase 4 |

## Integration with PDCA

Plan Plus produces the same output as `/pdca plan` and feeds seamlessly into the
standard PDCA cycle:

```
/plan-plus {feature}     ← Enhanced planning with brainstorming
    ↓
/pdca design {feature}   ← Standard PDCA continues
    ↓
/pdca do {feature}
    ↓
/pdca analyze {feature}
    ↓
/pdca report {feature}
```

## Usage Examples

```bash
# Start brainstorming-enhanced planning
/plan-plus user-authentication

# After Plan Plus completes, continue with standard PDCA
/pdca design user-authentication
/pdca do user-authentication
```
