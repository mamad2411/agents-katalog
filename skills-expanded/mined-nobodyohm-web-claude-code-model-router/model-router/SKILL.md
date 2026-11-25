---
name: model-router
description: Use when making any non-trivial model/effort routing decision, after a tier fails, or when fanning out parallel work — the full triage policy: pick the cheapest sufficient tier, delegate down, escalate to Fable.
---

# Model & effort router

Quality-first, but well-tuned: the main model (Opus 4.8, `high` effort) reasons strongly by
default, yet routes every task to the **cheapest tier that still meets the quality bar** and uses
the **matching effort** — so Opus is never burned on trivial work, and Fable is reserved for what
is genuinely hard. All four models and all four effort levels are in play.

## The ladder (cheap → flagship)

Model names below are illustrative; the actual model IDs, effort levels, and agent bindings are
configured per-tier in `config/router.config.json` — edit there, not here.

| Tier | Model · effort | Delegation target | Job |
|------|----------------|-------------------|-----|
| 1 | **Haiku 4.5** · low | `Explore`, `quick-haiku` | Broad read-only search; fully-specified mechanical edits; renames; formatting; running one known command; extracting a value; one-file "what does this do". |
| 2 | **Sonnet 5** · medium | `worker-sonnet` | Standard implementation, refactor within a known pattern, write/fix tests, self-contained chunks — especially in parallel/background. |
| 3 | **Opus 4.8** · high | *inline (main)* or `deep-opus` in parallel | Hard-but-well-posed reasoning: subtle multi-file bugs, non-trivial refactors, performance, architecture with a knowable answer. |
| 4 | **Fable 5** · xhigh | `deep-fable` | The escalation tier: genuinely complex, novel, ambiguous, open-ended, cross-cutting; or anything a lower tier already failed. |

`max` effort exists as a manual, session-only override (`/effort max`) for an exceptionally hard
stretch — not a standing default.

## Decision procedure (run per task)

1. **Trivial & fully specified?** (grep, rename, format, one-file edit, known command) → **Haiku**
   via `quick-haiku`, or `Explore` if it's a search. Don't do it inline on Opus.
2. **Broad discovery across many files / unknown naming?** → **Haiku** via `Explore` (returns
   `file:line` conclusions, not dumps) before spending a stronger model on the real work.
3. **Standard coding of moderate size, self-contained?** → **Sonnet** via `worker-sonnet`,
   especially if it can run in the background while you do something else. Fan out several when
   the chunks are independent.
4. **Hard but well-posed reasoning?** → handle **inline** (you are Opus), or dispatch `deep-opus`
   when you want it to run in parallel with other work.
5. **Genuinely complex / novel / ambiguous, OR a lower tier just failed?** → **Fable** via
   `deep-fable`. See escalation triggers below.

## The active layer (v2)

This policy isn't just guidance anymore — two hooks make it live:

- **Routing hint (`UserPromptSubmit`)** — `bin/classify.sh` runs local heuristics
  (`config/rules.json`) on every prompt and injects a one-line tier suggestion into context, with
  an optional small Haiku call for ambiguous cases. It is **advisory, not enforcement**: the pinned
  subagents above are still what actually restricts the model. It is also **fail-open** — if
  classification errors or times out, the turn proceeds unhinted, never blocked.
- **Telemetry (`PreToolUse(Task)`)** — `bin/log-dispatch.sh` logs every subagent dispatch to
  `~/.claude/router/dispatches.jsonl`. Run **`/router-stats`** for a report: dispatches per tier,
  actual tokens/cost per model, and estimated $ saved vs. an all-Opus baseline — evidence the
  routing is working, not just a claim.
- **Config, not prose** — tier→model mapping, effort levels, profiles (quality-first / balanced /
  max-savings), classifier knobs, and pricing all live in `config/router.config.json` (classifier
  signals in `config/rules.json`). To change a model, edit the config — model names elsewhere in
  this document are illustrative, the config is authoritative.

## Effort as an independent lever (v2.2)

Effort is no longer bolted to the tier. The classifier reads quick/thorough signals
(`config/rules.json` → `effort_signals`) and applies a **±1 modulation** to the tier's default
effort. Where a variant agent exists it is enforced:

- **hard + "quick/just"** → `deep-opus-medium` (Opus·medium): the answer is knowable, skip the
  full high-effort pass. If it fails, escalate **effort first** — retry on `deep-opus` (Opus·high)
  before bumping the model to Fable.
- **standard + "carefully/thoroughly"** → `worker-sonnet-high` (Sonnet·high): more reasoning
  without paying for a bigger model. If it needs cross-file architecture, escalate to `deep-opus`.

Where no variant exists the signal is still **logged** (visible in `/router-stats`) but not
enforced — data for adding future variants. The ledgers now carry the effort of every
classification and dispatch.

## Escalate UP to Fable when ≥1 holds

- Open-ended design with no established pattern to follow; the "right answer" isn't knowable up front.
- **A substantial plan or an architecture/design decision** — "make a plan for X", "what's the best approach", "weigh the options", "how should we structure this". Advanced reasoning should *participate* in planning via `deep-fable`, not be silently absorbed inline on Opus. (Quick, well-posed plans stay on Opus — escalate the substantial ones.)
- Deep multi-step reasoning, or many interacting constraints that must be held at once.
- A subtle root-cause hunt that a cheaper tier already attempted and got wrong.
- The user signals difficulty ("think hard", "this is tricky", "you keep getting this wrong").
- Any tier has **failed once** — escalate, do **not** retry the same tier on the same problem.

