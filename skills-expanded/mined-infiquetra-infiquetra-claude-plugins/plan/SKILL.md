---
name: plan
description: Create durable Infiquetra implementation plans with issue, review, test, and deploy gates. Interrogates HOW work gets built, writes an agent-consumable plan artifact, records a plan saga, and routes to doc-review and /work. Triggers on "plan this", "how should we build this", "create a plan", "break this down", or a handoff issue ready for planning.
---

# Plan

`/plan` answers **"How should it be built?"** It takes a settled WHAT — from `/brainstorm`'s
requirements doc, a handoff issue, or a clear ad-hoc request — and interrogates it into a durable,
agent-consumable implementation plan. It does **not** invent product behavior (that came from
`/brainstorm` or the issue) and it does **not** implement code. It plans, records a plan saga,
**dispatches the plan review and loops on repair until it passes**, and routes.

## Position in the lifecycle

`/plan` sits between requirements and execution:

- `/office-hours` answers: "What is even the right frame?"
- `/ideate` answers: "What are the strongest ideas worth exploring?"
- `/brainstorm` answers: "What exactly should one chosen idea mean?" (the WHAT)
- **`/plan` answers: "How should it be built?"** (the HOW — this engine)
- plan review (`/doc-review`) answers: "Is this plan ready to execute?" — and this engine runs it
  itself in Phase 5.4 rather than recommending it.
- `/work` answers: "Build it." (consumes the plan + saga)

`review` is a declared `lifecycle_phase` in `scripts/saga.py`, but no code path writes it. Plan
review is a step inside the plan phase, not a phase the saga records.

The handshake is deliberate. When the WHAT is unsettled, `/plan` recommends the operator step back to
`/brainstorm` first (a one-way forward route — `/plan` points there; it does not claim `/brainstorm`
"accepts" a handoff). When the plan is written, `/plan` does not recommend the review — it dispatches
it, repairs what it finds, and re-checks until nothing above `P2` is open or the operator overrides
one finding in one word.

## Core principles

1. **Decisions, not code.** Capture approach, boundaries, files, dependencies, risks, and per-unit
   test scenarios. Do not pre-write implementation code or shell-command choreography. Pseudo-code and
   DSL grammars are allowed only as explicitly directional high-level design, never as implementation
   specification.
2. **Ground before asking.** Read the code before you ask a question its answer is already in. Cite
   `path:line`. Quantify everything — "several files" is a bug; find the exact count. Never guess about
   the codebase; go read it.
3. **Agent-consumable plans.** The plan must let an unfamiliar implementer (human or `/work`) start
   confidently without re-asking the operator. Stable IDs (R-IDs, KTDs, U-IDs), per-unit test
   scenarios with repo-relative test-file paths, dependency-ordered units.
4. **Right-size via the warranted-gate.** Not every invocation produces a plan doc. Genuinely atomic
   work skips the artifact. But stress-test the "looks atomic" case — most requests hide KTDs.
5. **HOW-only.** Assume the WHAT arrived from `/brainstorm` or the issue. Do not re-litigate product
   scope, actors, or success criteria here — carry them forward as constraints.

## Interaction method

Use `AskUserQuestion` for choices from a known set (destination, execution backend, scope class,
resume-vs-mint). Call `ToolSearch` with `select:AskUserQuestion` first if its schema is not loaded.
Ask one question per turn; prefer a concise single-select when natural options exist. For open-ended
interrogation, ask inline in chat. Never silently skip a question.

In a channel session (`redis-channel` active), `AskUserQuestion` cannot be called — inline the choices
in your reply text instead. Follow the canonical channel-inline convention in
`saga/skills/brainstorm/SKILL.md` (do not duplicate its wording here).

Use repo-relative paths in every generated document. Absolute paths break portability across machines
and worktrees.

---

## Phase 0 — Enter and warranted-gate

Capture the input and decide whether a plan doc is even warranted before spending interrogation effort.

### 0.1 Capture input

The input is an issue reference, a requirements doc path, or an ad-hoc request. Take it from command
arguments or the active artifact. If empty, ask: "What would you like to plan? Point me at the
requirements doc, the issue, or describe the work." Do not proceed without one.

### 0.1b Admission — the first thing `/plan issue` does

<!-- gate-record: id=plan-admission-questionnaire absence=HALT transport=ask-user-question -->

When the input is an issue, run admission before anything else. It is where "answer the questions up
front" lives: the card validator runs, every defaultable run-configuration parameter is filled from
the per-repository profile, fleet-core's staffing component and the lifecycle repository's decided
defaults, and only what is left over is put to you — once, in one message.

```bash
python3 plugins/saga/scripts/admission.py --issue <N> --dry-run
```

Read what it prints. It names the defaults it filled with the source of each, and the questions that
remain. Then:

1. **A card that fails the validator stops here.** Admission exits 2 and names the missing fields.
   The repair belongs on the card, through `mission-control`, not in the plan — planning against a
   half-formed card is what the lifecycle repository's Shaping exit exists to prevent.
