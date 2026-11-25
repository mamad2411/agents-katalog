---
name: eval
description: Use this skill when running pre-release validation, detecting calibration regression, or tuning a skill — to run plugin evaluation tiers (Tier 1 linters and Tier 2 judge-calibration drift smoke) by wrapping the eval/runner.py harness. Tier 1 is free (no LLM); Tier 2 budgets tokens per `eval/config.json`. Tier 3 (full behavioral suites) is planned but not yet shipped — runner returns error code 3 if invoked.
context: fork
argument-hint: "[skill-name | --tier 1|2 | --rubric NAME]"
---

# /eval — Plugin Evaluation Harness

Validate the plugin against rubric-scored test cases. Two tiers shipped today:

- **Tier 1 — linters** (shipped, free): frontmatter, schema, hook-reference, char-limit, JSON-syntax, AST checks. No LLM calls.
- **Tier 2 — judge-calibration drift smoke** (shipped, opt-in): for each sampled rubric, the Haiku judge scores the shipped good + bad calibration samples, and the result is checked against a ±0.5 score-band tolerance around the score encoded in each filename (`<scenario>.score-X.X.md`). This catches three drift classes:
  1. **Rubric drift** — someone edits the rubric in a way that breaks scoring
  2. **Judge model drift** — Anthropic ships a new Haiku version that scores samples differently
  3. **Sample drift** — someone edits a calibration sample so it no longer hits its band
- **Tier 3 — behavioral** (planned, not shipped): full executor + judge + blind-comparator per skill case. `runner.py --tier 3` currently exits with error code 3.

## When to use

- Pre-release validation — run Tier 1 linters (free, no LLM) across all skills before tagging a release
- Calibration-drift detection — run Tier 2 to catch rubric drift, judge-model drift, or sample drift against the ±0.5 score-band tolerance
- Skill tuning — scope Tier 1 to one skill (`/eval <skill-name>`) or Tier 2 to one rubric (`/eval --tier 2 --rubric <name>`) while iterating
- Release gate — `/eval --all` to run Tier 1 + Tier 2 in a single pass

## Invocation

Shipped commands:

```text
/eval                                  # Tier 1 linters across all skills
/eval feature-design                   # Tier 1 lint scoped to one skill
/eval --tier 2                         # Tier 2 judge-calibration smoke (default 10 rubrics × 2 samples)
/eval --tier 2 --rubric feature-design # Tier 2 limited to one rubric
/eval --tier 2 --dry-run               # plan-only; no API calls (also auto-applies if anthropic SDK unavailable)
/eval --all                            # Tier 1 + Tier 2 in one run
```

Planned (not yet shipped — runner returns error code 3):

```text
/eval --tier 3                         # full behavioral suite (planned)
/eval --skill <name> --tier 3          # Tier 3 per-skill (planned)
/eval --baseline <skill>               # capture per-skill baseline scorecard (planned)
/eval --all --resume                   # resume after interruption (planned, Tier 3 only)
```

## Tier 2 details

Sample plan (default seed 42): 10 rubrics × 2 samples = 20 judge calls. Override via runner flags `--seed N`, `--sample-rubrics N`, `--samples-per-rubric N`, `--rubric NAME`.

Requires `ANTHROPIC_API_KEY` and the `anthropic` Python SDK. Without either, the runner reports `DRY-RUN ONLY` and skips actual API calls.

Default judge model: **Haiku** (`claude-haiku-4-5`). Per-rubric override allowed when calibration Spearman drops below threshold (see `plugin/eval/config.json` → `judge_models`).

## Token budgets

Per `plugin/eval/config.json`:

| Tier | Soft cap | Hard cap | Notes |
|---|---|---|---|
| Tier 1 | 0 | 0 | No LLM. Always free. |
| Tier 2 smoke | 50K | 150K | Default plan ~10–20K with Haiku. |
| Tier 3 (planned) | 30K | 100K | Per-skill (60K/150K with Sonnet judge override). Not shipped. |
| Tier 3 full suite (planned) | 500K | 1.5M | Release-gate run. Not shipped. |

## Output

- Tier 1: stderr findings + summary count of CRITICAL / WARNING. Exit code 0/1/2.
- Tier 2: per-sample PASS/FAIL with score delta + dry-run skip count. Exit code 0/1/2.

## Failure modes

- **Tier 3 invoked:** `runner.py --tier 3` (and any `--baseline`/`--resume`/per-skill Tier 3 form) is not shipped — the runner exits with **error code 3**. Use Tier 1 or Tier 2 instead.
- **Missing API key or SDK:** Tier 2 requires `ANTHROPIC_API_KEY` and the `anthropic` Python SDK. Without either, the runner reports `DRY-RUN ONLY`, skips all API calls, and performs no real scoring.
- **Token cap exceeded:** Tier 2 has a 50K soft / 150K hard cap per `plugin/eval/config.json`; a plan that would breach the hard cap is rejected before any API call.
- **Calibration drift detected:** a sampled good/bad sample scoring outside its ±0.5 band fails (rubric drift, judge-model drift, or sample drift) — exit code 1; inspect the per-sample score delta to localize which class drifted.
- **Future surfaces referenced:** `plugin/eval/cases/` and `plugin/eval/results/` directories do not exist, and the Tier-3 behavioral suite + blind-comparator are not yet wired — relying on those today fails. (The `eval-judge` agent itself *is* shipped — `plugin/agents/eval-judge.md` powers RALF subjective oracles now — but the Tier-3 behavioral path that would invoke it from `/eval` is not yet wired.)

## Integration

- **Wraps**: `plugin/eval/runner.py` (entry) + `plugin/eval/tier2.py` (Tier 2 implementation)
- **Reads**: `plugin/eval/config.json` (token caps + judge models + calibration thresholds)
- **Reads**: `plugin/eval/judge-rubrics/<rubric>.md` (per-rubric scoring criteria)
- **Reads**: `plugin/eval/calibration/<rubric>/{good,bad}/<scenario>.score-X.X.md` (Tier 2 calibration samples — 45 rubrics × 6 samples = 270 total)
- **Honors**: `userConfig.ralph_session_*` caps if eval cases ever trigger embedded RALF (Tier 3, planned)
- **Used by**: `/plugin-doctor --calibrate-judge` (Tier 2 opt-in)

## Future surfaces (not currently wired)

These are referenced by the planned Tier 3 design but **not implemented**:

- `plugin/eval/cases/<skill>/*.json` — per-skill behavioral test cases. Directory does not exist; expect to ship in Phase 4.
- `plugin/eval/results/<run-id>/` — per-run output artefacts.
- Tier-3 behavioral-suite invocation path that wires `plugin/agents/eval-judge.md` (shipped) to `plugin/eval/cases/` + `plugin/eval/results/` — the judge agent exists today; the case/result harness that drives it does not.
- `--baseline <skill>` capture to `.committed/eval-baselines/<release-tag>.json`.
- Blind-comparator (third agent in isolated context with skills suppressed) — design-only.

Do not write code that depends on these surfaces today; they are documented for design continuity, not behavior.
