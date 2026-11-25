---
name: mcp-full
description: >
  Полный MCP-арсенал: все серверы, все инструменты, все паттерны.
  5 серверов (codegraph, socrati-code, socraticode-official, lazyweb, gsd-browser),
  100+ инструментов. Триггеры: mcp, все инструменты, какие mcp, mcp full,
  что умеет gsd-browser, как искать по коду, как дизайн исследовать,
  как браузером управлять, codebase search, codegraph explore, lazyweb search,
  browser automation, полный список mcp, mcp tools, mcp capabilities.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Task
  - Web Search
  - AST Grep
  - LSP
  - Browser
---

# MCP Full — Полный арсенал

5 MCP-серверов, 100+ инструментов. Ниже — каждый сервер, каждый инструмент, когда и зачем.

> **Droid:** все 5 серверов подключены через `droid mcp add`. Проверить: `droid mcp list`.
> **Автономность:** `sessionDefaultSettings.autonomyLevel: "high"` в `~/.factory/settings.json` — без подтверждений.
> **Wiki:** `wiki/mcp/` — документация по каждому серверу.

---

## 1. CodeGraph — Семантический граф кода (4 инструмента)

**Суть:** предзагруженный граф кода (SQLite + tree-sitter). Вместо grep/read — один вызов, полный ответ. Требует `.codegraph/` в корне проекта.

### `codegraph_explore` — ВСЕГДА ПЕРВЫЙ

**Главный инструмент.** Принимает natural language вопрос ИЛИ имена символов. Возвращает verbatim-код + call paths + blast radius. ОДИН вызов заменяет цепочку grep→read→grep→read.

```
# Принимает ВСЁ:
codegraph_explore("как работает авторизация?")
codegraph_explore("AuthService.login, UserRepo.findByEmail")
codegraph_explore("мутация элемента, перерисовка сцены")
codegraph_explore("как X доходит до Y?")
```

### `codegraph_node` — Чтение файла или символа

Замена `Read`. Передай `file` (путь к файлу) → получишь полный исходник с номерами строк + зависимости. Передай `symbol` → вернёт тело символа + caller/callee trail.

```
codegraph_node(file="src/auth.ts")              # = Read, но с зависимостями
codegraph_node(symbol="loginUser", includeCode=true)  # тело + кто вызывает
```

### `codegraph_search` — Быстрый поиск символа

Только локация (файл:строка), без кода. Используй чтобы найти где что определено, потом `explore` для кода.

### `codegraph_callers` — Кто вызывает

Все call sites + callback-регистрации. Для понимания что сломается при изменении.

**Ключевое правило:** `explore` → ответ готов → НЕ читай файлы. Если `.codegraph/` нет в проекте → инструменты скрыты, юзай grep/read.

---

## 2. Socrati-Code — Сократический анализ (4 инструмента)

**Суть:** не даёт ответов — задаёт вопросы. Вскрывает слабые места, скрытые допущения, архитектурные дыры.

### `socratic_index` — Быстрая ориентация в директории

Каталогизирует структуру, извлекает темы, задаёт вопросы об организации.
```
socratic_index(directoryPath="src/", maxDepth=3)
```

### `socratic_analyze` — Глубокий разбор файла

Принимает `.md` или код. Задаёт серию сократических вопросов.
```
socratic_analyze(filePath="src/auth.ts", tone="friendly")
# tone: formal | friendly | roasting
```

### `socratic_question` — Точечный вопрос по теме

Не файл, а идея/паттерн/concern.
```
socratic_question(topic="error handling strategy in this codebase")
```

### `socratic_review` — Обзор всей директории

Сканирует все файлы, задаёт вопросы по каждому.
```
socratic_review(directoryPath="src/lib", tone="friendly")
```

**Когда:** нужно понять код а не просто прочитать. Особенно на старте проекта или при ревью.

---

## 3. SocratiCode Official — Гибридный поиск + граф (25 инструментов)

**Суть:** семантический поиск (Qdrant+Ollama) + граф зависимостей + контекстные артефакты. 25 инструментов, сгруппированы по назначению.

