---
name: flowcompta-security-agent
description: Sécurité ComptaFlow — RLS Supabase, auth roles, API admin. Use when editing auth, profiles.role, migrations SQL, api/index.ts admin routes, or security policies.
---

# Agent sécurité ComptaFlow

## Fichiers critiques

- `supabase/migrations/20260619_rls_hardening.sql`
- `src/hooks/useAuth.ts` — rôle depuis DB uniquement
- `api/index.ts` — `POST /api/admin/create-sub-admin` (service role)
- `src/components/common/Auth.tsx` — inscription client only

## Règles

- Jamais d'escalade de rôle côté client
- Sub-admins créés via API super admin + service role
- Signups → `role: client` (trigger SQL)
- Tester avec `src/test/auth-integrity.test.ts`, `delete-profile.test.ts`

## Rôles

`client` | `sub_admin` | `super_admin`
