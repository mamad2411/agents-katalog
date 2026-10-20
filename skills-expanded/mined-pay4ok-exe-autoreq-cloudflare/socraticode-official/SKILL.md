---
name: socraticode-official
description: >
  Official SocratiCode MCP server — 25 tools for hybrid semantic search (Qdrant+Ollama),
  dependency graphs (import/export/circular), execution flow tracing, blast radius
  analysis, context artifacts (DB schemas, API specs), codebase indexing and management.
  Use for: codebase_search, codebase_flow, codebase_impact, codebase_graph_*,
  codebase_context_*, codebase_symbols.
  Triggers: socraticode, codebase search, codebase flow, codebase graph,
  codebase index, codebase impact, blast radius, call flow, dependency graph,
  circular dependencies, codebase symbols, context artifacts, SocratiCode official.
allowed-tools:
  - Bash
  - Read
  - Task
---

# SocratiCode Official — Полный кодовый интеллект

25 MCP-инструментов. Гибридный поиск (семантический Qdrant+Ollama + keyword BM25),
граф зависимостей, flow-анализ, контекстные артефакты, индексация.

**Важно:** Требует Docker (Qdrant) + Ollama (embedding model). Проверь `codebase_health`.

## Главное правило: CodeGraph или SocratiCode?

| Задача | Инструмент |
|--------|-----------|
| «Кто вызывает функцию?» (точное имя) | **CodeGraph** `codegraph_callers` |
| «Как X доходит до Y?» (call path) | **CodeGraph** `codegraph_explore` |
| «Что сломается если поменять X?» | **CodeGraph** `codegraph_explore` |
| «Где определён символ?» | **CodeGraph** `codegraph_search` |
| «Прочитай файл» | **CodeGraph** `codegraph_node` |
| «Как работает авторизация?» (концепт) | **SocratiCode** `codebase_search` |
| «Найди где обрабатываются ошибки» | **SocratiCode** `codebase_search` |
| «Покажи граф зависимостей» | **SocratiCode** `codebase_graph_visualize` |
| «Есть ли циклические зависимости?» | **SocratiCode** `codebase_graph_circular` |
| «Что в БД-схеме?» | **SocratiCode** `codebase_context_search` |
| «Куда идёт выполнение от main()?» | **SocratiCode** `codebase_flow` |
| «Что сломается если удалить X?» | **SocratiCode** `codebase_impact` |

**Правило:** точное имя символа → CodeGraph. Концептуальный вопрос → SocratiCode.

---

## Инструменты

### Семантический поиск по коду

#### `codebase_search` — Главный поисковый инструмент
Семантический + keyword (BM25) поиск, RRF-фьюз. Natural language → релевантный код.
```json
{"query": "как обрабатываются JWT токены", "limit": 10, "fileFilter": "src/auth/"}
```
Фильтры: `languageFilter`, `fileFilter`, `minScore`. Поддерживает `includeLinked` для поиска по связанным проектам.

#### `codebase_symbols` — Символы в файле или поиск по имени
Два режима:
- `file="src/auth/service.ts"` → все символы в файле
- `query="validateToken"` → поиск по имени в проекте

#### `codebase_symbol` — 360° обзор символа
Определение, kind (function/class/...), callers, callees, confidence levels.
```json
{"name": "validateToken", "file": "src/auth/middleware.ts"}
```

### Индексация и управление

| Инструмент | Что делает | Когда |
|-----------|-----------|------|
| `codebase_health` | Docker + Qdrant + Ollama статус | Перед первым использованием |
| `codebase_index` | Запуск индексации (асинхронно) | Новый проект |
| `codebase_update` | Инкрементальное обновление | После изменений в коде |
| `codebase_status` | Прогресс (0-100%) | Ждать готовности индекса |
| `codebase_stop` | Остановить индексацию | Прервать долгую индексацию |
| `codebase_watch` | Авто-отслеживание (start/stop/status) | Держать индекс в актуале |
| `codebase_remove` | Удалить индекс | Очистка |
| `codebase_list_projects` | Все проиндексированные проекты | Обзор |
| `codebase_about` | О SocratiCode | Справка |

