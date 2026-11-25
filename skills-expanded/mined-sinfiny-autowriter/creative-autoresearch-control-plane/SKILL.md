---
name: creative-autoresearch-control-plane
description: Use when AI should run an autoresearch-style loop for creative writing, iterating on chapters, reveals, arcs, and webserial hooks against explicit rubrics, benchmark cases, and rewrite decisions instead of stopping at the first plausible draft.
---

# Creative Autoresearch Control Plane

Use this skill when the task is not just "write a story" but "improve a story through repeated judged experiments."

This is the control-layer skill for the repository's autonomous creative workflow.

## Quick Start

Use this skill when you need to:

- iterate on a chapter until it clears a quality bar
- benchmark one draft against another
- choose whether to rewrite prose, scene logic, chapter design, or arc structure
- improve addictive webserial properties such as hook strength, mystery carry, payoff, and strategic protagonist appeal

Pair with:

- `$strategic-webserial-architecture`
- `$faction-power-consequence-engine`
- `$strategic-cast-intelligence-engine`
- `$mystery-payoff-and-fairness-judge`
- `$autonomous-webserial-loop`

Read `references/system-map.md` first.

## Core Idea

Treat creative writing the way `autoresearch` treats model improvement:

- keep the editable surface constrained
- keep the evaluation budget explicit
- score outputs against a stable rubric
- keep or discard revisions based on judged improvement

The evaluator is the product. Generation is only one component.

## Operating Loop

1. Define the target unit:
   - opening chapter
   - chapter draft
   - reveal beat
   - confrontation
   - arc scaffold
2. Define the objective:
   - stronger retention
   - better clue fairness
   - more strategic character play
   - stronger leaderboard fit
3. Select or compose the benchmark in `runs/<story-slug>/benchmark.md`.
4. Select the skill lenses that will judge, guard, and mutate the run.
5. Produce or revise the unit under test.
6. Judge it with the local and chapter-level rubrics.
7. Decide the highest-level failure:
   - prose
   - scene
   - chapter
   - arc
   - premise
8. Apply only the necessary rewrite level.
9. Log the iteration under `runs/<story-slug>/loops/<loop-id>/`.
10. Stop when the unit clears the bar or when more iteration would require new author intent.

## Output Contract

```text
Target unit:
Objective:
Benchmark class:
Rubrics used:
Current strengths:
Current failures:
Highest-level repair:
Planned intervention:
Revised output or revised plan:
Judge delta:
Stop or continue:
```

## Rules

- Do not polish prose while structural failure is unresolved.
- Do not approve a draft because it feels smooth if it weakened obsession, tension, or payoff.
- Do not use benchmark rubrics as aesthetic dogma. They are instruments, not sacred law.
- Do not compare against copyrighted stories by imitation. Compare against abstract craft behaviors.
- Prefer measurable progress over vague approval.
