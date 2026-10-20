---
name: sk-features-index
description: Entry-point catalog of features already shipped by the TimeKast Starter Kit — answers "does the kit already ship X?" before a new feature is scaffolded. Rows cover auth, RBAC, notifications, email, PWA, navigation, tables, forms, audit logging, rate limiting, feature flags, and each row links to the detail `sk-*` skill. Use at the start of any new feature to decide between hooking into the existing system and building new.
last-verified: 2026-04-23
---

# sk-features-index — Kit-shipped feature catalog

> Catálogo de referencia. NO es SSOT de implementación — cada fila linkea a la skill que documenta el feature.

Pair: entry-point skill para el ecosistema `sk-*`. Este índice + las skills `sk-*` destino son el SSOT runtime de "qué trae el kit" (sucesor de `project/reference/features.md`, retirado en KIT-013).

---

## ¿Cómo usar este catálogo?

1. Al iniciar `/implement` de una feature nueva → consultar este índice primero ("¿el kit ya lo resuelve?").
2. Si la feature aparece en alguna tabla → ir a la skill destino (columna "Skill detalle") y engancharse al sistema existente.
3. Si NO aparece → feature real nueva; proceder con `kb-*` patterns + crear el sistema.

> Regla de oro: **NO re-implementar lo que el kit ya shipea**. Ver §Anti-patterns.

---

## Core Features (siempre activas)

