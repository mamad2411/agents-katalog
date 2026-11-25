---
name: check-cross-layer
description: "Cross-Layer Check"
---

# Cross-Layer Check

Check whether a change considered the boundaries between runtime code, modelling docs, validators, and tests.

> **Note**: Read `.trellis/spec/guides/pre-implementation-checklist.md` before implementation when a task changes cross-layer contracts.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `.trellis/spec/guides/pre-implementation-checklist.md` | Questions before changing contracts |
| `.trellis/spec/guides/code-reuse-thinking-guide.md` | Pattern recognition and drift checks |
| `.trellis/spec/guides/cross-layer-thinking-guide.md` | Data-flow and ownership thinking |

---

## Execution Steps

### 1. Identify Change Scope

```bash
git status
git diff --name-only
```

### 2. Check Cross-Layer Data Flow

Typical layers in this repo:
- Runtime / orchestration: `apps/agent/orchestrator.py`, `apps/agent/runtime/`
- Pipeline / domain logic: `apps/agent/pipeline/`, `apps/agent/ingest/`, `apps/agent/retrieval/`, `apps/agent/synthesis/`
- Persistence / modelling: `artifacts/modelling/`, fixtures, schemas
- Validation / scripts: `apps/agent/validators/`, `scripts/`
- Tests: `tests/agent/`

Checklist:
- [ ] Are contract fields consistent across code, docs, and tests?
- [ ] Are errors propagated intentionally?
- [ ] Are budget/paywall/citation guardrails preserved?
- [ ] Did fixture or schema files need updates too?

### 3. Check Reuse and Drift

```bash
rg -n "value-to-change|patternYouChanged|ConceptName" apps tests scripts artifacts
```

Checklist:
- [ ] Did you search for all usage sites before changing a shared value?
- [ ] Are there repeated dict keys, statuses, or enum values that should stay aligned?
- [ ] Did a helper already exist before adding a new one?

### 4. Report Outcome

Summarize:
1. Which layers were touched
2. What was verified
3. Any remaining sync risk between code, modelling artifacts, and tests
