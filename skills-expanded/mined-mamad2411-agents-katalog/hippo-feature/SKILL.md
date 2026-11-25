---
name: hippo-feature
description: Build one hippo feature from RESEARCH.md using the micro-eval TDD loop.
disable-model-invocation: true
---

You are entering **hippo-feature mode** to build a new memory mechanic from `RESEARCH.md`. Follow the eval pyramid strictly. Skipping tiers wastes hours of LoCoMo time.

## The eval pyramid (non-negotiable)

| Tier | Harness | Time | When |
|------|---------|------|------|
| 1 | `benchmarks/micro/run.py` | ~30s | Every code change |
| 2 | `benchmarks/locomo/run.py --conversations 1 --sample 10 --score-mode evidence` | ~5-10 min | Before opening a PR |
| 3 | LoCoMo full | ~85 min evidence / ~6h judge | Release gate only |

If a feature shows no Tier 1 signal, do not proceed to Tier 2. If Tier 2 shows a regression, do not run Tier 3.

## The loop

### 0. Pick the feature

If `$ARGUMENTS` names a feature (e.g. `acc-evc`, `vmpfc-value`, `dlpfc-goals`, `vlpfc-gate`, `pineal-salience-v2`), use it. Otherwise read the PFC priority table in `RESEARCH.md`, pick the top feature by effort × benchmark delta, and say in one line which you picked and which two you passed over.

### 1. RED: Write the failing micro fixture FIRST

- Drop a fixture at `benchmarks/micro/fixtures/<feature>.json` with shape:
  ```json
  {
    "name": "<feature>-<aspect>",
    "mechanic": "<feature>",
    "description": "<one sentence: what behaviour this proves>",
    "remembers": [...],
    "queries": [{"q": "...", "must_contain_any": [...], "top_k": N}]
  }
  ```
- The fixture must encode behaviour the *current* system **cannot** satisfy. If it passes on main today, the fixture is wrong; make it harder.
- Run `python benchmarks/micro/run.py --filter <feature>` and confirm it fails.
- Save the failing baseline: `python benchmarks/micro/run.py --out benchmarks/micro/results/baseline-<feature>.json`.

### 2. PLAN: Outside voice on non-trivial features

Per global CLAUDE.md outside-voice rule: if the feature touches schema, retrieval ranking, or storage (i.e. anything in the PFC priority table), run `/plan-eng-review` on the implementation plan **before** writing code. Skip only for one-line tweaks.

### 3. GREEN: Minimum implementation

- Smallest diff that makes the fixture pass.
- No new abstractions, no speculative config flags, no "while I'm here" cleanups.
- After each change, `python benchmarks/micro/run.py --filter <feature>` until it passes.

### 4. REGRESSION CHECK: Run all micro fixtures

- `python benchmarks/micro/run.py`: every existing fixture must still pass.
- If any fixture regresses, revert and reconsider. Do not "improve" the regressed fixture to make it pass.

### 5. TIER 2 SMOKE: Stratified LoCoMo subsample

```powershell
$env:HIPPO_BIN="node $HOME/hippo/bin/hippo.js"
python benchmarks/locomo/run.py `
  --data benchmarks/locomo/data/locomo10.json `
  --output-dir benchmarks/locomo/results `
  --output-name hippo-smoke-<feature> `
  --conversations 1 --sample 10 `
  --score-mode evidence
```

- Compare `mean_score` to the most recent smoke baseline.
- Required: non-negative delta on the affected categories. Variance dominates absolute scores at N=50, so trust the *direction*, not the level.
- If delta is negative, return to step 3.

### 6. COMMIT

- One logical commit per feature: code + fixture + result baseline.
- Reference the RESEARCH.md section in the commit body (e.g. `RESEARCH.md §4.3 ACC EVC-adaptive recall`).
- Never use `--no-verify`.

### 7. STOP: Do not run Tier 3

Full LoCoMo only on explicit user request (release gate). Even with a green Tier 2, do not run the 5-8 hour LoCoMo full unless the user asks.

## Hard rules

- **One feature at a time.** Don't bundle ACC + vmPFC into one branch even if RESEARCH.md groups them.
- **Real DB for tests.** No mocks where the real SQLite store is feasible.
- **Power models: DO NOT TOUCH**, in every repo.
- **Salience gate.** The v1 60% lexical-overlap gate destroyed LoCoMo from 0.28 to 0.02. Any salience work must be default-off and prove a positive delta on Tier 2 before being enabled.

## Pre-flight checks (run before step 1)

- `python benchmarks/micro/run.py`: baseline must currently be 1.00 pass rate
- `node bin/hippo.js --version`: record the starting version for the commit

## Proactivity: DEFAULT MODE (full-power)

This command runs in **full-power proactive mode**. Decide, act, report the decision in one line.

- **Dirty WIP on master?** Commit it to a `wip/<feature>-pre` branch (preserve, don't lose), reset master, then create `feat/<feature>` clean. Never overwrite WIP. Never block on it.
- **Already on a feature branch?** Continue on it.
- **On master with clean tree?** Create `feat/<feature>` and switch.
- **Outside-voice plan review?** Spawn a `senior-code-reviewer` sub-agent inline against the plan. Don't pause and ask the user to invoke `/plan-eng-review`.
- **Tier 2 smoke (5-10 min)?** Run in background; keep working on docs/commit prep; report on completion.
- **Real stop-points** (failing fixture after honest attempt, plan rejected by reviewer, Tier 2 negative delta, hippo CLI broken): surface those. Housekeeping is not a stop-point.

The user has authorised proactive execution. Ask only at real forks in the road.

---

Task / feature: $ARGUMENTS

If `$ARGUMENTS` is empty, pick the feature per step 0.