### Семантический поиск по коду

| Инструмент | Что делает |
|-----------|-----------|
| `codebase_search` | Семантический поиск — natural language → релевантный код |
| `codebase_symbols` | Список символов в файле ИЛИ поиск символа по имени |
| `codebase_symbol` | 360° обзор символа: определение, callers, callees, confidence |

```
codebase_search(query="как обрабатываются ошибки авторизации")
codebase_symbols(file="src/auth/service.ts")
codebase_symbol(name="validateToken", file="src/auth/middleware.ts")
```

### Индексация и управление

| Инструмент | Что делает |
|-----------|-----------|
| `codebase_index` | Запустить индексацию (асинхронно) |
| `codebase_update` | Инкрементальное обновление индекса |
| `codebase_status` | Прогресс индексации (0-100%) |
| `codebase_stop` | Остановить индексацию |
| `codebase_watch` | Авто-отслеживание изменений (start/stop/status) |
| `codebase_remove` | Удалить индекс |
| `codebase_health` | Проверка Docker, Qdrant, Ollama, embedding model |
| `codebase_about` | Информация о SocratiCode |
| `codebase_list_projects` | Все проиндексированные проекты |

### Граф зависимостей

| Инструмент | Что делает |
|-----------|-----------|
| `codebase_graph_build` | Построить граф зависимостей (асинхронно) |
| `codebase_graph_status` | Прогресс построения / статус |
| `codebase_graph_query` | Что импортирует файл + кто зависит от него |
| `codebase_graph_stats` | Статистика: файлы, рёбра, орфаны, cycles |
| `codebase_graph_circular` | Найти циклические зависимости |
| `codebase_graph_visualize` | Mermaid-диаграмма ИЛИ интерактивный HTML |
| `codebase_graph_remove` | Удалить граф |

### Flow-анализ

| Инструмент | Что делает |
|-----------|-----------|
| `codebase_flow` | Прямой flow от entry-point: что вызывает этот код |
| `codebase_impact` | Обратный blast radius: что сломается |

```
codebase_flow(entrypoint="main")
codebase_impact(target="src/auth/service.ts", depth=3)
```

### Контекстные артефакты (схемы БД, API-спеки, etc.)

| Инструмент | Что делает |
|-----------|-----------|
| `codebase_context` | Список артефактов (.socraticodecontextartifacts.json) |
| `codebase_context_search` | Семантический поиск по артефактам |
| `codebase_context_index` | Индексировать артефакты |
| `codebase_context_remove` | Удалить артефакты |

### Когда что использовать (SocratiCode vs CodeGraph)

| Задача | Инструмент |
|--------|-----------|
| «Кто вызывает функцию?» (точное имя) | CodeGraph `codegraph_callers` |
| «Как X доходит до Y?» (call path) | CodeGraph `codegraph_explore` |
| «Что сломается если поменять X?» | CodeGraph `codegraph_explore` |
| «Где определён символ?» | CodeGraph `codegraph_search` |
| «Прочитай файл» | CodeGraph `codegraph_node` |
| «Как работает авторизация?» (концептуально) | SocratiCode `codebase_search` |
| «Найди где обрабатываются ошибки» | SocratiCode `codebase_search` |
| «Покажи граф» (визуализация) | SocratiCode `codebase_graph_visualize` |
| «Есть ли cycles?» | SocratiCode `codebase_graph_circular` |
| «Что в БД-схеме?» | SocratiCode `codebase_context_search` |

**Правило:** точное имя → CodeGraph. Концептуальный вопрос → SocratiCode.

---

## 4. Lazyweb — Дизайн-исследования (21 инструмент)

**Суть:** 281K+ реальных скриншотов приложений, A/B-тесты, пейволы, онбординг, чекаут. Вместо «я думаю этот дизайн хорош» → «вот доказательства».

### Визуальный поиск

