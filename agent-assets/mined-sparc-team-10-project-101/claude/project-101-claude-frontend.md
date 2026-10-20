# Senior Frontend Developer Agent

Implements Jira tickets end-to-end on the CHH (Community Health Hub) React web frontend, in this monorepo's `frontend/` folder. Given a ticket ID, it reads the Jira story, gathers context from Confluence and the codebase, produces an implementation plan for developer and tech lead approval, implements the approved plan on a feature branch, reviews the code for quality and standards compliance, writes and verifies tests, then hands off to the (shared) PR Agent.

All configuration below is injected into every sub-agent. For the full task workflow, approval gates, and agent handoffs, read `.claude/agents/orchestrator.md`. For the backend counterpart, see `backend/CLAUDE.md`.

---

## Commands

Same commands as the backend side — `orchestrator.md` routes to this side automatically based on the ticket's `Side` (component/label, or `[FE]`/`[UI]` sub-task prefix from the Architect's task breakdown). See `backend/CLAUDE.md` §Commands for the full command list (`/task`, `/dev`, `/startup`, `/task-resume`, or just paste a Jira URL).

Example: `https://experionglobal.atlassian.net/browse/CHH-8` (this ticket has a `[FE] Mobile Entry Screen` sub-task).

---

## Project Identity

| Field | Value |
|---|---|
| Product | Community Health Hub (CHH) — see root `CLAUDE.md` and PRD-CHH-v2.2 |
| Stack Type | frontend |
| Primary Language | TypeScript |
| Repo shape | Single monorepo — this is `frontend/` inside it, not a standalone repo |
| Confluence Space Key | auto-derived at startup (shared with backend side) |

---

## Tech Stack

> **Locked:** framework choice below. No source (PRD, story pages, Jira) specifies
> a frontend framework — this was chosen deliberately to match the existing
> `frontend/` folder naming (not `mobile/`) and PRD's language ("mobile-first
> web platform" — a responsive web app, not a native app). Everything below
> the framework row is a reasonable default, not independently confirmed —
> adjust freely if the team wants something different; just update this file
> and the Decisions Log in root `CLAUDE.md` when you do.

| Concern | Technology |
|---|---|
| Framework | **React 18 + TypeScript + Vite** (locked) |
| Routing | React Router v6 |
| Server state / data fetching | TanStack Query (React Query) — wraps calls to the backend API |
| Local/UI state | React `useState`/`useContext` — no global store unless a real cross-cutting need appears (e.g. auth session) |
| Forms & validation | React Hook Form + Zod — mirrors the backend's schema-first FluentValidation approach; a Zod schema can mirror the contract's request shape |
| Styling | Tailwind CSS (mobile-first utility classes — fits the PRD's mobile-first requirement and needs no separate design-token setup while `needs-design` tickets are still pending real UI designs) |
| Component library | None locked — plain components for now. PRD §Questions notes design tokens are still TBC; revisit once real designs land. |
| HTTP client | `fetch` via a thin typed wrapper per API resource (see Application Code Structure) — generate types from `contracts/chh-api.v1.yaml` if/when an OpenAPI-to-TS generator is added |
| Auth | JWT stored in `localStorage` via `AuthProvider` (`context/AuthProvider.tsx`), so a page refresh doesn't drop the session — reversed from an earlier "in-memory only" decision by explicit product choice, 2026-09-07 (see that file's doc comment for the XSS-tradeoff reasoning); 24-hour session (widened from CHH-F01 AC3's original 1-hour value) |
| Testing | Vitest + React Testing Library + `@testing-library/user-event`; MSW (Mock Service Worker) to mock the backend contract in tests |
| Linter/Formatter | ESLint + Prettier |
| Build Tool | Vite (`vite build`, `vite preview`) |

---

## Layer Architecture

| Layer | Name | Purpose |
|---|---|---|
| Entry | Page | Route-level component (React Router route target); composes features, no business logic |
| Logic | Feature hook | Custom hook per feature (e.g. `useOtpRequest`) — form state, validation, calls the Data layer, exposes UI-ready state |
| Data | API client | Typed function per backend endpoint (e.g. `requestOtp(mobileNumber)`) — the only layer that calls `fetch`/TanStack Query directly |
| Cross-cutting | Providers | `AuthProvider` (JWT/session), `QueryClientProvider`, error boundary |

**Layer isolation rule (critical):** Pages must not call the API client directly — always through a feature hook. Feature hooks must not import React Router or page-level constructs. API client functions contain no component/hook logic — just typed request/response handling.

---

## Frontend-Specific Definition of Done

In addition to the root `CLAUDE.md` DoD checklist:

- [ ] Consumes the backend API exactly as documented in `contracts/chh-api.v1.yaml` (no guessed/undocumented fields) — see Interfaces section below
- [ ] No console errors or warnings in the browser console during the golden-path flow
- [ ] Mobile-first: verified at a narrow viewport (375px) before a desktop one — PRD is explicit this is a mobile-first product
- [ ] Basic accessibility: form inputs have associated labels, interactive elements are keyboard-reachable, color contrast isn't relied on alone for validation state (see CHH-F01 AC1's inline validation hint)

---

## Interfaces Consumed from Backend

Source of truth: `contracts/chh-api.v1.yaml` (see `.claude/rules/api-standards.md` §3 — contract-first rule, binding for both sides). Known CHH-F01 endpoints already scoped in the Jira task breakdown, not yet in the contract file:

- `POST /api/v1/auth/otp/request` — validate mobile number, trigger SMS OTP
- `POST /api/v1/auth/otp/verify` — verify 6-digit code, returns JWT + role

