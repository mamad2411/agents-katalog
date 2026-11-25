---
name: t-800-factory-scaffold
description: >
  Procedural checklist CREATE артефактов T-800 через factory
  (не ad-hoc Write в agents/skills/commands/rules/hooks).
  Use when /t800-start, factory CREATE, factory-brief, или «собери агента/skill/command».
  Do NOT use when /t800-fix PATCH, обычный код без Cursor-артефактов,
  или обучение новичка (→ Task t-800-operator).
metadata:
  t800_surface: factory-create
  t800_priority: P0
---

# T-800 — CREATE scaffold (procedural)

Это **не** субагент. CREATE-артефакты пишет только **Task(t-800-factory)** (внутри: architect→…→auditor).

## Что читать

- `shared/department-orchestration-contract.md`
- `shared/plan-to-factory-handoff-contract.md`
- `shared/project-memory-contract.md`
- `{memory_path}/factory-briefs/<slug>.yaml`

Детали: [create-checklist.md](references/create-checklist.md), [department-order.md](references/department-order.md).

## Алгоритм

1. Discovery: `bash scripts/discover-target-project.sh --workspace "<ROOT>"` → запомни `memory_path`.
2. Confirm brief + `STATE.md` (init/touch через loop scripts).
3. Порядок отделов: intake? → scout → research-lead → prompt-craft? → brain-lead → factory.
4. Factory АВТО: architect → builder → … → auditor (листов не звать вручную).
5. Перед «готово» — skill `t-800-run-gates` / `t800_run_gate.py`.
6. После каждого отдела — одна строка progress пользователю.

## Выход

```yaml
phase: scout|research|craft|brain|factory|gates
next_task: "Task(t-800-…)" | null
blockers: []
```

Без production Write вне factory.

## Связи

- Invoked by: director / factory CREATE
- Companions: `t-800-run-gates` после auditor

## Запреты

- Write/StrReplace в `agents/`, `skills/`, `commands/`, `rules/`, `hooks` из skill
- Skip factory / invent new research|brain agents
- MIR вне `~/.cursor/plugins/local/`
