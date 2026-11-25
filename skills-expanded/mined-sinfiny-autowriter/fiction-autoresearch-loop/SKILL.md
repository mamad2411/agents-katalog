---
name: fiction-autoresearch-loop
description: Use when a user wants to start, continue, or review a benchmarked fiction-improvement loop from an existing piece of writing. Initializes a recorded project structure, benchmarks the current draft from multiple lenses, generates assumption-driven variants, and keeps only improvements that clear the selected benchmark.
---

# Fiction Autoresearch Loop

Use this skill when the task is not merely "write a scene" or "edit this prose," but "run an autoresearch-style improvement loop on fiction."

This skill is the plugin entry point for the repository's intended use.

## Inspirations

This workflow translates two source patterns into long-form fiction:

- `karpathy/autoresearch`: keep a baseline, run bounded experiments, benchmark the result, keep or discard, and log every pass
- `forrestchang/andrej-karpathy-skills`: think before changing anything, keep interventions simple, make surgical edits, and define explicit success criteria

The implication for this plugin is strict:

- the benchmark is the program
- the baseline is mandatory
- variants should be minimal and assumption-driven
- prose cleanup is not a successful loop if the real failure is structural

## Use This Skill To

- start a new loop from an existing chapter, scene, outline, or arc
- continue a previous loop with new assumptions or rewrite levels
- compare multiple variants of the same fiction unit
- keep a clean record of baseline, variants, benchmarks, deltas, and decisions

## First Step

If the story does not already have a project workspace, initialize it with:

```bash
mix aw.init <story-slug> --title "<story title>" --loop <loop-id>
```

Use a loop id like `2026-04-17-baseline`, `2026-04-17-reveal-pass`, or `2026-04-17-arc-repair`.

## Required Project Structure

Keep all loop work under:

```text
runs/<story-slug>/
  README.md
  source/
    input.md
  hypotheses/
    backlog.md
  state/
    characters.md
    timeline.md
    threads.md
  benchmark.md
  loops/
    <loop-id>/
      plan.md
      baseline/
        input-snapshot.md
        benchmark-report.md
      variants/
        <variant-id>/
          assumption.md
          candidate.md
          benchmark-report.md
          delta.md
          decision.md
      summary.md
```

Read `references/run-lifecycle.md` and `references/skill-lens-map.md` before a long run.
Read `references/loop-role-map.md` before deciding which skills should judge, mutate, or guard the run.

## Core Loop

1. Read the current fiction unit from `source/input.md` or the active loop snapshot.
2. Read any relevant hypotheses from `hypotheses/`.
3. Read `benchmark.md`.
4. If the benchmark file is missing, blank, or missing its target unit, scoring lenses, pass floor, or rewrite routing priority, stop and run `$fiction-benchmark-composer` first.
5. Use the skill library as the source of available lenses.
6. Produce a baseline benchmark report in `loops/<loop-id>/baseline/benchmark-report.md`.
7. Identify the highest-level failure:
   - prose
   - scene
   - chapter
   - arc
   - premise
8. Record the rewrite level and the consulted hypotheses in the loop plan before drafting variants.
9. Generate at least three variants unless the user explicitly wants a smaller run.
10. Generate one variant per assumption, not one giant mixed rewrite.
11. For each variant, write:
   - `assumption.md`
   - `candidate.md`
   - `benchmark-report.md`
   - `delta.md`
   - `decision.md`
12. Record which skills were actually used for judging, mutation, and guardrails.
13. Keep a variant only if it improved the intended target under the active benchmark.
14. Write a loop-level `summary.md` that states what to keep, what to discard, and what to test next.

## Benchmark Rule

Treat the benchmark as the real control program for the run.

The benchmark should explicitly define:

- preset or custom profile
- control skill
- guardrails
- mutators
- scoring lenses and weights
- pass floor
- minimum variants
- rewrite routing priority

Do not begin substantive revision against an underspecified benchmark.

## Assumption Discipline

Each variant should test one main assumption only, for example:

- the chapter needs a stronger opening tradeoff
- the protagonist should act earlier
- the reveal order is wrong
- the scene is failing due to missing subtext, not weak prose
- the benchmark is overweighting readability and underweighting consequence

Do not combine multiple major hypotheses into one variant unless the benchmark itself demands a chapter- or arc-level rewrite.

Keep hypotheses separate from skills:

- hypotheses describe what might improve the work
- skills are the reusable tools that can test that hypothesis
- the run artifacts should record which skills were actually used

When possible, diversify variants by rewrite style:

- one structural or ordering change
- one character-pressure change
- one prose or pacing change

This keeps the loop from producing three near-identical paragraph polishes.

## Rewrite Escalation Rule

If the baseline identifies a scene, chapter, arc, or premise failure:

- do not default to sentence cleanup
- do not call prose cleanup a successful loop
- force at least one structural variant at the diagnosed level
- use prose mutators only as secondary cleanup after the structural issue is addressed

## Skill Routing

Use repository skills as evaluative or generative lenses inside the loop.

Start from this default route for `default-webserial`:

- `$creative-autoresearch-control-plane` for the top-level control decision
- judges:
  - `$mystery-payoff-and-fairness-judge`
  - `$narrative-hook-hold-payoff`
  - `$narrative-epistemic-targeting`
  - `$strategic-webserial-architecture`
- guardrails:
  - `$narrative-explicit-reasoning`
- conditional judges:
  - `$strategic-cast-intelligence-engine`
  - `$faction-power-consequence-engine`
  - `$narrative-contextual-prose-density`
- mutators:
  - `$narrative-auto-reasoning`
  - `$narrative-minimum-viable-prose`
  - `$narrative-surgical-editing`
  - `$sanderson-promise-progress-payoff`
  - `$sanderson-story-architecture`
  - `$sanderson-character-engine`

For preset-specific work:

- use `$narrative-subtext-mapping` as a core judge in `interaction-heavy`
- use `$grainbound-causal-worldbuilding` as a core judge in `worldbuilding-pressure`
- use `$autonomous-webserial-loop` only when the user explicitly wants the stricter mystery-heavy preset controller

Use extra lenses from `references/skill-lens-map.md` when composing a custom benchmark.

## Role Rule

Skills should play one of four roles in a run:

- `controller`
- `judge`
- `mutator`
- `guardrail`

Do not use a mutator as if it were a judge.
Do not use a judge as if it were the whole loop.
Do not use every available skill in one benchmark.

## Output Contract

For each active loop, the final status should be legible from files alone.

Write the following minimum summary:

```text
Target unit:
Benchmark profile:
Baseline result:
Highest-level failure:
Rewrite level:
Hypotheses consulted:
Judges used:
Mutators used:
Actual skills used:
Variants tested:
Variant kept:
Why it won:
What was discarded:
Next loop:
```

## Rules

- Do not overwrite the user's original input. Preserve it in `source/input.md` and snapshot it in each loop.
- Do not start revising against an empty benchmark template.
- Do not collapse the run into one rewritten draft when multiple variants were required.
- Do not merge variants prematurely. Benchmark them separately first.
- Do not keep a variant because it feels nicer if it did not improve the benchmark target.
- Do not polish prose if the benchmark shows a scene, chapter, arc, or premise failure.
- Prefer a simpler successful intervention over a sprawling one with similar scores.
- Every kept change should be explainable as a benchmark improvement, not just an aesthetic preference.
