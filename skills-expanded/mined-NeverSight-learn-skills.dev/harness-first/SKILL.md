---
name: harness-first
description: >-
  This skill should be used at the very start of a new (greenfield) project,
  before writing feature code or prompts, to build a self-verifying execution
  harness through five gated phases (reality model → boundaries → minimum runnable
  link → eval-first → Maker-Checker loop), each producing a concrete file. Trigger
  it when the user says things like "I'm starting a new project", "let's build an
  app that does X", "kick off a new agent/LLM app", "spin up a new backend/CMS/
  automation", "architect this from scratch", "should this be multi-agent or one
  call?", or "bootstrap this repo". It applies to any project type — not only AI
  ones. Use it even when the user only says "let's build X" without mentioning
  architecture or eval, because the right first move in any new project is building
  the harness, not the prompt or the code. Do not use it for changes to an existing
  codebase (a bug fix, one feature, a refactor, a review) — kickoff only.
version: 0.1.0
---

# Harness-First Project Bootstrap

The first move in a new project is **not** writing code or a prompt. It is
building a *harness*: an environment where work can be executed, observed, and
verified, so failure becomes a signal instead of a guess. This skill drives that
build through five gated phases. The agent's job here is to act as a **system
architect**, not a code generator — define the goal and the reality, then let
execution + feedback converge on it.

The core discipline (apply it everywhere below):

- **Reality before prompt.** Model how the task really happens before designing how a machine imitates it. A wrong reality model dooms every later prompt.
- **Constraints into mechanism, experience into context.** Anything that *must* hold goes into code / hooks / schema / validator / tests. Soft, inheritable knowledge goes into a config doc the agent reads. A model *seeing* a rule is not the system *enforcing* it.
- **Complexity must be earned by failure.** Every extra component (a sub-agent, a tool, a memory layer, a service) must point to one concrete failure that proves it is needed. Adding components from imagination is architectural overfitting.
- **The prompt is an output, not an input.** Build the minimum system first; let real failures tell you what the prompt and architecture should become.

## When to use / when not to use

Use it for **project kickoff** — the moment a new thing is being started:

- "I want to build an app that turns customer interviews into research reports — where do I start?"
- "Starting a new internal tool this week, it's basically a CMS for our product manuals."
- "Should this new assistant be one LLM call or a multi-agent thing?" → start here; the answer is grown from failure evidence, not guessed.

Do **not** use it for ongoing work on an existing codebase — these need a
different tool or just direct action:

- "Fix this null-pointer in the checkout flow." → bug fix, not a kickoff.
- "Add a CSV export button to the existing dashboard." → single feature.
- "Review this PR / refactor this module." → not greenfield.

If unsure whether a project is greenfield, ask once; do not run the five phases
on a mature codebase.

## How to run this skill

Run the five phases **in order**. Each phase produces one **deliverable file**
and ends at a **gate**. Do not enter the next phase until the gate passes — if it
fails, stay and fix the deliverable. Calibrate depth to project size: a weekend
script can spend two sentences per phase; a multi-month system deserves a full
page. Never skip a gate, even on small projects — a skipped gate is how a project
starts drifting on day one.

Copy this tracker into the working chat and keep it updated:

```
Harness-First Progress:
- [ ] Phase 0 — Reality model      → docs/reality.md          (Gate 1)
- [ ] Phase 1 — Boundaries         → docs/reality.md (table)  (Gate 2)
- [ ] Phase 2 — Minimum link       → runnable skeleton + CI   (Gate 3)
- [ ] Phase 3 — Eval first         → eval/cases.md            (Gate 4)
- [ ] Phase 4 — Maker-Checker loop → tests/checks wired in    (running)
```

Templates for every deliverable live in `references/templates.md` — read it when
you reach Phase 0 and copy the relevant block. Detailed gate criteria live in
`references/decision-gates.md` — read it when a gate's pass/fail is unclear. The
methodology and its rationale live in `references/methodology.md` — read it only
if the user wants the "why".

---

## Phase 0 — Reality model

**Action.** Resist writing any code or prompt. Reconstruct how this task happens
in the real world *today*. Interview the user (or reason from context) to fill
the reality template: who does it, the input, the intermediate judgment points,
the deliverable, where it usually fails, and which steps are deterministic
(machine/code/API) versus fuzzy (need a judgment call / LLM).

