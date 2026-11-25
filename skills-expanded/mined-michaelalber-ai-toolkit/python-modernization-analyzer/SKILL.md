---
name: python-modernization-analyzer
audience: team
description: >
  Analyzes legacy Python codebases and produces actionable modernization plans. Primary
  migration paths include Python 2 to 3.12+, sync to async, Flask/Django monolith to FastAPI,
  requirements.txt to pyproject.toml, and bare classes to Pydantic/dataclasses. Use when
  assessing or planning a Python upgrade or framework migration before doing it. Does NOT perform
  the migration — assesses, quantifies risk, and plans.
---

# Python Modernization Analyzer

> "The best time to modernize was five years ago. The second best time is now."
> -- Adapted from software engineering practice

> "Big bang rewrites fail. Incremental migration succeeds."
> -- Martin Fowler, *Refactoring*

## Core Philosophy

Legacy Python codebases accumulate technical debt in predictable patterns: Python 2 syntax that
`2to3` can partially fix, synchronous I/O that blocks under load, monolithic Flask/Django apps that
resist scaling, `requirements.txt` files with unpinned dependencies, and bare dictionaries where
Pydantic models would provide safety.

This skill assesses, quantifies, and plans — it does NOT perform the migration. The output is a
prioritized modernization plan with risk scores, effort estimates, and a recommended migration
sequence. The plan is the deliverable; execution is a separate task.

**Non-Negotiable Constraints:**
1. **Assess before acting** — never recommend a migration path without evidence from the codebase.
2. **Incremental over big-bang** — every recommendation must be achievable in phases, not a single rewrite.
3. **Preserve business logic unchanged** — the goal is modernization, not reimplementation.
4. **Dependencies are the real blockers** — a framework migration blocked by an unmaintained dependency is not viable.
5. **Every recommendation must cite evidence** — `grep -r "from flask"` is evidence; "I think this is Flask" is not.

**What this skill is NOT:** a migration execution tool (it produces a plan, not code); a code-quality
review (use `python-architecture-checklist`); a security review (use `python-security-review`).

The 10 domain principles and the knowledge-base lookup queries that ground every decision live in
`references/domain-principles.md`.

## Workflow

### Phase 1: SCAN
Inventory the codebase: Python version(s); framework (Flask/Django/FastAPI/bare/none); packaging
(`requirements.txt`/`setup.py`/`setup.cfg`/`pyproject.toml`); test framework and coverage; async
usage; ORM/database access pattern; deployment method.
Full detection command set (Python 2 markers, framework greps, packaging, coverage, async,
`2to3 -l`, `pyupgrade --dry-run`) is in `references/scan-commands.md`.

### Phase 2: ASSESS
Score each migration path by effort, risk, and blocker potential. The migration-path catalog (tool
+ assessment method) is in `references/scan-commands.md`; scoring dimensions and the full risk table
are in `references/migration-risk-matrix.md`.

### Phase 3: PLAN
Produce a prioritized, phased plan, each phase leaving the app in a working state:
0. **Prerequisites** — tests, CI/CD, Docker (if missing)
1. **Low-risk wins** — packaging, type hints, linting
2. **Framework-independent** — Python version upgrade, dependency updates
3. **Architecture** — service layer extraction, ORM adoption
4. **Framework** — Flask/Django → FastAPI (if applicable)
5. **Async** — sync → async migration (if applicable)
6. **Auth** — authentication modernization (last, highest risk)

### Phase 4: REPORT
Deliver the plan with evidence, risk scores, and effort estimates. Use the risk scoring table in
`references/migration-risk-matrix.md` and the deliverable layout in `## Output Template` below.

Apply the domain principles throughout (`references/domain-principles.md`), and follow the AI
discipline rules in `references/discipline-and-recovery.md` at every phase.

Evidence before recommendation, quantify before scoring, and incremental plans only — with worked
WRONG/RIGHT examples, the 10-row anti-pattern catalog, and error-recovery procedures (tools missing,
unknown dependency compatibility, zero test coverage) — are in `references/discipline-and-recovery.md`.

## State Block

```xml
<python-modernization-state>
  phase: SCAN | ASSESS | PLAN | REPORT | COMPLETE
  python_version: [2.x / 3.x / unknown]
  framework: flask | django | fastapi | bare | unknown
  packaging: requirements_txt | setup_py | pyproject_toml | unknown
  test_coverage: none | low | medium | high | unknown
  async_usage: none | partial | full
  migration_paths_identified: 0
  blockers_identified: 0
  last_action: [description]
  next_action: [description]
</python-modernization-state>
```

## Output Template

The full Modernization Assessment Summary (Markdown — header block, migration-paths table, blockers
table, phased plan) is in `references/assessment-summary-template.md`. Before/after compatibility
examples for Python 2→3, sync→async, and Flask→FastAPI are in `references/compatibility-patterns.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `python-architecture-checklist` | Run architecture review after modernization to verify the new structure meets quality gates. |
| `python-security-review` | Run security review after framework migration — new frameworks have different security patterns. |
| `alembic-migration-manager` | Database migration is often part of modernization. Use this skill for the migration lifecycle. |
| `fastapi-scaffolder` | When the modernization plan includes FastAPI adoption, use this skill for endpoint scaffolding. |
| `legacy-migration-analyzer` | Cross-reference for teams with mixed Python/.NET stacks. Assessment philosophy is identical; tooling differs. |