2. **Put the printed questions to the operator as one message** (`AskUserQuestion`, or
   channel-inline). One message, not one question at a time: the whole point is that the operator
   answers the run's shape once. Never invent an answer to any of them — the approval boundaries in
   particular are the operator's grant and nobody else's.

   **If the question cannot be put** — no `AskUserQuestion`, no channel back to the operator —
   **halt and say so.** Do not fill the answers from the card, do not take a default, and do not
   plan past them. The unanswered set is the run's authority: the approval boundaries are a grant
   only the operator can make, and a recorded grant nobody made is worse than a missing one, which
   is why the absence behaviour here is a halt rather than a safe default.
3. **Record the answers**, which writes the run record and clears the questions:

   ```bash
   printf '%s' "$ANSWERS_JSON" > /tmp/admission-answers.json
   python3 plugins/saga/scripts/admission.py --issue <N> --answers /tmp/admission-answers.json
   ```

The record lands at `<primary checkout>/.claude/saga/runs/issue-<N>.json` — an absolute path outside
any worktree, so every later role reads the same file. Say that path in your first message; later
steps and other sessions are told to read it.

An answer already in the record is never re-asked, so re-running `/plan` on an admitted issue prints
an empty question set and costs nothing. The schema is
`plugins/saga/references/run-record.md`; the profile is
`plugins/saga/references/repository-profile.md`.

The questions admission asks are the run's shape, not the plan's content: Risk tier and its
justification, the seven approval-boundary scopes, the destination, staffing overrides, the lens
declaration, the repair allowances, the response to unfinished functional testing, whether the
repository has a branch preview, whether `main` is consumed directly, and whether the change is
code, docs, or mixed. Phase 5's own questions (destination, backend) are separate and stay where
they are; where admission has already recorded the destination, do not ask it again.

### 0.2 Issue handoff routing

If the input is a GitHub issue, run `scripts/parse_issue.py` and inspect the `handoff` object. Pass
`--flags` to widen the keyword flags with a model judgment (widen-only: a keyword flag stays set
whatever the model answers).

- For `idea-ready` or `requirements-ready` handoff issues, create or update a durable plan from the
  issue and its `Source context` / linked source. These are the maturities `/plan` consumes.
- For `plan-ready` or `resume-ready` handoff issues, tell the operator `/work <issue>` is the more
  direct consumer unless they explicitly want to re-plan. A plan already exists for these.

Use the issue's `Handoff maturity` and `Source context` sections as authoritative input.

### 0.3 Saga scan — offer resume before minting

Before minting a new plan saga, run `scan` to offer resuming an existing one (slug-instability
mitigation — a drifting task description would otherwise fork a second saga for the same work):

```bash
python3 plugins/saga/scripts/saga.py scan
```

If a candidate matches this thread (same `issue_ref`, or the operator confirms "resume this"), reuse
it — Phase 5 appends a tick rather than minting. For an issue whose `issue-<N>` directory is absent,
resolve via `state.json.sagas[*].issue_ref` ending in `#N` (the id is sticky; never rename the
directory). See `references/saga-spec.md` §2.3 and §2.1.

### 0.4 Warranted-gate — decide whether a plan doc is warranted

Bias toward producing a plan; the risk asymmetry favors writing one. **Skip the plan doc only when ALL
hold:** the work is atomic (fits one commit, no unit boundaries), there are no Key Technical Decisions
worth recording, no scope boundaries worth pinning, and no upstream artifact needs traceability.

