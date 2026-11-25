---
name: refactor
description: Use this skill when breaking up large functions, migrating to new patterns, extracting to a library, or improving testability — to plan and execute a code refactor that changes structure without changing behavior via a multi-agent pipeline with a mandatory test-equivalence gate enforced by RALF. Not for adding features (use /develop) or fixing bugs (use /bugfix).
context: fork
argument-hint: "[--files <glob>] --goal '<plain-english goal>' [--preserve-tests]"
---

# /refactor — Behavior-Preserving Code Refactor

Plan + execute + verify a refactor that changes structure without changing behavior. RALF loop on the test suite ensures behavior equivalence.

## When to use

- Breaking up large functions / classes
- Migrating to new patterns (class → functional, raw SQL → ORM)
- Extracting to a shared library
- Improving testability (dependency injection, pure functions)

## Not for

- Adding features → `/develop`
- Fixing bugs → `/bugfix`
- Schema/library/version migrations → `/migrate`

## Invocation

```
/refactor --files "src/api/*.ts" --goal "extract auth middleware to shared lib"
/refactor --files "src/components/**/*.tsx" --goal "convert class-based to functional components"
/refactor --files "src/data/*.py" --goal "introduce Repository pattern" --preserve-tests
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `--files <glob>` | ask user | Glob pattern or file list |
| `--goal '<text>'` | required | Plain-English goal of refactor |
| `--preserve-tests` | true | Keep existing tests passing throughout |

## Output

- Refactored code in assigned files
- Test suite passing (tests updated only if signatures genuinely change)
- `<repo>/.ai-skills-memory/refactor/<run-id>/REFACTOR-LOG.md` — before/after comparison + rationale
- Pull request with diff + refactor log

## Agent roster

| Agent | Model | Effort | Tools | Role |
|---|---|---|---|---|
| `team-lead` (resolves to `feature-design-lead`) | Opus | high | Task | Plans refactor steps; assigns per file; verifies no behavior change |
| `developer` (per-stack) | inherit | high | Read, Write, Edit, Bash | Executes refactor per assigned file(s) |
| `qa-engineer` | inherit | medium | Bash, Read | Verifies behavior equivalence (full test suite) |

## Pipeline

```
┌─ PLAN:
│  └─ Lead reads target files, scopes refactor, breaks into per-file steps
│     Generates REFACTOR-PLAN.md with before/after sketches
│
│     Prerequisite checks:
│       • Coverage scan on target files. If line coverage <80%
│         → developer writes characterization tests as a SEPARATE PRIOR PHASE
│           per `references/characterization-tests.md` BEFORE refactor begins.
│       • If refactor crosses >5 files OR module/package boundaries
│         → use Mikado method per `references/mikado-method.md`;
│           emit MIKADO.md alongside REFACTOR-PLAN.md.
│       • REFACTOR-PLAN.md MUST list named refactorings per file using
│         canonical names from `references/fowler-catalogue.md`
│         (e.g. "Extract Function", "Replace Conditional with Polymorphism").
│
├─ Gate: user approval of plan
│
├─ EXECUTE (sequential per file per `subagent-isolation.md` Sequential Code-Modification Gate):
│  └─ developer: refactor assigned file(s)
│     After each file: run tests via /run-tests
│     If tests fail: diagnose, refactor until tests pass
│
├─ Gate: all files refactored, all tests passing
│
├─ RALF (test validation loop):
│  │  Oracle: cli:./run-tests.sh (or detected test command)
│  │  Kill-on: same-error-repeats:2
│  │  Caps: 4 iter / 200K tokens / 45 min
│  │  On fail: developer revises refactor; re-run tests
│  └─ (loop back to test run)
│
└─ Lead verifies no behavior change:
   - API diff check (public surface unchanged unless explicitly in goal)
   - Test coverage preserved
   Memory write: L4 refactor decision + rationale
   PR description: generated from REFACTOR-PLAN
```

## G7 spawn payloads

All spawns use structured G7 payloads per `plugin/schemas/spawn-payload.schema.json`. Lead validates returns against `plugin/schemas/return-contract.schema.json`.

## Eval rubric

Pointer: `plugin/eval/judge-rubrics/refactor.md` (B10).

Dimensions:
1. **Behavior equivalence** — all existing tests pass; no breaking changes to public API
2. **Code improvement** — readability, maintainability, or performance demonstrably improved
3. **Scope correctness** — refactor stays within stated goal; no unrelated changes
4. **Test coverage preserved** — test suite still exercises the code at same coverage
5. **Documentation updated** — docstrings, comments, README reflect changes

Pass: avg ≥ 4.0, no dimension < 3.

## RALF wiring

- **Oracle:** `cli:./run-tests.sh` (or auto-detected per project test command)
- **Kill-on:** `same-error-repeats:2` (two iterations with same error → likely a real behavior change, not a refactor bug)
- **Caps:** 4 iter / 200K tokens / 45 min — overridable in userConfig

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | After plan approval | `.ai-skills-memory/refactor/<run-id>/plan.md` |
| L4 | After completion | `.ai-skills-memory/refactor/<run-id>/final.md` — before/after stats (lines, complexity metrics) |

## Failure modes

- **Refactor scope creeps:** Lead stops work; user must clarify goal
- **Tests fail after refactor:** developer re-examines; if persistent (kill-on triggers), this likely indicates behavior change masquerading as refactor — escalate to user
- **`--preserve-tests` violated:** lead refuses to advance to next file; rolls back the offending change

## Observability events

- `workflow_start` — refactor + goal
- `plan_generated` — per-file plan
- `ralf_iter` — test validation iterations
- `workflow_end` — `PR_OPENED` or `ESCALATED`

## Integration

- **Orchestrator**: `feature-design-lead` (the only agent with `tools: Task`)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Sub-workflows**: `/run-tests` (test execution + auto-fix per failure)
- **Companions**: `/ralph` (RALF loop), `/context-load` (per-role context), `/subagent-spawn` (G7 payload assembly), `/create-pr` (PR after completion)
- **Rules**: `subagent-isolation` (Sequential Code-Modification Gate per file), `ralph-budget` (caps), `untrusted-content-wrapping` (G1 wrap on tool outputs + subagent returns), `memory-discipline` (REFACTOR-LOG.md → L4)
- **Hooks**: `tool-output-normalize.py` (G2 on test runner stdout)
