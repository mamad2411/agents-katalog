---
name: fiction-benchmark-composer
description: Use when defining or revising a fiction benchmark for a story, chapter, scene, reveal, confrontation, or arc by selecting evaluation lenses from the repository's skill library. Produces a reusable benchmark profile that can be applied across variants in an autoresearch loop.
---

# Fiction Benchmark Composer

Use this skill when the user wants to define the benchmark itself instead of only running against the default repository benchmark set.

This skill makes it trivial to create a custom benchmark by selecting a small set of repository skills as lenses and turning them into a reusable profile.

The benchmark is the loop's program.
If the benchmark is vague, the loop will drift toward shallow edits.

## When To Use

- a story needs a benchmark different from the default strategic-webserial emphasis
- the user wants to emphasize specific qualities such as subtext, clue fairness, pace, world logic, or strategic intelligence
- a loop is failing because the current benchmark is too broad or too vague
- multiple variants need to be compared against the same custom target

## Inputs

Read:

- `skills/`
- `../fiction-autoresearch-loop/references/skill-lens-map.md`

Write or update:

```text
runs/<story-slug>/benchmark.md
```

## Composition Workflow

1. Define the target unit:
   - opening
   - scene
   - chapter
   - reveal
   - confrontation
   - arc scaffold
2. Define the intended outcome:
   - stronger retention
   - smarter cast behavior
   - better clue fairness
   - stronger consequence density
   - clearer prose under complexity
   - denser subtext
3. Choose one control skill.
4. Choose two to four scoring lenses.
5. Choose any required guardrails.
6. Choose the mutators that are allowed to generate candidate variants.
7. Define scoring dimensions and weights.
8. Define the pass floor.
9. Define rewrite routing priorities.
10. Define the minimum number of variants to test.
11. Save the profile so later variants can be judged against the same target.

The benchmark should not be the hypothesis backlog.
Keep hypotheses separate and let the run record which hypotheses and skills were actually used.

## Output Contract

Use the profile shape in `references/benchmark-profile-contract.md`.

At minimum, the benchmark should define:

```text
Target unit:
Objective:
Controller:
Judges:
Guardrails:
Allowed mutators:
Scoring dimensions:
Pass floor:
Rewrite routing priority:
Minimum variants:
Stop rule:
```

## Rules

- Prefer the fewest skills that fully describe the benchmark.
- Every chosen skill should have an explicit role: controller, judge, mutator, or guardrail.
- Use judges to score, mutators to generate, and guardrails to prevent bad diagnosis.
- If the target unit is a chapter and the failure is structural, include at least one structural judge.
- Do not create a benchmark that mixes contradictory success criteria without stating the tradeoff.
- If a benchmark overfits one style preference, say so explicitly.
- If the benchmark is meant to compare variants, keep it stable for the whole loop.
- Change the benchmark only when the current one is clearly mis-scoring the work.