## Delegate DOWN (protect Opus budget) when

- The work is mechanical, well-specified, or in-pattern → Sonnet/Haiku, not inline Opus.
- It's a bulk of similar small edits → batch to `quick-haiku` (or fan out to workers).
- It's a self-contained slice that can proceed independently → `worker-sonnet` in the background.

## Escalation protocol (failure handling)

- **Never retry the same tier that just failed.** Move up a rung.
- Before the stronger tier redoes the work, have it **diagnose why the previous attempt failed** —
  don't walk the same path with a bigger model.
- After escalating and succeeding, that's the tier for that *class* of task going forward in the
  session — don't drop back down and re-fail.

## Parallelism & supervision

Independent subtasks run concurrently: dispatch several agents in ONE turn (multiple tool calls in
one message) and they execute in parallel, not serially. This is both faster and cheaper than doing
everything inline on the flagship main.

- **Haiku scout swarm** — for a broad hunt, fire N `Explore` (Haiku) agents at once, each scoped to
  a different area or naming convention. The MAIN model (the strong one) is the supervisor: it
  collects the `file:line` conclusions and decides the next move. This is the cheap-search-at-scale
  pattern the user asked for.
- **Worker fan-out** — split independent implementation chunks across several `worker-sonnet` (and
  `deep-opus`) agents running at once; the main integrates the results.
- **Supervision goes DOWNWARD only.** The supervisor is always the *stronger* model (main Opus, or a
  `deep-*` planner) coordinating *cheaper* workers — never a Haiku coordinating others: a small
  model is a poor orchestrator and its aggregation errors cost rework. A subagent can spawn its own
  sub-agents only if explicitly granted the `Agent` tool, and Claude Code caps nesting depth to
  prevent runaway recursion — keep it to one level (main → workers) in normal use.
- **Heavy deterministic orchestration** (dozens of agents, fan-out → verify → synthesise pipelines,
  loop-until-dry) is the **Workflow** tool, not ad-hoc dispatch. Powerful but token-heavy, and it
  requires explicit opt-in ("ultracode" or a direct request) — reach for it only when the user asks
  for that scale.

## Decomposition & integration (orchestrator pattern)

For a task too big or too mixed for one tier, the ORCHESTRATOR (the main model — the conductor) does
the split, not a worker. Decomposition and integration always live at the top; workers receive
slices sized to their tier.

1. **Split** — break the task into independent slices; size each: hardest/novel -> `deep-fable`,
   hard-but-known -> `deep-opus`, standard -> `worker-sonnet`, mechanical -> `quick-haiku`.
2. **Fan out in parallel** — dispatch the slices concurrently in ONE turn; mixed tiers in the same
   batch is fine (each agent call targets its own model). If slices edit the SAME files, give each
   agent `isolation: worktree` so parallel edits don't clobber.
3. **Verify** — validate each returned slice against its acceptance check. For a high-stakes slice,
   spawn an independent verifier (a fresh agent prompted to REFUTE the result) — don't self-certify.
4. **Integrate** — the main stitches the verified slices together; it holds the full context, so
   integration belongs here, never inside a worker.

Do NOT nest orchestration inside a worker (a `deep-fable` that itself spawns sub-agents): nesting is
depth-capped and you would pay flagship rates for coordination the orchestrator does for free. Fable
gets the hardest SLICE, not the conductor's baton.

When the decompose -> parallel -> verify -> synthesize flow must be deterministic and repeatable
across many items (a migration, a broad audit), that is the **Workflow** tool, not ad-hoc dispatch —
opt-in only ("ultracode" or a direct request).

## Anti-patterns (these defeat the point)

- Delegating a single trivial edit or grep the main finishes in one step — the spawn overhead then costs more than it saves; batch bulk/parallel work to Haiku, but do genuine one-offs inline.
- `xhigh`/`max` effort left on for routine turns — effort should match the tier, not sit at the ceiling.
- Retrying the same failing tier instead of escalating.
- Escalating to Fable for something well-posed that Opus/Sonnet handles fine — reserve the flagship.
- Reading whole large files when a targeted `Explore` search would answer the question.

## Changing the posture (one line each)

Current default profile is **quality-first**, defined under `profiles.quality-first` in
`config/router.config.json` (mirrored to `~/.claude/settings.json` for the *main* model). The three
profiles — `quality-first`, `balanced`, `max-savings` — and their `model`/`effortLevel` values live
in that config, not in this doc:

- **Quality-first (current):** Opus orchestrates, delegates down, escalates to Fable.
- **Balanced / cheaper:** Sonnet orchestrates, Opus becomes the "hard" delegation tier, Fable for
  complex.
- **Max token savings:** Haiku pilots and delegates almost everything upward. Weaker orchestration.

To switch, set `profile` in `config/router.config.json` (or use `/model` + `/effort` for a
session-only override). The tiered agents and this policy are unchanged across postures — only the
starting rung moves.
