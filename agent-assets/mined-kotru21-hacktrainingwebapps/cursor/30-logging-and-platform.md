---
description: Единый формат логов/аудита и контракты платформы скоринга (scoreboard/checker/planter).
globs: ["apps/**", "platform/**", "packages/shared/**"]
alwaysApply: false
---

# Логи, аудит и платформа скоринга

Спеки: `docs/SPEC.md` §6–§7, `docs/scoring.md`, запросы разбора — `docs/forensics.md`.

## Формат security-события (pino JSON, в stdout) — единый для обоих приложений
Обязательные поля: `ts` (UTC ISO), `level`, `service`, `team`, `reqId`, `event`, `route`,
`userId`, `srcIp`, `status`, `latMs`, и `meta`/`detail` (jsonb-подобный объект с контекстом).
- `reqId` — сквозной middleware, прокидывается через всю цепочку запроса (сшивка атаки в forensics).
- Логировать всегда: входящий запрос + security-события: `auth.login.ok/fail`, `auth.token.verified`,
  `authz.allow/deny`, `role.change`, `sql.error`, `ssrf.blocked`, `upload.url.fetch`, `content.store`.
- НЕ логировать: пароли, полные токены (только `sub`/`iat`/префикс), значения флагов.
- Дублировать security-события в таблицу `security_audit(id, ts, team, actor, event, route, src_ip, detail jsonb)`
  — переживает рестарт пода, основа для SQL-разбора.

## Платформа (контракты — соблюдать точно, `docs/scoring.md` §5)
- `flag-planter`: CronJob, tick=60c, кладёт `TRN{...}` в места из SPEC; таблица `planted_flags`.
- `scoreboard`: `POST /api/submit {team, flag}` c `X-Team-Token`; валидация+дедуп (`UNIQUE(submitter_team, flag)`),
  свежесть (`flag_ttl_ticks`), запрет own_flag, троттлинг 20/мин; ответы `accepted|duplicate|expired|own_flag|invalid`.
  Плюс `GET /api/scoreboard`, `GET /api/round`, `POST /api/round/next`. Таблицы: `planted_flags`,
  `submissions`, `sla_samples`, `rounds`.
- `checker`: CronJob, функциональный сценарий → `up|mumble|down` в `sla_samples`. Значения очков и веса —
  из `platform/scoreboard/config.yaml` (не хардкодить в коде).

## PostgreSQL стендов
ConfigMap `postgresql.conf`: `log_statement=all`, `log_connections=on`, `log_disconnections=on`,
`log_line_prefix='%m [%p] %u@%d %h '`. Grafana Alloy собирает логи postgres-подов с лейблом `service="postgres"`.