```bash
# Первый запуск:
codebase_health → codebase_index → codebase_status (до 100%)
```

### Граф зависимостей

| Инструмент | Что делает |
|-----------|-----------|
| `codebase_graph_build` | Построить граф (асинхронно) |
| `codebase_graph_status` | Прогресс / статус графа |
| `codebase_graph_query` | Что импортирует файл + кто зависит от него |
| `codebase_graph_stats` | Всего файлов, рёбер, топ-ноды, орфаны, cycles |
| `codebase_graph_circular` | Найти циклические зависимости |
| `codebase_graph_visualize` | Mermaid-диаграмма ИЛИ интерактивный HTML |
| `codebase_graph_remove` | Удалить граф |

```bash
# Интерактивная визуализация (откроется в браузере):
codebase_graph_visualize(mode="interactive")
# Mermaid-диаграмма для чата:
codebase_graph_visualize(mode="mermaid")
```

### Flow-анализ

#### `codebase_flow` — Прямой flow
От entry-point ВПЕРЁД: что вызывает этот код.
```json
{"entrypoint": "main"}
{"entrypoint": "handleRequest", "file": "src/server.ts", "depth": 5}
```
Без аргументов → авто-определение entry-points (main(), роуты, тесты).

#### `codebase_impact` — Обратный blast radius
От цели НАЗАД: что сломается если изменить.
```json
{"target": "src/auth/service.ts"}
{"target": "validateToken", "depth": 5}
```

### Контекстные артефакты

Для `.socraticodecontextartifacts.json` — внешние знания: схемы БД, API-спеки, инфра-конфиги.

| Инструмент | Что делает |
|-----------|-----------|
| `codebase_context` | Список артефактов |
| `codebase_context_search` | Семантический поиск по артефактам |
| `codebase_context_index` | Индексировать артефакты |
| `codebase_context_remove` | Удалить артефакты |

```json
{"query": "billing tables", "artifactName": "database-schema"}
```

---

## Рабочие процессы

### Первый запуск на проекте
```
1. codebase_health          → проверить инфраструктуру
2. codebase_index           → запустить индексацию
3. codebase_status          → ждать 100% (поллить каждые 60s)
4. codebase_graph_build     → построить граф (авто после индексации)
5. Готово.                  → codebase_search, codebase_flow и т.д.
```

### Исследование кода
```
1. codebase_search("как работает X")     → найти релевантные файлы
2. codebase_symbols(file="...")          → посмотреть символы в файле
3. codebase_symbol(name="...")           → 360° обзор конкретного символа
4. codebase_flow(entrypoint="...")       → трассировать поток выполнения
```

### Анализ влияния изменений
```
1. codebase_impact(target="src/auth.ts") → что сломается?
2. codebase_graph_query(filePath="...")  → прямые зависимости файла
3. codebase_graph_circular()             → есть ли cycles поблизости?
```

### Визуализация архитектуры
```
1. codebase_graph_visualize(mode="interactive") → открыть в браузере
2. codebase_graph_stats()                       → статистика для отчёта
3. codebase_graph_circular()                    → problem areas
```

---

## Конфигурация

### `.socraticode.json` (в корне проекта)
```json
{
  "linkedProjects": ["../other-project"],
  "extraExtensions": ".tpl,.blade"
}
```

### `.socraticodecontextartifacts.json` (в корне проекта)
```json
{
  "artifacts": [
    {
      "name": "database-schema",
      "description": "PostgreSQL schema for the main database",
      "path": "docs/schema.sql"
    },
    {
      "name": "api-spec",
      "description": "OpenAPI specification",
      "path": "docs/openapi.yaml"
    }
  ]
}
```

### Переменные окружения
```bash
SEARCH_DEFAULT_LIMIT=10       # Дефолтный лимит результатов
SEARCH_MIN_SCORE=0.10         # Минимальный RRF score (0-1)
EXTRA_EXTENSIONS=".tpl,.hbs"  # Доп. расширения для индексации
```