Do not guess a field or endpoint shape that isn't in the contract — flag it to the Architect/backend Coding Agent instead of working around it client-side (see `frontend-coding-agent.md` §What Not To Do).

---

## Agent Structure

Same monorepo layout as `backend/CLAUDE.md` §Agent Structure. This side's agents:

```
.claude/agents/
├── orchestrator.md                  ← shared — routes here by Side
├── startup-agent.md                 ← shared
├── pr-agent.md                      ← shared
├── frontend-knowledge-agent.md
├── frontend-planning-agent.md
├── frontend-coding-agent.md
├── frontend-code-review-agent.md
└── frontend-unittest-agent.md
└── designer.md                      ← shared frontend-design handoff
```

There is no `frontend-codebase-analysis-agent.md` — the Knowledge Agent does its own (smaller-scope) codebase exploration inline; a single component-tree scan doesn't warrant a separate delegate the way the backend's shared-repo-plus-microservice scan did.

---

## Application Code Structure

```
frontend/
├── src/
│   ├── pages/                 ← Entry Layer — route-level components
│   │   └── auth/
│   │       ├── MobileEntryPage.tsx
│   │       └── OtpVerificationPage.tsx
│   ├── features/              ← Logic Layer — one folder per feature
│   │   └── auth/
│   │       ├── useOtpRequest.ts
│   │       └── useOtpVerification.ts
│   ├── api/                   ← Data Layer — typed client per backend resource
│   │   └── authApi.ts
│   ├── components/            ← Shared, reusable UI components (no feature logic)
│   ├── context/                ← AuthProvider and other cross-cutting providers
│   ├── lib/                    ← Validation schemas (Zod), formatters, constants
│   ├── router.tsx
│   └── main.tsx
└── tests/
    └── setup.ts                ← Vitest + RTL + jsdom setup, MSW server bootstrap
```

Test files are co-located with source (`Component.test.tsx` next to `Component.tsx`) rather than mirrored into `tests/` — `tests/` holds only shared test infrastructure (setup, MSW handlers).

---

## Standards Documents

| Standard | File | Scope |
|---|---|---|
| API Standards | `.claude/rules/api-standards.md` | Shared contract-first rule (§3) — the API shape this side consumes |
| (Frontend coding/testing conventions) | Defined directly in `frontend-coding-agent.md` / `frontend-unittest-agent.md` — no separate standards file yet; split one out if this grows past what fits comfortably in those agent files |

---

## Test Configuration

| Config | Value |
|---|---|
| Test Command | `npm run test -- --run` (Vitest, non-watch mode) |
| Coverage Command | `npm run test -- --run --coverage` |
| Coverage Threshold | See `frontend-unittest-agent.md` §Test Quality Checklist |
| Test Environment | jsdom (via Vitest config) |
| Mocking | MSW for API calls; no real network access in tests |

---

## Deployment

| Concern | Value |
|---|---|
| Host | **Vercel** — git-push-to-deploy, project root set to `frontend/` |
| Build command | `npm run build` (Vite) |
| Output dir | `dist/` |
| URL | Vercel-generated (e.g. `https://chh-frontend.vercel.app`) until a custom domain is attached |
| API base URL | Set via a Vercel env var (e.g. `VITE_API_BASE_URL`) pointing at the deployed AWS backend — never hardcoded |
| CORS | Backend must allow the Vercel origin(s) (production + preview-deploy URLs) — see root `CLAUDE.md` Decisions Log 2026-09-05 |

---

## Memory

Shared with the backend side — see `backend/CLAUDE.md` §Memory. `.claude/repository-index.md` lists `frontend/` alongside `backend/` as a module row (see `startup-agent.md` Step 5).

---

## Output

Same as backend — see `backend/CLAUDE.md` §Output. Implementation plans, feature branches, and PRs all follow the same conventions across both sides (one shared PR Agent, one shared Git Branch Skill).

---

## Agent Directory

| Agent | File | Role |
|---|---|---|
| Orchestrator | `.claude/agents/orchestrator.md` | Drives the full task workflow; routes to backend-* or frontend-* agents by `Side` (shared) |
| Startup Agent | `.claude/agents/startup-agent.md` | Verify stack, module folders, and Jira access once per project (shared) |
| Knowledge Agent | `.claude/agents/frontend-knowledge-agent.md` | Fetch Jira ticket context; explore existing frontend patterns |
| Planning Agent | `.claude/agents/frontend-planning-agent.md` | Produce an approved implementation plan; checks design readiness |
| Designer | `.claude/agents/designer.md` | Design approved frontend stories before their Coding Agent is dispatched |
| Coding Agent | `.claude/agents/frontend-coding-agent.md` | Implement the approved plan in `frontend/` |
| Code Review Agent | `.claude/agents/frontend-code-review-agent.md` | Review quality, accessibility, type correctness, plan compliance |
| Unittest Agent | `.claude/agents/frontend-unittest-agent.md` | Write and verify tests; hand off to PR Agent when suite is green |
| PR Agent | `.claude/agents/pr-agent.md` | Draft and raise the pull request after tests pass (shared) |

Backend counterparts are listed in `backend/CLAUDE.md`.

---

## Skill Directory

Same skills as the backend side (`confluence-publish-skill`, `notify-skill`, `git-branch-skill`, `github-pr-skill`) — see `backend/CLAUDE.md` §Skill Directory. `ef-migration-skill` is backend-only, not used here.

---

## Orchestrator

For the full task workflow, approval gates, agent handoffs, and orchestration rules, read `.claude/agents/orchestrator.md`.
