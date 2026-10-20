---
name: decompose
description: Breaks a locked task card into an ordered, independently-verifiable wave plan (checkpoints + rollback). Use after the card locks, or /decompose. Not for writing the card or running waves.
---

# Decompose

You are the architect of execution order. Given a locked task card, you decide how to break the work
into **waves** — discrete, verifiable units where each leaves the project in a defined state. You
produce the contract executor follows; executor does not modify the wave plan.

The wave machinery is domain-neutral. What is domain-specific — the *ordering* of foundation work and
the *default verification method* — you read from the active domain pack, not hardcode. (A software
wave plan orders schema before API; a finance plan orders assumptions before projections; a robotics
plan proves in sim before hardware.)

## What this does / does not do

Does: read the locked card + the resolved domain, sequence independently-verifiable waves with
checkpoints / rollback targets / verification modes / execution metadata, route the plan through
reviewer, write a receipt. Does **not**: write the task card (specify), execute waves or write
artifacts (executor), or choose the domain (intake).

## When NOT to use

- `task-card.md` is not locked (no specify receipt) — specify must run first (I1/I10 chain). There is
  nothing stable to decompose.
- intake declared `collapse_eligible: true` and complexity is Low — the plan may collapse to a single
  wave; do not manufacture multiple waves to look thorough (I12).

## Reference Routing

| Situation | Reference |
|---|---|
| Parallel fan-out scoring + confidence-check rubric | `references/wave-scoring.md` |
| Blast-radius check before sequencing (reference-graph tool) | `references/blast-radius.md` |
| Wave-plan / receipt write delegation | `engine/shared/references/script-delegation-contract.md` |

## Inputs

- `<workspace>/specs/task-card.md` (locked) · `<workspace>/scope.md` · `<workspace>/intake.json`
- `library/domains/<domain>/domain.yaml` → `ordering_heuristics`, `verification_default`
- `engine/shared/references/invariants.md`

## How to do it

### Step 1 — Confirm the card is locked

Read the specify receipt. Missing or FAIL → stop, surface, route back to specify.

### Step 2 — Confirm complexity

intake scored it; re-confirm against the full card. If revised upward, note the reason in the plan.

### Step 3 — Sequence the waves

Before finalizing any wave, confirm all three hold:
1. **Independently verifiable** — its output can be confirmed without running later waves.
2. **Single dominant risk** — one class of failure to manage per wave.
3. **Clear done condition** — the checkpoint is unambiguous; the verifier can check it without interpretation.

Split any wave that bundles risk classes or whose checkpoint needs human judgment to interpret.

**Ordering:** apply the general rule *foundation before integration*, then the domain's specific
`ordering_heuristics` from `domain.yaml` (e.g. software: "schema before implementation"; finance:
"assumptions before projections"). If the pack declares none, use the general rule and note it.

**Cleanup wave:** after any wave with significant generation, plan a dedicated cleanup wave — a
focused pass to remove over-scaffolding and dead artifacts. Do not embed cleanup as a negative
instruction inside an implementation wave.

**Rollback target per wave:**

| Type | When |
|---|---|
| `null` | Wave 1 only |
| `wave-checkpoint` | default — executor copies wave outputs to `<workspace>/session/checkpoints/<wave-id>/` |
| `worktree` | complexity High AND the wave has an irreversible operation AND the product is under version control. Fallback to `wave-checkpoint` if VCS is unavailable. |

Assign `worktree` only when all three hold; if uncertain, default to `wave-checkpoint`. Wave 1 has
`rollback_to: null`; each later wave's rollback target is the previous wave's checkpoint.

Wave-count guidance: Low 1–2, Medium 2–4, High 4–8 (more than 8 needs user confirmation).

### Step 3c — Declare execution metadata per wave

Every wave declares:

- **verification_command** — the exact runnable command that proves the checkpoint, or, when no
  command exists (human judgment, live environment), set `verification_mode: Attestation` — never
  default to Observation, which silently removes the gate.
- **execution_mode** — `AFK` (autonomous; verification automated) or `HITL` (human present; judgment
  / external access / manual confirmation). Prefer AFK. Attestation ⇒ almost always HITL.
- **dispatch_type** — `sequential` (steps have data dependencies), `parallel` (independent steps,
  dispatched in one turn), or `decision-gate` (parallel enrichment, then one sequential decision).
  Default `sequential`; never `parallel` when a step consumes another step's output.
  - **fan-out shape** (when `parallel`) — classify before dispatch: `depth-first` (one question from N
    perspectives → one agent per perspective), `breadth-first` (N independent sub-questions → one agent
    per topic), or `straightforward` (no fan-out → a single agent). The shape sets the agent count and the
    per-agent prompt — classifying first prevents over-spawning a simple task or under-serving a complex one.
  - **file_ownership** (when `parallel`) — list the output paths each parallel unit writes. A path claimed
    by more than one unit is a conflict: serialize those units or re-scope to disjoint outputs. Disjoint
    ownership makes merge conflicts structurally impossible; an overlapping-writer parallel dispatch is rejected.
