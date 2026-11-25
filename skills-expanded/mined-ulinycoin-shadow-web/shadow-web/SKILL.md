---
name: shadow-web
description: >-
  Browser automation for Cursor via Shadow Web MCP and shadow-web exec: detail levels
  (minimal/terse/xml/full), page classifier, shadow_grep, navigate/click/fill by data-sid,
  SchemaSnap, content_outline/blocks, agent_run, diff snapshots, self-healing, Camoufox,
  navigation URL policy (url_guard), form fill (submit opt-in), price/stock change monitoring.
  Use when browsing the web, scraping, running shadow-web exec, compressing HTML, or when the
  user mentions shadow-web, shadow_grep, Action Map, data-sid, page_class, agent_run, url_guard.
---

# Shadow Web MCP

Shadow Web — локальный MCP для веб-автоматизации. Playwright смотрит всю страницу; **LLM видит только то, что запрошено** через `detail` и `shadow_query`.

**Не используй** `cursor-ide-browser`, если доступен `shadow-web`.

---

## Preflight / стоп-краны (любой кейс)

Перед browse/`exec`/`agent_run` — не начинай обходы, пока это не зелёное:

1. **LLM key в этом процессе.** `exec`/`agent_run` читают `os.environ` (+ `.env` из cwd/project). Hermes/tool runners часто **не** прокидывают секреты в children → всегда `--api-key "$DEEPSEEK_API_KEY"` или ключ в env MCP-сервера. Один fail `missing_api_key` / `No LLM API key` → чини ключ, **не** уходи в thin-обход.
2. **Browser honesty.** В ответе `navigate`/`snapshot` смотри `browser_type`, `browser_fallback`. Нужен Camoufox, а `browser_fallback=true` или `browser_type=chromium` без запроса → **стоп**, почини Camoufox (`camoufox fetch`, restart MCP). Тихий fallback выключен; опционально `SHADOW_WEB_ALLOW_CHROMIUM_FALLBACK=1`.
3. **`page_class` = закон.** `Anti-bot` / `SparseShell` → максимум **один** recovery (consent / другой URL той же задачи), потом стоп + отчёт. Не долби тот же tool с теми же args.
4. **Один фикс на ошибку.** Тот же fail ≥2 → эскалация человеку. Маршрут дальше только по сигналу страницы (`page_class`, `action_count`, `complete`/`next_hint`), не по нише сайта.
5. **URL policy (`url_guard`, v0.4.2).** Агентная навигация — только `http`/`https` на публичных хостах. Отказ на `file://`, `localhost`, `10.x`, `169.254.169.254` и т.п. — это политика, не поломка сайта; для локального сервера/тестов нужен `SHADOW_WEB_ALLOW_PRIVATE_URLS=1` в окружении **этого** процесса (никогда в деплое).

---

## Жёсткие правила (токены)

1. **Никогда** `detail="full"` без явной отладки по просьбе пользователя.
2. **Никогда** не читай/не пересказывай целиком `groups`, `xml_map`, `action_map` из ответа — они огромные.
3. После `navigate` / `snapshot` смотри только: `url`, `title`, `action_count`, `page_class`, `groups_summary` — затем **`shadow_query`**.
4. Лимит: **не более 1× `detail="xml"` или `full` на 5 tool calls**.
5. После клика — **`snapshot(diff=true, detail="terse")`**, не полный переснимок.
6. **Таблицы/формы** — `schema_session()` (не `detail=full`, не `get_page_html` без нужды). Default `max_rows=50`; полный HTML только с `max_rows=0` / `max_chars=0`.

---

## Уровни детализации (`navigate`, `snapshot`)

| `detail` | Когда | Что в ответе |
|----------|-------|--------------|
| **`minimal`** | Разведка URL, проверка доступности | `url`, `title`, `action_count`, `groups_summary`, `page_class` |
| **`terse`** (default) | 90% сценариев | top-15 `action_map` + `groups_summary`; при `diff=true` — `appeared/changed/disappeared` |
| **`xml`** | Нужна структура DOM без fat JSON | `xml_map` + метаданные |
| **`full`** | Только отладка | `groups` + `xml_map` + `clean_html_preview` (≤500 символов) |

```text
navigate(url, detail="minimal")           # разведка
shadow_query("intent:login", format="terse")
click("3")
snapshot(diff=true, detail="terse")
```

`terse` в `navigate`/`snapshot` — **первые 15 элементов**, не «самые важные». Если нужного sid нет → `shadow_query`, не `detail="full"`.

