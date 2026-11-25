---
name: founder-review
description: CEO/founder-mode scope and ambition review. Rethink the problem, find the 10x product, challenge premises, expand or cut scope deliberately — across four committed modes (SCOPE EXPANSION, SELECTIVE EXPANSION, HOLD SCOPE, SCOPE REDUCTION). Fires upstream of execution on a /plan artifact, STRATEGY.md, /brainstorm output, or an ad-hoc scope question; produces a scope decision and routes deep rigor back to /doc-review and /code-review in a closed loop. Triggers on "think bigger", "expand scope", "is this ambitious enough", "rethink this", "scope review", or a /ceo-review invocation. Does not implement, record strategy, file issues, or change code.
---

# Founder Review

`/founder-review` (alias `/ceo-review`) answers **"Is this the right, ambitious-enough thing to build
at all?"** It is the **scope / ambition / direction** review **lens** — the third member of the review
trio:

- **`/doc-review`** = *readiness* ("can this plan safely drive implementation?")
- **`/code-review`** = *code* ("is the built code safe to merge?")
- **`/founder-review`** = *scope & ambition* ("is this the right, ambitious-enough thing, and is the
  scope shaped correctly?")

Unlike its two siblings, it fires **upstream of execution** — on a `/plan` artifact, a `STRATEGY.md`,
a `/brainstorm` output, or an ad-hoc scope question — and its output is a **scope decision**, not a
readiness/code review artifact. It **challenges** direction; `/strategy` **records** it; `/plan`
**re-plans** accepted scope; and it hands any (re-)expanded plan **back** to `/doc-review` and
`/code-review` for depth — a real closed loop, not a hand-wave.

## Position in the lifecycle

`/founder-review` runs **before** the work thread, so it is **not** a saga consumer and **never
writes the saga** (no `saga.py` call, no `--review-paths`). Cross-session persistence is the
`docs/founder-reviews/` scope-decision artifact plus the engineering-journal ADR.

- `/office-hours` answers: "What should we even build?" (framing)
- `/brainstorm` answers: "What are the requirements and candidate approaches?" (the WHAT)
- **`/founder-review` answers: "Is this scope right and ambitious enough?"** (this engine)
- `/plan` answers: "How should it be built?" (the HOW)
- the `review` phase (`/doc-review`) answers: "Is this plan ready to execute?"
- `/work` -> `/code-review` -> `/qa` answer: "Build it, is it safe to merge, does it actually work?"

### founder-review vs doc-review (the boundary)

Both engines can target a `STRATEGY.md` or scope document (`/doc-review`'s path tie-breaker maps
`STRATEGY.md -> strategy/scope`). They are **complementary lenses, not a collision**:

- **`/founder-review` = the ambition lens** — *challenge the direction*: is it ambitious? coherent?
  worth doing? is the scope shaped right?
- **`/doc-review` = the readiness lens** — *check execution-readiness*: can this drive implementation
  without inventing missing decisions?

`/doc-review` already cross-suggests `/founder-review` "when strategy, product scope, ambition, or
user-facing behavior is prominent" — that is the **inbound** edge. `/founder-review` closes the loop
**outbound** by writing/updating the (re-)expanded plan and handing it back with the path. No
`/doc-review` edit is needed.

## Core principles

1. **Review, not implement.** `/founder-review` challenges scope/ambition/direction and captures
   decisions. It does **NOT** make code changes, does **NOT** start implementation, does **NOT**
   commit, does **NOT** push, does **NOT** open PRs, and does **NOT** file SDLC issues. Its only
   writes are the `docs/founder-reviews/` artifact and (downstream, separately) the journal. ZERO
   writes to reviewed code.
2. **User 100% in control.** Every scope change is an explicit opt-in through the native
   operator-choice contract, or inline in a channel. Never silently add or remove scope. Once a mode
   is chosen, **commit to it —
   no silent drift.** Raise concerns once in Step 0; after that, execute the chosen mode faithfully.
3. **Internalize the CEO patterns, don't enumerate them.** The 18 CEO cognitive patterns and 9 Prime
   Directives (`references/ceo-cognition.md`) are thinking instincts that shape the whole review, not
   a checklist to read aloud. They turn a vibe into a named, concrete scope finding.
4. **Ground before challenging.** Run the adapted pre-review system audit and the premise challenge
   first — a grounded critique, not opinion. Apply the **no-false-precision** posture: when you cite a
   number (effort, file count, scope size) present it and let the operator judge; use **no hardcoded
   "too big / too small" thresholds** (the `>15-files -> Reduction` line is a suggestion the operator
   can override, not a verdict). Stolen sharpened from CE `product-pulse`.
5. **Challenge direction, don't record it.** `/strategy` records the chosen direction;
   `/founder-review` challenges whether it is ambitious, coherent, and worth doing. On a `STRATEGY.md`
   target, `/founder-review` is the *ambition* lens and `/doc-review` the *readiness* lens —
   complementary, not duplicative.
6. **Agent-actionable + closed-loop.** Accepted scope -> `/plan` (re-plan). The (re-)expanded plan is
   written/updated and handed **back** to `/doc-review` (readiness) and `/code-review` (code) **with
   the artifact path** — so the deep rigor that gstack bundled into 11 sections actually runs, just in
   the right engine. Direction shifts -> `/strategy` (record). Nothing is left as vague intention.

## Interaction method

Follow `../../references/operator-choice.md` for choices from a known set (mode selection,
per-expansion opt-in, the chosen implementation approach, execution backend). Ask one issue per
question—never batch multiple decisions into one. Never silently skip a question or silently default.

In a channel session (`redis-channel` active), inline the choices in your reply text instead, and use
the **digest** path for expansions (see Phase 2 and
`references/review-modes.md`). Follow the canonical channel-inline convention in
`saga/skills/brainstorm/SKILL.md` (do not duplicate its wording here).

Use repo-relative paths in every generated document. Absolute paths break portability across machines
and worktrees.

---

## Phase 0 — Enter, detect target type, system audit

Capture the target AND **classify its type** — this drives the conditional ceremonies in Phase 1:

- **plan** — a `/plan` artifact under `docs/plans/` (run the full faithful gstack Step 0).
- **strategy** — `STRATEGY.md` or a strategy/scope document.
- **brainstorm** — a `/brainstorm` output under `docs/brainstorms/`.
- **scope-question** — an ad-hoc "is this ambitious enough?" with no artifact yet.

If the target is ambiguous, ask before reviewing.

Then run the **adapted pre-review system audit** (full procedure in `references/review-modes.md`):
git log/diff/stash + recently-touched files + TODO/FIXME scan; read the target + `docs/office-hours/`
notes + root `STRATEGY.md` + `docs/engineering-journal/` (DECISIONS/QUEUED) + `AGENTS.md`; then the
four lenses — retrospective check, frontend/UI scope detection (`DESIGN_SCOPE`), taste calibration
(EXPANSION + SELECTIVE only), and the landscape `WebSearch` (skip gracefully if unavailable: "Search
unavailable — proceeding with in-distribution knowledge only"). Report audit findings before Step 0.

---

## Phase 1 — Scope challenge & mode selection (Step 0)

Run Step 0 (sub-steps detailed in `references/review-modes.md`):

- **0A. Premise challenge** — right problem? actual outcome vs proxy? do-nothing cost? **+
  office-hours escape:** if the session is vague/unframed (can't articulate the problem, keeps
  changing it, "I'm not sure", clearly exploring), offer to run `/office-hours` now and resume after
  (re-read `docs/office-hours/` notes on return). A prose offer, not guilt.
- **0B. Existing-code leverage** — what already solves each sub-problem? Is this rebuilding something
  better refactored?
- **0C. Dream-state mapping** — current -> this plan -> 12-month ideal; moving toward or away?
- **0C-bis. Implementation alternatives — TARGET-CONDITIONAL.** target=plan -> produce 2-3 distinct
  approaches (one minimal-viable, one ideal-architecture, **equal weight**) + a recommendation, and
  get explicit approval before mode selection. target=strategy/brainstorm/scope-question -> **skip**,
  or downgrade to "strategic options" (channel -> single recommended-approach confirm).
- **0E. Temporal interrogation — TARGET-CONDITIONAL.** target=plan -> the HOUR-by-HOUR implementation
  interrogation (present human + CC effort scales; no false precision). Else -> **recast** as "what
  must be resolved before this becomes a plan?"
- **0F. Mode selection** — present the four modes through the native operator-choice contract
  (channel -> inline) with a
  context-default recommendation; state **"options differ in kind, not coverage — no completeness
  score"**; once selected, **commit, no silent drift.**

---

## Phase 2 — Mode-specific scope analysis

Run the branch for the committed mode (full ceremonies in `references/review-modes.md`):

- **SCOPE EXPANSION** — 10x check + platonic ideal + delight opportunities, then the **opt-in
  ceremony**: each expansion as its own native operator choice, recommended *enthusiastically*, framed
  **FLAT -> EXPANSIVE** (lead with the felt experience, close with effort + impact). Options:
  **A) add / B) defer (-> journal/QUEUED) / C) skip**.