- **execution_posture** (optional) — `test-first`, `characterization-first`, or `standard` (default).

### Step 4 — Assign verification mode per wave (I4)

Pick the strongest mode that applies; the pack's `verification_default` is the starting point.

| Mode | When |
|---|---|
| Test | automated assertion possible |
| Observation | artifact existence/state is the criterion |
| Measurement | a metric meets a declared threshold |
| Audit | compliance against the card's criteria or a standard |
| Review | output needs judgment |
| Attestation | irreversible action needs human sign-off |
| Demonstration | working proof must run against real conditions |

### Step 5 — Write the wave plan

Delegate the write (do not hand-author it). One entry per wave (contract below).

### Step 5.5 — Confidence check, then reviewer

Score each wave's sections against the rubric in `references/wave-scoring.md`; deepen any thin
section on a Medium/High wave (or any wave touching an irreversible operation) with one targeted
subagent before routing. Also run the fan-out assessment from the same reference. Then route the plan
to **reviewer** (a wave plan is a HIGH-impact decision — the execution contract): reviewer checks the
sequence is logical, each wave independently verifiable, rollback targets declared.

### Step 6 — Write the receipt

Base schema + `wave_count`, `complexity_confirmed`, `reviewer_triggered`, `rollback_checkpoints`,
`waves_with_verification_command` (must equal `wave_count`), `fanout_label`.

## Output Contract

**wave-plan.md** (`<workspace>/specs/wave-plan.md` — persistence: **Spec-Anchored**):

```markdown
# Wave Plan
**task_card:** <workspace>/specs/task-card.md
**domain:** <from intake.json>   **complexity:** Low|Medium|High   **collapse_eligible:** true|false
**generated_at:** <ISO-8601>

## Waves
### Wave 1: <name>
**inputs:** [card sections, context files]
**outputs:** [specific paths or named artifacts]
**checkpoint:** <condition true before Wave 2 begins>
**rollback_to:** null
**verification_mode:** <I4 mode>   **verification_command:** <runnable or "Attestation">
**execution_mode:** AFK|HITL   **dispatch_type:** sequential|parallel|decision-gate   **fanout_shape:** depth-first|breadth-first|straightforward (parallel only)
---
### Wave 2: <name>
… **rollback_to:** Wave 1 checkpoint …

## Deferred to Implementation
- [execution-time unknowns executor resolves against real artifacts — not gaps]

## Rollback Map
| Wave | Rollback target | Trigger |
|---|---|---|
| Wave 2 fails | Wave 1 checkpoint | HARD error or BLOCKED after 3 REVISE cycles |
```

**receipt** (`<workspace>/receipts/decompose-receipt.json`): base + the extension fields above.
persistence: Spec-Anchored.

## Proactive Triggers

- **A wave has no `verification_command` and mode is Observation**: Observation passes any wave whose
  artifact exists regardless of correctness — switch to Attestation or supply a command.
- **Two waves depend on each other's partial output**: neither is independently verifiable — re-sequence
  or merge.
- **Low complexity but 4+ waves**: over-decomposed (I12) — merge or collapse.
- **Two parallel waves (or fan-out agents) write the same path**: file-ownership conflict — make their
  outputs disjoint or serialize them; never dispatch overlapping writers in parallel.
- **Domain pack declares no `ordering_heuristics`**: fall back to "foundation before integration" and
  note it; do not import another domain's ordering.
- **A wave touches an irreversible operation with `rollback_to: null`**: every wave after Wave 1 needs
  a rollback target — assign the prior checkpoint or upgrade to worktree.

## Completion Criteria

**Done when:** `<workspace>/specs/wave-plan.md` exists; every wave is independently verifiable with a
checkpoint, rollback target, verification mode, and runnable verification_command (or Attestation);
reviewer returned a verdict; a decompose receipt with `waves_with_verification_command == wave_count`.

**Not done if:** any wave defaulted to Observation with no command; any wave after Wave 1 has
`rollback_to: null`; the plan was routed to executor without reviewer.

**Next step:** `executor` (run the wave plan) — guard gates each wave first.

## Related Skills

- **specify**: Use to author the locked card decompose consumes. NOT for sequencing waves — decompose.
- **executor**: Use to run the wave plan. NOT for producing or modifying it — decompose owns the plan.
- **reviewer**: Use to vet the wave plan before execution. NOT for writing it — decompose.
