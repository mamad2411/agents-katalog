---
name: "skill-hyper-sweeper"
description: "Runs N parallel variants of any skill with hyperparameter sweep (temp, top_p, prompt emphasis, system bias) then ranks outputs. Invoke BEFORE skill execution to maximize quality when stakes are non-trivial."
---

# Skill Hyper-Sweeper — N Parallel Variants → Best Output

Inspired by hyperparameter sweeps (sweeps.md). Every skill invocation = random seed. Run 3–9 variants, pick best. Target: +30%–+200% output quality / completeness over single-run.

## Trigger Conditions (ANY true → RUN)
- Task is non-trivial (code ≥20 lines / writing ≥5 paragraphs / design / refactor)
- User says: "maximize", "improve", "best", "better output", "sweep", "variants"
- Stakes: code that runs in production, launch copy, paid ad creative, deployment config
- Skill invoked ≥2 turns ago and user repeated request ("try again", "improve this")

## Sweep Grid (3 variants = default, 7 = high, 9 = max)
| Variant # | temperature | top_p | system_bias | prompt_emphasis | seed |
|---|---|---|---|---|---|
| 1 (BASE) | SKILL DEFAULT | SKILL DEFAULT | neutral | default | 1 |
| 2 (PRECISION) | temp × 0.55 | top_p × 0.7 | favor_correctness | explicit | 2 |
| 3 (CREATIVE) | min(temp × 1.55, 1.1) | min(top_p × 1.25, 0.99) | favor_originality | examples_first | 3 |
| 4 (COMPACT) | temp × 0.7 | top_p × 0.75 | favor_concision | remove_fillers | 4 |
| 5 (THOROUGH) | temp × 1.05 | top_p × 0.95 | favor_completeness | enumerate_examples | 5 |
| 6 (EDGE CASES) | temp × 0.85 | top_p × 0.85 | favor_edge_cases | test_cases | 6 |
| 7 (SIMPLIFY) | temp × 0.6 | top_p × 0.8 | favor_readability | short_paragraphs | 7 |
| 8 (OPTIMIZE) | temp × 0.9 | top_p × 0.9 | favor_performance | benchmarks | 8 |
| 9 (ALL BALANCED) | temp × 1.0 | top_p × 0.9 | neutral_balanced | all_criteria | 9 |

Default = V1+V2+V3 (3 variants). High = V1..V7 (7). Max = all 9.

## Selection Algorithm (Pick Best Variant)
Run ALL variants in parallel, then score each 0-100 on 4 dimensions (25pt each):
1. **Relevance** (25): % of user intent checkboxes covered
2. **Correctness** (25): factual/code checks passed, no errors, valid syntax
3. **Completeness** (25): edge cases covered, TODOs explicit, boundaries documented
4. **Actionability** (25): concrete steps, runnable, examples, copy-pasteable
Pick variant with HIGHEST total. If tie ≤5pt → merge best fragments from both into hybrid output.

## Output Wrapper (POTENCY MARKER)
Prepend the following 1-line header to output so downstream skills know this was swept:
```
[SWEPT N_VARIANTS=<n> BEST_SCORE=<0-100> SELECTED=<V#> HYBRID=<yes/no> SAVINGS_RATIO=<x>]
```

## Token Cost Amortization
Sweep cost = N × single_run_cost. BUT quality gain +30%–200% means fewer re-runs. Rule of thumb:
- If task rework probability ≥30% → RUN SWEEP (expected value positive)
- If task has hard correctness gate (code, math, legal) → ALWAYS RUN
- BUDGET guard: sweep tokens ≤ 1/3 of remaining session budget (auto cap variants N)

## Integration with Core Stack
- Hooks BEFORE skill execution: prediction engine → if "high stakes" flag → boost N
- Hooks AFTER skill execution: merge best results → send to output-minifier
- Cache: each variant result cached FOREVER by (skill, variant_id, input_hash)
- Cross-platform: variant_id list shared so 21 platforms reuse exact same seeds

## Disable String (exact match only, case-sensitive)
`SKILL_HYPER_SWEEPER_DISABLE_FULL_CONFIRM_88888`
