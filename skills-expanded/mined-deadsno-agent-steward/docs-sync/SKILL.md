---
name: Docs Sync (agent-steward)
description: Синхронизация документации плагина agent-steward — ARCHITECTURE, CONCEPT, FEATURES, PIPELINE, EXECUTION-LOOP, README, CHANGELOG, ROADMAP, локали и счётчики tools/RPC. Проверять после изменений API/поведения.
project: agent-steward
---

# Docs Sync — agent-steward

Локальная версия перекрывает глобальный `docs-sync` (тот указывает на `.opencode/skills/CONVENTIONS.md`
сайта brain-25-evidence — здесь не применим).

## Что синхронизировать

| Изменение | Документы |
|---|---|
| Новый/удалённый tool или RPC метод | `README.md`, `docs/ARCHITECTURE.md`, `docs/FEATURES.md`, `TEST-PLAN.md` — счётчики сверяет `node test-docs.mjs` |
| Схема БД / `SCHEMA_VERSION` | `docs/ARCHITECTURE.md` (текст версии обязателен для `test-docs`) |
| Поведение scheduler / gate / guard / worktree | `docs/PIPELINE.md`, `docs/EXECUTION-LOOP.md`, `docs/SAFETY.md` |
| Совместимость V1/V2 | `docs/COMPATIBILITY.md`, `docs/V1-V2-COMPATIBILITY-PLAN.md` |
| Локали | `locales/{ru,en,zh}.json` — новый ключ во всех трёх; `README.ru.md`, `README.zh.md` |
| Релиз | `CHANGELOG.md`, `package.json` version, `ROADMAP*.md` |

## Правила

- Приоритет факта: код → тесты → документы. Текст `Known limitations` может отставать от
  закрытых B1.x-фиксов; `docs/FEATURES.md` содержал ложное «Secrets are not encrypted».
- Актуальные счётчики (сверены с кодом 20.11.2026): **30** MCP-инструментов (`src/index.ts`),
  **57** RPC-методов (`SchedulerRpc.methods` в `src/rpc.ts`), **115** наборов тестов
  (`npm test`). Числа приведены во всех документах к одним значениям. При сомнении не копировать из соседнего
  файла, а пересчитать по исходникам и прогнать `node test-docs.mjs`.
- After правки: `node test-docs.mjs`, `npm run test:i18n`, `node test-package-exports.mjs`.

## Формат находки

`<файл>: <что расходится с кодом> — <P1|P2>. Действие: <обновить/сверить>`.
