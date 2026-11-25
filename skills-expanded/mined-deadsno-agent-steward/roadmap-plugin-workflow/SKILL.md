---
name: Roadmap Plugin Workflow
description: Use when working through the agent-steward ROADMAP one subtask at a time, using the scheduled-job plugin itself for tracking and diagnostics. Covers task markers, honest status, reports, gates, and bug hunting via plugin analytics.
project: agent-steward
---

# Roadmap Plugin Workflow

Цикл: **взял подзадачу → сделал → отчёт → следующая**. Никаких спринтов, никаких «пачками».
Плагин (`agent-steward`) используется и как трекер, и как источник диагностики.

## 1. Трекинг через плагин

- Для каждой подзадачи создать маркер `schedule_task` с `triggerType: "once"`,
  `runAt: "2030-01-01T00:00:00Z"`, `workingDirectory` = каталог репозитория плагина,
  `priority: 5`. Такие задачи **не должны запускаться** — они только трекинг.
- Связать цепочку через `nextTaskOnSuccess`: E-1.1 → E-1.2 → E-1.3 и т.д.
- `update_task` **не имеет поля `status`** (схема `src/index.ts:638-835`). Статус отмечать
  префиксом в `prompt`:
  - `🔄 [В РАБОТЕ] ...` при взятии в работу;
  - `📋 [ТРЕКИНГ][ЗАКРЫТО В ROADMAP/CHANGELOG] ...` после закрытия.
- **Никогда** не ставить `✅ [ВЫПОЛНЕНО]` на задаче-маркере, у которой `runsTotal=0`:
  это фейковый «выполнено» (реально выполнялся код в сессии, а не задача планировщика).
- Не трогать чужие задачи (github-ci-*, gui, проверка-статуса-10-утра, hello-1420) без
  явной просьбы пользователя.

## 2. Одна подзадача за раз

1. Прочитать очередь в `ROADMAP.md`; взять первую открытую (`⬜`) подзадачу.
2. Отметить её `🔄 [В РАБОТЕ]` в плагине.
3. Сделать код + тест + документацию одной правкой.
4. Прогнать гейты (минимум `npm run build`, точечный `node test-*.mjs`,
   `node test-docs.mjs`, полный `npm test`).
5. Perеместить подзадачу из `ROADMAP.md` в `CHANGELOG.md` (`[Unreleased]` → `Added`/`Fixed`).
   **Убирать строку из ROADMAP и добавлять в CHANGELOG — обязательно.**
6. Отчитаться в чат: что сделано, какие файлы, результаты тестов, ограничения.
7. Обновить маркер в плагине и сразу взять следующую подзадачу.

## 3. Поиск багов через плагин

- `get_analytics` / `get_metrics` — искать расхождения счётчиков, `tokens=0`, `costUsd=0`,
  аномальные модели (`skipped`, `(default)`).
- `get_history` — одна запись с `error "-"`, `durationMs` > 300000, `status=skipped` —
  повод проверить wrapper и запись usage.
- `get_task_logs` — пустой лог у задачи со статусом `error` means plugin-side подготовка
  обнулила файл до запуска обёртки или обёртка упала до ersten вывода.
- `list_tasks` — `orphaned=true`, `nextRun` в прошлом, `runsTotal` без статуса — признаки
  мусора; удалять/переименовать только по просьбе пользователя.
- Аудит `tool.blocked` / `permissions.defaultPolicy=hybrid` — если автономная задача
  падает из-за запрещённых `shell`/`question`, точечно выдать `allowedTools` для задачи,
  а не ослаблять глобальную политику.

## 4. Packaging-гейт (обязателен перед релизом)

- В `dist/*.js` **ноль** value-импортов `@opencode-ai/plugin` (v1 — только devDependency,
  тип-импорты допустимы в `.d.ts`). v1 `tool()` — identity, инлайнится локально.
- `npm run build && npm run build:gui`; `grep -r "@opencode-ai/plugin" dist src`;
  `node test-package-exports.mjs`, `node test-dual-entry.mjs`, `node test-v1-integration.mjs`,
  `node test-prod-install.mjs` (чистая установка tarball с `--omit=dev` + import точки входа),
  `npm pack --dry-run` (не должно быть `dist/**/*.test.*`).
- Не редактировать `dist/` вручную; уборка фантомов — точечное удаление ос Statics артефактов,
  которых нет в исходниках.
- Публикация только через `git tag` → `.github/workflows/release.yml`; локальный
  `npm publish` запрещён.

## 5. Правила общения

- Отчёт после каждой подзадачи, коротко: файлы, тесты, ограничения.
- Вопросы задавать сразу, если решение меняет политику безопасности или данные пользователя.
- Не пушить без явного запроса; коммит — по запросу.