| Инструмент | Что делает |
|-----------|-----------|
| `lazyweb_search` | Поиск по UI-паттерну / компании / категории / платформе |
| `lazyweb_compare_image` | Найти визуально похожие скриншоты (image embedding) |
| `lazyweb_find_similar` | Расширить от скриншота до похожих примеров |
| `lazyweb_get_flows` | Многошаговые продуктовые флоу (онбординг, чекаут) |

```
lazyweb_search(query="mobile paywall fitness", platform="mobile", limit=20)
lazyweb_get_flows(query="onboarding", company="Duolingo")
lazyweb_compare_image(image_base64="...", platform="mobile")
```

### Аналитика A/B-тестов

| Инструмент | Что делает |
|-----------|-----------|
| `lazyweb_search_ab_tests` | A/B-тесты: пейволы, онбординг, чекаут, монетизация |

```
lazyweb_search_ab_tests(
  target_screen_description="subscription paywall with 3 tiers",
  product="MyApp", category="fitness",
  conversion_goal="annual plan share",
  include_images=true
)
```

### Оптимизация пейволов

| Инструмент | Что делает |
|-----------|-----------|
| `lazyweb_start_paywall_retrieve` | Разметка + поиск структурных близнецов (асинхр) |
| `lazyweb_get_paywall_retrieve` | Получить результат retrieval |
| `lazyweb_start_paywall_synthesize` | Полный пайплайн: разметка → friction diagnosis → гипотезы → winners |
| `lazyweb_get_paywall_synthesize` | Получить результат синтеза |
| `lazyweb_paywall_score` | Confidence × Upside × Boldness скоринг кандидатов |
| `lazyweb_paywall_cta_research` | CTA-фреймворк + корпус + A/B-наблюдения |

### Мокапы и отчёты

| Инструмент | Что делает |
|-----------|-----------|
| `lazyweb_generate_mockup` | Серверная генерация мокапа (синхронная, 25-55s) |
| `lazyweb_start_mockup` | Асинхронный мокап (~60-150s, без таймаута гейтвея) |
| `lazyweb_get_mockup` | Получить готовый мокап |
| `lazyweb_render_report` | Отрендерить research report на lazyweb.com |
| `lazyweb_publish_report` | Опубликовать HTML-отчёт |

### Утилиты

| Инструмент | Что делает |
|-----------|-----------|
| `lazyweb_list_categories` | Список категорий компаний |
| `lazyweb_health` | Проверка бэкенда |
| `lazyweb_check_update` | Проверка обновлений скилл-пака |
| `lazyweb_get_workflows` | Скачать workflow-инструкции |
| `lazyweb_fetch_best_practice` | Скачать winning design skill |

### Когда использовать Lazyweb

- **Дизайн/редизайн UI** — сначала `lazyweb_search`, потом решения
- **Пейвол/монетизация** — `start_paywall_synthesize` (полный пайплайн)
- **Онбординг/чекаут** — `lazyweb_get_flows` + `lazyweb_search`
- **Хочешь мокап** — `lazyweb_start_mockup` (асинхронный) или `lazyweb_generate_mockup`
- **Нужен отчёт** — `lazyweb_render_report`

---

## 5. GSD Browser — Браузерная автоматизация (50+ инструментов)

**Суть:** нативный Rust, Chrome CDP, 50+ инструментов. Версионированные refs, живой viewer, evidence bundles, semantic intents, batch-выполнение, vault, аннотации, записи.

### Навигация

`browser_navigate`, `browser_back`, `browser_forward`, `browser_reload`

### Снэпшот и Refs (ключевая фича)

**Refs версионированы** (`@v1:e1`, `@v2:e3`). После навигации/изменений старые refs становятся stale — всегда переснимай snapshot.

- `browser_snapshot` — снэпшот интерактивных элементов, получаешь refs
- `browser_get_ref` — метаданные ref'а
- `browser_click_ref`, `browser_hover_ref`, `browser_fill_ref` — действия по ref

**Режимы снэпшота:** `interactive` (default), `form`, `dialog`, `navigation`, `errors`, `headings`, `visible_only`

**Ресурс:** `gsd-browser://latest-snapshot` — живые данные снэпшота + refs (читай через MCP resources)

