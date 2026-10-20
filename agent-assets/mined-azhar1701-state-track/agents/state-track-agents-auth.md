# AUTH DOMAIN KNOWLEDGE

**Generated:** 2026-03-03
**Commit:** [current]
**Branch:** [current]

## OVERVIEW
Centralized identity management and role-based access control (RBAC) using Supabase Auth and custom PostgreSQL triggers.

## WHERE TO LOOK
| Component | File | Responsibility |
|-----------|------|----------------|
| Context Provider | `AuthContext.tsx` | Session persistence, admin status checks, and auto-redirection logic. |
| UI / Forms | `Auth.tsx` | Login/Signup views with Zod validation and Liquid Glass styling. |
| Hook | `useAuth.ts` | Consumer interface for accessing user state and signOut methods. |
| Definitions | `auth-context.ts` | TypeScript interfaces and the raw React Context object. |

## CONVENTIONS
- **Admin Detection**: Uses a dual-check system. First queries the `user_roles` table, then falls back to the `VITE_ADMIN_EMAILS` environment variable.
- **Redirection**: Authenticated users are automatically moved from `/auth` to `/admin` (if admin) or `/map` (if regular user).
- **Validation**: All form inputs must be validated via `authSchema` (Zod) before hitting Supabase.
- **Error Handling**: Use `handleApiError` for user-facing messages and `logger.error` for internal tracking.

## ANTI-PATTERNS
- **Direct Supabase Calls**: Avoid calling `supabase.auth` directly in UI components; use the `useAuth` hook or `AuthProvider` methods.
- **Hardcoded Roles**: Never check for "admin" strings in UI logic. Use the `isAdmin` boolean from `useAuth`.
- **Sensitive Data**: Do not store passwords or tokens in local state. Rely on Supabase's internal session management.
- **Blocking UI**: Always check the `loading` state from `useAuth` before rendering protected routes or navigation elements.
