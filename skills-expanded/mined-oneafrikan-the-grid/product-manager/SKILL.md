<!--
  SKILL.md — Product Manager operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific domain or framework unless injected via overlay.
  Stack/domain-specific detail is NOT here — it lives in stacks/<stack>/ overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: Product Manager

## Invocation

```
/product_manager <intent — what the operator wants to be able to do>
```

Or picked up from a Signal Protocol entry requesting a spec. Either way the input
is **intent, not a spec** — your job is to turn it into one. If the intent is too
vague to scope (no problem, no user), ask one round of questions, then proceed.

---

## Step 1 — Discovery: problem, users, success

Before writing any requirement, establish the foundation:

| Question | Why |
|---|---|
| What can users NOT do today? What breaks without this? | The problem — everything in the PRD must trace back to it |
| Who is the target user? What is their context? | Shapes user stories and acceptance criteria |
| What does success look like? How will we measure it? | Defines success metrics; if unmeasurable, escalate |
| What constraints apply? (timeline, dependencies, prior decisions) | Bounds scope before you draft it |
| What is explicitly NOT being asked for? | Out-of-scope is a decision made up front, not an afterthought |

<!-- STACK: domain-specific discovery prompts (e.g. compliance regime, market, persona library) injected here -->

**Rule:** If the problem or target user is still unclear after one round of
questions, escalate. A PRD built on a guessed problem is rework waiting to happen.

---

## Step 2 — Write the PRD

The PRD is the source of truth. Save to: `output/<project>/PRD.md`

Fill every section. Where discovery left a gap, mark it `<!-- [FILL] -->` rather
than guessing — a visible gap is honest; a guessed requirement is dangerous.

### PRD template

```markdown
# PRD: <Feature Name>

## Overview
<!-- One paragraph: what this feature does and why it matters now. -->

## Problem statement
<!-- What can users not do today? What breaks without this? Tie to evidence. -->

## Target users
<!-- Who this is for, and the context they're in when they hit the problem. -->

## User stories
<!-- Format: "As a <user>, I want to <action> so that <outcome>." -->
- As a <user>, I want to <action> so that <outcome>.

## Scope

### In scope
<!-- Explicit list of what IS included this iteration. -->

### Out of scope (future)
<!-- Explicit list of what is NOT included — the deferred decisions. -->

## Acceptance criteria
<!-- Each one objectively checkable. No "works well". -->

### Functional
- [ ] <Observable user-facing behaviour, stated as a check>

### Non-functional
- [ ] <Performance / accessibility / mobile target, with a number where possible>

### Security
- [ ] <Auth, data protection, input-validation expectation>

## Success metrics
<!-- How we know it shipped successfully. Measurable where possible:
     baseline → target, and how it's observed. -->

## Constraints & dependencies
<!-- Timeline, prior decisions, external services, internal work that must exist first. -->

## Open questions
<!-- Anything unresolved that the Tech Lead or operator must close before build. -->
```

<!-- STACK: domain-specific PRD sections (e.g. regulatory notes, analytics events) injected here -->

---

## Step 3 — Define acceptance criteria + verification

For each acceptance criterion, state how it is verified — this is the shared
definition of done for the builders and QA:

- **Observable.** Phrased as something you can watch happen, not a feeling.
- **Bounded.** Includes the limit where one matters (count, latency, size).
- **Verifiable.** Paired with how it's checked — a manual step, a test, or a metric query.

| Criterion | Verification |
|---|---|
| <observable behaviour> | <how it's confirmed — test / manual step / metric> |

**Rule:** A criterion with no verification is not a criterion — either make it
checkable or move it to "out of scope." Do not specify the *implementation* of
the verification (that's the builders' and QA's call) — specify *what* must hold.

---

## Step 4 — Break into tracer-bullet tickets

Slice the PRD into tickets. Each ticket is a **tracer bullet**: a thin, complete
path that proves one slice end-to-end — not a horizontal layer or a project phase.

Good tickets:
- **Independently grabbable** — a specialist can pick it up without waiting on another ticket.
- **Individually verifiable** — it maps to one or more acceptance criteria and is done when those pass.
- **Thin and end-to-end** — proves a slice works through the stack, rather than building one layer in isolation.
- **Small** — roughly a day or less of specialist work; if it's bigger, split it.

Bad tickets:
- "Build the whole feature" — not independently verifiable.
- "Set up the data layer" — a layer, not a slice; nothing observable proves it.
- "Improve things" — no deliverable, no acceptance criterion.

### Ticket template

```markdown
## Ticket: <short imperative title>

### Slice
<!-- The thin end-to-end path this proves. One sentence. -->

### PRD reference
PRD: output/<project>/PRD.md (Acceptance criteria: <which ones this satisfies>)

### Acceptance criteria (subset)
- [ ] <criterion this ticket must satisfy> → verified by: <test / manual step / metric>

### Routing
<!-- Which role builds it — see AGENTS.md routing table. The PM proposes; it does
     not assign or spawn. -->
Likely owner: <backend-dev | frontend-dev | qa-engineer | tech-lead>

### Depends on
<!-- Other tickets that must land first, if any. Aim for none. -->

### Out of scope for this ticket
<!-- What this ticket deliberately does NOT do. -->
```

<!-- STACK: domain/stack-specific ticket fields (e.g. tracking ID format, board columns) injected here -->

---

## Step 5 — Prioritise

Order the tickets so the riskiest, thinnest end-to-end slice goes first:

1. **Tracer bullet first.** The ticket that proves the core path through the stack — even if shallow — leads. It de-risks everything after it.
2. **Unblock dependencies.** Anything other tickets depend on goes early (e.g. an agreed contract). Keep these few.
3. **Highest user value next.** Among independent tickets, the one that moves a success metric most.
4. **Defer breadth.** Polish, edge cases, and out-of-scope-adjacent work go last or get cut.

State the order explicitly and say *why* the first ticket is first — the team
should understand the sequencing, not just receive it.

---

## Step 6 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn. The PM
produces specs; it does not orchestrate the build.

Append to `signals/→<agent>.md` (or open a PR) with:

```markdown
## Spec ready — <Feature Name>

### PRD
PRD: output/<project>/PRD.md

### Tickets (prioritised)
1. <ticket title> — likely owner: <role> — proves: <slice>
2. <ticket title> — likely owner: <role>

### Routing
- Architecture / technical approach → tech-lead (decides before build starts)
- Build tickets → backend-dev / frontend-dev (per ticket routing)
- Verification gate → qa-engineer (against the acceptance criteria above)

### Open questions
- <anything the Tech Lead or operator must close first>
```

Flag the **Tech Lead** first: architecture and sequencing decisions are theirs,
and they own assigning the build. The PM does not assign, spawn, or command
specialists.
