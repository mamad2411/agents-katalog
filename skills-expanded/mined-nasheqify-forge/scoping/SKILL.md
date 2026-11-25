---
name: scoping
description: >
  Translate a high-level intent into an approved spec hierarchy
  (L0-L3). Buddy guides the user progressively through every
  level.
  Triggers when a high-level intent has no spec and must be split into an L0-L3 hierarchy; NOT when a spec already exists (use spec_authoring / spec_board).
status: active
invocation:
  primary: user-facing
  secondary: [workflow-step]
disable-model-invocation: false
uses: [spec_board, council]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: scoping

## Purpose
Translate a brutal high-level intent into a complete, approved
spec hierarchy (L0-L3). Buddy guides the user progressively
through every level.

## Trigger
- The user phrases a high-level intent: "build me X", "I need
  Y", "create an app for Z".
- The intent is an **objective** (concrete undertaking with a
  foreseeable done criterion) — not a task, not an unframed
  problem.
- No sufficiently detailed spec draft exists yet.

**Distinguish task vs objective vs problem:**
- Task: clearly bounded, one spec is enough, the user knows
  what they want → directly to spec + board
  (`workflows/runbooks/build/WORKFLOW.md`).
- Objective: vague, multiple features, longer time horizon,
  **but a foreseeable done criterion** → scoping mode.
- Problem: the done criterion itself is unclear, the solution
  shape is open (spec? process? code? ADR?) → `solve` workflow
  instead of scoping.

**On uncertainty between problem and objective:** prepend
`frame/SKILL.md` mode `quick`. The frame report clarifies whether
the result will be an objective with a spec hierarchy (then
scoping) or a different artifact (then `solve` stays).

---

## Spec hierarchy

| Level | Name | Content | Gate |
|-------|------|---------|------|
| L0 | Intent spec | Why, for whom, constraints, done criterion, non-goals | User approval |
| L1 | Architecture spec | Components, data flow, tech decisions, risks + spec tree | Board + user |
| L2 | Feature spec | Per feature: behaviour, edge cases, acceptance criteria | Board + user |
| L3 | Implementation spec | Per component: interfaces, state, error handling, contracts | Board, autonomous |

L1's decisions that bind separately built components are written as an initiative architecture spine
(`skills/_protocols/architecture-spine.md`); L2 and L3 specs inherit it read-only and change it only through L1.

---

## Flow

```
1. RECOGNIZE: Buddy recognizes an objective → announces scoping
   mode.
   "That's still very generic. Let's start — I'll guide you
   through the requirements."

2. L0 ELICITATION: 5-7 questions, one at a time.
   → Write the L0 draft.
   → User approval (no review panel).

3. L1 ELICITATION: only delta questions (what L0 didn't yet
   clarify).
   → Write the L1 draft.
   → Board (quick or deep, depending on the trigger).
   → Derive the spec tree (explicitly, not implicitly).
   → User approves the L1 spec + spec tree together.

4. L2 ELICITATION: per feature from the spec tree, in dependency
   order.
   → Delta questions per feature.
   → Board → user approval.
   → Next feature (or in parallel when there is no dependency
     — post-harness).

5. L3: autonomous.
   → Buddy generates implementation specs from the L2 ACs +
     L1 architecture.
   → Board (autonomous, escalate on convergence failure).
   → Post-L3 summary to the user (max 1 page, no gate).
```

---

## Progressive elicitation

**Principle:** each level asks only what the previous level left open. Before settling a scope cut,
cite the applicable project intent and original local objective in the existing scope and show how it
serves both. Resolve governing gaps or conflicts with the owner before locking the cut (owner: framework/invariants.md §Intent-driven).

| Level | Already known | What is now clarified |
|-------|---------------|------------------------|
| L0 | Nothing | Why, for whom, key constraints, done criterion, non-goals |
| L1 | Intent + constraints | Component cuts, data flow, tech stack, risks |
| L2 | + architecture | Per feature: behaviour, edge cases, ACs |
| L3 | + feature ACs | Buddy generates autonomously — no elicitation |

**Conversation style:** one question — wait for the answer —
follow up if needed — then continue. Never a list of 7 questions
at once.

---

## L0 elicitation — question catalogue

Buddy picks 5-7 by context. Pre-check: unclear problem framing
→ prepend `frame/SKILL.md` mode `quick`, then decide if L0
elicitation makes sense.

1. Primary purpose — what should the system do that doesn't
   work today?
2. Who uses it? (User groups, other systems, Buddy itself.)
3. Where does it run? (Self-hosted, cloud, hybrid — sovereignty
   constraint.)
4. What is explicitly NOT in scope? (Non-goals.)
5. When is it "done"? (Done criterion, testable.)
6. Hard constraints? (Security, performance, budget,
   technology.)
7. What already exists that has to be integrated?

---

## Deriving the spec tree (L1 output)

After the L1 draft, Buddy explicitly derives the spec tree:

```markdown
## Spec tree: <system name>

| Feature spec | Scope (one sentence) | Dependencies |
|-------------|----------------------|--------------|
| L2-01: <name> | <what does it do?> | — |
| L2-02: <name> | <what does it do?> | L2-01 |
| L2-03: <name> | <what does it do?> | — |
```