**Deliverable.** `docs/reality.md`, using the Reality block in
`references/templates.md`.

**🚪 Gate 1 — Reality confirmed?**
- Are deterministic steps identified, not just fuzzy ones? If *every* step reads as "the model decides," the task is under-decomposed — break it down further before continuing.
- Is the failure-prone step named explicitly? An unnamed failure mode cannot be designed against.

> Why this is first: most long-chain projects fail not because the prompt was weak but because the *reality abstraction* was wrong (a task assumed to be "one summary" is actually "multi-round evidence-gathering + judgment"). Get this wrong and no later polish recovers it.

## Phase 1 — Boundaries

**Action.** For every step in the reality model, assign an owner: `code`,
`llm`, `tool`, or `human`. This is where you decide what the machine does, what
the model decides, what an external tool provides, and where a human must stay in
the loop.

**Deliverable.** A boundary table appended to `docs/reality.md` (template in
`references/templates.md`).

**🚪 Gate 2 — Boundaries safe?**
- Does any step sit in a high-failure zone with *no* `human` checkpoint and *no* deterministic `code`/`tool` guard? That is a time bomb — add a guard or a checkpoint.
- Are the must-hold constraints routed to *mechanism* (code/schema/validator/test), not left as prose hopes in a future prompt?
- If the agent inherits any persistent memory/context across runs: does it have an **invalidation rule** (when a stored note expires or gets re-validated)? Append-only memory with no expiry compounds yesterday's error into every future run. N/A if no persistent memory yet.

## Phase 2 — Minimum runnable link

**Action.** Stand up the smallest skeleton that runs end-to-end along the *single
main path* — and nothing else. One route, one happy path, one CI/compile/test
command that goes green. Explicitly defer auth, payments, admin, analytics,
marketing, dashboards, multi-agent orchestration, large retrieval, complex memory.

**Deliverable.** A running skeleton + one passing CI/build/test command. The
skeleton is your *instrument*, not your product.

**🚪 Gate 3 — No earned-by-failure violations?**
- For each component already added, can you state one concrete failure that would occur without it? If not, remove it (architectural overfitting).
- Does the skeleton actually run and can it be observed (logs / test output / state you can inspect)? If you cannot watch it fail, you cannot iterate on it.

> Why minimal: the simpler the system, the faster it exposes the real defect — wrong reality model, wrong I/O contract, a missing constraint, a tool that cannot supply ground truth. Complexity hides the cause.

## Phase 3 — Eval first

**Action.** Before writing bulk feature code, define how you will *know* it works.
Write the success criteria, the failure criteria, and what to record on failure.
For an agentic system, evaluate the trajectory (did it reach the goal, how many
steps, were tool calls sane, did it damage existing behavior), not only the final
answer.

**Deliverable.** `eval/cases.md` with concrete cases (template in
`references/templates.md`).

**🚪 Gate 4 — Failure reproducible?**
- Can a failure be reproduced on demand? A non-reproducible eval is no eval.
- Are the eval cases isolated from the prompt/memory so they cannot be silently "memorized" (leakage)? Beware local-pass / production-fail skew — favor cases that mirror the real environment.
- Does each case have a **cost/latency budget**, with breaches recorded as a failing signal? Long-chain agents usually die from cost before they die from wrongness. Rough numbers ("≤ $0.05 / ≤ 30s") are fine; what matters is the number exists and overspends are visible, not silently absorbed.

## Phase 4 — Maker-Checker loop

**Action.** Only now hand execution to a coding agent (Claude Code / Cursor /
Codex / Composer). Mount a **Maker-Checker** loop and keep it running:
- **Maker:** the agent makes the change.
- **Checker:** the agent *must* run tests / lint / type-check / the validation script before claiming success, reads the failure output, and adjusts the next attempt from that ground truth.

Your role shifts from coder to harness-tuner. When the agent fails repeatedly,
do **not** blame the model — fix the harness: stale docs, an unclear constraint
in the config, a wrong Checker standard, a tool that cannot return ground truth.
Each new component you add (sub-agent, tool, memory layer, workflow branch) must
still earn its place via a real failure — the Phase 2 rule never expires.