| Feature                                                              | Entry point (path)                                                                                                                                                                                                                                                                      | Env vars                                                                                                                    | Skill detalle                                        |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Auth system (NextAuth v5)                                            | `src/lib/auth/` (auth.ts, utils.ts, password-reset.ts, super-admin.ts)                                                                                                                                                                                                                  | `AUTH_SECRET`, `AUTH_GOOGLE_*`, `AUTH_GITHUB_*`                                                                             | [`sk-security`](../sk-security/SKILL.md)             |
| RBAC (3 roles + fund_roles)                                          | `src/config/roles.ts` + `src/lib/auth/permissions.ts`                                                                                                                                                                                                                                   | —                                                                                                                           | [`sk-security`](../sk-security/SKILL.md)             |
| Super admin bootstrap                                                | `src/lib/auth/super-admin.ts` + `pnpm db:seed`                                                                                                                                                                                                                                          | `SUPER_ADMIN_EMAIL`, `SUPER_ADMIN_PASSWORD`, `SUPER_ADMIN_NAME`                                                             | [`sk-security`](../sk-security/SKILL.md)             |
| Notifications (in-app + push + email + prefs)                        | `src/lib/notifications/` + `src/config/notifications.ts`                                                                                                                                                                                                                                | `NEXT_PUBLIC_NOTIFICATIONS_ENABLED`, `NEXT_PUBLIC_VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT`, `RESEND_API_KEY` | `sk-notifications` + `kb-notifications`              |
| Navigation (Sidebar + BottomNav)                                     | `src/config/navigation.ts` + `src/components/layout/`                                                                                                                                                                                                                                   | —                                                                                                                           | `sk-navigation`                                      |
| PWA (SW, install, offline, push)                                     | `src/app/sw.ts` + `src/lib/pwa/`                                                                                                                                                                                                                                                        | `NEXT_PUBLIC_PWA_ENABLED`                                                                                                   | `sk-pwa`                                             |
| Pull-to-refresh primitives (shell-wide default + per-screen wrapper) | `src/components/pwa/PullToRefreshShell.tsx` (mounted in `DashboardShell`, gated by `isMobile()`, `router.refresh()`) + `src/components/pwa/PullToRefresh.tsx` (per-screen wrapper for custom scroll containers) + `src/lib/pwa/shellPullToRefresh.tsx` (`useDisableShellPTR()` opt-out) | —                                                                                                                           | `sk-pull-to-refresh`                                 |
| UI primitives (tables, forms, dialogs, layout)                       | `src/components/ui/` + `src/components/layout/`                                                                                                                                                                                                                                         | —                                                                                                                           | [`sk-ui`](../sk-ui/SKILL.md)                         |
| Design tokens (neomorphism DS)                                       | `src/app/globals.css` + `.claude/docs/design-system-neomorphism.md`                                                                                                                                                                                                                     | —                                                                                                                           | `sk-tokens-neomorphism`                              |
| Server Actions (withAuth / withSelf)                                 | `src/lib/actions/helpers.ts`                                                                                                                                                                                                                                                            | —                                                                                                                           | [`sk-api`](../sk-api/SKILL.md)                       |
| DB helpers (auditFields, softDelete, humanId, pagination)            | `src/lib/db/helpers/` + `src/lib/db/utils/pagination.ts`                                                                                                                                                                                                                                | `DATABASE_URL`                                                                                                              | [`sk-db`](../sk-db/SKILL.md)                         |
| CRUD scaffold (URL convention, page shells, breadcrumbs)             | `src/lib/contexts/` + `src/app/(protected)/` page shells                                                                                                                                                                                                                                | —                                                                                                                           | `sk-crud-scaffold`                                   |
| Email (Resend + 9 templates)                                         | `src/lib/email/` + `src/lib/email/templates/`                                                                                                                                                                                                                                           | `EMAIL_PROVIDER`, `RESEND_API_KEY`, `EMAIL_FROM`                                                                            | [`sk-email`](../sk-email/SKILL.md)                   |
| Invite system                                                        | `src/lib/invites/` + `invite_tokens` table                                                                                                                                                                                                                                              | `INVITATIONS_ENABLED`                                                                                                       | [`sk-security`](../sk-security/SKILL.md) §invites    |
| Audit log                                                            | `src/lib/audit.ts` + `audit_logs` table                                                                                                                                                                                                                                                 | —                                                                                                                           | [`sk-security`](../sk-security/SKILL.md) §audit      |
| Rate limiting                                                        | `src/lib/rate-limit.ts`                                                                                                                                                                                                                                                                 | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`                                                                        | [`sk-security`](../sk-security/SKILL.md) §rate-limit |
| Breadcrumb context                                                   | `src/lib/contexts/` + `BreadcrumbProvider`, `BreadcrumbSetter`                                                                                                                                                                                                                          | —                                                                                                                           | [`sk-ui`](../sk-ui/SKILL.md)                         |
| Unsaved changes guard                                                | `src/lib/contexts/UnsavedChangesContext.tsx` + `useUnsavedChangesGuard`                                                                                                                                                                                                                 | —                                                                                                                           | [`sk-ui`](../sk-ui/SKILL.md)                         |
| Structured logger                                                    | `src/lib/logger.ts`                                                                                                                                                                                                                                                                     | —                                                                                                                           | (trivial — `logger.info()` / `logger.error()`)       |
| Middleware (correlation-id)                                          | `middleware.ts`                                                                                                                                                                                                                                                                         | —                                                                                                                           | (trivial — no auth routing en SK)                    |
| Health check                                                         | `src/app/api/health/route.ts`                                                                                                                                                                                                                                                           | —                                                                                                                           | (trivial — `GET /api/health`)                        |
| Environment validation (Zod)                                         | `src/lib/env.ts`                                                                                                                                                                                                                                                                        | — (SSOT)                                                                                                                    | (trivial — `getEnv()`, nunca `process.env`)          |
| API client (typed fetch)                                             | `src/lib/api/client.ts`                                                                                                                                                                                                                                                                 | —                                                                                                                           | [`sk-api`](../sk-api/SKILL.md)                       |
| Theming (light / dark / midnight)                                    | `src/app/globals.css` + `next-themes`                                                                                                                                                                                                                                                   | —                                                                                                                           | `sk-tokens-neomorphism`                              |
| Testing (Vitest unit + component)                                    | `vitest.config.ts` + `vitest.setup.ts`                                                                                                                                                                                                                                                  | —                                                                                                                           | [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md) |
| E2E (Playwright + Neon branching)                                    | `playwright.config.ts` + `scripts/tools/e2e-runner.ts`                                                                                                                                                                                                                                  | `NEON_API_KEY`, `NEON_PROJECT_ID`                                                                                           | [`sk-e2e`](../sk-e2e/SKILL.md)                       |

---

## Optional Features (env-configured)

> Habilitadas/deshabilitadas vía env vars — todas viven detrás de un feature flag en `src/lib/env.ts`.

| Feature                         | Env flag                                                                                         | Dónde se consume                                                                                  | Skill detalle                                     |
| ------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Invitations (email-driven)      | `INVITATIONS_ENABLED`                                                                            | `src/lib/invites/`, `/api/invites/*`                                                              | [`sk-security`](../sk-security/SKILL.md) §invites |
| Hero images (landing / auth)    | `HERO_IMAGE_URL`                                                                                 | Páginas `(auth)/*` + landing                                                                      | —                                                 |
| PWA (service worker + install)  | `NEXT_PUBLIC_PWA_ENABLED`                                                                        | `src/app/sw.ts`, `src/lib/pwa/`                                                                   | `sk-pwa`                                          |
| Google OAuth                    | `NEXT_PUBLIC_AUTH_GOOGLE` + `AUTH_GOOGLE_ID/SECRET`                                              | `src/lib/auth/auth.ts`                                                                            | [`sk-security`](../sk-security/SKILL.md)          |
| GitHub OAuth                    | `NEXT_PUBLIC_AUTH_GITHUB` + `AUTH_GITHUB_ID/SECRET`                                              | `src/lib/auth/auth.ts`                                                                            | [`sk-security`](../sk-security/SKILL.md)          |
| Magic link auth                 | `NEXT_PUBLIC_AUTH_MAGIC_LINK` (requires email)                                                   | `src/lib/auth/auth.ts`                                                                            | [`sk-security`](../sk-security/SKILL.md)          |
| Self-registration (open signup) | `NEXT_PUBLIC_AUTH_REGISTRATION` + `NEXT_PUBLIC_AUTH_PASSWORD` (both default `true`; double gate) | `/register` page + `RegisterForm.tsx` + `/api/auth/register` (rate-limited via `register` bucket) | [`sk-security`](../sk-security/SKILL.md) §6.5     |
| Password reset                  | `NEXT_PUBLIC_AUTH_PASSWORD_RESET` (default `true`)                                               | `/forgot-password`, `/reset-password`                                                             | [`sk-security`](../sk-security/SKILL.md)          |
| Email verification              | `NEXT_PUBLIC_AUTH_EMAIL_VERIFY`                                                                  | `src/lib/auth/auth.ts`                                                                            | [`sk-security`](../sk-security/SKILL.md)          |
| Login alert (security email)    | `NEXT_PUBLIC_AUTH_LOGIN_ALERT`                                                                   | `src/lib/auth/auth.ts` callbacks                                                                  | [`sk-security`](../sk-security/SKILL.md)          |
| Sentry (error tracking)         | `NEXT_PUBLIC_SENTRY_DSN`, `SENTRY_ORG`, `SENTRY_PROJECT`, `SENTRY_AUTH_TOKEN`                    | `next.config.ts`                                                                                  | —                                                 |

---

## Env vars críticas

> **SSOT:** `src/lib/env.ts` (Zod schema) + `.env.example`. NUNCA usar `process.env` directo — siempre `getEnv()` / `getAuthFeatures()`.

| Variable                                                                     | Requerida                      | Propósito                                     |
| ---------------------------------------------------------------------------- | ------------------------------ | --------------------------------------------- |
| `DATABASE_URL`                                                               | ✅                             | Neon Postgres connection                      |
| `AUTH_SECRET`                                                                | ✅                             | NextAuth session encryption                   |
| `NEXT_PUBLIC_APP_URL`                                                        | ✅                             | Canonical URL (OAuth redirects, email links)  |
| `NEXT_PUBLIC_APP_NAME`                                                       | ✅                             | Branding display                              |
| `NEXT_PUBLIC_COMPANY_NAME`, `NEXT_PUBLIC_COUNTRY`, `NEXT_PUBLIC_LEGAL_EMAIL` | —                              | Legal pages content (`/privacy`, `/terms`)    |
| `SUPER_ADMIN_EMAIL`, `SUPER_ADMIN_PASSWORD`, `SUPER_ADMIN_NAME`              | — (seed only)                  | Bootstrap via `pnpm db:seed`                  |
| `NEXT_PUBLIC_NOTIFICATIONS_ENABLED`                                          | —                              | Feature flag del notification system completo |
| `NEXT_PUBLIC_VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT`         | —                              | Push notifications (web-push)                 |
| `RESEND_API_KEY` + `EMAIL_FROM`                                              | — (si `EMAIL_PROVIDER=resend`) | Email delivery                                |

> Lista completa: `src/lib/env.ts` (Zod schema, ~40 vars) + `.env.example` (179 líneas con docs inline).

---

## Config files (SSOT de configuración del kit)

| Archivo                       | SSOT de                                                                  |
| ----------------------------- | ------------------------------------------------------------------------ |
| `src/config/roles.ts`         | `ROLES`, `ROLE_HIERARCHY`, `ROLE_CONFIG` (3 roles + metadata por rol)    |
| `src/config/auth-features.ts` | Feature flags de auth (lazy Proxy, derivados de env)                     |
| `src/config/branding.ts`      | `appName`, `appTagline`, logos theme-aware                               |
| `src/config/navigation.ts`    | Sidebar items + BottomNav config (máx 4 tabs + "Más" sheet)              |
| `src/config/notifications.ts` | Categories (`system`, `security`, `general`), types, channels, retention |
| `src/config/status.ts`        | Entity status styling (`active`/`inactive` badges)                       |
| `src/config/app.ts`           | App-level constants                                                      |

---

## Anti-patterns (🔴 NO hacer)

> **NO re-implementar sistemas del kit.** Mirar la tabla Core antes de crear.

| ❌ Prohibido                                                     | ✅ Usar en su lugar                                                              |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Llamar `process.env.FOO`                                         | `getEnv()` desde `@/lib/env`                                                     |
| Hardcodear items de navegación en componentes                    | Append a `navigation[]` en `src/config/navigation.ts`                            |
| Hardcodear roles o labels de rol en UI                           | `ROLE_CONFIG` en `src/config/roles.ts` (`displayName`, `style`, etc.)            |
| Escribir `auth()` + `requirePermission()` + `safeParse()` a mano | `withAuth()` / `withSelf()` de `@/lib/actions/helpers`                           |
| Crear tabla sin `auditFields` + `softDeleteFields`               | Helpers en `src/lib/db/helpers/`                                                 |
| Enviar email con `fetch` directo a Resend                        | `sendEmail()` de `@/lib/email` + template existente                              |
| `console.log()` en prod                                          | `logger.info()` / `logger.error()` de `@/lib/logger`                             |
| Crear componente UI sin revisar catálogo                         | Consultar `project/reference/INVENTORY.md` ([`sk-ui`](../sk-ui/SKILL.md) §reuse) |
| Crear hook / helper / form-kit wrapper sin revisar registro      | Consultar `project/reference/HOOKS.md` — nombres canónicos e import paths        |
| Re-implementar notificaciones                                    | `notify()` / `notifyMany()` de `@/lib/notifications/service`                     |
| Delete físico                                                    | Soft delete vía `softDeleteFields` + `notDeleted()` query helper                 |

---

Cross-reference: [`sk-api`](../sk-api/SKILL.md) | [`sk-db`](../sk-db/SKILL.md) | [`sk-security`](../sk-security/SKILL.md) | [`sk-ui`](../sk-ui/SKILL.md) | [`sk-notifications`](../sk-notifications/SKILL.md) | [`sk-navigation`](../sk-navigation/SKILL.md) | [`sk-pwa`](../sk-pwa/SKILL.md) | [`sk-tokens-neomorphism`](../sk-tokens-neomorphism/SKILL.md) | [`sk-crud-scaffold`](../sk-crud-scaffold/SKILL.md) | [`sk-testing-nextjs`](../sk-testing-nextjs/SKILL.md) | [`sk-e2e`](../sk-e2e/SKILL.md)
