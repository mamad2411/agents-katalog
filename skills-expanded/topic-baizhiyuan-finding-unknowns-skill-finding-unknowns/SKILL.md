---
name: finding-unknowns
description: "Use at the start of an ambiguous or unfamiliar task to surface the user's unknowns (unknown unknowns, unknown knowns) before, during, and after implementation — via blind-spot pass, brainstorm/prototype, interview, references, implementation plan, implementation notes, pitch, and quiz. For high-stakes work, escalate to Cartographer mode — an interactive, per-quadrant ambiguity-scored, quadrant-coverage-gated, regret-weighted protocol backed by a lifecycle-persistent unknowns ledger, ending in a cross-validated, approval-gated execution bridge. Invoke manually when scope is unclear or the domain/codebase is new."
---

# Finding Unknowns

*Distilled from Thariq Shihipar's essay "A Field Guide to Fable: Finding Your Unknowns"*
*(@trq212 — https://x.com/trq212/status/2073100352921215386). Community skill; not affiliated*
*with or endorsed by Anthropic.*

<Purpose>
The map is not the territory. The map is what the user gives you — prompt, context, skills.
The territory is where the work happens — the codebase, the real world, its constraints. The
gap between them is unknowns, and every unknown forces you to guess the user's intent. This
skill converts unknowns into knowns cheaply, before they get expensive to fix: eight
lightweight discovery techniques dispatched by quadrant, four companion agents for the cases
where isolation or independent judgement pays, and Cartographer mode — a coverage-gated,
regret-weighted protocol for high-stakes work that refuses to let implementation start while
the territory is unmapped.
</Purpose>

<Use_When>
- The user is starting work in a new domain or an unfamiliar part of the codebase
- The task involves taste — "I'll know it when I see it" criteria that resist specification
- The task is long-horizon and a wrong early assumption would compound
- A previous attempt came back wrong and the spec, not the execution, is the suspect
- The user says "blindspot pass", "unknown unknowns", "interview me", "brainstorm directions",
  "quiz me", or "Cartographer mode"
</Use_When>

<Do_Not_Use_When>
- The request is specific and trivial (typo, one-liner, obvious bug fix) — execute directly
- The user has a detailed spec with file paths and acceptance criteria — go build it
- The user wants ontology/entity-convergence tracking or OMC-native state/pipeline
  machinery (autopilot/ralph/team handoff) — use `oh-my-claudecode:deep-interview` instead;
  Cartographer covers ambiguity gating and an approval-gated bridge without that runtime
- The user explicitly says "just do it" — respect that; offer one sentence of risk if
  material, then proceed
</Do_Not_Use_When>

<Why_This_Exists>
Model capability is no longer the bottleneck on long-horizon work; clarity is. Generic
requirements gathering asks "what do you want?" — but users cannot answer for the unknowns
they are not aware of. This skill's premise is that different kinds of unknowing need
different instruments: blind spots need reconnaissance, tacit taste needs reaction to
prototypes, nameable gaps need targeted questions, and comprehension needs examination. A
single uniform interview under-serves all four.
</Why_This_Exists>

<Execution_Policy>
- ALWAYS locate the unknown on the quadrant map (Phase 0) before choosing a technique
- Establish the user's starting point — where they are in their thinking, their experience
  with this problem and codebase. The same task needs different probing for an expert than
  for a first-timer
- Discovery ends at understanding. No discovery technique slides into implementation
- Never ask the user a question the territory can answer — explore the codebase first
- Interview via AskUserQuestion (clickable options). Up to 3 *independent* questions per
  round, ordered by blast-radius/regret; never bundle *dependent* questions — where one
  answer would change the next question's framing, ask those one at a time
- Architecture-changing unknowns outrank trivia, always
- "You have no significant unknowns here" is a valid and valuable result — say it plainly
  rather than manufacturing concerns
- Deviations get logged, not buried. Comprehension is the merge gate, not a green diff
- Prefer single-file self-contained HTML artifacts for anything the user must react to or
  review (prototypes, plans, quiz reports); markdown fallback for pure-terminal flows
- Delegate to companion agents when installed and the case is non-trivial; run inline
  otherwise. Every technique works standalone
</Execution_Policy>

<Steps>

## Phase 0: Locate the unknown (blocking prerequisite)

Before any technique, classify where the gap lives and announce the routing:

| | User is aware of it | User is not aware of it |
|---|---|---|
| **User knows it** | **KK — Known Knowns**: in the prompt. Write them down; implicit knowns drift. | **UK — Unknown Knowns**: know-it-when-I-see-it criteria. → Technique 2, 4 |
| **User doesn't know it** | **KU — Known Unknowns**: nameable gaps. → Technique 3, 5 | **UU — Unknown Unknowns**: blind spots. → Technique 1, 8 |

Then choose the lane and say so:

> **Routing:** {quadrant(s) identified} → {technique(s) or Cartographer mode} — {one-line reason}

Lane selection:
- Low/medium stakes, one dominant quadrant → run the matching technique(s) from Phase 1–3
- High stakes (hard to reverse, wide blast radius, unfamiliar territory + long horizon) →
  offer Cartographer mode explicitly; do not silently escalate

## Phase 1: Pre-implementation techniques

### Technique 1 — Blind-spot pass (UU)

Delegate to `blindspot-scout` when a real codebase/domain sweep is involved; inline for
small conversational cases.

1. Establish goal + experience level (inferred conservatively if unstated).
2. Explore the territory first: module, tests, git history, conventions, prior art; for
   external domains, what practitioners consider table stakes.
3. Report in exactly five sections: **Landmines** (typical newcomer mistakes + repo-specific
   potholes, cited), **Hidden context** (constraining decisions and invariants, with
   evidence), **What good looks like** (2–3 real examples), **Questions you should be
   asking** (3–5 expert questions with best-guess answers + confidence), **Rewritten
   request** (the user's request, upgraded by what you found).

Stop when the report is delivered. Guardrail: prioritize architecture-changing findings;
cite evidence for every non-obvious claim.

### Technique 2 — Brainstorm & prototype (UK)

Delegate to `prototype-smith` for multi-direction artifacts.

1. Gather raw material (data samples, constraints, references) so options are concrete.
2. Produce N genuinely different directions (default 4) — different hierarchies, framings,
   interaction models. Variations on one idea are a failure mode.
3. One self-contained HTML artifact; each direction labelled with a one-sentence thesis
   plus what it optimizes for and sacrifices.
4. Close with a reaction guide: 3–5 questions helping the user articulate what they like.

Stop when the user has reacted; convert reactions into explicit criteria before real code.
Guardrails: fake every backend; never modify the real application while prototyping.

### Technique 3 — Interview (KU)

For high-stakes cases use Cartographer mode instead — it adds regret targeting and a gate.

1. Read everything already established; never ask what is answered or discoverable.
2. Privately sort open ambiguities by blast radius: architecture-changers first (data
   model, interfaces, approach), then behavior definers (edge cases, failure modes,
   defaults), polish last — usually propose-and-move-on.
3. Ask via AskUserQuestion — up to 3 independent questions per round, each with context
   that makes it matter, 2–3 concrete options, and your recommendation. Bundle only
   questions whose answers do not depend on each other; ask a dependent follow-up in the
   next round. Accept "you decide" as an answer you then own.
4. Every few questions, checkpoint: restate all decisions in one tight list.

Stop when remaining unknowns are cheaper to discover during implementation than to ask
about — and say so. End with the final decision list. Guardrail: if an answer contradicts
an earlier decision, flag the conflict immediately.

### Technique 4 — References (UK)

1. Have the user point at the reference (path, repo, URL) and name the property they want:
   semantics, structure, feel. `blindspot-scout` can do large reads.
2. Read the underlying implementation, not a screenshot or summary.
3. Extract the transferable essence — behavior, invariants, structure — and state what
   will NOT transfer (language idioms, deps, scale assumptions).
4. Confirm the extraction before reimplementing.

Stop when the user confirms the extracted semantics. Guardrail: when the reference
conflicts with host-codebase conventions, surface the conflict; don't silently pick a side.

### Technique 5 — Implementation plan (KU)

The plan's job is to put expensive-to-change decisions in front of the user while changing
them is free — not to prove thoroughness. `prototype-smith` can render HTML.

1. Three-line opener: what is being built, chosen approach, single riskiest assumption.
2. **Decisions likely to change** first: data model, interfaces, API shapes, anything
   user-facing — each with the choice, one alternative, and the cost of changing later.
3. **Known unknowns and their defaults**: the default to be taken and the signal that
   would trigger a pivot.
4. **Mechanical work** last, compressed.
5. End with the 2–4 decisions needing a yes/no or a pick.

Stop when the user rules on the flagged decisions. Guardrails: reviewable in minutes;
leave room for improvisation; present mid-planning pivots as their own decision.

## Phase 2: During implementation

### Technique 6 — Implementation notes

1. At build start create `implementation-notes.md` with headings: **Deviations**,
   **Discovered edge cases**, **Questions for review**.
2. When reality forces an unplanned choice: pick the conservative option (conservative =
   most reversible, not simplest), log what the plan said / what was done / why / cost to
   revisit — and keep going. Don't block the user on reversible decisions.
3. Log edge cases even when handled cleanly.
4. Irreversible or scope-changing choices go under Questions for review AND stop work at a
   safe checkpoint.
5. End with a five-line summary; reference the file in the handoff or PR.

Guardrails: entries 2–3 lines; an unlogged deviation is worse than no notes — the file
claims completeness.

## Phase 3: Post-implementation

### Technique 7 — Pitch & explainer

Package prototype + spec/plan + implementation notes into one document. Lead with the
demo; follow with decisions taken and the failure points an expert reviewer would probe
(pulled from Deviations). Reviewers' objections are predictable from the unknowns already
logged — answer them preemptively.

### Technique 8 — Quiz (UU, post-hoc)

Delegate to `quiz-master` — an examiner that didn't write the change probes what its
author glosses over.

1. Report first: **Context**, **What changed** (grouped by intent, not file), **How it
   interacts** (existing paths that now behave differently, including files the diff
   doesn't show), **Intuition** (2–3 mental-model updates).
2. Then 5–8 questions weighted toward deviations, edge cases, interaction effects; mix
   recall and prediction. Never trivia about names.
3. Grade honestly; for each miss give the answer AND classify it — gap in the user's
   model, or change too clever. Say which.

Stop when the user passes, or after two failed rounds → recommend simplifying or
splitting the change, not re-quizzing. Guardrail: never mark correct out of politeness; an
unexplained diff hunk absent from notes/ledger is an **unlogged deviation** — flag it.

## Phase C: Cartographer mode (high-stakes escalation)

Gates on **coverage** (all four quadrants probed) AND **clarity** (per-quadrant ambiguity
scored every round, weighted total at or below threshold), persists across the **whole
lifecycle**, and orders work by **regret**. Two axes, two jobs: regret prices *rows*
(which unknown to clear next); ambiguity scores *quadrants* (whether the user can see how
clear the map actually is). The interactive loop is mandatory — scores are shown after
every round so the user can steer instead of discovering drift at the end.

**Resolve the clarity threshold first (blocking).** Read
`findingUnknowns.ambiguityThreshold` from `./.claude/settings.json` (project) then
`~/.claude/settings.json` (user); project wins; default **0.25**. Presets when invoked
with a depth flag: `--quick` 0.35 · `--standard` 0.25 · `--deep` 0.15. Announce on entry,
first line exactly:

> Clarity threshold: {X}% (source: {project settings | user settings | default | flag})
>
> Entering Cartographer mode. I will maintain unknowns-ledger.md, clear the highest-regret
> unknown each round by its route, score all four quadrants' clarity after every round, and
> will not proceed to implementation until the coverage gate passes AND weighted ambiguity
> is at or below {X}%.

**Round 0 — topology gate (one question, before any scoring).** Enumerate the task's 1–6
top-level components (outcomes that can succeed or fail independently — not sub-features)
and confirm via one question: "I read this as N components: … Add, remove, merge, split,
or defer any?" Lock the confirmed list into the ledger header. Quadrant scores are then
tracked per component where components differ materially; the reported score for a
quadrant is its weakest active component's score — depth-first clarity on the
best-described component must not hide sibling fog. Deferrals need a user-confirmed
reason and are excluded from ambiguity math but stay listed.

**Quadrant clarity model.** Each quadrant scores 0.0–1.0 with a one-clause justification
and a named gap when below 0.9:

| Quadrant | Scores high when |
|----------|------------------|
| KK | stated knowns are written down, internally consistent, and confirmed against the territory |
| KU | known gaps are enumerated, each with a route and a resolution or logged default |
| UK | taste/recognition criteria have been elicited — prototype reactions or reference extractions converted into explicit criteria |
| UU | blind-spot probes ran and are going dry; findings are tracked rows |

`ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)` — UU carries the most weight
because unprobed blind spots are the failure mode this skill exists to prevent. Scoring is
`ledger-keeper`'s SCORE-QUADRANTS operation when installed; inline otherwise. Consistency
beats flair: justify from ledger evidence, never from how productive the round felt.

### C0: Seed the ledger

Create `unknowns-ledger.md` (owned by `ledger-keeper` when installed). The file opens
with a header block — clarity threshold + source, the Round 0 locked topology (components,
statuses, deferral reasons), and a per-round quadrant score history table — followed by
the rows:

| id | quadrant | unknown | cost-if-wrong (1–5) | P(wrong) | regret | **route** | status | phase | resolution / default |
|----|----------|---------|--------------------|----------|--------|-----------|--------|-------|----------------------|

- Run Technique 1 (blind-spot pass) → seed UU rows. Naming a blind spot makes it trackable.
  For high-stakes tasks, prefer a **multi-lens sweep**: parallel scouts with distinct lenses
  (e.g. domain-risk / engineering / statistics) — diversity catches what one lens cannot.
  When the Workflow tool is available (and the user has opted into orchestration), run the
  sweep as the `fu-multi-lens-sweep` script in `references/workflows.md`: scouts fan out,
  each finding is adversarially verified as its lens completes (pipeline, no barrier), and
  the result is schema-validated ledger rows — no lens or verification step can be
  silently dropped. Without Workflow, follow the fallback ladder in that file.
- Run Technique 2/4 where taste is involved → seed UK rows.
- Write down KK; list KU.
- **Domain checklist hook**: after seeding, check the ledger against a domain checklist
  derived from the user's profile, and add any missing rows. Example (quant trading):
  funding/borrow costs · liquidation distance · capacity/liquidity · per-leg attribution ·
  fee/slippage realism · regime dependence. A checklist row you can immediately mark
  resolved costs one line; a missing one costs a blown-up backtest.
- `regret = cost-if-wrong × P(wrong)` — the only prioritization signal.
- **`route` — HOW the row gets cleared** (regret decides order; route decides instrument):
  - `interview` — the answer exists only in the user's head (preferences, intent, context)
  - `territory` — verifiable by reading/checking code or data (assign to a scout or a check;
    NEVER ask the user — the no-discoverable-questions rule applies per row)
  - `experiment` — needs a backtest/prototype/measurement to settle
  - `audit` — needs review of an external artifact (a pipeline, a dependency, a document)
- `status ∈ {open, probing, resolved-provisional, resolved, deferred}`; deferred REQUIRES a
  conservative default; resolved-provisional (single-source or refutable evidence, cost ≥ 4)
  REQUIRES a named discriminating check. Rows are never deleted. `phase ∈ {pre, during,
  post}` records when the unknown surfaced.

### C1: Clearing loop

The engine is a **router, not an interview**: each round clears the highest-regret open row
by its route. Repeat until the gate passes or the user exits:

1. **Target**: the highest-regret open row (keeper picks when installed) — or, for the
   `interview` route, the top 1–3 *independent* rows to clear in one round. Leave-open rule:
   rows with regret < 1.0 get a conservative default logged and are not worth a round.
2. **Dispatch by route**:
   - `interview` → ask via AskUserQuestion, prefixed with the targeting rationale. Ask 1–3
     *independent* interview-route rows in one round (highest regret first); keep dependent
     rows for later rounds:

     ```
     Round {n} | Targets: {id(s)} {unknown(s)} | Regret: {r each} ({cost}×{p}) |
     Route: interview | Why now: {one sentence per target}

     {1–3 questions, each with 2–3 concrete options + recommendation}
     ```

   - `territory` → run the check now (Grep/Read/scout); report the evidence found.
   - `experiment` → do NOT block the loop: record the experiment spec (what to run, what
     result clears the row) as the row's clearing action; the row stays `probing`.
   - `audit` → likewise: name the artifact, what to look for, and the expected effort;
     the row stays `probing` until the audit result arrives.
3. **Re-score** the row's P(wrong) from the answer/evidence; recompute regret. Answers may
   spawn NEW rows (quadrant + regret + route) — that chain is the ledger working correctly.
3.5 **Verify before resolving (evidence discipline, for rows with cost ≥ 4)**:
   - **Adversarial check**: before marking the row resolved, construct the strongest
     alternative explanation consistent with the SAME evidence. If a plausible refutation
     exists, the row stays `resolved-provisional` and the ledger records the one
     discriminating check that would separate the explanations. (Example: a strong
     backtest IC resolves "is the signal real?" only provisionally — leakage produces the
     same IC; the discriminating check is a pipeline audit.) With Workflow available, use
     the `fu-verify-panel` script (`references/workflows.md`): three refuters with distinct
     lenses (alternative-explanation / evidence-independence / reproduction); the
     resolution survives only if ≥2 fail to refute, and refuters' discriminating checks
     land in the ledger verbatim.
   - **Cross-reference rule**: a cost ≥ 4 resolution backed by a single evidence source is
     `resolved-provisional`, never `resolved`. Two independent sources (different
     instruments — e.g. an experiment AND an audit) are required for full resolution.
   - Record per resolution: the evidence, its source(s), and a confidence label
     (high/medium/low). Separate fact from inference explicitly.
3.8 **Score the quadrants** (every round, no exceptions): re-score all four quadrants per
   the clarity model in the Phase C header (`ledger-keeper` SCORE-QUADRANTS when
   installed). Append the scores to the ledger's score history. The next round's target
   is the highest-regret open row, tie-broken toward the weakest quadrant.
3.9 **Challenge modes** (each used exactly once, then back to normal clearing):
   - Round 4+, **Contrarian**: the next interview question challenges a core assumption —
     "what if the opposite were true / this constraint doesn't exist?"
   - Round 6+, **Simplifier**: probe removable complexity — "what's the simplest version
     that would still be valuable?"
   - Round 8+ if ambiguity still > 0.30, **Ontologist**: "what IS this, really — which
     component is the core and which are supporting views?" (may revise the Round 0
     topology; re-lock it if so)
4. **Report** after every round, in exactly this format:

```
Round {n} complete.

Ledger: {open} open | {probing} probing | {resolved} resolved | {deferred} deferred
Top regret: {id} ({regret}) — {unknown} [route: {route}]

| Quadrant | Score | Weight | Gap |
|----------|-------|--------|-----|
| KK | {s} | 0.20 | {gap or "clear"} |
| KU | {s} | 0.25 | {gap or "clear"} |
| UK | {s} | 0.25 | {gap or "clear"} |
| UU | {s} | 0.30 | {gap or "clear"} |
| **Ambiguity** | **{a}%** | threshold {X}% | {weakest quadrant × component + why it's next} |

Coverage gate:
[{x| }] KK locked          [{x| }] KU resolved/deferred
[{x| }] UK extracted       [{x| }] UU probed
[{x| }] no open row with regret ≥ 1.0
[{x| }] ambiguity {a}% ≤ threshold {X}%

{gate passes ? "Gate PASSED — ready to build."
 : "Next target: {id} — {reason}"
 : when only probing rows with pending experiments/audits remain:
   "Gate BLOCKED on external work: {list of clearing actions}. No further rounds add
    value — execute the clearing actions, then resume (the ledger is the state)."}
```

### C2: Gate check (blocking, dual-axis)

Implementation may start only when ALL hold — coverage AND clarity:

- [ ] KK locked — knowns written down
- [ ] KU resolved or deferred-with-default
- [ ] UK extracted — at least one brainstorm/prototype/reference ran
- [ ] UU probed — at least one blind-spot pass ran; findings are tracked rows
- [ ] No open row has regret ≥ 1.0
- [ ] Weighted ambiguity ≤ threshold (per-quadrant scores from the latest round)

The two axes catch different failures: coverage catches "we never looked there";
ambiguity catches "we looked, but the user still can't tell how clear it is". Passing one
does not imply the other. Round limits: soft warning at round 10 (show scores, offer
continue/proceed-with-risk), hard cap at round 20 (proceed noting the residual ambiguity).
Early exit from round 3+ is allowed — display the current score table and open gaps once,
transparently, then respect the exit.

If UU was never probed the gate FAILS — that is its entire point. When `ledger-keeper` is
installed its verdict is final; never pass the gate out of politeness.

**Completeness critic (final sub-step before declaring PASS)**: when all five conditions
appear satisfied, run one explicit "what's missing?" pass before announcing PASS — a
domain-checklist re-scan plus three questions: which quadrant was probed most shallowly?
which resolution is single-source or provisional? what would an expert reviewer ask that
no row covers? Anything surfaced becomes a new row and the gate re-evaluates. A PASS
without the critic pass is invalid. If the critic names UU as the shallow quadrant and
Workflow is available, run `fu-uu-until-dry` (`references/workflows.md`): differently
angled probes loop until two consecutive rounds surface nothing new — bounded by
information, not by a fixed count.

### C2.5: Close-out report (structured, Deep-Research style)

When the gate passes — or when suspending on external work — deliver a structured report,
not a prose summary:

```
# {task}: Unknowns Report
*Rounds: {n} | Rows: {total} ({resolved}/{provisional}/{deferred}/{open}) | Gate: {verdict}*

## Executive summary        — 3–5 sentences: what is now known, what still blocks
## Findings by row          — per high-regret row: evidence, source(s), confidence
##                            (high/med/low), fact vs inference labelled
## Gaps & provisional items — every resolved-provisional row with its discriminating
##                            check; every deferral with its conservative default
## Methodology              — which routes ran (interview/territory/experiment/audit),
##                            which agents/lenses, what was NOT examined
```

Acknowledging gaps is a deliverable, not an apology — an unlisted gap is an unlogged
deviation waiting to happen.

**Crystallized spec.** On gate PASS, also write `unknowns-spec-{slug}.md` next to the
ledger — the handoff artifact for Phase E: goal (one sentence, covering every active
topology component), constraints, non-goals, testable acceptance criteria, the final
quadrant clarity table (scores + ambiguity % + threshold + source), an assumptions
exposed → resolved table, and a ledger snapshot reference. The spec is marked
**pending approval** — writing it grants no execution permission.

### E: Cross-validated execution bridge (approval-gated)

Never auto-execute. After the spec, ask ONE question — "Spec ready (ambiguity {a}%).
How to proceed?" — with these options:

1. **Consensus-refine, then separate execution approval (recommended).** A planner-role
   agent drafts the implementation plan from spec + ledger; an INDEPENDENT reviewer-role
   agent (architect/critic framing: "find what breaks this plan against the spec and the
   ledger's deferred defaults") reviews it; loop until the reviewer approves, ≤3
   iterations. Then STOP with the consensus plan marked pending approval — execution is a
   separate explicit yes.
2. **Execute via Workflow orchestration** (requires the user's orchestration opt-in): run
   `fu-execute-verified` from `references/workflows.md` — tasks pipeline through an
   implement agent and an independent refute-framed verify agent; a task closes only on
   its verifier's pass. Fallback ladder as ever: Workflow → parallel Agent calls → inline
   implement-then-independent-review.
3. **Refine further** — return to the C1 loop.

Normative invariant (extends "separation of judgment"): **the context that authored a
spec or plan never self-approves its execution.** Author and approver are always
different contexts — a second agent, or the user.

### C3: During & close-out

- Keep the ledger open through the build: every mid-build discovery becomes a row
  (quadrant + regret), conservative option chosen and logged (Technique 6 feeds the ledger).
- Post: build the quiz FROM the ledger — one question per resolved high-regret row and per
  named UU. Merge only when no open row has regret ≥ 1.0.

</Steps>

<Agent_Delegation>
| Agent | Backs | Contract: give it → it returns |
|-------|-------|-------------------------------|
| `blindspot-scout` | Technique 1, 4 | goal + experience level → five-section recon report (read-only; cannot implement) |
| `prototype-smith` | Technique 2, 5 | problem + data sources + N → one HTML artifact of N divergent directions + reaction guide (writes only throwaway files) |
| `ledger-keeper` | Cartographer | task/answers/discoveries → updated ledger, regret scores, next target, gate verdict (touches only the ledger) |
| `quiz-master` | Technique 7, 8 | diff + notes + ledger → HTML report + must-pass quiz (read-only; flags unlogged deviations) |

- Relay agent reports; do not re-run their exploration in the main context.
- The gate verdict belongs to `ledger-keeper`; the quiz belongs to `quiz-master`. Do not
  overrule either to be agreeable.
- Trivial cases stay inline; agent overhead needs a payoff. Cost anchors: a codebase
  blind-spot pass typically costs ~50–100k subagent tokens and a few minutes — worth it
  when a wrong assumption forces a redesign; not worth it for a one-file question.
- For high-stakes tasks, `blindspot-scout` may be run as a multi-lens sweep: several
  parallel scouts, each with ONE named lens (e.g. domain-risk / engineering / statistics)
  stated in its prompt. Merge their findings into the ledger; duplicate findings across
  lenses are confirmation, not waste.
- **Workflow orchestration (preferred at Cartographer stakes when available)**: the three
  fan-out-heavy operations — multi-lens sweep, cost ≥ 4 verification panel, UU
  loop-until-dry — have ready-to-run Workflow scripts in `references/workflows.md`, with
  structured (schema-validated) outputs that feed the ledger mechanically. Workflow use
  requires the user's orchestration opt-in; the file's fallback ladder covers plain-Agent
  and fully-inline environments. The logic is normative; the mechanism is not.

### Model routing

Route by role, the way OMC does (opus for judgment/reasoning, sonnet for execution, haiku
for cheap breadth) and Deep Research does (the strongest model synthesises at the centre;
cheaper sub-agents fan out). The twist: the top tier is **`inherit`, not a pinned model** —
respect the model the session is already running (Fable / Opus / Sonnet) and never downgrade
its reasoning strength.

| Role | Agent | Model | Why |
|------|-------|-------|-----|
| Orchestrator / task centre | (the main conversation) | the session model | your chosen strength runs the interview, routing, and synthesis |
| Judgment — scoring & gate verdict | `ledger-keeper` | `inherit` | the verdict must be as strong as the session, not capped at opus |
| Creative — divergent brainstorm | `prototype-smith` | `inherit` | idea quality is the skill's core value |
| Judgment — independent grading | `quiz-master` | `inherit` | examination is judgment work |
| Breadth — reconnaissance | `blindspot-scout` | `sonnet` (overridable to `inherit`) | fans out in parallel (multi-lens sweep = 3–5 instances); cheap breadth feeding a strong synthesiser |

`inherit` uses Claude Code's native subagent model-selection: a `[1m]` session resolves to
its base tier for subagents — reasoning strength preserved, the 1M context (which subagents
do not need) is not. In Workflow scripts the same rule holds: scout stages carry
`agentType: 'blindspot-scout'` (→ sonnet); scoring and verification stages omit `model` so
they inherit the session's strength.
</Agent_Delegation>

<Examples>
<Good>
Routing announcement before any technique:
```
Routing: UU + UK → blind-spot pass, then 4-direction prototype — you're new to this
subsystem (UU) and the dashboard layout is know-it-when-you-see-it (UK).
```
Why good: quadrant diagnosis is explicit, the technique choice follows from it, and the
user can veto the routing before any work happens.
</Good>

<Good>
Regret-weighted targeting in Cartographer mode:
```
Round 3 | Target: U2 "which auth path to extend" | Regret: 2.0 (4×0.5) | Why now:
highest-regret open row; a wrong guess here forces a rewrite of the middleware layer.

Should this feature extend the existing JWT middleware in src/auth/ (found via scout,
pattern: passport + JWT), or diverge with a separate flow?
  a) Extend existing (recommended — consistent, less surface)
  b) Separate flow (isolates risk, duplicates session logic)
```
Why good: names the row, shows the arithmetic, explains why now, cites scout evidence
instead of asking the user to rediscover it, offers options with a recommendation.
</Good>

<Good>
Honest gate failure:
```
Coverage gate: [x] KK [x] KU [x] UK [ ] UU [x] regret
Gate FAILED — no blind-spot pass has run. Clarity on the questions we thought to ask is
not coverage of the ones we didn't. Run the scout before building.
```
Why good: refuses to conflate "all known questions answered" with "territory mapped" —
the exact failure mode this mode exists to prevent.
</Good>

<Bad>
Bundling dependent questions in one prose blob:
```
"What's the target audience? And given that, which tech stack, and given the stack, how
should auth work, and where does that deploy?"
```
Why bad: each answer changes the next question's framing, so asking them together forces
shallow answers and makes regret re-scoring meaningless. Independent questions are fine to
batch (up to 3) via AskUserQuestion's clickable options — chained ones are not.
</Bad>

<Bad>
Asking what the territory can answer:
```
"Does your project use pandas or polars for the data layer?"
```
Why bad: one Grep answers this. Interview questions are for information that exists only
in the user's head.
</Bad>

<Bad>
Sliding from discovery into implementation:
```
"While doing the blindspot pass I noticed the config parser was messy, so I refactored
it and also started the feature since I was in there."
```
Why bad: discovery techniques end at understanding. Unrequested mutation during recon
destroys the user's trust that a scout is safe to run.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **User says "just build it" mid-discovery**: stop the technique, state in ≤3 lines the
  highest-regret unresolved unknowns and the conservative defaults you will take, then
  proceed. Respect the exit; make the risk visible once, not repeatedly.
- **Interview stalls** (answers stop changing any row's regret): stop interviewing; the
  remaining unknowns are cheaper to discover during implementation. Say so.
- **Two failed quiz rounds**: recommend simplifying or splitting the change. Do not keep
  quizzing.
- **Scout finds nothing significant**: report "no significant blindspots" and end — do not
  pad the report.
- **Cartographer round 10 without gate progress**: surface the top-3 stuck rows and ask
  the user to resolve, defer-with-default, or exit to lightweight techniques.
- **Interview question times out / user is away**: the row stays `open` (no re-score
  without an answer), mark it "re-askable", report the round with the gate suspended, and
  deliver whatever territory/experiment routes can proceed without the user. Never invent
  an answer on the user's behalf.
- **Only probing rows with pending experiments/audits remain**: stop looping — further
  rounds add no information. State the clearing actions and suspend; resume from the
  ledger when results arrive.
- **Any technique asked to mutate product code**: refuse within the technique; discovery
  is read-only except for its own artifacts (prototypes/, notes, ledger, reports).
</Escalation_And_Stop_Conditions>

<Final_Checklist>
Lightweight lane:
- [ ] Phase 0 routing was announced (quadrant → technique) before any technique ran
- [ ] No discovery technique mutated product code
- [ ] Interview questions were single, blast-radius-ordered, and non-discoverable
- [ ] Artifacts delivered in reactable form (HTML default) with a reaction guide
- [ ] Deviations logged at decision time, not reconstructed afterwards

Cartographer lane (additionally):
- [ ] Ledger exists with quadrant, cost, P(wrong), regret, route, status, phase per row
- [ ] The domain checklist hook ran at seeding; missing domain rows were added
- [ ] Every row was cleared via its route — no territory-answerable question was asked of
      the user, and no experiment/audit row blocked the loop with useless extra rounds
- [ ] Every round reported the ledger summary + gate checklist in the standard format
- [ ] Gate verdict came from ledger-keeper when installed; UU probe was not skipped
- [ ] Deferred rows all carry conservative defaults; no rows were deleted
- [ ] First announcement line stated the clarity threshold and its source
- [ ] Round 0 topology was confirmed by the user before any quadrant scoring
- [ ] Every round's report included the four-quadrant score table with weighted ambiguity
- [ ] Gate checked both axes: coverage conditions AND ambiguity ≤ threshold
- [ ] On PASS, unknowns-spec-{slug}.md was written and marked pending approval
- [ ] Execution bridge asked before any execution; plan author ≠ plan approver throughout
- [ ] Quiz was generated from the ledger; merge recommendation followed the pass rule
</Final_Checklist>

<Advanced>
## Resume

The ledger IS the state. To resume an interrupted Cartographer session, re-read
`unknowns-ledger.md` (and `implementation-notes.md` if the build started), announce the
current gate status, and continue from the highest-regret open row. Do not re-seed.

## Defaults (override by telling the skill)

| Knob | Default | Meaning |
|------|---------|---------|
| Prototype directions N | 4 | genuinely different directions per brainstorm |
| Regret question bar | 1.0 | rows below this get defaults, not questions |
| Quiz size | 5–8 | questions per round |
| Quiz rounds | 2 | before recommending simplify/split |
| Cartographer soft cap | 10 rounds | then surface stuck rows / show scores |
| Cartographer hard cap | 20 rounds | proceed, noting residual ambiguity |
| Ambiguity threshold | 0.25 | override via settings or --quick 0.35 / --deep 0.15 |
| Consensus iterations | 3 | planner↔reviewer loops in Phase E option 1 |
| Questions per round | ≤3 independent | interview-route rows batched per round (dependent ones one at a time) |

## Threshold configuration

Optional, read at Cartographer entry (project overrides user; degrade silently to the
default — no OMC runtime required):

```json
{ "findingUnknowns": { "ambiguityThreshold": 0.25 } }
```

## Relationship to heavier tooling

- Cartographer's ambiguity gating, topology gate, and challenge modes are adapted from
  `oh-my-claudecode:deep-interview` (itself Ouroboros-inspired), re-based on the four
  quadrants. Deep-interview still wins when you want ontology/entity-convergence tracking,
  OMC state persistence, or automatic handoff into autopilot/ralph/team; Cartographer adds
  what deep-interview lacks — quadrant coverage, regret-priced rows, route-typed clearing,
  and lifecycle persistence through build and review. Complementary, not competing.
- Divergent option generation as a discipline → `superpowers:brainstorming`. Rigorous
  written plans → `superpowers:writing-plans` / `oh-my-claudecode:plan`. Spec already
  concrete → skip discovery and execute.
</Advanced>
