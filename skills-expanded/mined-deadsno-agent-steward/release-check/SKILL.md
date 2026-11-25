---
name: Release Check (agent-steward)
description: Проверка готовности плагина agent-steward к коммиту, тегу и релизу — сборка, тесты, локали, упаковка, docs/CHANGELOG и безопасность публикации. Заменяет глобальный release-check для этого репозитория.
license: MIT
project: agent-steward
---

# Release Check — agent-steward

Локальная версия перекрывает глобальный `release-check` (тот ориентирован на pytest и
`docs/data.json` сайта). Проверять оба «полюса»: **код** и **артефакты публикации**.

## Чек-лист

### 1. Git и рабочее дерево
- `git status --short` чист или содержит только ожидаемые правки.
- В staged нет `.env`, `*.key`, `*.secret`, `secrets.json`, больших файлов >10 MB.
- Коммит: `type(scope): description` латиницей (feat/fix/docs/chore/test/ci/refactor).

### 2. Сборка и качество
- `npm run build` — tsc без ошибок, `dist/` свежий (тесты идут против `dist/`).
- `npm run lint` — без ошибок.
- `npm run build:gui` — GUI-бандл пересобран; `dist/gui-experimental.cjs` — это stub,
  рабочий бандл — корневой `gui-experimental.cjs` (не редактировать руками).

### 3. Тесты
- `npm test` или `npm run test:parallel` — зелёный (~130 `test-*.mjs`).
- `npm run test:en`, `npm run test:zh`, `npm run test:i18n` — паритет `ru/en/zh`.
- `node test-docs.mjs` — счётчики tools/RPC, версия схемы (`SCHEMA_VERSION=12`), ключи конфига.
- `node test-workflows.mjs` — permissions/guards в `.github/workflows`.
- `node test-package-exports.mjs` + `npm pack --dry-run` — все цели `exports` есть в тарболе,
  включая `./rpc`.
- При изменениях durable-слоя / scheduler — `npm run test:chaos` (nightly) и кросс-ОС тесты.

### 4. Документы и версия
- `package.json` version, `CHANGELOG.md`, `README.md`, `docs/ARCHITECTURE.md`,
  `docs/FEATURES.md`, `docs/PIPELINE.md`, `ROADMAP*.md` — согласованы.
- `test-docs` не ругается на счётчики (30 MCP-инструментов / 57 RPC-методов / 115 наборов —
  сверять по исходникам: `src/index.ts`, `SchedulerRpc.methods`, `npm test`).
- `docs/COMPATIBILITY.md` обновлён, если затронут dual V1/V2 path.

### 5. Публикация
- **Локальный `npm publish` запрещён.** Релиз только через `git tag vX.Y.Z` →
  `.github/workflows/release.yml` (verify → OIDC publish с `--provenance`).
- `workflow_dispatch` = dry-run `npm pack` — безопасно для проверки тарбола.
- `prepublishOnly` уже вызывает build + build:gui; не обходить его ручной сборкой.

## Формат вывода

Пройдены ли все 5 блоков. Каждое расхождение — одной строкой:
`<что>: <файл и проверка> — <P0|P1|P2>. Действие: <что сделать>`.

- P0 — сборка/тесты красные, секрет в staged, тарбол битый → чинить до тега.
- P1 — docs/версии рассинхронизированы, missing тест, GUI-бандл устарел → в этом батче.
- P2 — косметика README → отдельным ID в бэклог.
