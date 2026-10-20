---
description: app2-billing — уязвимости OWASP Top 10, разный код в vulnerable/reference, каждая с PoC и SOLUTION.
globs: apps/app2-billing/**
alwaysApply: false
---

# app2 «Billing» — правило OWASP Top 10

Полный список — `docs/SPEC.md` §5 (V2.1–V2.6). Уровень: чинится ПРАВКОЙ КОДА.

## Реализация уязвимостей
- `vulnerable/src` и `reference/src` — РАЗНЫЙ код. `vulnerable/` воспроизводимо уязвим, `reference/`
  закрыт правильным паттерном. Общая схема БД/ассеты — в `apps/app2-billing/shared/`.
- Уязвимости должны быть НАХОДИМЫ за 60–90 мин с двухуровневой подсказкой (см. `docs/instructor-guide.md`)
  и при этом реалистичны (не «учебно-игрушечны» до абсурда).
- Флаги извлекаемы ТОЛЬКО через уязвимость; штатное API их не отдаёт (напр. `secret_flags` для SQLi,
  admin-only `/api/admin/flag` для privesc, `internal-metadata` для SSRF).

## Правильные паттерны фикса (reference/)
| Vuln | Уязвимо (vulnerable) | Фикс (reference) |
|------|----------------------|------------------|
| V2.1 IDOR | нет проверки владельца | `ownerId === user.id || admin`, 404 не-владельцу |
| V2.2 SQLi | конкатенация строк | параметризация `pg` (`$1`), allow-list сортировки |
| V2.3 Stored XSS | EJS `<%- %>` | `<%= %>` / DOMPurify + CSP |
| V2.4 Mass-assign | `Object.assign(user, body)` | явный allow-list полей; `role` — отдельным admin-путём |
| V2.5 Crypto | MD5/plaintext + `Date.now()` токен | `bcrypt`/`argon2` + `crypto.randomBytes(32)` + TTL + one-time |
| V2.6 SSRF | `fetch(userUrl)` без проверки | allow-list схем/хостов, блок приватных диапазонов, таймаут |

## Обязательно к каждой уязвимости
Security-события в логах и `security_audit` (см. правило logging) с полями, по которым
`docs/forensics.md` строит разбор: `authz.deny/allow`, `sql.error`, `role.change`, `ssrf.blocked`,
`upload.url.fetch`, `content.store`. Без этих событий разбор не соберётся — они часть Definition of Done.
