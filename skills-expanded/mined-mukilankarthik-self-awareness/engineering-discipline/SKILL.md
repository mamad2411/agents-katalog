---
name: engineering-discipline
description: Behavioral guidelines to reduce common agent coding mistakes — thinking before coding, simplicity, surgical changes, goal-driven execution, and mandatory verification for data/BI work. Adapted from andrej-karpathy-skills (MIT), with a data/BI engineering layer added. Use this skill whenever writing, editing, or reviewing code, and especially before any change to a data pipeline, fact table, or stored proc.
---

# Engineering Discipline

Sections 1-4 are adapted from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (MIT) — Forrest Chang's write-up of [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls, which Karpathy then amplified. Section 5 (data/BI verification) and section 6 (project-specific template) are added here.

**Tradeoff:** these rules bias toward caution over speed. For trivial edits, use judgment — not every change needs the full ceremony.

**This is behavioral context, not a contract.** Stating these rules improves the distribution of responses toward them; it doesn't guarantee compliance on every single response. Treat a lapse as a signal to re-check the diff, not proof the rules failed.

## 1. Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

- State assumptions out loud before implementing. If uncertain, ask instead of guessing.
- When a request has more than one reasonable reading, present both. Don't silently pick one.
- If a simpler approach exists, say so. Push back when the pushback is warranted.
- When something is unclear, stop and name exactly what is unclear. A vague "let me know if that's not right" at the end doesn't count.

## 2. Simplicity first

The minimum that solves the stated problem. Nothing speculative.

- No features that weren't asked for.
- No abstraction layer for something used once.
- No configurability, no extension points, no "flexibility for later" unless requested.
- No error handling for cases that can't occur.
- If it came out at 200 lines and 50 would do, rewrite it.

Test: would a senior engineer reviewing this call it overbuilt? If yes, cut it.

## 3. Surgical changes

Touch only what the task requires. Clean up only your own mess.

- Don't "improve" adjacent code, comments, naming, or formatting.
- Don't refactor what isn't broken.
- Match the surrounding style even where you'd personally do it differently.
- Spot unrelated dead code? Mention it. Don't delete it.
- Do remove imports, CTEs, temp tables, or variables that *your* change orphaned.

Test: every changed line traces directly back to the request.

## 4. Goal-driven execution

Define success criteria up front, then loop until they're met. Strong criteria let you run independently; "make it work" guarantees a round trip.

For multi-step work, state the plan as steps paired with checks:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Reframe imperatives as verifiable goals — see `references/goal-driven-execution.md` for the full reframing table (e.g. "Fix the bug" → "Write a test that reproduces it, then make it pass").

## 5. Verification for data and BI work

Data pipelines have no test suite to hide behind, and the failure mode is silent wrong numbers rather than a stack trace. Before touching a fact table, stored proc, or reference data, read `references/data-verification.md` in full — it covers grain, reconciliation queries, snapshot/SCD date-key filters, fan-out joins, and environment promotion rules. Do not skip it because the change "looks small."

## 6. Project-specific

Every repo this skill is dropped into should fill in its own specifics: environments and naming conventions, which control tables require insert-then-swap, tables too large for an ad-hoc full scan, and where deployment scripts and review process live. Use `references/project-specific-template.md` as the starting shape and fill it in per project — don't leave it as a placeholder.

## These guidelines are working if

- Diffs contain only requested changes.
- Clarifying questions arrive before implementation rather than after a bad run.
- Every data change comes with the reconciliation output attached.

## Reference Files

- `references/examples.md` — concrete before/after code examples for each principle
- `references/goal-driven-execution.md` — imperative-to-verifiable-goal reframing table, with examples
- `references/data-verification.md` — grain, reconciliation queries, SCD/snapshot filters, fan-out checks, environment promotion
- `references/project-specific-template.md` — template to fill in per repo (naming conventions, control tables, deployment process)

## Sources

- https://github.com/multica-ai/andrej-karpathy-skills
- https://www.towardsdeeplearning.com/a-single-claude-md-file-went-viral-the-reason-is-embarrassingly-simple-5b515c9e4cca
