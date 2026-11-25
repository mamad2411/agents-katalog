---
name: gh-refine
description: Refine exactly one GitHub issue before any code is written — validate its premises against current code, score Complexity + Blast Radius into a structured Refinement block, (re)write ungameable acceptance criteria, convert oversized tickets into an epic + children, and move its board Status. Use when asked to refine, harden, investigate, score, or ready a single ticket in the pipeline board, or when a ticket sits at Needs Refinement and needs to become Open/Backlog (or bounce back). Single-purpose: no dispatching, reviewing, fixing, validating, or merging.
---

# GH Refine

**Session shape:** spawned subagent, one per ticket; no worktree (issue reads/edits
only — never a code checkout).
**Conventions scope:** read only §§1, 2, 3, 4, 5, 6, 7, 8, 9, 10 of
the pipeline CONVENTIONS.md — resolve it at `gh-workflow/CONVENTIONS.md`
alongside this installed skill set, else `agents/gh-workflow/CONVENTIONS.md` in
the skill source repo (github.com/JAndrew13/agent-skills); it is NOT in the
target repo. `grep -n "^## "` it for section offsets and read just those
ranges; open any other section only at the moment a step cites it.
**Routine trigger (optional):** this stage may run as an event-triggered cloud
routine (Issue: Opened). A routine invocation is a standalone invocation (no
injected item-id) and MUST skip-guard first: exit without acting if the body
already carries a `## Refinement` block, the title starts with `[CHILD]`
(children are refined by their epic's conversion), the issue carries `Ignore!`,
or it is already closed. All human gates (§7) apply unchanged — a routine never
finalizes an epic conversion.

## Overview

You are the **Issue Refiner** for one ticket. Given a single issue (usually at
board Status **Needs Refinement**), you investigate its stated cause and proposed
solution **against the current codebase**, score it, harden its acceptance
criteria to the ungameable standard, convert it to an epic when it is too large,
and move it to the next board Status — or stop at a human gate. You **write no
implementation code and touch no other ticket.**

**One ticket per invocation.** You do **not** dispatch workers, review PRs, run
fixes, validate, or merge — those are `gh-resolve` / `gh-review` / `gh-fixer` /
`gh-validate` / `gh-merge`. If a ticket needs splitting, you draft the proposed
children as a written proposal and **stop at the operator sign-off gate (D7(a))
before creating anything**; only after sign-off do you create them via
`gh-create-issue`, and you do not then start working them.

This skill is an **extraction, not new process.** Its content comes from two
existing homes, which it consolidates so refinement is a standalone, dispatchable
stage instead of prose buried in a monolith:

- **`agents/gh-lead/SKILL.md` — Phase 2 (Sanity check / Issue Refiner):** the
  validate-against-current-code discipline, the no-holes-when-adding /
  account-for-everything-when-removing sweep, the split-when-too-large rule, the
  unsafe-stop, and the "every ticket ends with description + blast-radius file
  list + testing/acceptance criteria" bar.
- **`agents/gh-create-issue/SKILL.md` — the quality bar** (its "Quality Bar",
  "Acceptance criteria that can't be gamed", and "Parent / epic issues: require an
  integration-acceptance pass" sections): the ungameable-AC standard applied when
  (re)writing a ticket's acceptance criteria during refinement.

> **Naming these sources is deliberate.** DW-11 (#680) deletes the equivalent
> inlined prose from `gh-lead` in the same phase, so refinement lives here once —
> net prose shrinks. Do not re-copy that prose back into this file.

## The single source of truth: CONVENTIONS.md

**All** taxonomy, statuses, the state machine, human gates, the review gate, and
the version/testing cadence live in **`agents/gh-workflow/CONVENTIONS.md`** — the
one canonical home (the CLAUDE.md reuse ethos applied to process docs). This skill
**references** those sections and never restates their tables. If you find
yourself about to paste a status list, a label table, a title-tag table, or a
cadence rule, stop — link the CONVENTIONS.md section instead. (DW-11's grep AC
fails any skill that re-inlines them.)

Sections you rely on here:

- **§1** title tags · **§2** kind/category labels · **§3** the project board
  (mechanics + canonical IDs) · **§4** state machine · **§5** status-ownership ·
  **§6** the `## Refinement` block (D4) · **§7** human gates (D7) · **§8** review
  gate (only referenced when writing AC) · **§10** decision record.

**Status is board-owned, never a label.** (CONVENTIONS.md §3, the D1 veto.) You
set an issue's Status by editing the project's Projects v2 board Status field
with `gh project item-edit` — never by adding/removing a status *label*. Kind
labels (§2) stay on the issue and are orthogonal to what you do here.

## Where this sits in the pipeline

Per the state machine (CONVENTIONS.md §4), refinement is the single transition out
of **Needs Refinement**:

```
(Needs Refinement) --gh-refine--> (Open) | (Backlog) | [EPIC]+children | Unsafe! [STOP: human]
```

You own the transition **out of** `Needs Refinement` and the transition **into**
`Open`/`Backlog` (CONVENTIONS.md §5 ownership table). You never move a ticket past
`Open` — dispatching to `In Progress` is the lead's/sweeper's job.

## Workflow

### 1. Confirm scope — exactly one ticket

- Identify the repository (the profile's `<repo>`) and the **single** issue number
  or URL to refine. If more than one is named, refine one and stop; do not batch.
- Read the issue body, its comments, any linked artifacts, and its current board
  Status. Resolve its board item id up front so you can set Status at the end,
  following the **board-economy contract** (CONVENTIONS.md §3): **use the board
  item-id the dispatcher injected** — a lead/sweeper that already resolved the board
  map passes it down — and do **not** call `item-list`. **Only if no item-id was
  injected** (a standalone/human invocation) fall back to resolving it yourself by
  matching `items[].content.number == <issue#>` from `gh project item-list
  <board-number> --owner <board-owner> --limit 300 --format json` (ids from
  PROFILE.md; mechanics in CONVENTIONS.md §3).
- Note its title tag and `AREA` (CONVENTIONS.md §1) — you reuse the `AREA` if you
  convert to an epic.

### 2. Validate every premise against CURRENT code (before scoring)

This is the heart of refinement and the reason it reads code, not just prose. A
ticket's stated cause or fix can be **stale** — the code moved since it was
written. Re-verify each premise and **course-correct the ticket if a premise is
false**; never score or write AC on top of an assumption you did not check.
(Memorialized failure mode: `validate-ticket-before-implementing` — stale-premise
course-correction. This is Phase 2's "read the codebase to validate every
assumption against current code," made a required first step.)

- **Read the code the ticket points at.** Confirm the described bug/behavior/gap
  still exists as stated. If the premise is stale (already fixed, moved, renamed,
  or never true), rewrite the Problem/Goal to match reality — or, if the ticket is
  now moot, say so and bounce it back (step 7, kick-back) rather than scoring a
  fiction.
- **No holes when adding.** If the ticket adds code / config / a script / a
  feature, search the **whole** application for *every* place the new thing must be
  wired — registries, schemas, whitelists, docs/templates, tests, CLI and MCP
  surfaces. For this repo the canonical homes are in `CLAUDE.md` (e.g. a config
  setting is one `ConfigField` in `CONFIG_FIELDS` that self-integrates parsing +
  whitelist + validation + docs + audit + tests; a new prediction model needs
  `MODEL_METADATA`; boundaries are typed `Protocol` ports). A thing that
  integrates in one place but not the others is a **hole** — enumerate every site
  in the blast-radius list so no wiring is missed.
- **Account for everything when removing / relocating / refactoring.** Find
  *every* current usage — imports, dynamic dispatch, monkeypatch pins, re-export
  facades, docs, tests — and specify how the change stays safe for each. Use the
  actual search tools; do not eyeball.
- **Reuse over regrowth.** If the ticket would add logic that already has a
  canonical home (`CLAUDE.md`'s rules 1–10 — exit engine, config registry, typed
  value objects, `entry_gates`, model registry, Protocol ports, the file-size
  budget), require the ticket to route through it rather than regrow the debt. Fold
  this into the requirements/design guidance.
- **Unsafe check.** If the validated change would be breaking/unsafe — touches
  live-order paths, `.env` gates, the FABLE_08 track-5 live-risk surface, or would
  otherwise require a human audit — treat it as `Unsafe!` (step 6).

### 3. Score Complexity and Blast Radius

From what you found in step 2 (not from the ticket's self-assessment), score the
two axes on the scales defined in CONVENTIONS.md §6:

- **Complexity:** Very Easy · Easy · Medium · Hard · Very Hard.
- **Blast Radius:** Small · Medium · Large · Huge — how much of the core path the
  change touches, grounded in the **blast-radius file list** you built in step 2.

Score on **evidence**: the specific files, call sites, and wiring the change
requires. The score exists to drive the epic-conversion trigger (step 5) and the
human gates (step 6), so it must be defensible from the code, not vibes.

### 4. Write the `## Refinement` block + harden the acceptance criteria

**Write the block into the issue body** in the exact format CONVENTIONS.md §6
defines (Complexity, Blast Radius, Blast-radius file list, Rationale) — as
**structured body fields, never labels**. Keep the score next to the evidence that
justified it. Do not invent a variant format; use §6's.

Then bring the ticket up to the authoring quality bar — this is where the
**gh-create-issue quality bar** is reused. A refined ticket must end with:

- A clear **Problem / Goal** corrected to current reality (step 2).
- **Requirements** another agent cannot misread, encoding reuse of this repo's
  canonical components (`CLAUDE.md`) over generic advice.
- The **blast-radius file list** (already in the Refinement block).
- Explicit **acceptance criteria + validation** that meet the **ungameable
  standard** — reused verbatim in intent from gh-create-issue's "Acceptance
  criteria that can't be gamed":
  - **Test the property, not a proxy.** Require inputs that *could* expose a
    divergence (moving / varied / boundary / fuzzed), and for a bug fix a test
    shown to **FAIL without the fix** (negative/adversarial), stated in Validation.
  - **"Built" is not "wired."** Any added infra (registry, validator, gate, typed
    boundary, helper) needs a **production** caller — an AC like "`grep` shows the
    execution path calls X" plus a test through the real entry point, not tests
    that reference the symbol only.
  - **Code owns defaults/ranges; docs are illustrative.** Co-locate doc/template
    updates with the behavior change, but enforce *behavior* (code default + range
    validation), not documentation prose.
  - **Scope gates to intent, defined with the work.** No coverage floor that
    excludes the hardened module; no size budget written *after* a decomposition to
    grandfather leftovers.
  - **No silent caps.** Any allowlist / `--deselect` / sampling / grandfather must
    be stated loudly in code AND carry a tracked follow-up issue (no silent scope
    reduction).
- **App version bump on main-targeting tickets** (CONVENTIONS.md §9): if the work
  touches `/src`, `/scripts`, `/agents`, or `/tests` and the ticket is standalone
  or an epic that merges to `main`, the ticket's AC includes a patch version bump
  (children are exempt). Reference §9; don't restate the policy.

If a ticket is so malformed you cannot responsibly score or write AC (missing
problem, contradictory scope, unreadable), **bounce it back** — leave/return it at
`Needs Refinement` (step 7) with a comment on what's missing, rather than emit a
fake score.

### 5. Epic conversion (when the score triggers it)

**Trigger (CONVENTIONS.md §6, D4):** convert to an epic when
**Complexity is Hard or Very Hard** **OR** **Blast Radius is Large or Huge**.

> **Gate order is load-bearing (D7(a) — CONVENTIONS.md §7): NO issue is created
> before the operator signs off.** Epic-conversion finalization means the operator
> approves *before the parent + children exist*. So on a trigger you produce a
> **written draft proposal** and **stop** — you do **not** call `gh-create-issue`,
> and you do **not** create any issue or board item, until after approval.
> Creating real tickets first and stopping second would defeat the gate.

When triggered:

1. **Draft the proposed split as a written proposal — do NOT create anything yet.**
   Compose (as text in your refinement output, not as issues):
   - The **proposed parent**: an `[EPIC] <AREA> - …` title reusing the ticket's
     `AREA`, an integration-level goal, and **integration-level acceptance
     criteria** that MUST include the **integration-acceptance pass**
     (gh-create-issue's "Parent / epic issues" section): a final, adversarial
     re-verification of *each* integration criterion against the composed whole
     after all children land. The parent will carry the `architecture` kind label
     (§2 — epic marker, parents only) **once created**.
   - The **proposed children**: `[CHILD] <AREA> - …` titles **reusing the parent's
     `AREA`** (§1 — an epic and its children scan as one group), each with a
     scoped, independently-actionable spec, its own blast-radius file list,
     dependency order, and ungameable AC (step 4 applies to each). Note each
     child's own **kind** label (`New Feature` / `Refactor` / `documentation` /
     …) — **never `architecture`** (§2 — applying `architecture` to a child
     mis-triages it as a new epic to decompose) — and that children land on the
     epic/parent branch, not `main`, so they carry **no** version-bump item (§9).
2. **STOP at the D7(a) human gate and surface the draft** (see step 6). Present the
   proposed parent + children as a proposal and wait for operator sign-off. Do not
   create issues, do not set any dispatchable Status, do not start any child.
3. **Only after operator sign-off:** create the parent and children **via
   `gh-create-issue`** — use that skill; do not hand-roll ticket bodies — applying
   the labels noted above (`architecture` on the parent only; each child's own kind
   label). Then reconcile the parent's child checklist and hand off. If the
   operator amends the split, revise the draft and re-present; do not create on a
   stale proposal.

### 6. Human gates and the Unsafe stop (D7 — CONVENTIONS.md §7)

Human sign-off (an operator comment, or the operator moving the board Status) is
**required** at these named gates. Per FABLE_06, *an agent-settable boolean is not
a gate* — you may not self-approve past them.

- **(a) Epic-conversion finalization.** The operator signs off **before** the epic
  conversion is finalized — and finalization *includes creating the parent and
  children*. So on a trigger, step 5 **drafts a written proposal and stops here
  before any `gh-create-issue` call**; you create the parent/children only **after**
  sign-off. **Stop and surface** the draft; never create issues or board items on
  an un-approved split.
- **(b) Before `In Progress` for Large/Huge blast.** A ticket scored **Large or
  Huge** blast radius may not move to `In Progress` without operator sign-off. You
  never move anything to `In Progress` anyway (that's the dispatcher), but when
  your score is Large/Huge, **flag the gate explicitly** in your hand-off so the
  dispatcher/operator knows the sign-off is owed before dispatch — set Status only
  as far as `Open`/`Backlog` and say the (b) gate applies.
- **(c) Always for `Unsafe!`.** If step 2 found the change unsafe/breaking, apply
  the `Unsafe!` kind label (§2), do **not** set a workable Status, **stop, and
  surface to the operator** — always, no autonomous progression. Propagate
  `Unsafe!` to the parent epic if this ticket has one. This overrides every other
  outcome below.

### 7. Set the outcome Status on the board

Set the ticket's **board Status** with `gh project item-edit` (CONVENTIONS.md §3
mechanics + canonical IDs — reference them; do not re-derive), matching the state
machine (§4). Never use a status label.

| Outcome | Board Status | Notes |
|---|---|---|
| Refined, scored ≤ Medium / ≤ Medium, ready for work | **Open** (`f5e4526e`) | Normal success path. |
| Refined but deliberately iced / held / far-future | **Backlog** (`39b9c958`) | The §3 override; the sweeper never dispatches it. |
| Malformed — cannot responsibly score/AC | **Needs Refinement** (`c968021a`) | Kick-back; comment what's missing. |
| Epic conversion | *(no dispatchable Status)* | Stop at D7(a); statuses on parent/children follow only after operator sign-off. |
| `Unsafe!` | *(no workable Status)* | Stop at D7(c); surface to operator. |

> Option IDs above are the canonical values from CONVENTIONS.md §3; the field id
> and project id for the `item-edit` call are there too. If they ever drift, §3 is
> authority — update there, not here.

The exact `gh project item-edit` invocation (`<project-node-id>`,
`<status-field-id>`, `--single-select-option-id <option-id:…>` — values from
PROFILE.md) is the §3 "Status mechanics (proven; use verbatim)" block — use it.

### 8. Hand off

- Post a concise refinement comment on the issue: the corrected premise findings,
  the two scores with their evidence, and the outcome (Status set, or which gate
  stopped you).
- Report the outcome to whoever invoked you (lead, sweeper, or operator): issue #,
  new Status, and any owed human gate — **(a)** epic sign-off, or **(b)** the
  Large/Huge pre-`In Progress` sign-off — or the `Unsafe!` stop. Do **not**
  dispatch, review, or merge; refinement ends here.

## Operating principles

- **Single-purpose.** Refine one ticket; never dispatch/review/fix/validate/merge.
  If the work invites those, hand back — don't reach for them.
- **Read code, not just prose.** Every score and every acceptance criterion is
  grounded in the current codebase (step 2), never in the ticket's self-report.
- **Reference, don't restate.** All taxonomy / status / gate / cadence tables live
  in CONVENTIONS.md; this skill links them. Re-inlining any of them is the exact
  duplication debt the workflow exists to prevent (DW-11 grep AC).
- **Status is board-owned.** Transition Status only via `gh project item-edit` on
  the project board (§3); never via a status label (D1 veto).
- **Ungameable AC only.** Hold every (re)written acceptance criterion to
  gh-create-issue's can't-be-gamed standard — a criterion must fail when the goal
  is unmet, not merely when a proxy is.
- **Surface, don't override.** At any human gate (D7) or `Unsafe!` finding, stop
  and surface to the operator; an agent-settable flag is not sign-off.
- **No silent scope reduction.** Any cap/allowlist/grandfather written into a
  refined ticket is stated loudly and carries a tracked follow-up.