**Stress-test the "looks atomic" case** — many requests look atomic but hide KTDs ("add caching" →
TTL / invalidation / key shape; "migrate A to B" → semantic-difference KTDs; "add rate limiting" →
algorithm / scope / configurability). See `references/plan-sections.md` ("Decide whether a plan doc is
warranted") for the full skip-vs-write rubric. When skipping, route directly to `/work` and let
decisions land in the commit message; otherwise continue.

### 0.5 Scope classification

Classify the work into one depth, which sizes the plan (Phase 3) and gates the deepening pass (Phase 4):

- **Lightweight** — small, well-bounded, low ambiguity. ~2-4 units. Omit optional sections.
- **Standard** — normal feature or bounded refactor with technical decisions to document. ~3-6 units.
- **Deep** — cross-cutting, strategic, high-risk, or highly ambiguous. ~4-8 units; optional analysis
  sections warranted.

If depth is unclear, ask one targeted question, then continue.

---

### 0.6 Submit the card's move to `Planning` / `Designing` — Mission Control executes it

**Actor:** this skill. **Trigger:** planning has started for a real issue — §0.4 judged a plan
document warranted and the issue reference is known. **Move:** the live pair `Stage` = `Planning`,
`Status` = `Designing`.

**The trigger names only what exists at §0.6.** An earlier form required the saga tick to be minted
and "the plan artifact's path is settled": the tick is minted in §5.3 and the artifact in
Phase 3, so neither condition can be true where the move is placed. An agent reading the section
literally would either never submit the move or submit it from the wrong phase, and the card would
sit in the stage before. A board move's trigger must be observable at the point the move is made —
which is the whole point of moving the card *early*, when planning starts rather than when it ends.

**Deciding and submitting is not writing.** Mission Control remains the only executor of a `Stage`
or `Status` write; this skill submits the move and never composes or executes one itself. The
submission goes through the reconcile controller, which owns the certificate gate, the idempotency
ledger and the replay key:

```bash
python3 plugins/saga/scripts/reconcile_controller.py reconcile \
  --op set-field-status --repo <owner/repo> --number <N> \
  --target-state "Designing" \
  --payload '{"assignments": [["Stage", "Planning"], ["Status", "Designing"]]}'
```

**Submit both halves, and check both.** The move is one invocation carrying two assignments, and
Mission Control does **not** roll the pair back: a `Stage` write can land while `Status` fails.
Read the record the same way Phase 5.5 does, and read it by more than its `status` word. The
record's `field` is the whole submission's identity: `Stage+Status` when both halves were executed,
a bare `Status` when they were not — which is what an installed saga older than the pair contract
reports after writing the `Status` half alone, `written` and all. `skipped` is not a synonym for
success either: it also means "already keyed" or "could not judge", and carries a `note` in the
second case. A `failed` record names which half landed and which did not; `halt`/`gated` falls back
to the operator-prompted Mission Control path rather than forcing the write. Submitting the
`Status` half alone is the failure worth naming: `Designing` is a legal `Status` on its own, so a
half-write looks like success while `Stage` stays where it was.

When there is no issue, there is simply no card to move; say nothing further.

### 0.7 Structured pre-answers — intake, evaluated once

A caller that has already settled a decision may hand it to `/plan` in the invocation text — a
fenced JSON block, schema `plan_pre_answers.v1` — instead of letting the conversation re-ask it.
Contract: `references/saga-spec.md` §15. Evaluate it once, at entry, before the first question,
with the runnable validator:

```bash
python3 plugins/saga/scripts/plan_pre_answers.py --invocation-file <invocation-text-file> \
  --established backend=<already-settled-value> --established destination=<already-settled-value>
```

Pass one `--established <field>=<value>` for each decision already established in this thread
(repeatable), so the validator can detect a carrier that contradicts it; omit any flag whose
decision is not yet settled — on a fresh thread, omit both.

It prints the outcome as JSON and exits 0 when there is no stop (a clean apply, or no carrier) and
2 with `stop` set otherwise — on 2, surface the `stop` reason exactly; never continue silently.
Two other failures also exit 2: an unreadable `--invocation-file` prints the same JSON shape with a
`stop` naming the unreadable path, and a malformed command line prints argparse's usage with no
JSON at all — treat both as stops, never as a clean apply.
This is intake, not a phase: its only visible effects are narration of an applied value together
with the `caller` that supplied it, and the absence of a question that would otherwise have been
asked. Five rules govern it:

- **Apply and narrate.** A valid `destination` (Phase 5.1's enum) and an `inline` backend are
  applied to their decisions and visibly narrated together with the `caller` that supplied them. Do
  not ask the operator to repeat a settled decision. `cc-workflows-ultracode`
  are legal plan values, but the carrier never applies them automatically — they require explicit
  operator invocation, so the validator stops and surfaces them instead of applying.
- **Absence falls through.** A missing carrier, or a carrier omitting a field, is not an error: the
  omitted decision follows the normal adaptive conversation exactly as it does today.
- **Invalid or contradictory stops.** A value outside its enum, or one contradicting a value already
  established in this thread (supplied to the validator as `--established <field>=<value>`), stops
  and surfaces the conflict with the validator's reason — never a silent default, never preferring
  either side.
- **Unknown schema refused whole, two cases.** A non-v1 token inside the `plan_pre_answers` family
  is refused in its entirety — no field from that carrier is applied. A foreign schema family is
  not a carrier at all and is ignored.
- **A malformed carrier stops.** The carrier's fence info string must be exactly `json` — any other
  info string is not a carrier and is silently ignored, so a carrier fenced any other way drops
  without effect. A `json` fenced block whose raw text names the `plan_pre_answers` family and
  fails to parse, carries duplicate JSON keys, or appears alongside a second carrier stops the run
  — never resolved silently; an unrelated malformed JSON example (no family token) is ignored. A
  carrier with an unadmitted key (anything but `backend`, `destination`, `caller`, `schema`) or a
  non-string `caller` is refused the same way.

Direct `/plan` — an issue, a prompt, or a Brainstorm document, no carrier — is unchanged: nothing
applied, nothing narrated, nothing stopped. Exactly two decision fields are admitted, `backend` and
`destination`; `caller` is envelope metadata for the narration, not a decision field.

## Phase 1 — Ground (HOW)

Read code before asking. This is the moment the operator sees you grounded in their actual repo, not a
generic checklist.

1. **Read the upstream artifact first.** If a `/brainstorm` requirements doc (`docs/brainstorms/*-requirements.md`),
   the handoff issue, or a linked source exists, read it thoroughly and carry forward its problem frame,
   requirements, scope boundaries, KTDs, and open questions as constraints the plan must honor.
2. **Read `STRATEGY.md`** if present and anchor plan decisions to the active tracks; flag any decision
   that pulls away from the stated approach.
3. **Read the engineering journal** (`docs/engineering-journal/`) for relevant prior LEARNINGS and
   DECISIONS so the plan follows established patterns instead of reinventing them.
4. **Quantify.** Find exact counts (files, call sites, tables). Cite `path:line` in your prose.
5. **Dispatch generic `Explore` agents in parallel** for grounding — repo patterns, relevant files,
   existing test conventions, adjacent implementations. Use the generic `Explore` agent; the `ce-*`
   research agents do **not** exist in this plugin.

**Cold-start (no upstream WHAT).** If there is no brainstorm doc, no issue, and the request is bare:
run a light Why-check (problem frame, intended behavior, obvious non-goals, success signal — keep it
brief; see `references/interrogation.md`). If the WHAT itself is unsettled — product framing, user
behavior, or scope is genuinely open — **recommend the operator run `/brainstorm` first** to settle
the WHAT, then return to `/plan`. This is a one-way forward route: point them there, offer to continue
planning with explicit assumptions if they decline, and do not claim `/brainstorm` "accepts" a handoff.

---

## Phase 2 — Interrogate (HOW)

**Load `references/interrogation.md`** and run the HOW-interrogation register against the grounded
evidence. Ambiguity is a bug; find it. The register covers:

- **Failure-mode enumeration** — for each unit, what happens when the input is empty, null, huge,
  duplicated, called by the wrong role, or called twice. Unenumerated failure modes are unwritten test
  scenarios.
- **Scope-lock** — lock what is explicitly out of scope early. When the operator opens a new front
  mid-plan, name it: "That's a separate issue — let's finish this one."
- **KTD-forcing** — surface the load-bearing technical decisions and force a choice with rationale.
  An open design fork the plan never resolves is a gap, not a decision.
- **Anti-premature-solution** — do not jump to implementation detail before the approach, boundaries,
  and failure modes are pinned.

Push on **vagueness** and **ungrounded assumptions** (not the operator's judgment): an undefined term,
a "several files" that should be a count, a behavioral assumption you have not verified in the code.
Push twice, then respect the answer. Escape hatches are in `references/interrogation.md`.

---

## Phase 3 — Synthesize the plan artifact

Write the plan to `docs/plans/YYYY-MM-DD-<topic>-plan.md` per `references/plan-sections.md`. Right-size
by the Phase-0.5 scope class. **Never code during this phase** — research, decide, and write the plan.

Follow the shared formatting contract in `saga/references/formatting-style.md` for the plan's visual
structure: lead each unit and major section with a one-line summary, keep narrative fields as short
(≤3-sentence) blank-line-separated prose, render comparative/scored data as a table, and never stack
bold labels without a blank line between them. Per-unit fields stay as blank-line-separated
`**label:**` lines under each `### U<N>.` heading (the contract's prose-heavy per-unit branch) — not a
table.

**Hard floor (every warranted plan carries these):**

- **Summary** — what the plan proposes, in 1-3 lines.
- **Problem Frame** — why the work is being done (may merge into Summary for compact plans).
- **Requirements** — with stable **R-IDs** (`R1.`, `R2.`); the reviewer's and `/work`'s checklist.
- **Key Technical Decisions** — the **KTDs**, each `<decision>: <rationale>`; the load-bearing choices
  that constrain implementation.
- **Implementation Units** — with stable **U-IDs** (`U1.`, `U2.`), each independently landable, with
  per-unit test scenarios and repo-relative test-file paths. Feature-bearing units require real test
  scenarios; only non-feature units (config, scaffolding) may use `Test expectation: none -- [reason]`.
- **Scope Boundaries** — what is explicitly out of scope, with `Deferred to Follow-Up Work` kept
  distinct from true non-goals.

**Deep adds (warranted only, never boilerplate):** High-Level Technical Design (HTD), Risk Analysis &
Mitigation, Alternatives Considered, Success Metrics. Include only when the content earns the section.

The plan must serve **three audiences**: the implementing agent (informed starting baseline), the
reviewer (load-bearing decisions in one pass), the future reader (why the work was done).

**Plan-doc frontmatter** (NOT the saga fields — those land in Phase 5):

```yaml
---
title: <verbatim plan title, matches the H1>
type: <feat|fix|refactor|chore|docs|perf|test>
status: active
date: YYYY-MM-DD
origin: <repo-relative path to the upstream brainstorm/requirements doc, when planning from one>
backend: <inline|cc-workflows-ultracode>
deepened: <YYYY-MM-DD, optional; added when the confidence pass deepened the plan>
---
```

`backend:` is required on every newly created plan; a legacy plan that lacks it stays compatible
through `/work`'s attended offer — never rejected, never rewritten. `origin:` MUST be emitted
whenever an upstream artifact exists so the review phase can trace the plan back to its source; when
there is no upstream doc (cold-start ad-hoc), it may be omitted. The body MUST use
the exact section markers `Implementation Units`, `Key Technical Decisions`, and the `U1` U-ID prefix —
`/doc-review` parses these to recognize the document as a plan.

**Record the KTDs to the engineering journal** (`docs/engineering-journal/DECISIONS.md`) — the journal
is the canonical decision record; the saga's `## Decisions` mirrors it.

---

## Phase 4 — Deepen (condensed confidence pass, conditional)

After writing the plan, evaluate whether it needs strengthening. The condensed confidence-pass rubric
lives in the **Confidence pass (deepening)** section of `references/plan-sections.md` — per-section gap
checklist, risk-weighted "is this plan thin?" scoring, and the top-N section cap.

- **Auto-run** for Deep plans, high-risk topics (auth, payments, data migration, external APIs,
  privacy), or thin grounding (Phase 1 found fewer than ~3 local patterns for what the plan needs).
- **Skip** for Lightweight, well-grounded plans — report "Confidence check passed" and continue.

When deepening, dispatch generic `Explore` / `Task` agents (not `ce-*` agents) at the top-scoring
sections only. Strengthen rationale, sequencing, test scenarios, and risk treatment in place. **Never
renumber existing U-IDs** when reordering or splitting units (the most likely accidental-renumber
vector). Add `deepened: YYYY-MM-DD` to frontmatter when the plan was substantively improved.

---

## Phase 5 — Saga, plan review, board move, and route

### 5.1 Ask the destination

Ask the routing intent (`AskUserQuestion`, or channel-inline): **plan-only / pr / merge /
nonprod-deploy**. This becomes the saga `--destination`. (If a Phase 0.7 pre-answer carrier
already applied `destination`, skip this question — the applied value stands, narrated at
intake.)

**Deploy-autonomy follow-up (only when destination is `nonprod-deploy`).** When — and only when —
the operator picks `nonprod-deploy`, ask one more question (`AskUserQuestion`, or channel-inline) to
capture the gate-or-auto posture at the saga→deploy edge (issue #395, KTD3). Skip this question for
every other destination.

> **When a merged item reaches deploy, should nonprod promotion happen automatically, or wait for
> your explicit confirmation each time?**
> **A) Gate** (default, pre-select) — deploy asks for explicit confirmation before promoting.
> **B) Auto** — deploy may auto-promote to **nonprod only** (staging/production always confirm).

This becomes the saga `--deploy-autonomy` value shown in §5.3’s generated examples. It is authored **once** here and read — never
re-asked — by `deploy_handoff.offer` at handoff time; there is deliberately no way to widen it to
`auto` at deploy time. **Pre-select Gate**: a missing or gate posture can never auto-fire, which is
the safe failure direction (R5). Omit `--deploy-autonomy` entirely for any non-deploy destination —
`deploy_handoff` reads an absent posture as `gate`.

### 5.2 Record the execution backend

**Write the backend into the plan document's `backend:` frontmatter field**, not only into the saga
tick. The tick is untracked local state: it does not survive a worktree boundary, another machine,
or another vendor, so an executor that did not run in this directory cannot see it. The plan
document travels with the work because the executor commits it alongside the changes, which makes
it the place a decision made here can reliably be read later. `/work` honours that field and does
not ask again.

The recorded enum has one value: `inline`. It matches `ORCHESTRATION_MODES` in `saga.py` and
§1 of [`references/operator-choice.md`](../../references/operator-choice.md). Issue #1030 archived
the `team-execution` plugin and removed the `cc-workflows` plugin, so there is no offer to render
and no choice to put to the operator. Still call `lifecycle_state.py recommend-backend` and
still record both `--orchestration-recommended` and `--orchestration-mode` (R12 telemetry), so a
tick continues to carry recommended-and-chosen rather than going silent on the decision — the
recommender now returns `inline` with a work-shape rationale rather than a different backend.

A saga written before that release may still carry `team-execution` or `cc-workflows-ultracode`.
Either reads back and renders its label; neither can be written again.

#### 5.2a Derive the per-unit tiers

This applies to **any** backend that spawns a per-unit agent, not only to a Claude Code
Workflow: the honoring seam below names the `agent`, `external-engine` and `workflow` spawn
kinds alike. Where admission already recorded a staffing plan for the run, that plan is the
authority for the roles it names and this step fills in only the units it does not cover.

**Step 1 — Derive per-unit tiers.** For each Implementation Unit in the plan, assign a `{model, effort}`
tier from the work-shape heuristic (R10). Surface the tier table for operator override before locking:

<!-- BEGIN GENERATED TIER TABLE (rendered from staffing.json via render_tier_table.py — do not hand-edit; a seeded divergence fails tests/test_tier_resolver.py::test_skill_registry_sync) -->
| Work shape | Default tier | Rationale |
|---|---|---|
| Judgment, design, adversarial review, architectural decisions | `opus / high` | Judgment, design, adversarial review, architectural decisions — deep reasoning needed; cost-justified. |
| Mechanical, deterministic, scripted transforms, scaffolding | `sonnet / medium` (or `haiku / low` for purely mechanical) | Mechanical, deterministic, scripted transforms, scaffolding — bounded output, predictable steps.; Purely mechanical work within the mechanical work-shape — cheapest tier still safe for bounded, predictable steps. |
| Read-only survey, search, grep, sampling, census | `sonnet / low` | Read-only survey, search, grep, sampling, census — low-effort read, no write risk. |
| External-engine delegation, `intent=offload`, `verifiability=test-gated` (ratify-only) | `haiku / low` | External-engine delegation, intent=offload, verifiability=test-gated — chaperone ratifies the declared test oracle and provenance; keep the chaperone cheap unless evidence size escalates. |
| External-engine delegation, `intent=offload`, `verifiability=unverifiable` or absent | `sonnet / medium` | External-engine delegation, intent=offload, verifiability=unverifiable or absent — chaperone performs full review; a heavier default would erase the token savings that motivated delegation (KTD2). |
| External-engine delegation, `intent=second-opinion` (U12) | `opus / high` | External-engine delegation, intent=second-opinion — adversarial verification IS the product; extra spend assumed; fable/xhigh available as a per-unit override, never a default (KTD2). |
| External-engine delegation, `intent=divergence` (adversarial review) | `opus / high` | External-engine delegation, intent=divergence — agreement and disagreement are both explicit adversarial-review outcomes; use the high-tier chaperone posture. |
<!-- END GENERATED TIER TABLE -->

Apply the heuristic per unit, then present the full tier table (U-ID, label, proposed tier, rationale)
and ask the operator to confirm or override before proceeding. Do not lock tiers silently.

**Run-start posture seeds the defaults (#380).** When the run carries a committed intent envelope
(`ExecutionSpec.intent`, or the parent outcome's `OutcomeSpec.intent` — see
`plugins/saga/references/intent-envelope.md`), derive each unit's PROPOSED tier through
`intent_envelope.seeded_tier(spec, work_shape)` (equivalently `intent_envelope.py recommend
--work-shape <shape> --run-mode <mode>`): the posture was asked ONCE at run start, and an
unattended posture proposes one rung cheaper than the attended default for the same work shape.
This changes only the table's proposed defaults — the table itself, the operator-override flow,
and the `VERIFY_N_CAP` mechanics are unchanged, and no per-unit posture question is ever asked
(the fleet drift guard fails on one).

**The Estimate column (#402) is retired.** It rendered an ordinal, index-weighted spend per unit from `spend_estimate.py`, which issue 1030 removed with the spend readers; the tier table is U-ID, label, tier and rationale.


**The mid-run tier lever is gone (#365, removed by issue 1030).** The `/tier` command and its
run-scoped ceiling file are removed, so the table this skill authors is the tier a unit runs at. An
operator who wants a different tier mid-run re-plans the unit; there is no longer a lever that
clamps an already-emitted spec.

**Persisted tier preferences (#368).** Before deriving cold from the registry table above, resolve
each work-shape through fleet-core's staffing component
(`fleet_commons/staffing.py`, `load_overlay` and `resolve_shape`) — precedence is **repo overlay >
issue band > shared registry**. Issue 1030 removed saga's own `tier_defaults.py`; the component it
delegated to is the one implementation and is now read directly:

1. **Repo overlay** — a committed `.saga/tier-defaults.json` (`{"<work-shape>": {"model", "effort"}}`)
   pins repo-tuned defaults. `staffing.load_overlay(root)` returns them. Missing file → clean registry
   fallback; malformed (bad JSON, unknown shape, off-palette or unrunnable tier) → `StaffingError`, halt
   and surface (never degrade silently).
2. **Issue band** — when the driving issue carries a `### Recommended Tier Band` section
   (auto-stamped by `mission-control:issue` at creation), parse it with `parse_tier_band(body)` and
   pass it to `resolve_tier_for_plan(work_shape, issue_band=band)`. The band seeds the proposed tier
   only where no repo override exists; an absent band is normal (`None`), a present-but-invalid one
   fails loud.
3. **Write-back** — when the operator confirms a tier override in the Step 1 table, persist it with
   `write_tier_default(work_shape, model, effort)` so the next `/plan` proposes the accreted
   preference. Read-merge-write: never clobbers other keys. The file is **tracked** — commit the
   dirtied overlay with the run's changes (the repo accretes tier judgment). Every persisted override
   originates from an explicit operator confirmation; never auto-promote silently.

<!-- BEGIN GENERATED EFFORT HONORING NOTE -->
<!-- Source: plugins/saga/references/plan-save-contract.yaml; renderer: plugins/saga/scripts/plan_save_contract.py.
Do not hand-edit; guard: tests/test_saga_spec_consumer_row.py::test_plan_docs_generated_regions_match_contract. -->
<!--
The honoring seam is `fleet_commons.effort_rider.inject_effort(prompt, effort, spawn_kind)`.
For `external-engine`, `workflow`: effort already rides on real controls; injecting a rider would double-count it.
For `agent`: prepend an `EFFORT_RIDER` directive: a labeled proxy because the Agent tool has no per-call effort parameter.
See `plugins/fleet-core/references/staffing.md`.
The proposed tier cell is `<model>/<effort>`: use `tier_resolver.resolve(...).model`
and `tier_resolver.resolve(...).effort` verbatim so dispatch receives both resolved values.
Team Execution A7 uses the same pair and splits on `/`; its older note is tracked by #993.
-->
<!-- END GENERATED EFFORT HONORING NOTE -->

For a unit carrying `engine`/`capability` (U12 chaperone-worker units), the recommendation row also
carries the unit's `intent` and a **plan-time resolution preview**: for a capability-routed unit, call
`engine_resolver.resolve({"role_kind": "worker", "capability": <value>}, mode="advisory", registry=…)`
(`mode="advisory"` — R7 — since this is a non-binding preview, not the run-time dispatch) and surface
"resolves today to `<engine_id>/<variant>`" alongside the tier row; an explicit-engine unit has no
preview to show (naming the engine already fixes it — R26 halts rather than substitutes if it becomes
unavailable). This preview is the baseline the chaperone's `substituted-engine` disposition compares
the run-time resolution against (KTD4; the external-engine worker contract lived in the
team-execution plugin, which issue #1030 archived) — record it in the saga tick / emitted plan
alongside the tier so it survives to `/work`.

### 5.3 Write the saga tick

Emit a **runnable** saga `save` command — never prose like "write a saga", and never `git add` the
tick (saga state is git-ignored, machine-local). Use the real flags:

<!-- BEGIN GENERATED PLAN SAVE EXAMPLES: default -->
<!-- Source: plugins/saga/references/plan-save-contract.yaml; renderer: plugins/saga/scripts/plan_save_contract.py.
Do not hand-edit; guard: tests/test_saga_spec_consumer_row.py::test_plan_docs_generated_regions_match_contract. -->
**Example: default**

```bash
python3 plugins/saga/scripts/saga.py save \
  --kind '<issue|task>' \
  --id '<issue-number-or-task-slug>' \
  --lifecycle-phase plan \
  --phase-status complete \
  --plan-path 'docs/plans/YYYY-MM-DD-<topic>-plan.md' \
  --destination '<plan-only|pr|merge|nonprod-deploy>' \
  --adr-refs 'ADR-NNNN|ADR-MMMM' \
  --decisions 'KTD1: rationale. KTD2: rationale.' \
  --orchestration-mode '<inline>' \
  --orchestration-recommended '<inline>'
```

- `--deploy-autonomy '<gate|auto>'` only when `--destination nonprod-deploy`.
<!-- END GENERATED PLAN SAVE EXAMPLES: default -->

**For `cc-workflows-ultracode`:** also pass `--orchestration-ref` pointing at the **spec JSON** (the
canonical artifact, per KTD1/KD3 — regenerable, so the ref is the spec not the `.workflow.js`):

<!-- BEGIN GENERATED PLAN SAVE EXAMPLES: workflow -->
<!-- Source: plugins/saga/references/plan-save-contract.yaml; renderer: plugins/saga/scripts/plan_save_contract.py.
Do not hand-edit; guard: tests/test_saga_spec_consumer_row.py::test_plan_docs_generated_regions_match_contract. -->

<!-- END GENERATED PLAN SAVE EXAMPLES: workflow -->

The `.workflow.js` is regenerable at any time from the spec (`execution_spec.py emit`); the spec JSON is
the durable canonical artifact. `orchestration_ref` is the repo-relative path to the spec JSON, so
`/work` can re-emit fresh without any prose-parsing.

Also pass `--orchestration-recommended <the backend the recommender suggested>` so the tick records
recommended-vs-chosen on this decision (R12 override-rate telemetry); `orchestration_operator_choice`
auto-derives from `--orchestration-mode`, so the only added burden is naming the recommendation.

`--id` is the only strictly required flag (`--kind` defaults to `issue`); for ad-hoc work pass
`--kind task --id <slug>`. The flags in the save examples above and the `/plan` consumer row
in `references/saga-spec.md` §11 are rendered from the same `references/plan-save-contract.yaml`
contract. The [maintainer runbook](../../references/plan-save-contract.md) documents editing,
the runnable recommender call, and recovery from a failed render.
`--phase-status complete` is what the chain
dispatch table routes on: a finished plan goes onward to `/doc-review`, and omitting it leaves the
tick at the `pending` default, which routes the already-finished plan right back into `/plan`.
When resuming (Phase 0.3 matched), this appends a tick to the existing saga directory rather than
minting a new one.

**Check the save's exit status.** A non-zero exit means the save failed, and the error message
names which write did. If the tick envelope was never written and the full tick chain contains no
reference to the same normalized plan path, the plan document named in the error is on disk with
no saga state referencing it, so `/work` cannot see it; when any earlier tick already
records the plan path, the document is tracked and only this save's tick is missing. If the envelope
landed but the `state.json` index rewrite failed, the tick IS tracked — `restore` reads the envelope
directly —
and re-running the same save once the write failure is cleared rebuilds the index and appends one
additional tick carrying the same state (harmless to `restore`, visible to `saga.py ticks`).
Either way, STOP and surface the error to the operator — do not continue to Phase 5.4 on a
failed save.

### 5.4 Dispatch the plan review, and loop until it passes

<!-- gate-record: id=plan-review-floor absence=HALT transport=ask-user-question -->

**`/plan` does not recommend the review; it runs it.** The plan is not finished when the document
is written — it is finished when a Plan Reviewer has read it and nothing above `P2` is open, or the
operator has said one word to go past a finding that is. An operator who has to remember to type
`/doc-review` is the transport for a gate, and a gate with a human transport is a gate that gets
skipped on the busy days it matters most.

**Who reviews, decided from the run record and not from this session.** Read the run record at
`<primary checkout>/.claude/saga/runs/issue-<N>.json` and take the first of these that holds:

1. Its `roster` array already carries a live row whose role is `plan-reviewer` — dispatch to that
   pane.
2. Its `run_configuration.staffing_models_and_efforts` names `plan-reviewer`, and
   agent-launcher's roster helper can run here — stand the pane up and dispatch to it:

   ```bash
   R=$(ls -d ~/.claude/plugins/cache/*/agent-launcher/*/skills/agent-launcher/scripts/roster.py \
       | sort -V | tail -1)
   python3 "$R" up   --issue <N>
   python3 "$R" wait --issue <N> --timeout 600000
   ```

   The helper writes the pane into the record's `roster` array, briefs it from
   `plugins/agent-launcher/roles/plan-reviewer.md` by absolute path, and `down` later closes only
   what that array names. It refuses outside a herdr pane with **exit 4** — the ordinary case for a
   background driver, which falls through to option 3 — and reports a blocked role with **exit 5**,
   which is reported, never answered.
3. Otherwise, review in **this session in review-only mode**: run `/doc-review` against the plan
   path yourself, applying the same rubric, and say in one line that no reviewer pane existed.

Say which of the three happened and why. The choice is read from the record rather than probed
from the environment because the same run continues in other sessions and on other machines, and a
rule that reads the environment answers differently in each of them.

**The loop is the repair protocol.** Dispatch, read the result, repair the plan document, dispatch
again — recording **one entry per turn** in the record's `review_cycles` (its cycle number, its
result, and where its findings are). Exit on one of exactly three conditions:

- **Pass.** No `P0` and no `P1` remains. Continue to §5.5.
- **The operator's word.** A `P0` or `P1` is open and the operator overrides it in one word, with
  a rationale recorded alongside the finding. This is the **only** override. No finding count, no
  cycle count, no unattended mode, and no sentence in this skill produces one on its own.
- **Exhausted allowances.** The record's `standard_cycle_allowance` and
  `escalated_cycle_allowance` bound the loop (a cycle is one completed review result followed by
  one repair batch; a re-dispatch after no repair is not a cycle). Exhausting them **stops and
  reports** — it never passes. The numbers live in the record, not here, so a run can lower them
  without editing this skill.

A finding the reviewer raises against a revision you have since changed is not answered by the
change alone: re-dispatch so the verdict is bound to the revision that will be built.

### 5.5 Submit the card's move to `Planning` / `Ready for Active` — Mission Control executes it

**Actor:** this skill. **Trigger:** §5.4's review loop recorded a **pass**, or the operator's
one-word override, so the card is no longer being designed -- it is ready to build. The trigger is
observable here and nowhere earlier: before §5.4 runs there is no review result to read, which is
why this move sits after the loop rather than at the head of the phase. **Move:** the live pair `Stage` =
`Planning`, `Status` = `Ready for Active`. `Ready for Active` is the schema's own named terminal
option for the Planning stage; there is no bare `Ready` option on either live field.

**Deciding and submitting is not writing.** As in Phase 0.6, this skill submits the move and
Mission Control executes it, derived from what this skill durably produced: the plan document, the
saga tick, and the review cycles in the run record.

```bash
python3 plugins/saga/scripts/reconcile_controller.py reconcile \
  --op set-field-status --repo <owner/repo> --number <N> \
  --target-state "Ready for Active" \
  --payload '{"assignments": [["Stage", "Planning"], ["Status", "Ready for Active"]]}'
```

**Submit both halves, and check both** — the pair is not rolled back if one half fails, so a
`failed` record naming the landed and the unlanded assignment is the signal to repair the half that
did not land. Check the record's `field` reads `Stage+Status` before reporting the move: a
`written` from a saga too old to carry the pair names a bare `Status` and moved one field.
`halt`/`gated` falls back to the operator-prompted Mission Control path. When there is no issue,
there is no card to move; say nothing further.

### 5.6 Continue into `/work`

**`/plan` does not recommend the build; it starts it.** The review has run and the card has moved,
so there is nothing left for the operator to decide before the work begins — every decision the
build needs was taken at admission and written into the run record. An operator who has to remember
to type `/work` is the transport between two steps that already agree with each other (issue
#1029).

**Read the destination from the run record, not from this session.** Take
`admission.destination` at `<primary checkout>/.claude/saga/runs/issue-<N>.json`:

- **`plan-only`** — stop here. Report the plan path, the review result, and the board move, and say
  the destination stopped the run. Do not enter `/work`.
- **`pr`, `merge`, `nonprod-deploy`** — run `/work` against the plan path in this same turn, and
  say in one line that you are doing so and which destination authorized it.

When §5.4 exited on exhausted allowances rather than a pass, **stop and report** — that exit never
passes, so it never continues either.

**Continuation changes what happens automatically; it changes nothing about what is confirmed.**
`/work`'s pull-request open, review-request, and merge stay explicitly operator-confirmed exactly
as they are today. A continuation that would fire one of those without a confirmation is a stop,
not a shortcut.

Two exits remain the operator's to take, and neither is automatic: `mission-control` hands the plan to an
SDLC issue through `mission-control`, and `/brainstorm` steps back when the review found the WHAT
was not actually settled. Name them in one line; do not run them.

### 5.7 Hard boundary

`/plan` authors a plan artifact, has it reviewed, repairs it, and starts the build by entering
`/work`. It does **NOT** implement code itself — `/work` owns that, and every boundary `/work`
declares stays `/work`'s. It does **NOT** file SDLC issues (`mission-control` owns issue creation).
Plan, write the saga, run the review to a verdict, then continue into `/work` or stop on a
`plan-only` destination.
