---
name: migrate
description: Use this skill when planning database schema changes with rollback, framework version upgrades, or library replacements — a planned migration with rollback plan across schema, library, version, and framework, run as a multi-agent pipeline with RALF on validation. Not for refactors without external contract change (use /refactor) or small bug-fix releases (use /develop).
context: fork
argument-hint: "<migration description, e.g. 'Postgres 13 → 14'> [--staged]"
---

# /migrate — Versioned Migration with Rollback

Plan + execute + validate a migration with a documented + tested rollback procedure. RALF loop on data-integrity validation ensures the migration is safe AND reversible.

## When to use

- Database schema migration with potential data implications
- Framework version upgrade (Django 3.2 → 4.0, Spring Boot 2.x → 3.x)
- Library replacement requiring code changes (lodash → ramda, raw SQL → ORM)
- Postgres major version upgrade

## Not for

- Refactors without external contract change → `/refactor`
- Small bug-fix releases → `/develop`
- Infrastructure changes without code → `/infra-change`

## Invocation

```
/migrate "Postgres 13 → 14"
/migrate "React class → functional components" --staged
/migrate "Django 3.2 → 4.0"
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `<migration>` (positional) | required | Source → target description |
| `--staged` | off | Use blue-green or canary pattern (requires ops sign-off) |

## Output

- Migration code (schema scripts, version pins, compatibility shims)
- `<repo>/.ai-skills-memory/migrate/<run-id>/MIGRATION-PLAN.md` — detailed steps + rollback + risk matrix
- `<repo>/.ai-skills-memory/migrate/<run-id>/VALIDATION.md` — test results + data integrity checks
- PR with migration + rollback procedures documented

## Agent roster

| Agent | Model | Effort | Tools | Role |
|---|---|---|---|---|
| `team-lead` (`feature-design-lead`) | Opus | xhigh | Task | Plans migration, risk assessment, rollback strategy |
| `devops-engineer` | inherit | high | Bash, Read, Write, Edit | Infrastructure migration (DB schema, deploy config) |
| `developer` (per-stack) | inherit | high | Read, Write, Edit, Bash | Application-level migration (code, compatibility shims) |
| `qa-engineer` | inherit | high | Bash, Read, Grep | Data integrity validation, rollback testing |

## Pipeline

```
┌─ PLAN:
│  └─ Lead: research target version, compatibility matrix, rollback strategy
│     PLAN MUST classify the migration: (a) additive-only (single safe step),
│     (b) requires expand-contract (multi-phase per
│     `references/expand-contract.md`), or (c) blue-green data migration.
│     Detect target stack to pick migration tool from
│     `references/migration-tools-by-stack.md`.
│     Generates MIGRATION-PLAN.md with:
│     - Pre-flight checklist (dependencies, backups)
│     - Step-by-step migration procedure (one phase per deploy if expand-contract)
│     - Rollback procedure (TESTED, not theoretical)
│     - Risk matrix (data loss, compatibility, performance)
│
├─ Gate: USER APPROVAL of rollback procedure (not just migration plan)
│
├─ EXECUTE (sequential per `subagent-isolation.md`):
│  ├─ devops-engineer: DB schema migration (if applicable)
│  │  - Create migration scripts (forward + rollback)
│  │  - Test on replica
│  │  - Document data transformation
│  │
│  └─ developer: application-level changes
│     - Update deps, compatibility shims, feature flags
│     - Parallel-run mode (old + new API, use new)
│
├─ VALIDATE (sequential):
│  │  - Run full test suite via /run-tests
│  │  - Data integrity checks (row counts, checksums, foreign key constraints)
│  │  - Performance baseline (query times, throughput)
│  └─ If rollback needed: execute rollback procedure, validate revert
│
├─ RALF (validation loop):
│  │  Oracle: python:./validate-migration.py (custom validation script, exit 0 = pass)
│  │  Kill-on: oracle-pass OR no-progress:2
│  │  Caps: 5 iter / 300K tokens / 90 min
│  └─ (loop back to VALIDATE)
│
└─ Lead sign-off on migration safety
   Memory write: L4 (committed) migration decision + rollback proof
```

## G7 spawn payloads

All spawns use structured G7 payloads per `plugin/schemas/spawn-payload.schema.json`. Lead validates returns against `plugin/schemas/return-contract.schema.json`.

## Eval rubric

Pointer: `plugin/eval/judge-rubrics/migrate.md` (B10).

Dimensions:
1. **Plan completeness** — pre-flight, forward, rollback all documented
2. **Rollback safety** — rollback procedure TESTED and proven reversible
3. **Data integrity** — validation checks confirm data preserved
4. **Performance** — no unexpected degradation post-migration
5. **Risk awareness** — identified risks with mitigations for each

Pass: avg ≥ 4.0, no dimension < 3.

## RALF wiring

- **Oracle:** `python:./validate-migration.py` (custom validation script, exit 0 = pass)
- **Kill-on:** `oracle-pass` (happy stop) OR `no-progress:2` (two iterations with no change → escalate)
- **Caps:** 5 iter / 300K tokens / 90 min — overridable

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 (committed) | After plan approved | `.ai-skills-memory/.committed/migrations/<name>/plan.md` — strategy for team review (versioned in git) |
| L4 (committed) | After validation pass | `.ai-skills-memory/.committed/migrations/<name>/validation-report.md` — data integrity proof (versioned) |

Both committed paths must match `committed-allowlist.txt` patterns — `pre-tool-use-committed-write.py` hook enforces.

## Failure modes

- **Rollback procedure fails during testing:** ESCALATE AS CRITICAL; do not proceed with migration until rollback is proven safe
- **Data loss detected post-validation:** kill migration; trigger full diagnostic via `/env-analyze`; surface to user with `RUNBOOK-EMERGENCY` reference
- **Performance regresses materially:** Lead presents trade-off to user with quantified delta; user decides accept or rollback
- **`--staged` selected but no canary infrastructure:** Lead detects absence; refuses with "no canary deployment infrastructure detected; use --staged with manual canary or proceed without"

## Observability events

- `workflow_start` — migrate + source→target
- `plan_approved` — user gate passed
- `validation_start` — data integrity checks begin
- `ralf_iter` — validation loops
- `workflow_end` — `COMPLETE` or `ROLLBACK_EXECUTED` or `ESCALATED`

## Integration

- **Orchestrator**: `feature-design-lead` (Opus, `tools: Task`)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Sub-workflows**: `/run-tests` (test suite verification), `/env-analyze` (pre-flight environment check)
- **Companions**: `/ralph` (validation RALF), `/subagent-spawn` (G7 payload), `/create-pr` (after completion)
- **Rules**: `subagent-isolation` (Sequential Code-Modification Gate), `ralph-budget` (validation caps), `untrusted-content-wrapping` (G1 wrap on subagent returns + project file reads), `memory-discipline` (committed writes via allowlist)
- **Hooks**: `pre-tool-use-committed-write.py` (validates `.committed/` paths against allowlist), `tool-output-normalize.py` (G2 on validation script output)
