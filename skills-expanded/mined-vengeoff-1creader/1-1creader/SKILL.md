---
name: Работа с конфигурацией 1С через 1creader
description: Read-only чтение конфигурации 1С из файловой ИБ (1Cv8.1CD). Карта, Obsidian vault, MCP. Используй при задачах про метаданные 1С, модули, справочники, документы, регистры, встроенный язык 1С.
---

# Конфигурация 1С через 1creader

См. также `AGENTS.md` в корне репозитория (общие правила для Cursor, Claude Code, Codex).

## Первый запуск

1. Пользователь кладёт папку ИБ (`1Cv8.1CD`) в workspace.
2. `onecreader init ./папка-ИБ --index` или MCP: `config_init` → `config_index`.
3. Читай `.onecreader/MAP.md` и `vault/00-Index.md`.

## Работа

1. Контекст: `MAP.md` + `config_get_index`.
2. Obsidian: `config_get_vault_note(ref)` или `vault/Objects/`.
3. Точечно: `config_get_object`, `config_get_module`, `config_catalog_data`.
4. Поиск: `config_find`, `config_search_code`.
5. После изменений в конфигураторе: `config_index(force=true)`.

## Ограничения

- Формат: 1CD 8.3.8+. **Только чтение** — запись в ИБ не поддерживается.
