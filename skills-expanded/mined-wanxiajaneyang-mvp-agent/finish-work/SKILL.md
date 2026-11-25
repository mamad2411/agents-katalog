---
name: finish-work
description: "Finish Work - Pre-Completion Checklist"
---

# Finish Work - Pre-Completion Checklist

Before treating a task as done, use this checklist to ensure the repo, specs, and Trellis state all line up.

**Timing**: After code or docs are updated and before you hand off, commit, merge, or record completion.

---

## Checklist

### 1. Verification

```bash
python -m ruff check apps tests scripts tools
python -m mypy apps tools
python scripts/validate_artifacts.py
python scripts/validate_decision_record_schema.py
python -m compileall -q apps tests scripts tools
python evals/run_eval_suite.py
python -m unittest discover -s tests -t . -p "test_*.py" -v
```

- [ ] Ruff lint passes for touched files?
- [ ] Mypy type check passes?
- [ ] Relevant validation commands passed for the files you touched?
- [ ] Python code compiles cleanly?
- [ ] Unit tests pass?
- [ ] Eval suite passes when models or validators changed?
- [ ] Modeling/schema validators still pass when relevant?

### 2. Code-Spec Sync

- [ ] Does `.trellis/spec/backend/` need updates?
- [ ] Does `.trellis/spec/frontend/` need updates?
- [ ] Does `.trellis/spec/guides/` need updates?

**Rule**:
If you changed a contract, convention, guardrail, or non-obvious workflow detail, update the relevant spec before treating the work as complete.

### 3. Public Contract Changes

If you modified a public contract:
- [ ] Function signature or payload shape documented?
- [ ] Callers and tests updated to match?
- [ ] Modeling/spec docs updated if the contract is part of planned architecture?

### 4. Persistence or Schema Changes

If you modified database schema or persistence rules:
- [ ] `artifacts/modelling/data_model.md` updated if runtime schema expectations changed?
- [ ] Validation or fixture data updated?
- [ ] Related scripts/tests updated?

### 5. Cross-Layer Verification

If the change spans multiple layers:
- [ ] Typed enums/dataclasses/dicts remain consistent across layers?
- [ ] Errors are propagated intentionally?
- [ ] Budget/paywall/citation guardrails still hold?

### 6. Trellis State

- [ ] Active Trellis task still reflects the work in progress?
- [ ] Session recording will not create a hidden commit unless explicitly intended?
- [ ] The work should be recorded in `.trellis/workspace/` when finished?

---

## Quick Check Flow

```bash
python -m ruff check apps tests scripts tools
python -m mypy apps tools
python -m compileall -q apps tests scripts tools
python -m unittest discover -s tests -t . -p "test_*.py" -v
git status
git diff --name-only
```

---

## Common Oversights

| Oversight | Consequence | Check |
|-----------|-------------|-------|
| Code-spec docs not updated | Others don't know the change | Check `.trellis/spec/` |
| Runtime/model schema drift | Planned contracts diverge from code | Check `artifacts/modelling/` and tests |
| Types not synced | Runtime errors | Check enums, dataclasses, dict keys |
| Tests not updated | False confidence | Run the relevant suite |
| Hidden auto-commit behavior | Surprise commits in docs-only sessions | Check `add_session.py` flags |

---

## Relationship to Other Commands

```text
Development Flow:
  Write code -> Verify -> $finish-work -> commit/handoff -> $record-session
```

- `$finish-work` - completeness check
- `$record-session` - Trellis workspace/task recording
- `$break-loop` - bug-analysis follow-up when needed

---

## Core Principle

Complete work = verified change + synced specs + correct Trellis state.