---

## Класс страницы (`page_class`)

Каждый ответ `navigate`/`snapshot` содержит `page_class` и `page_class_reason`. Действуй по классу:

| Класс | Что делать |
|-------|------------|
| **Static** | Стандартный workflow |
| **SPA** | Readiness: consent dismiss + wait + scroll-until-content при бедном first paint. Если `action_count=0` → `snapshot(detail="terse")` ещё раз или сообщи пользователю |
| **SparseShell** | **Стоп.** Cookie/anti-bot шелл без контента после readiness (скролл не спас). Не индексируй и не долби `navigate` — сообщи пользователю |
| **Anti-bot** | **Стоп.** Сообщи: captcha/Cloudflare, headless не прошёл. Не долбить повторными `navigate` |
| **Shadow DOM** | Ок, flatten включён. При пропусках: `navigate(..., capture_mode="dual")` |
| **Closed Shadow** | `capture_mode="a11y"` или `dual` |
| **Iframe-heavy** | Предупреди: cross-origin iframe недоступен |
| **Auth-gated** | `shadow_query("intent:login")` → fill/click или попроси пользователя залогиниться |
| **WebMCP** | `webmcp_list_tools` → `webmcp_execute_tool`, DOM не нужен |

---

## Workflow по сценарию

| Сценарий | Шаги |
|----------|------|
| **Логин / форма** | `minimal` → `form_fill_plan(profile)` → `form_fill_execute(plan, answers)` |
| **Найти кнопку** | `shadow_query("label~/submit\|send\|ok/i")` или `type:button` + `type:a` |
| **Меню / навигация** | `shadow_query("group:Navigation")` |
| **Таблицы, odds, цены** | `schema_session()` или `shadow_query` по `label~` / `group:` |
| **Структура формы** | `schema_session()` → `forms[].fields` перед `fill` |
| **Статический HTML** | `compress_html` / `shadow_grep_html` / `schema_page(html)` — без браузера |
| **Мультишаг** | один baseline `navigate` → действия → только `snapshot(diff=true)` |
| **Поиск в сети** | `web_search(query)` → `shadow_query` по результатам → `click(sid)` |
| **Длинный текст / каталог / лента** | `content_outline` → `content_blocks(ids)`; catalog → `cards=`, feed → `feeds=` (без цен) |
| **Один JSON-ответ (sub-agent)** | MCP `agent_run(goal)` или shell: `shadow-web exec "task" --model …` (`pip install "shadow-web[agent]"`); смотри `complete`/`truncated`/`next_hint`; bulk → thin + pagination |
| **SPA-каталог в exec** | `schema_page` пустой → `content_outline` → `content_blocks(ids)` → `done` (не кликать по Action Map) |
| **Reddit search / read** | Skill `reddit-search-read`: только `old.reddit.com`, Camoufox, outline→pick ids (не p0–p5) |

---

## Инструменты

| Задача | Инструмент |
|--------|------------|
| Открыть страницу | `navigate(url, detail="minimal"\|"terse")` |
| Фильтр элементов | `shadow_query(query, format="terse")` |
| Клик / ввод | `click(sid)`, `fill(sid, value)` |
| Дельта после действия | `snapshot(diff=true, detail="terse")` |
| HTML без браузера | `compress_html`, `shadow_grep_html`, `schema_page(html)` |
| Таблицы / формы / списки | `schema_session()` после `navigate` (default max_rows=50) |
| Таблица → CSV / JSON | `schema_session_csv()` / `schema_session_json()` |
| Только таблицы | `schema_table(html)` или `schema_csv(html)` |
| Сырой HTML сессии | `get_page_html(max_chars=50000)` — осторожно с токенами |
| Web search | `web_search` |
| Form fill plan | `form_fill_plan(profile, url?, auto_submit=False, form_index)` — `auto_submit` по умолчанию **False** |
| Form fill execute | `form_fill_execute(plan, answers, profile, multi_step, max_steps, validate, auto_submit=False)` — одна отправка на URL, неотвеченные `ask` блокируют submit |
| Толстый агент (один JSON) | `agent_run(goal, max_steps, max_tokens, model, browser, session)` — свой браузер; конверт `stop_reason`/`complete`/`truncated`/`next_hint`; нужен `pip install "shadow-web[agent]"` + LLM-ключ в env процесса |
| Chrome 145+ WebMCP | `webmcp_list_tools`, `webmcp_execute_tool` |

