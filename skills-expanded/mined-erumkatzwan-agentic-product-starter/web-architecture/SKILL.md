---
name: web-architecture
description: Use when adding or changing a page, API call, feature flag or UI component in the Web app (apps/web-app). Covers structure, the API layer, auth, flags and the design system.
---

# Web architecture

React 19 + TypeScript (strict) + Vite + React Router.

## Where code goes

| Folder | Holds | Rules |
|---|---|---|
| `src/api/client.ts` | `request()` and `ApiError` | The only file that calls `fetch` |
| `src/api/endpoints.ts` | Every backend call, typed | Add new endpoints here; mirror the backend contracts |
| `src/auth/` | Session context and token storage | Pages use `useAuth()`, never storage directly |
| `src/features/<name>/` | One folder per page | Pages get `api` as a prop so tests can pass a fake |
| `src/ui/ui.tsx` | Button, TextField, Card, Alert, Page | Reuse before creating new components |
| `src/styles/` | `tokens.css` (generated) + `global.css` | Only `var(--…)` tokens; never hard-coded colours or sizes |

## Rules

- Change colours, spacing or type in `design/tokens.json`, then run `node design/build.mjs`. Never edit `tokens.css`.
- Show backend validation errors next to their field (`ApiError.fieldErrors`), other errors in an `Alert`.
- Every form has labels; every button has text; pages work with the keyboard.
- Feature flag keys match the backend and the iOS app.

## Checklist: new page

1. Endpoint in `src/api/endpoints.ts` (and in `test/fakeApi.ts`).
2. Page in `src/features/<name>/`, using `ui` components.
3. Route in `App.tsx`, behind a flag if unfinished.
4. Unit tests for the page's behaviour; an end-to-end test for the user journey.
