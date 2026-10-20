---
name: frontend-engineering
description: Write, refactor, debug and explain React or Angular frontend code with tests and accessibility checks. Use when the user asks to build a React or Angular component, fix hooks, signals or RxJS, add a form, or write component tests.
---

# Frontend Engineering (React · Angular)

Produce working, accessible, tested UI code that fits the user's framework, version and existing style, with the trade-offs explained.

## Inputs
- A task in words ("booking search screen with filters", "why does this re-render?")
- Existing components, `package.json`, `angular.json`, `tsconfig.json`, console errors, screenshots
- API contract (OpenAPI, sample JSON, problem-details error shape)
- Design notes or mock-ups (Figma links, screenshots)

If code is given, it wins over the written description when they disagree; flag the conflict.

## Defaults (state them at the top of the answer when used)
| Setting | Default if not stated | Detect from |
|---|---|---|
| React | React 19 + TypeScript (strict), Vite, TanStack Query for server state, Vitest + React Testing Library | `react` version in `package.json`, `vite.config.*`, Next.js `app/` folder |
| Angular | Angular 17+ standalone, signals, `@if`/`@for`, OnPush, typed reactive forms, `inject()` | `@angular/core` version, `angular.json` test builder |
| Angular tests | TestBed + the repo's runner (Vitest in new v21+ projects, Jest, or Karma/Jasmine) | `angular.json`, `jest.config.*`, `karma.conf.js` |
| Styling | Whatever the repo uses (CSS Modules, SCSS, Tailwind, Angular Material, MUI) | Existing components |
| Accessibility | WCAG 2.2 AA | Always |

Ask **one** question only if the framework or major version is unknown *and* the answer changes the code (e.g. Angular 15 NgModules vs 17+ standalone). Otherwise assume the defaults and say so.

## Which reference to read
| Request is about… | Read |
|---|---|
| React, JSX/TSX, hooks, Next.js/Vite React, Zustand, Redux Toolkit, TanStack Query, RTL | `references/react.md` |
| Angular, components, signals, RxJS, NgRx, reactive forms, interceptors, TestBed | `references/angular.md` |
| Accessibility, forms UX, loading/error/empty states, i18n, XSS, token storage, CSP | `references/ui-shared.md` (always skim for any new component) |
| A distinctive, heavily specified UI (login, OTP, wizard, marketing) | `references/ui-shared.md` → **Spec-level UI prompt** + **Design system first**; pair with `frontend-design` / Taste |
| Reviewing a finished component before returning it | `templates/component-checklist.md` |
| UI plus backend API (e.g. Angular UI + .NET API) | Framework file here; hand the API to the backend-engineering skill; share one contract |
| None clearly match | Ask one question: React or Angular, and which version? |

## Steps
1. **Clarify framework and version.** Detect from code or `package.json`; otherwise apply Defaults and state them.
2. **Route.** Read the matching framework file and `references/ui-shared.md`.
3. **Understand the existing code** (if given): folder layout, state library, styling, naming, test runner. Match it.
4. **Plan briefly** (2–5 bullets): components, state location, data flow, API calls, states to handle.
5. **Write the code** with a file path heading per file (e.g. `src/features/bookings/BookingList.tsx`). Complete units: imports, types, exports, providers/registration.
6. **Handle every UI state**: loading, error (with retry), empty, success; plus validation messages for forms.
7. **Write tests** in the repo's runner: render, user interaction, one error or empty state, one accessibility query (by role/label).
8. **Explain key decisions**: state choice, change detection/memoisation, trade-off rejected.
9. **Run the self-check** below and `templates/component-checklist.md`; fix before returning.

## Shared rules (both frameworks)
- **Don't mix framework idioms** (no `useEffect` thinking in Angular, no services/DI terms in React answers, no `*ngIf` in new Angular 17+ code).
- **TypeScript strict**; no `any` in public props/inputs; type API responses.
- **Accessible by default**: semantic HTML first, labels on every input, keyboard reachable, visible focus, `role="alert"`/`role="status"` for async messages.
- **Validate on the client for UX, never for security**; the API validates again.
- **Never** use `dangerouslySetInnerHTML` / `bypassSecurityTrust*` with untrusted data; never put tokens in `localStorage` by default (see `references/ui-shared.md`).
- **No secrets** (API keys with privileges) in frontend code or `.env` files shipped to the browser.
- **Cancel stale requests** (AbortController / `switchMap`); avoid race conditions on fast input.
- **Tests query by role/label/text**, not CSS classes or test IDs first.
- **Match the user's style and versions**; suggest upgrades separately.
- **Complete snippets**: no `...` or `// TODO` inside state, validation, auth, or error handling.
- **Flag deprecated APIs** (e.g. `ReactDOM.render`, `forwardRef` in React 19, `*ngIf`/`*ngFor` (deprecated in v20), class-based guards/interceptors, `HttpClientModule`).
- **Explain trade-offs** briefly; keep prose shorter than the code.

## Self-check
- [ ] Framework and version stated (detected or assumed)
- [ ] Correct reference file used; no mixed idioms
- [ ] Every file has a path; code compiles as written (imports, types, providers)
- [ ] Loading, error, empty and success states handled
- [ ] Accessibility checks from `references/ui-shared.md` pass
- [ ] Tests cover render, interaction, and an error/empty state
- [ ] No unsafe HTML, no tokens in `localStorage`, no secrets
- [ ] No `...` or TODO in critical logic; deprecated APIs flagged

## Output
1. **Assumptions** line: framework, version, state library, test runner.
2. **Plan** (2–5 bullets).
3. **Code**, one block per file with its path.
4. **Tests**, one block per file with its path, plus the run command (`npm test`, `ng test`, `npx vitest`).
5. **Key decisions & trade-offs** (≤ 6 bullets).
6. **Needs input / next steps**: API gaps, design questions, packages to install.

After editing this skill, rerun `evals/test-cases.md` (see benchmark-skill).