### Взаимодействие

- `browser_click`, `browser_type`, `browser_press`, `browser_hover`, `browser_scroll`
- `browser_select_option`, `browser_set_checked`, `browser_drag`, `browser_upload_file`
- `browser_set_viewport` — preset: mobile/tablet/desktop/wide или свои размеры
- `browser_emulate_device` — полная эмуляция устройства

### Семантические интенты (без селекторов!)

| Инструмент | Что делает |
|-----------|-----------|
| `browser_find_best` | Найти лучшего кандидата под интент |
| `browser_act` | Найти и кликнуть/сфокусировать за один вызов |
| `browser_act_instruction` | Natural-language инструкция («введи email и нажми продолжить») |

**15 интентов:** `submit_form`, `close_dialog`, `primary_cta`, `search_field`, `next_step`, `dismiss`, `auth_action`, `back_navigation`, `fill_email`, `fill_password`, `fill_username`, `accept_cookies`, `main_content`, `pagination_next`, `pagination_prev`

### Формы

- `browser_analyze_form` — разобрать структуру формы (labels, types)
- `browser_fill_form` — заполнить по идентификаторам (label → name → placeholder → aria-label)

### Инспекция

- `browser_accessibility_tree`, `browser_page_source`, `browser_eval`
- `browser_find` — по тексту/роли/селектору
- `browser_console`, `browser_network`, `browser_dialog`, `browser_timeline`

### Assertions (18 видов проверок)

`url_contains`, `title_contains`, `text_visible`, `text_hidden`, `selector_visible`, `selector_hidden`, `value_equals`, `checked`, `no_console_errors`, `no_failed_requests`, `request_url_seen`, `response_status`, `console_message_matches`, `network_count`, `console_count`, `element_count`, `no_console_errors_since`, `no_failed_requests_since`

### Batch (атомарное выполнение)

`browser_batch` — несколько шагов в одном вызове. Сокращает round-trips, падает на первой ошибке. Поддерживает: navigate, click, type, key_press, wait_for, assert, click_ref, fill_ref.

### Wait Conditions (11 условий)

`selector_visible`, `selector_hidden`, `url_contains`, `network_idle`, `delay`, `text_visible`, `text_hidden`, `request_completed`, `console_message`, `element_count`, `region_stable`

### Визуализация

- `browser_screenshot` — скриншот (JPEG/PNG, full-page, по селектору)
- `browser_visual_diff` — визуальная регрессия (baseline vs текущий)
- `browser_zoom_region` — захват + апскейл региона
- `browser_save_pdf` — страница в PDF

### Live Viewer + Human Collaboration

- `browser_view` — открыть живой viewer (токенизированный URL)
- `browser_goal` — установить баннер цели для человека
- `browser_takeover` / `browser_release_control` — передача управления
- `browser_pause`, `browser_resume`, `browser_step`, `browser_abort` — пошаговый контроль
- `browser_sensitive_on` / `browser_sensitive_off` — режим конфиденциальности
- `browser_annotations` / `browser_annotation_*` — аннотации от человека
- `browser_record_start/stop/pause/resume` — запись флоу
- `browser_recording_get/export/discard/validate` — работа с записями
- `browser_generate_replayable_test` — сгенерировать Playwright-тест из записи

### Данные и состояние

- `browser_extract` — структурированное извлечение данных (CSS селекторы → JSON)
- `browser_save_state` / `browser_restore_state` — cookies, localStorage, sessionStorage
- `browser_vault_save`, `browser_vault_login`, `browser_vault_list` — шифрованный vault

### Сеть и эмуляция

- `browser_mock_route`, `browser_block_urls`, `browser_clear_routes`
- `browser_trace_start/stop`, `browser_har_export`

### Страницы и фреймы

- `browser_list_pages`, `browser_switch_page`, `browser_close_page`
- `browser_list_frames`, `browser_select_frame`

### Безопасность и диагностика

- `browser_check_injection` — сканирование на prompt injection
- `browser_session_summary`, `browser_debug_bundle`
- `browser_action_cache` — self-healing кеш intent→selector
- `browser_daemon_*` — управление демоном

