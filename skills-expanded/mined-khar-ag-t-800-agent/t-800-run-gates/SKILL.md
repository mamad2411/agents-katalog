---
name: t-800-run-gates
description: >
  Какие machine gates гонять перед «готово» в прогоне T-800
  (run_gate, frontmatter, doctor/audit по режиму).
  Use when перед сдачей CREATE/PATCH, STATE Gates, strict-create,
  или exit code gates.
  Do NOT use when проектирование промпта (prompt-craft), обучение новичка,
  или cloud conversation hooks как sole-gate (P1).
paths:
  - "**/STATE.md"
  - "**/scripts/t800_*gate*"
  - "**/scripts/t800_run_gate.py"
metadata:
  t800_surface: gates
  t800_priority: P0
---

# T-800 — run gates (procedural matrix)

Канон: `python3 scripts/t800_run_gate.py` (+ флаги). Skill не заменяет скрипты.

## Что читать

- `shared/loop-engineering-contract.md`
- T800-SYSTEM-MAP / docs gates table
- `scripts/t800_run_gate.py --help`

Матрица: [gate-matrix.md](references/gate-matrix.md).  
CREATE: [strict-create.md](references/strict-create.md).  
Router modes: [router-modes.md](references/router-modes.md) (`shared/router-cost-policy-contract.md`).

## Алгоритм

1. Classify mode: CREATE | PATCH | LOOP | AUDIT.
2. Выбрать required checks из matrix.
3. Запустить команды (не объявлять PASS заранее).
4. Parse JSON / exit code.
5. Обновить `STATE.md` → Gates.
6. PASS только при exit 0, когда check required.

## Выход

```yaml
mode: CREATE|PATCH|LOOP|AUDIT
commands_run: []
ok: true|false
blockers: []
STATE_updated: true|false
```

## Запреты

- Self-PASS без machine evidence
- afterFileEdit / conversation hooks как sole production gate
- Silent skip `--strict-create` на CREATE
