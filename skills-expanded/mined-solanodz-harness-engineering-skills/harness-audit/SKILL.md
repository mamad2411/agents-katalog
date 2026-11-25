---
name: harness-audit
description: >-
  Scores your project setup 0–100 and shows what to fix first. Use when the
  agent keeps failing, before improving a harness, or to see which subsystem
  is the bottleneck (instructions, state, verification, scope, lifecycle).
---

# Harness Audit

## What this does for you

- **See what's weak** — score 0–100 across five areas
- **Know where to start** — highlights the likely bottleneck
- **Stop guessing** — concrete checklist instead of vague "make it better"

Based on Lesson 02 (five subsystems) and the course audit exercise.

## Run automated audit

```bash
node scripts/validate-harness.mjs --target /path/to/project
node scripts/validate-harness.mjs --target /path/to/project --json
node scripts/render-assessment-html.mjs --target /path/to/project
```

Exit code ≠ 0 if overall score < 70 (configurable with `--min-score`).

## Manual checklist by subsystem

Rate each subsystem from 1 to 5:

### 1. Instructions (1–5)

- [ ] `AGENTS.md` or `CLAUDE.md` exists
- [ ] Explicit startup flow (what to read, in what order)
- [ ] Verification commands listed and copy-pasteable
- [ ] ≤ ~100 lines in root file (progressive disclosure to `docs/`)
- [ ] Clear definition of done

### 2. State (1–5)

- [ ] `feature_list.json` or equivalent machine-readable tracker exists
- [ ] `progress.md` or `claude-progress.md` exists
- [ ] State reflects reality (not aspirational)
- [ ] Git history complements on-disk state

### 3. Verification (1–5)

- [ ] `init.sh` or equivalent documented commands exist
- [ ] Tests/lint/type-check are runnable by the agent
- [ ] Smoke test or e2e is documented
- [ ] Agent cannot mark done without evidence

### 4. Scope (1–5)

- [ ] One active feature at a time
- [ ] Features have observable verification criteria
- [ ] Dependencies between features are documented
- [ ] No silent rewriting of the feature list

### 5. Lifecycle (1–5)

- [ ] init.sh verifies environment health before work
- [ ] Handoff template exists (`session-handoff.md`)
- [ ] Clean-state checklist at session close
- [ ] Commit only when safe to resume

## Report to user

Format:

```markdown
## Harness Audit: [project]

| Subsystem | Score | Status |
|-----------|-------|--------|
| Instructions | X/5 | ... |
| State | X/5 | ... |
| Verification | X/5 | ... |
| Scope | X/5 | ... |
| Lifecycle | X/5 | ... |

**Likely bottleneck**: [lowest subsystem]

**Top 3 improvements** (ordered by impact):
1. ...
2. ...
3. ...
```

## Ablation (optional)

To quantify marginal value of each component (Lesson 02, exercise 2):

1. Fix model and task
2. Remove ONE subsystem at a time (e.g. delete AGENTS.md)
3. Measure performance drop
4. Combine with failure logs — largest drop suggests but does not prove the bottleneck

## Next step

Based on the weakest subsystem, invoke the corresponding skill:

- Instructions → `harness-instructions`
- State → `harness-state`
- Verification → `harness-verification` or `harness-e2e`
- Scope → `harness-scope`
- Lifecycle → `harness-lifecycle`

For a **specific repeated failure**, use `harness-diagnose` before re-auditing. For **done-but-wrong** outcomes, use `harness-evaluator`.
