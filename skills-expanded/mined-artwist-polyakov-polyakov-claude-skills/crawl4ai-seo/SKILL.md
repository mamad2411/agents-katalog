---
name: crawl4ai-seo
description: |
  SEO-краулер сайтов на базе Crawl4AI.
  Полный аудит страниц: title, meta, H1, canonical, breadcrumbs, навигация, внутренние ссылки.
  Инвентаризация сайта, навигационный аудит, сравнение лендингов, анализ конкурентов.
  Работает для Google и Яндекс SEO (Cyrillic URL, коммерческие факторы, региональность).
  Связка с yandex-search-api, yandex-metrika, yandex-webmaster, scrapedo-web-scraper.
  Triggers: crawl4ai, seo crawl, site audit, page inventory, site inventory,
  on-page audit, internal links, internal linking audit, navigation audit,
  landing comparison, competitor analysis, competitor pages, orphan pages,
  technical seo, аудит сайта, краулер, перелинковка, навигационный аудит.
---

# crawl4ai-seo

SEO-краулер для аудита сайтов и конкурентного анализа. Отвечает на вопрос: **"что реально лежит на страницах и как сайт устроен изнутри"**.

Не заменяет SERP-инструменты (позиции, видимость) — дополняет их данными о содержимом и структуре страниц.

## Что умеет

| Задача | Описание |
|--------|----------|
| **Site inventory** | Полная инвентаризация страниц: URL, status, title, H1, meta, canonical, word count |
| **On-page audit** | Поиск проблем: пустые title/H1, дубли заголовков, битые canonical, thin content |
| **Internal linking audit** | Граф внутренних ссылок, orphan pages (0 входящих), слабо связанные страницы |
| **Navigation audit** | Breadcrumbs, nav-блоки, menu consistency, hub-страницы без исходящих ссылок |
| **Landing comparison** | Сравнение shortlist URL по on-page сигналам (title, H1, content, links) |
| **Competitor research** | Прогон страниц конкурентов через тот же pipeline, сравнение шаблонов |

## Config

Глобальные defaults: `config/defaults.example.json`, локальный override — `config/defaults.json`.
Подробности: [config/README.md](config/README.md).

Правило: в defaults **не** храним конкретный сайт или параметры клиента. Всё site-specific приходит через launch params и фиксируется в `cache/jobs/<job_id>/resolved_config.json`.

## Workflow

### Перед любым crawl

1. **Проверь окружение:**
   ```bash
   python3 scripts/doctor.py
   ```
   Если crawl4ai/playwright не готовы — остановись на seed/discovery, не имитируй crawl.

2. **Определи цель исследования:**
   - Полный аудит сайта → site inventory + navigation audit
   - Аудит лендингов → landing comparison
   - Анализ конкурентов → competitor research
   - Аудит перелинковки → internal linking audit

3. **Собери launch params:**
   - `target.domain` — домен исследования
   - `job.project` — проект/клиент
   - `job.label` — метка запуска

### Основной pipeline

```bash
# 1. Создать job
python3 scripts/init_job.py --domain https://example.com --project client-a --label full-audit

# 2. Собрать seed URL из sitemap/robots
python3 scripts/seed_urls.py --job-id <job_id>

# 3. Запустить crawl
uv run --script scripts/crawl_batch.py --job-id <job_id>

# 4. Построить навигационный отчёт
python3 scripts/build_navigation_report.py \
  --seed-job-id <seed_job_id> \
  --crawl-job-id <crawl_job_id> \
  --report-dir reports/<project>/<label>

# 5. Сравнить страницы
python3 scripts/compare_pages.py --job-id <job_id>
```

### Быстрый вариант (без отдельного init)

```bash
python3 scripts/seed_urls.py --domain https://example.com --project client-a --label quick-check
uv run --script scripts/crawl_batch.py --job-id <job_id>
```

## Scripts

| Script | Назначение |
|--------|-----------|
| `doctor.py` | Проверка окружения: uv, Python, crawl4ai, playwright, config |
| `init_job.py` | Создание job: `job_id`, `launch_params.json`, `resolved_config.json` |
| `seed_urls.py` | Discovery URL из sitemap/robots/файла → `seed.json` (работает без crawl4ai) |
| `crawl_batch.py` | Batch crawl через crawl4ai → `pages.ndjson`, `links.ndjson`, `summary.json` |
| `compare_pages.py` | Табличное сравнение crawled pages по on-page сигналам |
| `build_navigation_report.py` | Сводный навигационный аудит: orphans, weak hubs, breadcrumbs, menu drift |
| `common.py` | Shared helpers (не запускать напрямую) |

## Extracted SEO Signals

На каждую страницу (`pages.ndjson`) извлекаются:

**On-page:** title, description, keywords, canonical, robots, og:title, og:description, og:image, H1, headings hierarchy, word count.

**Navigation:** path depth, breadcrumbs (texts + URLs), nav blocks count, nav links count, nav URLs sample.

**Links:** internal/external links count. В `links.ndjson` — полный граф: source → target, anchor text, nofollow, same_domain.

## Navigation Audit Findings

`build_navigation_report.py` автоматически находит:

| Проблема | Что значит для SEO |
|----------|-------------------|
| **Orphan pages** (0 входящих ссылок) | Поисковик не найдёт страницу или не передаст ей вес |
| **Weakly linked** (1 входящая) | Страница получает минимум link equity |
| **Missing breadcrumbs** | Нет навигационной цепочки для бота и пользователя |
| **Breadcrumb inconsistency** | Разные trail signatures в одной секции — путаница в иерархии |
| **Weak nav template** | Hub-страница с подозрительно малым числом nav-ссылок |
| **Menu inconsistency** | Страницы теряют часть common nav targets (шаблон "дрейфует") |
| **Weak hubs** | Категория/раздел отдаёт <5 внутренних ссылок |
| **Duplicate titles** | Несколько страниц с одинаковым title — каннибализация |
| **Canonical mismatches** | canonical указывает не на себя |
| **Technical junk** | login-URL, php endpoints, asset-ссылки в навигационном слое |
| **Linked-not-seeded** | Сайт линкует URL, которых нет в sitemap |

## Связка с другими скиллами

| Сценарий | Скилл-партнёр | Порядок |
|----------|--------------|---------|
| SERP → on-page audit | `yandex-search-api` | Получи shortlist из SERP → прогони через crawl4ai |
| Organic landings → audit | `yandex-metrika` | Возьми top organic pages → проверь on-page quality |
| Индексация + audit | `yandex-webmaster` | Сравни indexed pages с crawled inventory |
| Anti-block fallback | `scrapedo-web-scraper` | При блокировке crawl4ai — fallback через Scrape.do |

## Cache Layout

```text
cache/jobs/<job_id>/
  launch_params.json      # raw params этого запуска
  resolved_config.json    # effective config после merge defaults + params
  manifest.json           # operational state и artifact paths
  seed.json               # seed URLs и метаданные discovery
  pages.ndjson            # одна запись на страницу
  links.ndjson            # одна запись на link edge
  summary.json            # компактная сводка
  markdown/               # сохранённый markdown контент
```

Каждый job изолирован. Параллельные запуски по разным сайтам безопасны.

## Output Hygiene

- stdout: только preview и пути к файлам.
- Полные данные: только в job files.
- Для анализа используй `rg`, `head`, `wc -l` по ndjson-файлам, не поднимай browser повторно.

## References

- [Workflow recipes and integration scenarios](references/WORKFLOWS.md)
- [Cache layout and output schema](references/OUTPUT_SCHEMA.md)
