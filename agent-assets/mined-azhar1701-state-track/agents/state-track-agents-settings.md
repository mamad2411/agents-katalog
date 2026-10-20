# Admin Settings Knowledge Base

## OVERVIEW
Centralized system configuration for geospatial layers, user roles, security policies, and automated reporting workflows.

## WHERE TO LOOK
| Feature | File | Responsibility |
|---------|------|----------------|
| User Access | `UserManagementSettings.tsx` | Role-based access control (RBAC) and activity logs. |
| Geo Config | `GeoLayerSettings.tsx` | CRS enforcement, default opacity, and Z-index management. |
| Security | `SecuritySettings.tsx` | MFA, session timeouts, rate limiting, and data encryption. |
| Reporting | `ReportSettings.tsx` | Bulk CSV import, auto-approval, and validation rules. |
| Data Safety | `BackupSettings.tsx` | Manual/scheduled JSON exports and database restoration. |
| Taxonomy | `CategorySettings.tsx` | Dynamic report categories with custom icons and colors. |
| Logic Hook | `../useSystemSettings.ts` | Shared persistence layer for configuration state. |

## CONVENTIONS
- **Persistence**: Use `useSystemSettings` for database-backed config; fallback to `localStorage` for UI-only state.
- **Validation**: Perform client-side checks (e.g., min/max photos, CRS strings) before calling `saveSetting`.
- **Feedback**: Always use `sonner` toasts with appropriate icons for success/error states.
- **Language**: Use Bahasa Indonesia for all user-facing labels and descriptions.

## ANTI-PATTERNS
- **Direct Mutation**: Never bypass `useSystemSettings` or `useAuth` when updating global state.
- **Silent Errors**: Avoid empty catch blocks; use `handleApiError` or `logger.error` for traceability.
- **Hardcoded IDs**: Don't hardcode UUIDs for roles or categories; fetch them from Supabase.
- **Blocking UI**: Always implement `saving` or `loading` states for long-running operations like bulk imports.
