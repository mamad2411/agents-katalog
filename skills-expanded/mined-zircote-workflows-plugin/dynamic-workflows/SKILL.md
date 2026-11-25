---
name: dynamic-workflows
description: Apply a consistent set of orchestration patterns whenever writing or reviewing a Claude Code dynamic workflow script (the Workflow tool — agent/parallel/pipeline/phase/log/workflow/args/budget). Use before authoring any workflow script, when the user says "use a workflow", "ultracode", "orchestrate this with subagents", or asks to review/harden an existing workflow script for full use of pipeline, verification, and budget patterns. Anti-trigger; for spawning a single one-off subagent with no multi-stage structure, use the Agent tool directly instead.
argument-hint: "<the task to orchestrate as a dynamic workflow (optional)>"
---

# dynamic-workflows

Gives every dynamic workflow script you write a consistent, load-bearing
structure instead of an ad-hoc pile of `agent()` calls. It combines two
sources that play different roles:

- **`reference/api.md`** (authoritative) — distilled from Anthropic's own
  dynamic-workflows docs and the `Workflow` tool's own spec. This is the
  actual mechanics: what `agent()`/`parallel()`/`pipeline()`/`workflow()`
  do, what the runtime enforces (determinism, concurrency caps, no mid-run
  input), and what the tool's own quality-pattern guidance says. **When in
  doubt about what a call does or what's allowed, this file is the one that's
  right.**
- **`reference/patterns.md`** (semantic framework) — a vocabulary layer
  distilled from the field note *"Dynamic Workflow Design Patterns"*
  (zircote, July 2026): 20 named patterns across four families plus 8 named
  anti-patterns, GoF-style. This gives shapes names ("Scout-Worker",
  "Adversarial Verify", "Loop-Until-Dry") so a script's structure can be
  discussed and reused instead of reinvented per task. **It is a naming and
  decision-making convenience over the API, not a second spec** — if a
  pattern description and the API reference ever seem to conflict, the API
  reference is correct and the pattern's phrasing should be read loosely.

Both sources are vendored under `vendor/` with a `VENDOR.lock` recording
where each came from and when it was last refreshed — see the plugin
[README](../../README.md) for how to re-hydrate them as the product and the
field note evolve.

## Before writing any workflow script

1. **Confirm the opt-in.** Only write a `Workflow` call when the user
   actually asked for multi-agent orchestration (their own words, the
   `ultracode` keyword, a skill/command that says to, or a named saved
   workflow) — see `reference/api.md` for the exact bar. Otherwise use the
   `Agent` tool directly, or describe the option and ask.
2. **Pick the shape before the items.** You don't need to know the exact
   work-list up front, but decide the *pattern* first: is this a known list
   to fan out over (Streaming Pipeline), an unknown-size discovery problem
   (Loop-Until-Dry), a fix-and-recheck loop (Converge-Until-Green), or a plan
   that needs to be weighed from several angles (Judge Panel)? See the
   decision guide at the end of `reference/patterns.md`.
3. **Default to `pipeline()`, not `parallel()`.** Reach for a barrier only
   when a stage genuinely needs the complete prior result set (dedup,
   aggregate branching, ranking). This single habit avoids the catalog's
   most common mistake, *Barrier Abuse* — see `reference/api.md`'s
   "pipeline() vs parallel()" section for the smell test.
4. **Schema every `agent()` call that feeds another call.** Bind `schema` on
   anything downstream code or another agent will consume; free-text parsing
   between stages is the *Free-Text Parsing* anti-pattern and silently
   forfeits the ability to route that stage to a cheaper model.
5. **Decide the verification story up front**, not as an afterthought: does
   a finding need *Adversarial Verify* (independent skeptics, majority vote),
   *Perspective-Diverse Verify* (distinct lenses), or a *Test Gate* (an
   executable oracle)? "More agents" alone does not raise confidence —
   arranging agents to check each other does.
6. **Guard every unbounded construct**: a `budget`-driven loop must check
   `budget.total != null` before looping on `budget.remaining()`; a
   discovery loop must have a round cap or a K-consecutive-empty-rounds stop
   condition. Both are the entry point for the *Unbounded Loop*
   anti-pattern.
7. **Use `log()` at every meaningful milestone.** Nothing that happens
   inside a running workflow reaches the conversation except the final
   return value — the progress view and `log()` lines are the only window
   into a background run while it's going.

## Reviewing an existing workflow script

Walk it against the 8 named anti-patterns in `reference/patterns.md` (Barrier
Abuse, The Impatient Monitor, Hidden Clock, Context Flood, Mid-Run
Conversation, Unbounded Loop, Free-Text Parsing, Monolithic Agent) before
suggesting changes — each has a one-line symptom and a named fix. Then check
it against the hard constraints table in `reference/api.md` (determinism,
concurrency/agent caps, batch-size limits, no mid-run input) — those are
enforced by the runtime, not stylistic preferences, so a violation there is a
bug, not a style note.

## Quick pattern index

| Need | Reach for |
|---|---|
| Process a known list of items, multi-stage | Streaming Pipeline (default) |
| A later stage needs the *whole* result set first | Barrier Rendezvous (`parallel`) |
| The item list isn't known yet | Scout-Worker |
| Reuse a proven orchestration as one step | Sub-Workflow Composition (`workflow()`) |
| Concurrent writers to the same files | Worktree Isolation |
| Unknown-size discovery (bugs, flaky tests, edge cases) | Loop-Until-Dry |
| Fix-and-recheck against a compiler/linter/test suite | Converge-Until-Green |
| Depth should scale to a token target | Budget-Scaled Depth |
| Human sign-off needed mid-task | Phase-Gated Staging (separate workflows) |
| Stages vary widely in required judgment | Model Routing |
| A finding needs independent confirmation | Adversarial Verify |
| A finding can fail in more than one way | Perspective-Diverse Verify |
| Wide solution space, want best-of-N | Judge Panel |
| Research/fact-heavy synthesis | Cross-Checked Claims |
| An executable oracle exists | Test Gate |
| Any multi-stage data handoff | Structured Output Contract (always) |
| Round-based dedup | Seen-Set Ledger |
| Fan-out where agents may die | Null-Tolerant Collection (always) |
| Workflow will be saved and reused | Parameterized Command |

Full pattern entries, applicability, and consequences: `reference/patterns.md`.
Full API mechanics, limits, and canonical code examples: `reference/api.md`.
