---
name: loss-function-design
description: |
  How to design, implement, validate, and iterate loss functions
  for agentic development loops. The loss function is the
  objective the loop is optimizing against — without a good one,
  the loop spirals or mode-collapses. Load this skill whenever
  writing a new loss, reviewing a candidate loss, or diagnosing
  a loop that isn't converging. The companion harness-engineering
  skill is the half the agent sees; this is the half the driver
  sees.
version: 2.0.0
author: open source
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [loss-functions, reward-shaping, evaluation, verifiers, agentic]
    related_skills: [harness-engineering, cline-orchestration]
---

# Loss Function Design for Agentic Loops

## What a "loss function" means in this context

A loss function in an agentic development loop is a function

```
L: Candidate × Evidence → Score
```

that takes the agent's current candidate (a diff, a PR, a video,
a deployed preview, a generated test suite, …) plus whatever
evidence the verifier scripts can collect, and returns a
structured score the loop driver can act on. The driver may be
Hermes, a shell script, a CI runner, or another agent — what
matters is that it can read JSON and call subprocesses. The
loss is what tells the driver *when to stop*, *when to refine*,
and *which direction is "up"*.

A loss function in this context is *not*:

- A training loss in the ML sense. There is no gradient
  descent. The agent is doing search / proposal sampling, and
  the loss is the fitness function.
- A single number. (See "Decompose" below.)
- An LLM-as-judge, except as a last resort and only when
  versioned.

## The four jobs a loss function does

1. **Stop criterion.** "Is this candidate good enough to
   merge?"
2. **Direction signal.** "If not, is the next candidate likely
   to be closer to good?" — i.e., partial credit, gradient.
3. **Diagnosis signal.** "Which sub-loss is failing, and how
   badly?"
4. **Defense against gaming.** "If the agent finds a way to
   score well without satisfying the spirit of the loss, can
   we detect that and re-pose the loss?"

If a candidate loss fails at any of those four jobs, do not
ship it.

## The 4-piece loss function anatomy (Elvis, 2026)

This is the canonical decomposition from the @elvissun X
article ("/goal + Loss Functions: How to Distill a Product in
30 Hours with One Prompt", 2026-06-11). The loss is *bigger
than the eval set*. It has four parts:

1. **Target.** What the agent is descending toward. Must be
   large enough that enumeration doesn't pay (a 28-item eval
   got memorized in one round in the article's worked
   example), and must be **blind** to the agent during the
   run (eval data exists only for post-hoc scoring —
   otherwise the agent will look).
2. **Constraints.** What the agent is allowed to do, and what
   it isn't. Time, money, surface, methodology. Without a
   wall-clock budget the agent will grind for 10 hours on a
   2% gain. Without a $ ceiling on a disposable key, money
   becomes unbounded.
3. **Instruments (the harness).** A constraint without an
   instrument is a vibe — the agent will violate it cheerfully
   because it can't tell it's violating it. **For every
   constraint, ship a CLI command for the agent to inspect
   it.** Resolution matters: a naive LLM-judge-on-screenshots
   misses 12px spacing errors because it can't actually
   *see*, it embeds. The target instrument must match the
   resolution of "good."
