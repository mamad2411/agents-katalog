---
name: t-800-fix-pack
description: >
  Структура fix-pack и constraints factory PATCH для /t800-fix.
  Use when правка существующего артефакта, fix-packs/<slug>.md,
  audit→fixpack, или mode PATCH.
  Do NOT use when полный CREATE /t800-start, Loop report-only (/t800-loop),
  или doctor/plugin-audit без PATCH.
paths:
  - "**/fix-packs/**"
  - "**/templates/fix-pack*"
metadata:
  t800_surface: factory-patch
  t800_priority: P0
---

# T-800 — fix-pack → PATCH

Procedural map: fix-pack → `/t800-fix` → **Task(t-800-factory)** PATCH → run_gate.

## Что читать

- `shared/fix-pipeline-contract.md`
- `templates/fix-pack.md.template`
- `commands/t800-fix.md`

Секции: [pack-sections.md](references/pack-sections.md).  
Ограничения: [patch-constraints.md](references/patch-constraints.md).

## Алгоритм

1. Read `{memory_path}/fix-packs/<slug>.md`.
2. Validate required sections (см. refs).
3. `research_mode`: skip | light | deep (default skip/light).
4. Brain LIGHT: `Task(t-800-brain-lead)` с `mode: PATCH`.
5. Factory **только** `files[]` из pack.
6. `python3 scripts/t800_run_gate.py` (+ флаги по режиму).
7. Обновить STATE Gates / Completed.

## Выход

```yaml
pack_ok: true|false
missing_sections: []
patch_scope: []
next: t-800-factory|blocked
```

## Запреты

- DEEP research по умолчанию
- Расширять scope без обновления pack
- Править production site/deck
- Self-PASS без machine gate
