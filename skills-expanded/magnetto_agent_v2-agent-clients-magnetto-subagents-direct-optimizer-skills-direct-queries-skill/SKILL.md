---
name: direct-queries
description: |
  Работа с bad_queries — поисковые запросы автотаргетинга. Трактовка is_chronic / is_recent, TargetingCategory, подбор минус-слов, матчинг matched_keyword ↔ keyword.
---

# Анализ поисковых запросов Директа

## Таблица magnetto.bad_queries

Рейтинг реальных поисковых запросов пользователей (search terms). В отличие от bad_keywords (фразы, которые добавили мы), здесь — запросы, которые Яндекс сматчил с нашими ключами. Окно **180 дней** (больше чем у keywords/placements). Обновление ежедневно.

Витрина собрана `UNION ALL` из 4 клонов `direct_search_queries_goals_cab1..4` — содержит колонку **`cabinet_name` LowCardinality(String)** (`audit-magnetto-tab1..tab4`). Бенчмарки (`bench_roas`, `bench_goal_score`) и зоны считаются **per-cabinet × CampaignId**. Маппинг кабинет→проект см. в `direct_performance` skill.

**Ключевые поля**: **cabinet_name**, Query, CriterionType (KEYWORD/AUTOTARGETING), TargetingCategory, CampaignId, CampaignName, matched_keyword, clicks, impressions, cost, ctr, cpc, bounce_rate, days_active, is_chronic, is_recent, purchase_revenue, roas, goal_score, goal_score_rate, goal_rate_deviation, roas_deviation, bench_roas, bench_goal_score, zone_status, zone_reason.

## Особенности метрик

### goal_score — расширенный (20 целей vs 10 у keywords)
Включает дополнительные цели: Заявка на тендер, Начало оформления заказа, Заполнил/Отправил контакты, Клик по телефону (моб.), Скачивание файла, Добавить в избранное и др.

`goal_score_rate = goal_score / clicks` (без ×100, в отличие от bad_keywords).

### is_chronic и is_recent
- `is_recent = 1` — активен в последние 20 дней
- `is_chronic = 1` — активен 14+ дней (days_active ≥ 14): систематический запрос
- Хронический нецелевой (`is_chronic=1, goal_score=0`) — первый кандидат в минус-слова

### matched_keyword
Ключ, с которым сматчился запрос. Помогает понять: проблема конкретного ключа или широкое несоответствие.

## zone_status

**pending**: is_recent=0 ИЛИ clicks<5 ИЛИ cost<200.
**green**: ROAS>2, ИЛИ (goal_rate_deviation≥0 И goal_score≥20).
**red**: bounce>90%+нет ROAS / bounce>60%+нет ROAS+goal_dev<-0.5 / нет конверсий+cost>400.
**yellow**: всё остальное.

`zone_reason`: `r:bounce>90+no_roas`, `g:roas>2`, `g:gdev>=0+gs>=20` и т.д.

## Когда zone_status пересмотреть

- Информационные запросы в yellow → потенциальные клиенты ранней стадии
- Запросы конкурентов → однозначно минус, даже если cost < 400
- Брендовые запросы (Magnetto, Costura) → НИКОГДА в минус-слова
- Хронический red с низким расходом → is_chronic=1, cost=50, алгоритм ставит pending, но это систематика

## SQL-шаблоны

### Красные запросы — кандидаты в минус-слова
```sql
SELECT cabinet_name, Query, matched_keyword, CampaignName,
       clicks, cost, bounce_rate, goal_score, days_active, is_chronic, zone_reason
FROM magnetto.bad_queries
WHERE zone_status = 'red'
  -- AND cabinet_name = 'audit-magnetto-tab2'   -- если спрашивают про конкретный проект
ORDER BY cost DESC
LIMIT 30
```

### Хронические красные запросы — срез по всем кабинетам
```sql
SELECT cabinet_name, count()          AS red_queries,
       round(sum(cost))               AS wasted_cost,
       sum(clicks)                    AS wasted_clicks
FROM magnetto.bad_queries
WHERE zone_status = 'red' AND is_chronic = 1
  AND report_date = (SELECT max(report_date) FROM magnetto.bad_queries)
GROUP BY cabinet_name
ORDER BY wasted_cost DESC
```

### Хронические нецелевые — системная проблема
```sql
SELECT Query, matched_keyword, CampaignName,
       days_active, clicks, cost, goal_score, bounce_rate, zone_status
FROM magnetto.bad_queries
WHERE is_chronic = 1 AND goal_score = 0 AND is_recent = 1
ORDER BY cost DESC
```

### Зелёные — добавить как ключи
```sql
SELECT Query, matched_keyword, CampaignName,
       clicks, cost, roas, goal_score, goal_score_rate,
       round(goal_rate_deviation * 100, 0) AS deviation_pct, zone_reason
FROM magnetto.bad_queries
WHERE zone_status = 'green'
ORDER BY goal_score DESC
```

### Запросы автотаргетинга
```sql
SELECT Query, TargetingCategory, CampaignName,
       clicks, cost, bounce_rate, goal_score, zone_status, zone_reason
FROM magnetto.bad_queries
WHERE CriterionType = 'AUTOTARGETING' AND is_recent = 1
ORDER BY cost DESC
```

### Запросы по ключу — что реально ищут
```sql
SELECT Query, clicks, cost, bounce_rate, goal_score, zone_status
FROM magnetto.bad_queries
WHERE matched_keyword ILIKE '%<ключ>%'
ORDER BY cost DESC
```

### Срез по кампании
```sql
SELECT zone_status, count() AS queries, sum(cost) AS total_cost,
       sum(goal_score) AS total_gs, round(avg(bounce_rate), 1) AS avg_bounce
FROM magnetto.bad_queries
WHERE CampaignName ILIKE '%<название>%' AND is_recent = 1
GROUP BY zone_status
ORDER BY total_cost DESC
```
