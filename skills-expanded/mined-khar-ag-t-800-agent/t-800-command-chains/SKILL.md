---
name: t-800-command-chains
description: >
  Как читать и обновлять machine-readable command_chains T-800
  и не плодить orphan commands/agents.
  Use when правка commands/*, registry, graph команд↔агенты,
  или после добавления /t800-* команды.
  Do NOT use when soft prose orchestration в agent body без JSON,
  plugin-audit полный отчёт (→ t-800-plugin-auditor), или product chains адаптера.
paths:
  - "**/command_chains*"
  - "**/command-chains*"
  - "**/registry/**"
  - "**/commands/**"
metadata:
  t800_surface: command-graph
  t800_priority: P0
---

# T-800 — command chains (procedural)

Companion к JSON graph + orphan gate. Schema SoT: **`shared/command-chains.json`**.  
Скрипт gate — handoff artifact-scripts (не этот skill).

## Что читать

- `shared/command-chains.json` (SoT)
- `registry/agents-registry.json`
- `shared/plugin-audit-contract.md` (orphans)

Схема полей: [chain-schema.md](references/chain-schema.md).  
Правила orphan: [orphan-rules.md](references/orphan-rules.md).

## Алгоритм

1. Locate chains: `shared/command-chains.json` (не `registry/command_chains.json`).
2. Validate vs schema / gate script.
3. Map command stem → `lead` Task + `pipeline`.
4. Check consistency с registry ids / `calledBy` soft links.
5. Run orphan gate (когда скрипт есть).
6. Update chains **только** вместе с matching `commands/<stem>.md` и agent files (через factory).

## Выход

```yaml
chains_path: shared/command-chains.json
valid: true|false
orphans: []
patch_plan: []
```

## Запреты

- Invent chains без файла JSON на диске
- Дублировать soft graph только в prose агента
- Править agents/commands без factory
