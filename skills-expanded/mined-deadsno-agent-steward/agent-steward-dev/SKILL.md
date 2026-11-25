---
name: Agent Steward Dev
description: Use when changing code in the agent-steward plugin repository — architecture map, build/test commands, module-to-test mapping, worktree lifecycle, durable layer, i18n and release artifacts. Use instead of generic web-search guessing.
project: agent-steward
---

# Agent Steward Dev

Репозиторий: плагин OpenCode для шедулинга и оркестрации (V1 ≥1.18.29 + V2). Стек:
TypeScript strict/ESM, Node ≥22.22 (`node:sqlite`, WAL; chokidar 6), zod 4, yaml, iconv-lite;
`@opencode/plugin ^2.2.7` + `@opencode/schema` (V2), `@opencode-ai/plugin 1.19.5` (V1-типы);
GUI — SolidJS + Vite; TUI — OpenTUI; SQLite `scheduler.db`, `SCHEMA_VERSION=12`;
бэкенды ОС — `schtasks` / `crontab` / `launchd`; локали `locales/{ru,en,zh}.json`.

## Что где лежит

- `src/index.ts` — `Plugin.define`, ~30 agent tools, регистрация RPC и встроенного скилла.
- `src/core/*` — scheduler (Windows/POSIX/mac, cron↔schtasks, at-fallback), guard, matrix,
  worktree, execution, recovery, router/capability, notifications, triage, secrets.
- `src/db/*` — схема/миграции, durable runs, DLQ, run journal, step idempotency.
- `src/rpc.ts` — `Rpc.define` контракт сервер↔GUI; `src/gui.tsx` — дашборд; `src/server.ts` — HTTP.
- `src/skill.ts` — загрузчик встроенного скилла из `skills/scheduled-job-best-practices`.

## Команды

`npm run build` (tsc + d.ts) → `npm run lint` → `npm test` (~130 `test-*.mjs` против `dist/`) →
`npm run build:gui`. Быстрее: `npm run test:parallel`. Локали: `npm run test:en`, `test:zh`,
`test:i18n`. Мета-гейты: `node test-docs.mjs`, `node test-workflows.mjs`,
`node test-package-exports.mjs`. Стресс: `npm run test:chaos`, `npm run bench:local`.
Тесты изолированы через `OPENCODE_SCHEDULER_HOME` — не трогают реальные данные ОС.

## Маппинг правка → проверка

| Правка | Обязательные тесты |
|---|---|
| `src/core/scheduler/*`, cron, schtasks, launchd, at | `test:cron-to-schtasks`, `test:schtasks-*`, `test:mac-*`, `test:at-*`, `test:posix-e2e` |
| `src/core/worktree*`, guard, W-1…W-4 | `test:worktree`, `test:guards`, `test:w4` |
| `src/db/*`, SCHEMA_VERSION | `test:run-*`, `test:step-idempotency`, `test:run-dlq`, nightly chaos |
| i18n / locales / GUI-строки | `test:i18n`, `test:en`, `test:zh` (все три локали обязаны совпадать) |
| GUI / RPC | `test:dlq-gui`, `test:pause-gui`, `test:gui-bundle`, smoke в Playwright |
| permissions / secrets / audit | `test:permissions-policy`, `test:secrets`, `test:audit` |
| docs / README / CHANGELOG | `test:docs`, `test:workflows` |

## Правила

- Новый модуль в `src/core` → новый `test-*.mjs`. Изменение без теста не принимается.
- Миграции БД аддитивные/идемпотентные; смена `SCHEMA_VERSION` → обновить текст в `docs/ARCHITECTURE.md`
  (проверяет `test-docs`).
- Не ломать dual-export `setup`/`server`; V2-only вызовы в общем коде — только с правкой
  `docs/COMPATIBILITY.md`.
- Не редактировать вручную `dist/`, `gui-experimental.cjs`, `legacy/gui-experimental.cjs`.
- Публикация: только `git tag vX.Y.Z` → `.github/workflows/release.yml`; локально —
  `npm pack --dry-run`. `npm publish` из рабочей машины не делать.
- CI: 3 ОС × Node 22.22/24, lint, en/zh, `compat-v1`, `compat-v2`, `shim-smoke`, `lockfile-drift`.

## Важная оговорка про доки

`Known limitations` в `docs/ARCHITECTURE.md` / `docs/EXECUTION-LOOP.md` могут отставать от
закрытых B1.x-фиксов — при ревью проверять фактом по коду, а не верить тексту. Утверждение
«Secrets are not encrypted» в `docs/FEATURES.md` уже исправлено: сейчас там описан
AES-256-GCM (см. CHANGELOG). Актуальные счётчики — 30 tools / 57 RPC / 115 наборов тестов;
сверять через `node test-docs.mjs`, а не копировать из соседнего файла.
