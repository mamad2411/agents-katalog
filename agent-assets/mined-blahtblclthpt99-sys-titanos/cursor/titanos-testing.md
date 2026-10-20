---
description: Testing — unit, integration, e2e, regression, perf, a11y, security, offline, GPS, voice, AI
alwaysApply: true
---

# TESTING

Automated tests protect money, driver, auth, and critical OS flows. Prefer fast Node unit tests; keep e2e thin.

## Pyramid

| Layer | Tool | Focus |
|---|---|---|
| Unit | `node --test` + `scripts/node-test-setup.mjs` | Pure libs: fees, money, driver, export, search, settings, AI intents, GPS owner, voice parse |
| Integration | Node + ops scripts | API error hygiene, RLS (`test:db-security`), payments drills |
| E2E | Playwright (`test:e2e`) | Smoke critical paths; Chromium in CI; Firefox/WebKit local |
| Regression | Hardening + suite pack | Source/policy smoke + full `npm test` |
| Performance | Microbench + `ops:load*` | Search/export hot paths; HTTP load against deploy |
| Accessibility | Catalog + source checks | Documented settings; touch/contrast rules smoke |
| Security | Existing + security regression | Payments, hire, auth guards, AI allowlist, no secret leaks |
| Offline | Local store / search snapshot | Reads/writes without network |
| GPS simulation | `gpsOwner` + DoorDash fixtures | DoorDash wins GNSS; no dual-owner claim |
| Voice | `voiceCommands` / coach parse | Intent mapping without mic hardware |
| AI workflows | `ALLOWED_AI_INTENTS` + honesty | No hallucinated intents; send_invoice labeled |
| Cross-browser | Playwright projects | chromium / firefox / webkit |
| Cross-device | Playwright viewports | mobile / tablet / desktop |

## Commands

- `npm test` — full unit/integration pack (CI)
- `npm run test:e2e` — Playwright smoke after `npm run build` (Chromium; CI installs browsers)
- `npm run test:e2e:browsers` — Chromium/Firefox/WebKit + mobile viewport
- `npm run test:db-security` — live Supabase (secrets)
- `npm run ops:load:smoke` — deploy perf smoke

E2E expects a production build (`dist/`). Playwright starts `vite preview` unless `PLAYWRIGHT_BASE_URL` is set.

## Definition of done

Incomplete if new business logic ships without a Node test, if CI skips `npm test`, if AI/money paths lack allowlist/security coverage, or if final-qa structural gates are skipped.