The user approves the L1 spec **and** the spec tree together.
L2 elicitation only starts after approval.

**Dependency order:** L2 specs with dependencies are only
authored after the predecessor spec is approved. The dependent
spec receives the predecessor as `referenced_spec` in the
review handover.

---

## Backtrack protocol

When Buddy spots a fundamental L0 mistake during L1 elicitation:
BACKTRACK signal to the user with two options — (A) revise L0
then continue with L1 (recommended), or (B) document the
assumption and continue. The user decides; no silent continuing
on a faulty foundation.

**Sharpening vs extension:** sharpening doesn't change any AC
(`spec_version`++, continue). Extension adds an AC or changes
scope (board delta review needed).

---

## L3 — post-L3 summary

After every L3 spec is closed, Buddy sends:

```
## L3 summary: <system name>

The following implementation specs were generated and reviewed
autonomously:
| Spec | Most important decision | Accepted risks |
|------|-------------------------|----------------|
| L3-01: <name> | <one sentence> | — |
| L3-02: <name> | <one sentence> | AR-1 (see spec) |

No gate — you can intervene now before implementation starts.
On objections: [A] revise the spec | [B] proceed.
```

For approved outcomes spanning separately commissioned work, keep the
summary to one page and carry forward the approved outcomes, specs, decisions
and accepted risks. Include current plan and evidence links with their owners.
Cover each outcome and its evidence, prerequisites and uncertainties, first
slice and later work, integration and activation. Repair missing coverage
before transferring the summary to Build in the existing no-gate handoff.
In the summary itself, direct the Build receiver to retrieve the current plan
and evidence from their owners immediately before filing or releasing work.
The receiver compares them with the agreement and holds for missing coverage,
evidence due now or authority, even after acknowledgment
(owner: workflows/runbooks/solve/REFERENCE.md §Planning and plan maintenance).

---

## Outputs

`workspaces/<objective>/specs/`: `l0-intent.md` ·
`l1-architecture.md` · `l1-spec-tree.md` ·
`l2-<feature-name>.md` (per feature) ·
`l3-<component-name>.md` (per component) ·
`review-history/` (l1/l2/l3-rounds.md per gate run).

## Contract

### INPUT
- **Required:** high-level intent (objective) — "build me X",
  "I need Y".
- **Required:** the intent is an objective (foreseeable done
  criterion, multiple features).
- **Optional:** existing partial specs — for delta elicitation.
- **Context:** no external context needed — scoping works in
  dialog with the user.

### OUTPUT
**DELIVERS:**
- L0 intent spec (why, for whom, constraints, done criterion,
  non-goals) — user-approved.
- L1 architecture spec (components, data flow, tech decisions,
  risks) + spec tree — board + user-approved.
- L2 feature specs (per feature: behaviour, edge cases, ACs) —
  board + user-approved.
- L3 implementation specs (per component: interfaces, state,
  error handling, contracts) — board-approved (autonomous).
- Post-L3 summary to the user.

**DOES NOT DELIVER:**
- No coding — scoping ends at the L3 specs; implementation
  starts via `build`.
- No architecture decisions — on >1 path → `council` or
  `solution-expert`.
- No problem analysis — on an open solution shape → `solve`
  workflow.

**ENABLES:**
- Build workflow: L2 / L3 specs as delegation-ready artifacts
  for MCA.
- Spec board: L1 / L2 / L3 specs as review input.
- Task creation: feature decomposition → tasks per L2 / L3
  spec.

### DONE
- L0 user-approved.
- L1 board-approved + user-approved (incl. spec tree).
- All L2 specs board-approved + user-approved.
- All L3 specs board-approved (autonomous).
- Post-L3 summary sent to the user.
- Specs persisted under `workspaces/<objective>/specs/`.

### FAIL
- **Retry:** board NEEDS-WORK → fix → re-board per level.
- **Escalate:** backtrack signal on a fundamental L0 mistake →
  the user decides (revise or document the assumption).
- **Abort:** the user aborts scoping → existing specs remain
  as a draft.

## Boundary

- **No unframed problem** — on an open solution shape →
  `solve` workflow (prepend `frame quick` on uncertainty).
- **No single task** — when one spec suffices → `build`
  workflow directly with the specify phase.
- **No ADR** — architecture decision with >1 path → `council`
  or `solution-expert`.
- **No coding process** — scoping ends at the L3 specs;
  implementation starts via `build`.

## Anti-patterns

- **NOT** ask 7 questions at once. **INSTEAD** one question, an
  answer, possibly a follow-up, then continue. Because:
  multi-question lists lead to shallow answers and lost
  nuances.
- **NOT** start L1 without user approval of L0 + spec tree.
  **INSTEAD** L0 approved, then L1 elicitation. Because: a
  faulty L0 spreads through every level.
- **NOT** continue on a faulty L0 when L1 analysis shows a
  problem. **INSTEAD** backtrack signal to the user, offer
  options. Because: silent continuing leads to specs that have
  to be fundamentally revised later.
- **NOT** skip scoping on multi-feature objectives because "in
  a hurry". **INSTEAD** push through progressive L0 → L1 → L2
  elicitation. Because: multi-feature objectives built without
  decomposition collapse during implementation.
