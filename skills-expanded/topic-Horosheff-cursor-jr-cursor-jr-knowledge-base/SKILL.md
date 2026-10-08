---
name: cursor-jr-knowledge-base
description: >
  Техническая карта KB плагина CursorJr для ОБНОВЛЕНИЯ базы знаний (sync, CHANGELOG).
  НЕ вызывать для ответов пользователю — для этого субагент Task(cursor-jr).
disable-model-invocation: true
---

# CursorJr — карта KB (только для maintainer)

Это **не** субагент. Пользователю отвечает **Task(cursor-jr)** → `agents/cursor-jr.md`.

Используй этот skill только когда:
- запускается `/cursor-jr-sync`
- rule `cursor-jr-knowledge-refresh` активен
- нужно обновить `knowledge-base/` после `sync-docs.ps1`

Контракт: `shared/knowledge-update-contract.md`

## Пути

- `knowledge-base/INDEX.md` — карта
- `knowledge-base/UPDATE-QUEUE.md` — очередь после sync
- `knowledge-base/manifest.json` — хеши страниц
- `scripts/sync-docs.ps1` — синхронизация
- `scripts/install-plugin.ps1` — деплой в ~/.cursor/agents/