### `capture_mode` (при Shadow DOM / a11y)

`auto` (default) | `dom` | `a11y` | `dual` — передай в `navigate(url, capture_mode="dual")` при `Closed Shadow` или пустом Action Map на видимой странице.

---

## shadow_grep — синтаксис

```text
type:button              # тег; многие «кнопки» — type:a
intent:login             # login, cart, search, …
group:Login Form         # семантическая группа
label~/checkout/i        # regex по label
type:a intent:cart       # AND
id:1,3,5                 # конкретные sid
```

Форматы `shadow_query`: **`terse`** (default), `json`, `xml`.

---

## Self-healing

`click`/`fill` → binding path → local heal (кэш `~/.shadow-web/heal_cache.json`) → LLM heal (`SHADOW_WEB_HEAL_URL` + `/v1/heal`).

v0.4.2: ключ кэша включает query string и fragment (хилл на одном SPA-роуте не переиспользуется на другом; старые записи кэша инвалидированы), контекст страницы перед отправкой во внешний heal-endpoint редактится (значения `textarea`/`input value`/`data-*` секреты вырезаны), верификация селектора — порог 0.8 и fail-closed. `SHADOW_WEB_HEAL_SHARE_CONTEXT=0` — слать только stub-лейбл.

```bash
python3 -m uvicorn server.main:app --host 127.0.0.1 --port 8000
```

Нужны `DEEPSEEK_API_KEY` или `OPENAI_API_KEY` в `.env` (читается из корня репо / `--env-file`, но **не** из cwd — с 0.4.2).

---

## Версия и состояние (проверять на диске, не по этому файлу)

| Факт | Значение |
|------|----------|
| Версия | `0.4.4` (`pyproject.toml` == `lhm.plugin.json` == `shadow_web.__version__` == `server.py` app version == README-баннер, сверяет `tests/test_tool_surface.py`) |
| Тесты | `548 passed, 2 skipped` из репо (`.venv/bin/python3 -m pytest tests/ -q`, ~14 с); локально 553 — плюс 5 в untracked `tests/test_upwork_alert_triage.py`, в репо не уезжает |
| Зависимость ядра | `schemasnap>=0.1.9` (PyPI) — `schema_snap.py` здесь фасад на 64 строки, ядро в `~/Desktop/schemasnap`. Релизить ядро **до** shadow-web |
| MCP | 27 tools; список генерится из кода, расхождение ловит `tests/test_tool_surface.py` |
| Каналы | PyPI (`pip install shadow-web`, `uvx shadow-web-mcp`), LobeHub (`lhm.plugin.json`), `npx skills add ulinycoin/shadow-web` (этот файл). `.claude-plugin/` в репо нет |
| Деньги | managed price/stock change monitor для DTC: `scripts/price_change_report.py scan|diff` → `reports/price_watch/` (гейты: PDP identity, trusted ≥70%, отказ self-diff). OSS — distribution, не выручка |
| Не продукт | security scan, token compression API, hosted browser cloud, anti-bot гарантии (`ROADMAP.md` kill list) |

Скрипты: `scripts/price_change_report.py` (scan/diff), `scripts/price_monitor_probe.py`, `scripts/localpdf_competitor_scan.py`, `scripts/security_surface_scan.py`, `scripts/demo_30s.sh`, `scripts/smoke_install.sh`.

---

## Ограничения

- Первый `navigate`: cold start Camoufox/Chromium ~3–8 с. В ответе всегда есть `browser_type`.
- Одна браузерная сессия — новый `navigate` заменяет контекст (в MCP — per-session: у каждой MCP-сессии своё состояние и свой лок, v0.4.2).
- `web_search` — Brave Search (+ Yahoo fallback), без API-ключей; headless с stealth UA.
- Anti-bot / SparseShell в headless → стоп (см. preflight), не бесконечный retry.
- **Camoufox живёт вне кэша:** `CAMOUFOX_INSTALL_DIR=~/Desktop/shadow/web/.camoufox` (инжектится в `~/.hermes/mcp-shadow-web-bridge.py`). Чистка диска стирает `~/Library/Caches/camoufox` вместе с браузером; после пересоздания `.venv` патч `camoufox/pkgman.py` (`INSTALL_DIR` из env) надо применить заново, затем `camoufox fetch`.

## Отладка

Output panel → **MCP Logs** (ищи `Browser: camoufox` vs fallback). Локально: `.venv/bin/shadow-web-mcp`.