**When the same failure persists across 2–3 retries, stop and run the attribution
triage before touching the harness again.** A retry that does not first ask
"is this my harness or the agent this round?" is how you waste a day tuning the
wrong thing. Walk this list top-down — the first row that fits is the most likely
root cause, fix that one thing, then resume:

| Signal you are seeing | Likely root cause | Fix *this*, not the model |
|-----------------------|-------------------|---------------------------|
| Failure message is concrete and stable across retries (same error, same place) | **Harness** — I/O contract, schema, test, or tool return is wrong | Fix the contract / test / tool; do not retry the agent |
| Failure drifts each retry (different error, different step) | **Agent variance** — not yet converged | Re-run once or twice; if it still drifts, tighten the task spec or shrink the step |
| Agent "succeeds" but the Checker catches nothing, or there is no Checker | **Harness** — missing ground truth | Add / fix the Checker before any more Maker runs |
| Agent keeps hitting a step that has no deterministic guard | **Harness** — under-decomposed (Gate 1/2 debt) | Go back and split the step; do not paper over it in prompt |
| Only this one case fails; siblings pass | Could be either — re-run that case 2× first | If it reproduces: harness. If it flaps: agent variance; add to eval as a flake case |

This triage is a **diagnostic, not a gate** — it never blocks progress on its own.
It exists so that when you *do* stop, you stop for the right reason.

When a workflow stabilizes and repeats across projects, capture it as a skill using
`../skill-authoring/` — apply the craft layer while drafting, then hand off to
skill-creator for eval and packaging.

**Deliverable.** Tests/checks wired so every change is verified by machine, not
by hope. From here the system iterates: failures feed the next prompt, workflow,
or architecture change, converging on the goal.

> Workflow shapes (routing, parallelization, orchestrator-workers,
> evaluator-optimizer) are grown *from failure evidence*, never designed up front.
> See `references/methodology.md` if you need to pick one.

---

## Worked example & contrast pairs

One worked Input → Output for Phase 0, then the two mistakes a model most often
makes. Study the contrasts — they mark the exact line where this skill is misread.

**Input** (a one-line brief the user might give):
> "I want to build a thing that takes a customer support email and drafts a reply."

**Output** (the Phase 0 decomposition that should result — not "send email to LLM, get reply"):

```
1. receive + parse email           → deterministic (code)
2. classify intent / urgency       → fuzzy (llm)
3. look up account + order history → deterministic (tool)
4. decide if policy allows action  → fuzzy (llm) + human checkpoint (refunds)
5. draft reply                     → fuzzy (llm)
6. validate reply against policy   → deterministic (code/validator)
7. send                            → deterministic (code), human-approved first
Failure-prone step: #4 (model promises something policy forbids).
```

**Contrast 1 — decompose the reality (Phase 0 / Gate 1):**
- Correct: the 7-step mix above, with deterministic steps separated from fuzzy ones.
- Incorrect: "1. email in → LLM → reply out." Everything is one fuzzy step.
- Rationale: a single fuzzy blob hides the deterministic guards (lookup, policy validation, human approval) that are exactly where reliability comes from. Under-decomposition fails Gate 1.

**Contrast 2 — earn complexity by failure (meta-gate / Gate 3):**
- Correct: ship the single chain first; add a routing layer *after* observing that support and sales emails need different handling.
- Incorrect: design a multi-agent orchestrator with a router, a memory store, and three sub-agents on day one because the domain "feels complex."
- Rationale: every component must trace to an observed failure. Architecture built from imagination is overfitting — it adds surfaces to debug before any evidence says they are needed.

## Pre-flight checklist (every new project)

- [ ] `docs/reality.md` exists; deterministic vs fuzzy steps separated; failure zone named (Gate 1).
- [ ] Boundary table assigns `code`/`llm`/`tool`/`human` to every step; no unguarded high-failure step (Gate 2).
- [ ] Must-hold constraints live in mechanism (code/schema/validator/test), not prompt prose.
- [ ] Persistent memory (if any) has an invalidation rule; no append-only context poison (Gate 2).
- [ ] Minimum link runs end-to-end with one green check; no unearned components (Gate 3).
- [ ] `eval/cases.md` defines success, failure, and what to record; failures reproducible; no leakage; each case has a cost/latency budget with breaches recorded (Gate 4).
- [ ] Maker-Checker loop wired before bulk feature work begins; attribution triage used when a failure persists 2–3 retries (Phase 4).