- **SELECTIVE EXPANSION** — run the HOLD analysis (complexity + minimum-change) as the bulletproof
  baseline, then the expansion scan, then the **cherry-pick ceremony** (same A/B/C, **neutral**
  posture).
- **HOLD SCOPE** — complexity check + minimum-change rigor. Do not silently expand or reduce.
- **SCOPE REDUCTION** — ruthless cut to the minimum that ships value; split the rest into follow-ups.

**Cap the ceremony:** if more than 8 candidates, present the **top 5-6** and note the remainder.
**Channel session:** present a **digest** ("5 opportunities — one-at-a-time, or recommend the top
2?") — never 5 serial inlined blocks. Accepted items join scope for the rest of the review; rejected
go to "NOT in scope".

---

## Phase 3 — Founder rigor pass (directives + patterns -> concrete findings)

Apply the 9 Prime Directives and 18 CEO patterns (`references/ceo-cognition.md`) at the
**scope/direction layer**, producing **named, concrete scope-level findings** — not vibes:

- zero-silent-failures-as-scope, every-error-has-a-name, data-flows-have-shadow-paths,
  observability-is-scope, optimize-for-the-6-month-future, inversion reflex, focus-as-subtraction,
  proxy skepticism, scrap-it permission, design-for-trust (when `DESIGN_SCOPE`), …

Each finding is concrete (e.g., "this accepted expansion adds a data flow with no named error path —
resolve before `/doc-review`"), then the **ambition / coherence / worth-it verdict**.

**Route deep rigor in a CLOSED LOOP — do NOT reproduce gstack's 11 review sections.** The deep
section-by-section rigor (Architecture, Error-&-Rescue map, Security, Data-flow, Code-quality, Test,
Performance, Observability, Deployment, Long-Term Trajectory, Design & UX) is the **readiness** and
**code** lenses' job. After scope is decided, **write/update the (re-)expanded plan artifact** and
name the **concrete handback**: "run `/doc-review docs/plans/<file>` for readiness depth; `/code-review`
once built." Without writing the artifact and naming its path, expanding scope then "recommending
`/doc-review`" silently drops the rigor — the closed loop is what prevents that.

---

## Phase 4 — Synthesize the scope-decision artifact

Write `docs/founder-reviews/YYYY-MM-DD-<topic>-founder-review.md` — its **own** scope-decision
directory (**NOT** `docs/reviews/` = readiness, **NOT** `docs/code-reviews/` = code, and deliberately
**not** a `/handoff` artifact source). Format (full template in `references/review-modes.md`):

- **Frontmatter** — `status`, `type: founder-review`, `date`, `origin` (the target path/identity).
- **Mode** + target (type + path).
- **Vision** (EXPANSION + SELECTIVE only) — 10x check + platonic ideal.
- **Scope Decisions** table — `# | Proposal | Effort | Decision (ACCEPTED/DEFERRED/SKIPPED) |
  Reasoning`.
- **Accepted Scope** — now in this plan.
- **Deferred** — routed to the engineering journal / QUEUED with enough context to pick up cold (never
  a stray `TODOS.md` — vague intentions are lies).
- **Premise findings** — the concrete 0A/0B/0C findings.
- **Founder verdict** — **ship / sharpen / scrap-and-rethink** + the concrete next-command handback
  (the expanded-plan path -> `/doc-review`).

---

## Phase 5 — Route + operator-choice

**Closed-loop route:**

- Accepted scope -> **`/plan`** (re-plan). Write/update the (re-)expanded plan.
- The (re-)expanded plan -> **`/doc-review docs/plans/<file>`** (readiness depth) **with the path**,
  and **`/code-review`** (code) once built. This is the closed loop — name the path, don't just say
  "run /doc-review".
- Direction shifts -> **`/strategy`** (record the chosen direction).

**Operator-choice.** On a scope-expansion or scrap-and-rethink verdict, **OFFER** routing the accepted
changes through an execution backend per `../../references/operator-choice.md` (the plugin-root
decision contract). There are exactly three active Codex workflow modes — `inline | manual | verified-workflow`.
Read the work shape, recommend the cheapest-correct backend and pre-select it,
but surface the alternatives so escalation is one step. Use `manual` when automation is unsafe or
unavailable. Never offer source-only workflow backends in Codex. The offer is never auto-run.

**No saga write.** `/founder-review` runs upstream of the work thread and does **not** touch the saga
— no `saga.py` invocation, no `--review-paths`. Persistence is the `docs/founder-reviews/` artifact +
the journal ADR.

**Hard boundary.** `/founder-review` challenges, captures, and routes. It does **NOT** implement,
does **NOT** record strategy (`/strategy` does), does **NOT** file SDLC issues (`mission-control` does),
does **NOT** commit, push, or open PRs, and does **NOT** make code changes. Challenge the scope, write
the scope-decision artifact, route — then stop.

---

## Reference files

- `references/ceo-cognition.md` — the 18 CEO cognitive patterns (internalized, not a checklist) + the
  9 Prime Directives + Engineering Preferences + the founder posture (incl. the sharpened
  no-false-precision steal). "How a founder thinks."
- `references/review-modes.md` — the 4 modes (definitions + context-defaults + commit-no-drift) +
  expansion-framing (FLAT vs EXPANSIVE) + the opt-in/cherry-pick ceremonies (capped + the channel
  digest) + the adapted pre-review system audit + the Step-0 sub-steps with the **target-conditional**
  0C-bis/0E gating + the office-hours escape + the scope-decision artifact format. "How the review
  runs."
