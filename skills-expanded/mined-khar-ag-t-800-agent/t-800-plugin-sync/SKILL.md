---
name: t-800-plugin-sync
description: >
  Procedural install/sync T-800 в ~/.cursor/plugins/local с CONTENT_DRIFT
  --check и обязательным Reload Window.
  Use when install-plugin, sync --check, CONTENT_DRIFT, stale marketplace pin,
  или «плагин не обновился».
  Do NOT use when KB sync-docs (/t-800-sync → t-800-knowledge-base),
  factory CREATE артефактов, или MIR в ~/.cursor/{agents,skills,rules}.
disable-model-invocation: true
metadata:
  t800_surface: ops-sync
  t800_priority: P0
---

# T-800 — plugin sync (ops checklist)

Skill задаёт **порядок шагов**. Скрипты install/sync — отдельный deliverable factory (artifact-scripts).

## Что читать

- `shared/auto-update-contract.md`
- `scripts/install-plugin.sh` / `.ps1`
- docs install/update в плагине

Детали: [content-drift.md](references/content-drift.md), [reload-checklist.md](references/reload-checklist.md).

## Алгоритм

1. Confirm SoT `plugin_root` (git checkout T-800).
2. Sync **`--check`** → отчёт CONTENT_DRIFT (если скрипт есть). Не запускайте скрипт без флагов — default = apply.
3. Apply MIR **только** в `~/.cursor/plugins/local/t-800-agent`.
4. `verify-install` / health по docs.
5. Сказать пользователю: **Reload Window**.
6. После Reload — продолжить исходную задачу.

## Выход

```yaml
drift: none|found
applied: true|false
reload_required: true
next: []
```

## Запреты

- Marketplace reinstall как first fix
- Copy в `.cursor/` workspace skills / user-home mirrors
- Strip `displayName` из plugin.json
- Skip Reload после apply
