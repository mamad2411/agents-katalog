---
name: OpenCode Plugin Dev
description: Use when developing, debugging, reviewing or migrating an OpenCode plugin — V2 Plugin API, entrypoints (server/TUI/GUI/RPC), config keys, skills registration, package exports and testing an installed plugin. Source of truth is the V2 docs at opencode.ai/docs.
project: agent-steward
---

# OpenCode Plugin Dev

Только OpenCode **V2**. V1-доки и V1-синтаксис (`plugin`, `@opencode-ai/plugin`) используй
исключительно как миграционный вход; итоговые рекомендации — V2. Источник правды:
<https://opencode.ai/docs/> — перед ответом загрузи соответствующую страницу целиком.

## Версии и конфиг

- V2: ключ `plugins`; V1: `plugin`. В этом репозитории both supported — не ломать dual-export.
- Конфиг: JSONC, `$schema: https://opencode.ai/config.json`. Глобальный —
  `~/.config/opencode/opencode.jsonc`, проектный — `opencode.jsonc` / `.opencode/opencode.jsonc`.
  Изменения подхватываются без рестарта; `/reload` — полная перезагрузка.
- MCP по V2 — `mcp.servers`; в локальном глобальном конфиге исторически плоский блок `mcp`,
  он работает через обратную совместимость. Не «чинить» молча во время правки плагина.
- **LSP в V2 отсутствует**: нет страницы в docs, нет поля `lsp`, нет permission action `lsp`.
  Диагностика = `npm run lint`, `npm run build`, тесты.

## Точки входа плагина

`Plugin.define({ id, setup })` из `@opencode/plugin`. Экспорты пакета:
`.` (server), `./tui`, `./gui-experimental`, `./rpc`. Каждый парт использует свой
`@opencode/plugin/*` entrypoint. Локальные плагины грузятся автоматически из `.opencode/plugins`
или через `plugins` в конфиге (у нас — `file:///` dev-установка).

## RPC

Контракт описывается `Rpc.define` (`@opencode/plugin/rpc`) в `src/rpc.ts`: `methods` с
`input`/`output`/`errors` (JSON Schema или Standard Schema), опциональный `events`.
Сервер: `await ctx.rpc.register(Contract, handlers)`; вызов из того же плагина —
`ctx.rpc(Contract)`; GUI — `ctx.client.rpc(Contract)`. `ctx.client` читать в момент вызова
(он меняется после рестарта сервера). Для внешних клиентов и других плагинов контракт
должен быть экспортирован как `./rpc` — иначе они не могут импортировать типизированный
контракт, не загружая реализацию.

## Скиллы

Скилл — каталог с `SKILL.md`; ID = имя каталога (не frontmatter `name`). Для портативности —
нижний регистр kebab-case. Проектные `.opencode/skills` перекрывают глобальные при том же ID.
Подключение:Discovery автоматическая; дополнительные каталоги — массив `skills` в конфиге.
`metadata.opencode/autoinvoke: false` убирает скилл из автопоказа, но оставляет загрузку по ID.

Плагин регистрирует свой скилл сам через `ctx.skill.transform` (см. `src/index.ts`), а тело
читает из `skills/` пакета (`src/skill.ts`). Папка `skills` обязательно остаётся в `files`
`package.json`.

## GUI

GUI — отдельный SolidJS-бандл (`vite build`), публикуется как `./gui-experimental`.
Собирать бандл перед релизом; тестировать **установленный пакет**, а не workspace-link.
Проверять GUI в браузере: консоль, сеть, пустые/error-состояния, вызовы RPC.

## Быстрый чек-лист ревью плагина

1. API по V2-докам, а не по памяти (загрузить страницу).
2. Нет V1-синтаксиса в общем коде без правки `docs/COMPATIBILITY.md`.
3. `./rpc` в `exports`; контракт импортируется по имени пакета.
4. GUI-бандл собран и свеж; `npm pack --dry-run` содержит все цели `exports`.
5. Скилл грузится из пакета, ID совпадает с каталогом.
6. Нет ссылок на LSP.

Подробная шпаргалка: [references/v2-plugin-api.md](references/v2-plugin-api.md).