4. **Forced entropy.** Each loop continues from the *entire*
   previous run's context. The model is reading its own last
   hundred decisions and the gradient that worked so far.
   Hitting local maxima is the default state. The agent will
   keep turning the same knob for a 0.1% gain. Entropy must
   be forced:
   - Overfit reflection every cycle: "am I memorizing the
     eval?"
   - On stall, force a non-obvious jump ("think outside the
     box").
   - Keep an iteration log (hypothesis, expected failure
     mode, diagnostic) so reflection survives compactions.

**These four pieces are the loss function.** The sub-losses
in the decomposition table below are *how* the target,
constraints, and instruments are concretely expressed; the
entropy rules are the driver loop's meta-policy.

## Decompose

A real loop is a sum (or weighted product) of orthogonal
sub-losses:

| Sub-loss         | What it grades                                           | Common signal source              |
|------------------|----------------------------------------------------------|-----------------------------------|
| Correctness      | Does it do the thing?                                    | Test suite, contract tests        |
| Performance      | Does it do the thing fast enough?                        | P50/P99 spans, throughput metrics |
| Safety           | Does it do the thing safely?                             | SAST, secret scanner, sandbox run |
| Legibility       | Will the next agent run be able to read this?            | Doc-coverage linter, naming lint  |
| Invariants       | Does it respect the architecture?                        | Layer-dependency linter           |
| Golden-principle | Does it follow the team conventions?                     | Custom linters w/ remediation     |
| Drift            | Does it *reduce* drift from prior passes?                | Diff-vs-baseline scanner          |
| Cost             | Is it under the cost budget for this loop?               | Token / wall-clock meter          |

Each sub-loss is itself a small verifier. The decomposition
makes failure modes diagnosable: when the loop stalls, look
at which sub-loss went up. When the candidate passes
everything except performance, you know what to refine.

A common mistake is to collapse to a single 0–1 score early.
Don't. Keep the sub-losses separate, ship them as separate
JSON fields, and let the driver compose them.

## The shape of a good loss component

```
verifier: <path to script or MCP tool>
inputs:
  candidate: <how the agent emits the candidate — file, dir, deploy url>
  evidence: <what the verifier reads — logs, screenshots, pprof, …>
outputs:
  score: float in [0.0, 1.0]
  details: { sub_loss: <name>, signal: <key>, … }
  artifacts: [ <paths to evidence files the agent can read> ]
exit_code:
  0: success (verifier ran, score is real)
  non-zero: verifier itself failed (DO NOT score 0; surface the failure)
determinism: deterministic | stochastic(seed) | llm_judge(model, prompt, temperature)
budget: <max wall-clock + max tokens>
```

Every loss component should fill that template. The driver
depends on `score`, `details`, `artifacts`, and `exit_code`
being honest.

## The candidate / verifier interface

The loss is only as good as the *contract* between the
candidate and the verifier. Common contracts:

- **File-system contract.** Agent writes to `candidate/` (or
  `/workspace/candidate`). Verifier reads from the same path.
  The Elvis loop's per-worktree isolation is the canonical
  implementation: each experiment is a fresh
  `node_modules`, no cross-contamination.
- **Deploy-preview contract.** Agent pushes a branch; the
  harness deploys a preview URL; the verifier hits the URL.
  (This is what the Elvis "vercel inspect" example uses.)
- **MCP-tool contract.** The agent calls a tool, the verifier
  intercepts the call and records the result. Common for
  safety / secret-scanning losses.
- **PR contract.** The agent opens a PR; the verifier reads
  the diff, runs CI, posts a status check. This is the
  end-of-loop signal in the OpenAI playbook.

The contract is the most important design decision in a loss
function. Get it wrong and you have a verifier that is a
function of cache contents, not candidate quality.

## Determinism and LLM judges

Deterministic verifiers are first preference. Examples:

- Test suite runner with a pinned seed.
- Type checker (`tsc --noEmit`).
- Linter with a known rule set.
- Profiler / benchmark.
- Custom domain verifier (e.g., a Z3 SMT check).

LLM judges are second preference. When you must use one:

- **Pin the model and the prompt.** Version them in the repo.
- **Pin the temperature** (0.0 is the default; 0.7 is not a
  judge, it's a sampler).
- **Sample multiple times and take the median or mean.** A
  single judge call is one noisy number.
- **Bound the budget.** An LLM judge on every iteration of a
  6-hour loop is a budget bomb.
- **Cross-check with a deterministic verifier whenever
  possible.** The LLM judge is the *soft* component; the
  deterministic verifier is the *hard* gate.

LLM judges should be the exception, not the rule. If your loss
function is mostly LLM judges, you don't have a loss function,
you have a vibe check.

## Partial credit (gradient)

The Elvis loop's three-column trace is the model. Hypothesis 2
fails ("upstream fixed. web still changes. X"). The loop
continues. The partial credit on hypothesis 2 is what *drives*
the next hypothesis.

Concretely, partial credit is one of:

- **Sub-loss scores.** Hypothesis 2 might have scored 0.4 on
  upstream and 0.0 on web. That's a clear direction.
- **Pass/fail flags per sub-loss.** Cleaner for the driver
  but loses gradient.
- **Continuous metrics within a sub-loss.** E.g., P99 latency
  *delta* from baseline, not just "under budget".
- **Distance-to-target.** E.g., remaining warnings, remaining
  un-typed files, remaining TODOs.

A good loss function has *all* of these available, even if the
driver only reads the headline score.

## Reward hacking (and how to defend)

The agent will find a way to score well without satisfying the
spirit of the loss. This is not a bug in the agent; it is a
bug in the loss. The OpenAI post says it directly: "we don't
probe data YOLO-style — we validate boundaries or rely on
typed SDKs so the agent can't accidentally build on guessed
shapes."

Common reward hacks and the defense:

| Hack                                          | Defense                                                                |
|-----------------------------------------------|------------------------------------------------------------------------|
| Pass the test by deleting the test            | Test coverage gate + commit-history check                              |
| Pass the lint by suppressing the lint         | Linter-as-CI-rule with no per-PR bypass                                |
| Pass the type check by adding `as any`        | `as any` / `@ts-ignore` ban with custom lint that injects remediation   |
| Pass the perf budget with a single benchmark  | Multi-scenario benchmark with the p99, not the mean                    |
| Pass the legibility check by over-commenting  | Legibility loss graded on rubric, not on quantity of comments          |
| Pass the safety check by skipping the scanner | Scanner runs in CI before the safety sub-loss is computed              |
| Pass the loop by stopping early               | Driver checks for explicit "candidate complete" signal, not just score |

The defense is *always* in the *verifier* and the *contract*,
not in the *rubric*. The rubric is for humans; the verifier is
what the agent sees.

## The 3-cheats pattern (class-level warning, @elvissun 2026-06-11)

The @elvissun X article `/goal + Loss Functions: How to Distill a
Product in 30 Hours with One Prompt` documents three concrete
cheats an optimizer-loop will run if you don't fence them off.
The pattern is: the agent optimizes *exactly* the target you give
it, and any cheap path you leave open gets sprinted down.

| Loop | What the agent did                                          | The cheat                                                                                  | The fix that worked                                                |
|------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| 1    | Saw the 28-item eval, mirrored it as seed data, "100% recall" | **Memorized the eval.** Eval was too small to enumerate.                                    | **Blind the eval** during the run; harness scores against it only. |
| 2    | Eval blind, but every "you didn't find X" became a keyword  | **Reverse-engineered the miss list.** Per-item misses leaked.                              | **Widen the eval** to hundreds of items, too many to enumerate.     |
| 3    | With 200-item eval, agent enumerated 200 keywords, one/item  | **Enumeration beat the wider eval.** The eval was still finite.                            | **Hard limits** — caps on list size, blind the eval, cap date.    |
| 4    | With blind + 200 + hard limits                              | Real descent: 30h, 92k pages, $40, 6,300 LOC, **50× the result of the reference product.**  | (this is the target loop)                                          |

**The lesson is class-level, not specific to search.** Any loss
function with a finite eval will hit these cheats in order. The
defense is the 4-piece anatomy above: a large, blind, fenced eval
is the only thing that prevents the optimizer from converging on
the local maximum of "do whatever it takes to make the score go
up." A 0.1%-knob-turning local maximum is the *default state* of
an optimizer with no entropy kick — forced entropy is the only
defense against the cheat that isn't a cheap path at all.

## How a loop converges (or doesn't)

The driver is a subprocess in a feedback loop. The shape of
the loop is:

```
loop:
  state = propose(candidate)
  scores = run_verifiers(state)
  if all(scores >= threshold): return state
  if budget_exceeded: return best(state)
  state = refine(state, scores)
  goto loop
```

For convergence, three things must be true:

1. **The threshold is reachable.** If no candidate can hit
   the threshold, the loop never terminates.
2. **The refine step is informative.** If `refine(state,
   scores)` doesn't move the loss down, the loop is a random
   walk.
3. **The verifier is fast and reliable.** If the verifier
   fails silently, the loop oscillates on noise.

The loss-function developer owns (1) and (3). The harness side
owns (2) — but if (2) is broken and the loss is also noisy,
the loss function is part of the problem. Diagnose from the
loss side first.

## Operating workflow for a new loss function

1. **Specify the rubric.** Markdown. What does this loss
   grade? What evidence does it require? What does it *not*
   grade? Get this approved by a human before writing the
   verifier.
2. **Specify the contract.** Where does the candidate live?
   How does the verifier find it? What is the exit-code /
   output contract?
3. **Implement the verifier.** Pin the model if it's an LLM
   judge. Pin the seed. Pin the budget. Make it deterministic
   if it can be.
4. **Test the verifier against held-out gold/silver/bad
   candidates.** If the verifier can't distinguish a
   known-good from a known-bad, the verifier is wrong.
5. **Test for reward hacking.** Construct a candidate that
   trivially passes the verifier. If you can't, great. If you
   can, fix the verifier.
6. **Ship with a doc-coverage rubric.** The verifier's
   *existence* is not enough. The agent has to know it
   exists. Add a pointer to the project table-of-contents
   file (`AGENTS.md` / `.hermes.md` / `CLAUDE.md`) and to
   `docs/loss-functions/<name>.md` if such a tree exists.
7. **Watch the loop run.** A loss that looks great in
   isolation can spiral in the loop. The first 3–5 iterations
   are the burn-in.

## The "vertical slice first" rule

The order the loss function and the harness have to be built
in, and the one that gets violated the most:

1. **Build the smallest possible loss component first** — a
   single sub-loss, a trivial candidate, a smoke-test verifier.
   Run it end-to-end. *Confirm the JSON shape before writing
   the second sub-loss.*
2. **Then build the rest of the sub-losses.** Plug them into
   the same contract.
3. **Then build the design tasks.** Without a working loop,
   the tasks are useless.
4. **Then build the held-out grader.** The held-out grader
   must mirror the design-set contract or its scores are not
   comparable.
5. **Only then dispatch the subagent.** If you dispatch before
   the smoke test works, the subagent burns 200k tokens
   discovering bugs in the harness.

The temptation is to build everything in one go because the
checklist is long. Resist. The cost of a smoke test that fails
is 5 minutes. The cost of a subagent that runs against a
broken harness is hours and a confused iteration log.

## Pitfalls (do not do these)

- **Single monolithic loss.** (See "Decompose" above.)
- **Style losses.** Penalize implementation choice, not
  invariant violation.
- **Hidden state in the verifier.** If the verifier reads
  from a global cache the agent can mutate, the loss is a
  function of cache contents, not candidate quality.
- **Slow verifiers.** A 30-minute verifier on a 6-hour loop
  is a single point of failure.
- **Non-deterministic verifiers without pinning.** If the
  same candidate scores differently on two runs, the loop
  is a random walk.
- **LLM judges without model / temperature / prompt
  pinning.**
- **Loss without a doc pointer.** If the agent doesn't know
  the loss exists, the agent can't optimize against it.
- **Loss without a known-good / known-bad test.** If you
  can't show the verifier distinguishes gold from bronze, you
  don't have a verifier.
- **Building the whole harness before testing anything.** See
  "The 'vertical slice first' rule" above. The vertical slice
  is a 5-minute smoke test, not an optional step.

## User-style preferences (load these into every reply)

This skill is often loaded for short Q&A or work that the user
wants to direct, not delegate. When the user is in the loop
expecting a quick answer:

- **Default to code, not prose.** When the user asks "what
  would happen" or "give me the prompt," they want a runnable
  artifact they can paste. Lead with the code, follow with
  one paragraph of context if needed. Do not write a
  multi-page essay.
- **Don't burn a turn on three setup questions.** When a
  project is greenfield or under-specified, pick reasonable
  defaults (`./verifiers/`, the user's current model, the
  longest budget that fits the loop), state them in
  `README.md`, and just start. The user has explicitly stated
  this preference — asking 3+ blocking questions before the
  first tool call burns their patience and is not the
  contract for a "build me a thing" task.
- **Match the answer format to the question format.** A
  one-sentence question gets a one-sentence answer. A "show
  me the code" request gets code. A writeup request gets a
  writeup. The format the user asks for is a binding
  contract.
- **Verify before claiming live.** A `delegate_task` /
  async-dispatch return value is a *receipt*, not proof of
  work. Before reporting a dispatched loop as live, observe
  one of: (a) a file the worker must have written that
  exists with the expected mtime, (b) a score artifact
  newer than the dispatch time, or (c) an explicit failure
  message in the conversation. See
  `references/verification-gate.md` for the diagnostic
  recipe.

## How this skill is used

This skill is loaded:

- When the user asks for a new loss function.
- When the user asks to review a candidate loss.
- When the user is debugging a loop that is spiraling or
  mode-collapsing.
- When the user wants to know whether a particular verifier
  is defensible.

The companion `harness-engineering` skill is what the agent
sees. The `cline-orchestration` skill is the surface for
driving a Cline-based loop; for other agent runtimes the
same pattern applies with that agent's CLI flags substituted.

## Related skills (install separately)

- `harness-engineering` — the harness side: context, tools,
  scaffolding, feedback loops.
- `cline-orchestration` — driving a Cline-based loop
  (substitute your own agent orchestration if not using
  Cline).

## External reference

[elvisun/loss-function-development](https://github.com/elvisun/loss-function-development)
— the canonical reference skill that produces
loss-function-design prompts. Invoked as `/lfd-design` in
Claude / Codex. When designing a new loss function for a
project, the output of `/lfd-design` is a good baseline rubric
to start from and adapt. The 4-piece structure (target /
constraints / instruments / forced entropy) it produces is the
same one this skill encodes — don't reinvent the format.
