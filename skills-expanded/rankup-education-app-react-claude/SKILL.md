# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

React 19 + TypeScript + Vite web client for school administration, quiz management, directory, and reporting. Talks to the RankUp Education .NET Web API (`../WebApi`, default `http://localhost:5255`). Same backend also serves the Flutter app (`../Mobile`).

## Commands

```powershell
npm install
copy .env.example .env     # sets VITE_API_BASE_URL=http://localhost:5255/api
npm run dev                # http://localhost:5173
npm run build               # tsc -b && vite build (build fails on type errors)
npm run preview
npm run lint                 # eslint .
npm run test                  # vitest run (all tests, once)
```

Single test file: `npx vitest run src/features/quizzes/domain/quizTypes.approval.test.ts`
Watch mode for one file: `npx vitest src/features/quizzes/domain/quizTypes.approval.test.ts`

CI (`.github/workflows/react-ci.yml`) runs on `React/**` changes: `npm ci`, lint, test, build — all four must pass.

## Architecture

Feature-first, mirroring the same Clean-Architecture split used in the Flutter app:

```
features/<feature>/
├── data/           API calls, mapping raw responses to domain types
├── domain/         types, business rules that are pure TS (these are what get unit-tested)
└── presentation/
    ├── components/
    ├── hooks/      TanStack Query hooks (useXQueries.ts)
    └── pages/
```

Features: `admin`, `authentication`, `dashboard`, `directory`, `home`, `notifications`, `parent`, `questions`, `quizzes`, `reports`, `student`, `teacher`.

Shared code lives in:
- `src/app/` — `App.tsx`, `router.tsx` (route table + role guards), `AppQueryProvider.tsx`, `environment.ts` (reads `VITE_*` env vars).
- `src/core/api/apiClient.ts` — the one HTTP client: JSON envelope parsing, auth header injection, 401 → token refresh. `src/core/api/types.ts` defines the shared `ApiResponse`/`ApiError` envelope shape.
- `src/core/auth/` — auth context/hooks consumed by route guards.
- `src/core/lookups/` + `src/core/components/LookupSelect.tsx` — generic dropdown data (`GET /api/lookups?type=...`).
- `src/core/components/`, `src/components/ui/` — Radix-UI-based design-system primitives (shadcn-style), styled with Tailwind.
- `src/lib/stores/` — Zustand stores for client-only UI state.

Every API response follows the backend's envelope: `{ success, message, data, errors }`. New API calls in `features/*/data/` should go through `apiClient.ts` and expect this shape — don't hand-roll `fetch`.

### Auth flow

Login (`POST /api/auth/login`) stores access + refresh tokens in `localStorage`; app boot validates via `GET /api/auth/me`; `apiClient` refreshes on 401 via `POST /api/auth/token/refresh`; logout calls `POST /api/auth/logout` and clears storage. Multi-role users switch their active session role via `POST /api/auth/switch-role` (`CurrentUser.role` = active/"Acting as", `CurrentUser.roles` = full list). Route guards in `features/authentication/presentation/components/RouteGuards.tsx` gate pages by role — check the route table in `README.md` before adding a page to know which roles should see it.

### UI convention: back button placement

`.cursor/rules/page-back-beside-title.mdc` (always-apply): on any page with a back control, the chevron sits **inline with the title, same row, left of it** — never stacked above/below. Use `PageHeader`/`AppPageHeader` with `backTo`/`onBack`, or match the `DirectoryListChrome` pattern manually. Primary actions (Create/Import/Refresh) go on the opposite side of the header, never between the back button and the title.

### Quiz domain rules that affect this codebase (see `.cursor/rules/quiz-*.mdc` and `docs/05_RankUp_Quiz_Business_QA.html` for full detail)

These are enforced by both API and UI — when changing quiz/question UI, check the docs, not just the current component:

- **Lifecycle**: Draft(60) → Published(61) → Archived(63); `62 Assigned` is retired (legacy only). Only PortalAdmin moves Draft → Published.
- **Approval ≠ publish**: Pending(40) → SchoolApproved(41) → Approved(42), or Rejected(43). School/Campus-admin approval never publishes — it just reaches SchoolApproved and the quiz stays Draft until PortalAdmin publishes. SchoolAdmin/CampusAdmin/Parent-created quizzes skip SchoolApproved and go straight Pending → (PortalAdmin) Approved → Published. Only the original creator can resubmit a Rejected quiz.
- **Published catalog is shared across schools**: `/quizzes` for Teacher/Coordinator/SchoolAdmin/CampusAdmin/PortalAdmin/Parent shows every published school-type quiz regardless of creator/school — don't filter the manage list by "my school" for these roles; a "Mine only" toggle is an optional client-side filter, not the default. Students remain scoped to their own assignments + Public audience.
- **Quiz edit requests**: after SchoolApproved/Approved/Published/Assigned, the owner can't PUT the quiz directly — the UI must route through "Request edit" (`/quizzes/:id`) and PortalAdmin/School/CampusAdmin review it from the "Edit requests" tile on `/quizzes`. A granted edit resets the quiz to Draft+Pending, so the UI should expect a resubmit step afterward.
- **One attempt only**: quiz create/edit/settings/assign forms never show an "allowed attempts" field, and the assign picker must lock/skip students who already have an assignment row for that quiz. Do not build retry/reassign UI.
- **Create-form optional fields**: Topic and Difficulty are always optional. School/Campus are role-scoped (see rule for the exact matrix) and must serialize as `undefined`/absent (→ API stores `NULL`), never `0`, when unset.
- **Result announcement**: while a quiz's assignment window is open, hide marks/correctness entirely (no "View result" button). After the due date, show partial (auto-graded-only) results. After the owner finalizes review, show full results including teacher-graded questions and lock the review page.
- **Partial-marks display**: values are always floored (`Math.floor`), never rounded, when showing calculated/awarded marks — mirror the backend formula in `WebApi/CLAUDE.md` rather than recomputing differently.

### Question bank approval is a different model from quiz approval

`docs/04_RankUp_Questions_Business_QA.html`: a question is bank-usable (attachable to a quiz) only once **PortalAdmin** publishes it (`Visibility=Public`, `IsActive=true`). A CampusAdmin/SchoolAdmin "approve" in the question UI is an endorsement only — it stays Inactive and restricted to the creator's own admin chain, and must not be shown as if it made the question quiz-ready. CampusAdmin can browse/endorse questions but has no quiz-attach UI at all (they can't manage quizzes).

### Auth: role requests & companion grants are mostly directory-only UI

Self-service extra-role requests (`/account`), directory companion grant/remove (Teachers/Parents/Coordinators list ⋯ menus), and the school-change admin queue (`/admin/directory/school-changes`) are real subsystems with their own rule matrix in `docs/02_RankUp_Authentication_Logic.html` §7b/§8 — check that doc before changing any of those flows, since role-combination rules (Parent+Teacher+Coordinator combinable; Student/PortalAdmin/SchoolAdmin/CampusAdmin exclusive) and PortalAdmin-only carve-outs (Parent companion mutations) are easy to get wrong.

### `docs/RankUp_Flutter_Mobile_App.md` is not current-state truth

That file is the original ambitious mobile spec (gamification, AI assistant, career guidance, portfolios). Later QA docs (`docs/04_RankUp_Students_QA.html` §7/§11) explicitly say most of that was dropped from the live product ("no fake rank/AI/streak cards"). Don't use it as a reference for what the React app should do — the dated `docs/0*_QA.html` files and this repo's actual code are authoritative.

### Docs discipline

Per `.cursor/rules/update-docs-with-every-change.mdc`, when a change affects a documented business rule, update the relevant `.cursor/rules/*.mdc` and (if applicable) the QA doc generator under `../docs/build_*.mjs` in the same change — don't leave the rule only encoded in the component.

## Related

- Full current route table and per-page role access: `README.md` in this folder (kept up to date there; not duplicated here to avoid drift).
- Backend contract/business rules: `../WebApi/CLAUDE.md`.
- Deployment checklist: `docs/DEPLOYMENT.md`.
