---
description: Final QA — production readiness gates before calling TitanOS shippable
alwaysApply: true
---

# FINAL QA

Do not call TitanOS production-ready until critical / high / medium issues are cleared **and** residual risk is documented honestly.

## Automated gates (must pass)

| Gate | Command |
|------|---------|
| Unit + structural pack | `npm test` (includes `test:final-qa`) |
| Lint | `npm run lint` |
| Typecheck | `npm run typecheck` |
| Production build | `npm run build` |
| E2E smoke | `npm run test:e2e` (after build; Chromium) |

## Structural contracts (`scripts/final-qa.test.mjs`)

- Every `APP_NAV_ITEMS` path resolves in `TabStack` (tabs or `NON_TAB_ROUTES`)
- History/reports money lists ship `ExportMenu` (Estimates, Leads, Payments, Tax, Contracts, …)
- Migrations **031–034** present on disk; hardening list includes **032** integrity
- GPS auto-trip watcher **stops** the geolocation watch when DoorDash owns GNSS
- Escrow page stays honest (practice hold / no fake money release)

## Manual / ops still required

Automated QA does **not** replace:

- Apply Supabase migrations **031–034** then `npm run test:db-security`
- One live Stripe Checkout → webhook settle
- Device GPS / background / poor reception on a real phone
- Auth-gated click-through of every screen after login

## Severity bar

- **Critical / High / Medium** — fix before “production-ready”
- **Low / controlled beta** — document in `docs/FINAL_QA.md`; do not claim zero residual risk

## Definition of done

Incomplete if `npm test` skips final-qa, nav paths are unrouted, money list exports are missing, or ops migrations/money E2E are claimed done without evidence.
