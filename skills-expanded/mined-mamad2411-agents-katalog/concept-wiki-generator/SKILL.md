---
name: concept-wiki-generator
description: Generate atomic LLM-Wiki concept pages from existing sources (QUICKSTART, ADR, methodology, research). Use when populating wiki/concepts/, regenerating wiki/INDEX.md and wiki/graph.json, or adding new concepts to an existing wiki layer. Triggers on /wiki-generate or manual concept harvest.
trust_tier: 1
trust_tier_label: Structured
model_routing:
  scan: haiku
  synthesize: sonnet
  graph_build: haiku
---

# Concept Wiki Generator

Генерирует LLM-Wiki слой (по концепции Karpathy) поверх существующих документов в проекте: атомарные self-contained концепт-страницы + canonical index + JSON-граф для LLM resolver.

## Когда использовать

- Создаётся новый концепт (доменная сущность 1-го класса)
- Регенерируется wiki/ после изменений в ADR / methodology / research
- Добавляются "See also" backlinks в существующие документы
- Расширяется coverage от пилота (5 концептов) к полному (~20)

## Что такое "концепт 1-го класса"

Доменная сущность, удовлетворяющая всем трём критериям:

1. **Появляется в QUICKSTART.md** как именованный архитектурный/бизнес-элемент
2. **Поддерживается минимум 1 ADR** (архитектурное решение про неё)
3. **Поддерживается минимум 1 methodology или research** (числовое или фактологическое обоснование)

Концепты НЕ являются: ADR (они — pillar, не концепт), методология (тоже pillar), отдельный feature ADR на S-tier (слишком мелко).

## Output Format

### Концепт-страница `wiki/concepts/{slug}.md`

YAML frontmatter:
```yaml
---
slug: <kebab-case>
type: concept
title: <Human Title>
pillars:
  adr: ["<adr-slug>"]
  methodology: ["<methodology-slug>"]
  research: ["<research-slug>"]
related_concepts: ["<other-concept-slug>"]
status: active | proposed | deprecated
last_updated: YYYY-MM-DD
---
```

Тело (max ~80 строк):
1. **TL;DR** — 1 параграф, атомарное определение (читается БЕЗ контекста)
2. **Three Pillars** — таблицы по 3 раздела (ADR / Methodology / Research)
3. **Related Concepts** — `[[wikilinks]]` к смежным концептам + 1 строка про каждую связь
4. **Context Bundle for LLM** — нумерованный список минимальных файлов для inject в LLM-контекст
5. **Open Questions** — что неясно/требует решения

### Index `wiki/INDEX.md`

Canonical map ВСЕХ узлов (concept + adr + methodology + research) с таблицей покрытия пилларов.

### Graph `wiki/graph.json`

```json
{
  "version": "0.1.0",
  "nodes": [{"id": "...", "type": "concept|adr|methodology|research", "title": "...", "file": "..."}],
  "edges": [{"from": "...", "to": "...", "type": "supported-by-adr|supported-by-methodology|supported-by-research|related-concept"}],
  "integrity": {
    "concepts_with_full_triple_pillar": <int>,
    "concepts_missing_research": [...],
    "concepts_missing_methodology": [...],
    "concepts_missing_adr": [...]
  }
}
```

## Pipeline (8 шагов)

### Step 1 — Source scan (haiku)
Просканировать `QUICKSTART.md`, `adrs/`, `methodologies/`, `researches/`. Извлечь все anchor-имена (концепты, упоминаемые ≥2 раз).

### Step 2 — Concept candidate ranking
Применить 3 критерия из секции "Что такое концепт 1-го класса". Отсортировать кандидаты по количеству inbound-ссылок.

### Step 3 — Pillar mapping (haiku)
Для каждого кандидата найти его поддерживающие ADR / methodology / research через grep + semantic match.

### Step 4 — Atomic page synthesis (sonnet)
Сгенерировать `wiki/concepts/{slug}.md` следуя Output Format. Если pillar отсутствует — добавить `<promise>TRIPLE_PILLAR_INCOMPLETE</promise>` секцию и явный warning.

### Step 5 — Cross-link insertion
Заполнить `Related Concepts` через `[[wikilinks]]` к другим концепт-страницам.

### Step 6 — Backlinks в source files
В каждый ADR/methodology/research добавить секцию между маркерами `<!-- wiki:see-also-start -->` и `<!-- wiki:see-also-end -->`. Если маркеры уже есть — заменить содержимое. НЕ трогать остальной текст.

### Step 7 — Index + graph regeneration (haiku)
Перегенерировать `wiki/INDEX.md` и `wiki/graph.json` со всеми узлами и рёбрами. Подсчитать integrity-метрики.

### Step 8 — Validation
Запустить `/triple-check wiki/concepts/*.md` для каждой новой страницы. Завершиться с `<promise>WIKI_GENERATED</promise>` если все концепты ≥3 pillars, иначе `<promise>WIKI_GENERATED_INCOMPLETE</promise>`.

## Rules

1. **НЕ дублировать контент** — концепт-страница ссылается на источник, не копирует его (TL;DR — единственное синтезированное)
2. **TL;DR должен быть atomic** — читается без контекста, без отсылок к "выше в документе"
3. **Каждая ссылка кликабельна** — относительный path к существующему файлу или валидный URL
4. **YAML frontmatter обязателен** — без него страница не парсится в graph.json
5. **Маркеры backlinks неприкосновенны** — `<!-- wiki:see-also-start -->` / `<!-- wiki:see-also-end -->` всегда регенерируются 1:1 с graph.json
6. **3-pillar discipline** — концепт без 3 китов помечается `INCOMPLETE`, не скрывается

## Anti-Patterns

| Anti-Pattern | Why bad | Fix |
|--------------|---------|-----|
| Концепт-страница длиннее 100 строк | Теряет atomic-свойство | Разбить на 2 концепта или вынести детали в pillar |
| Дублирование ADR-decision в концепт-странице | DRY violation, drift при изменении | Только ссылка на ADR + 1 предложение summary |
| Скрытие отсутствия pillar | Подрывает integrity | Явно `<promise>TRIPLE_PILLAR_INCOMPLETE</promise>` |
| Концепт без обратных ссылок в source | Граф направленный, не связный | Step 6 обязателен |
| Wikilinks без существующих target | Mort | Перед commit запустить `/wiki-link-check` |

## Related

- `commands/triple-check.md` — валидатор 3-pillar discipline для любого .md
- `shards/triple-pillar.shard.md` — governance shard для интеграции в pipeline phases
- `templates/concept.template.md` — шаблон atomic концепт-страницы
- `governance/triple-pillar.governance.md` — домен-агностичная спецификация 3-pillar протокола