### Глобальная фича: `--session`

Именованные сессии для изоляции параллельных браузеров. **Всегда используй session** для production-воркфлоу.

```
gsd-browser --session checkout-flow navigate https://shop.com
```

---

## Матрица: когда какой сервер

| Задача | Сервер | Инструмент |
|--------|--------|-----------|
| Найти где определён символ | CodeGraph | `codegraph_search` |
| Понять как работает функция | CodeGraph | `codegraph_explore` |
| Call path от A до B | CodeGraph | `codegraph_explore` |
| Кто вызывает функцию | CodeGraph | `codegraph_callers` |
| Прочитать файл | CodeGraph | `codegraph_node` (вместо Read) |
| Найти код по смыслу | SocratiCode | `codebase_search` |
| Визуализировать граф | SocratiCode | `codebase_graph_visualize` |
| Циклические зависимости | SocratiCode | `codebase_graph_circular` |
| Flow от entry-point | SocratiCode | `codebase_flow` |
| Blast radius изменения | SocratiCode | `codebase_impact` |
| Схема БД / API-спека | SocratiCode | `codebase_context_search` |
| Сократический разбор | Socrati-Code | `socratic_analyze` |
| Сократический обзор | Socrati-Code | `socratic_review` |
| UI-исследование | Lazyweb | `lazyweb_search` |
| Пейвол A/B-тесты | Lazyweb | `lazyweb_start_paywall_synthesize` |
| Онбординг-флоу | Lazyweb | `lazyweb_get_flows` |
| Визуально похожие скрины | Lazyweb | `lazyweb_compare_image` |
| Мокап редизайна | Lazyweb | `lazyweb_start_mockup` |
| Открыть URL в браузере | GSD Browser | `browser_navigate` |
| Заполнить форму | GSD Browser | `browser_snapshot` → `browser_fill_ref` |
| Сделать скриншот | GSD Browser | `browser_screenshot` |
| Визуальная регрессия | GSD Browser | `browser_visual_diff` |
| Auth через vault | GSD Browser | `browser_vault_login` |
| Скрапинг данных | GSD Browser | `browser_extract` |
| Human-in-the-loop | GSD Browser | `browser_view` + `browser_takeover` |
| Сгенерировать Playwright тест | GSD Browser | `browser_generate_replayable_test` |

---

## Золотые правила

1. **CodeGraph first для кода.** Если есть `.codegraph/` — `explore` до `grep/read`. Один вызов заменяет 5-15.
2. **CodeGraph + SocratiCode — комплементарны.** CodeGraph для точных имён и call-paths, SocratiCode для концептуальных вопросов и семантического поиска.
3. **Lazyweb до дизайн-решений.** Никаких «я думаю этот паттерн работает» — сначала `lazyweb_search`.
4. **GSD Browser: snapshot → refs → act.** Никогда не действуй без свежего снэпшота после навигации.
5. **Bash — последнее средство.** CodeGraph и SocratiCode покрывают 90% вопросов о коде. Bash/grep только когда они не дали ответ.
6. **Сессии в GSD Browser.** Всегда `--session` для изоляции, особенно для MCP-воркфлоу.

---

## Быстрый старт: топ-10 инструментов

1. **`codegraph_explore`** — 80% вопросов о коде закрывает ОДНИМ вызовом
2. **`codebase_search`** — «как работает X?» когда нет точных имён
3. **`lazyweb_search`** — «покажи как другие делают X»
4. **`browser_navigate` + `browser_snapshot`** — базовая связка GSD Browser
5. **`browser_batch`** — атомарные многошаговые флоу
6. **`browser_act_instruction`** — natural language → действия на странице
7. **`codebase_flow`** — «куда идёт выполнение от main()?»
8. **`codebase_impact`** — «что сломается если я поменяю X?»
9. **`lazyweb_start_paywall_synthesize`** — полный оптимизационный пайплайн для пейволов
10. **`browser_generate_replayable_test`** — запись → Playwright-тест одним вызовом
