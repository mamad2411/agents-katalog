---
name: frontend-feature-sliced-design
description: Use when applying Feature-Sliced Design (FSD) to a React app — layer model, Steiger linter, when FSD shines vs hurts.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [react, typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related:
    [react, typescript, frontend-react-router, frontend-tanstack-query, frontend-msw, frontend-tailwind, ux-essentials]
---

# Feature-Sliced Design (FSD)

**Iron Law: imports flow downward only. `features/` may import `entities/` and `shared/`; it may NEVER import another `features/*` sibling, never `widgets/`, never `pages/`. If two features need to talk, the contract lives in `entities/` or `shared/` — not in a sibling import.**

**Versions:** Current `2.1` · No LTS series — _2.1 removed the `processes/` layer (use `features/` or `widgets/`); slice-name kebab-case is enforced; public API via `index.ts` only. Steiger `@feature-sliced/steiger-plugin-fsd` is the canonical linter — runs in CI, not just locally._

## Layer model (top → bottom)

| Layer       | Owns                                              | Imports from                        | Example                                                    |
| ----------- | ------------------------------------------------- | ----------------------------------- | ---------------------------------------------------------- |
| `app/`      | providers, routing, global styles, error boundary | every layer below                   | `App.tsx`, `<RouterProvider>`, `<QueryClientProvider>`     |
| `pages/`    | one screen = one slice; composes widgets/features | widgets, features, entities, shared | `pages/reports/` = `/reports/:id`                          |
| `widgets/`  | self-contained UI blocks shared across pages      | features, entities, shared          | `widgets/report-header/`, `widgets/sidebar-nav/`           |
| `features/` | one user-facing action / interaction              | entities, shared                    | `features/export-report-pdf/`, `features/toggle-favorite/` |
| `entities/` | business nouns + their UI/model/api               | shared                              | `entities/report/`, `entities/inspection/`                 |
| `shared/`   | framework-y, domain-agnostic                      | nothing above                       | `shared/api/`, `shared/ui/button/`, `shared/lib/dates/`    |

**`processes/` is deprecated in 2.1+.** If you see it in a tutorial, mentally map it to `features/` (single-action) or `widgets/` (composed UI).

## Slice and segment

- **Slice** = vertical business domain inside a layer: `features/export-report-pdf/`, `entities/report/`.
- **Segment** = horizontal split inside a slice. Standard set:

```
features/export-report-pdf/
├── ui/        # React components, presentational
├── model/     # state, hooks, store slices, business logic
├── api/       # network calls, request/response types
├── lib/       # local utilities (formatters, validators) — domain-bound
├── config/    # constants, feature flags
└── index.ts   # public API — re-exports ONLY what consumers may import
```

**Other segments are forbidden** by the linter. Don't invent `helpers/` or `utils/` — they go in `lib/`.

## Public API rule

```ts
// features/export-report-pdf/index.ts
export { ExportReportButton } from "./ui/ExportReportButton";
export { useExportReport } from "./model/useExportReport";
// internals stay internal — no export of api/request types
```

Consumers import from the slice root, never from segments:

```ts
import { ExportReportButton } from "@/features/export-report-pdf"; // ✅
import { ExportReportButton } from "@/features/export-report-pdf/ui/..."; // ❌ Steiger fails
```

## Steiger — the FSD linter

```bash
pnpm add -D steiger @feature-sliced/steiger-plugin
npx steiger ./src
```

Add a `steiger.config.ts` at repo root:

```ts
import { defineConfig } from "steiger";
import fsd from "@feature-sliced/steiger-plugin";

export default defineConfig([
  ...fsd.configs.recommended,
  { files: ["src/shared/**"], rules: { "fsd/public-api": "off" } },
]);
```

Wire it into CI alongside ESLint. Steiger checks: layer order, import direction, public API, segment whitelist, slice naming. ESLint won't catch any of this.

## Project skeleton

```
src/
├── app/
│   ├── providers/        # QueryClientProvider, ThemeProvider, ErrorBoundary
│   ├── router/           # route tree
│   ├── styles/           # global.css, tokens
│   └── index.tsx         # ReactDOM.createRoot
├── pages/
│   ├── report-detail/    # one route → one slice
│   └── report-list/
├── widgets/
│   ├── report-header/
│   └── sidebar-nav/
├── features/
│   ├── export-report-pdf/
│   ├── filter-reports/
│   └── toggle-favorite/
├── entities/
│   ├── report/           # Report type, useReport(id), ReportCard, ReportStatusBadge
│   └── user/
└── shared/
    ├── api/              # axios instance, MSW handlers (see Skill(frontend-msw))
    ├── ui/               # design-system primitives (Button, Input)
    ├── lib/              # date, money, formatters
    └── config/           # env, feature flags
```

## When FSD pays off

| Pays off                                                        | Doesn't                                        |
| --------------------------------------------------------------- | ---------------------------------------------- |
| 10+ devs, multiple teams touching shared code                   | Solo dev, weekend project                      |
| Long-lived codebase (2+ years)                                  | Throwaway prototype                            |
| Clear business domains (reports, inspections, users)            | Single-purpose tool — landing page, calculator |
| Domain language already exists (PO writes "the report feature") | Domain is one noun — "the editor"              |
| Onboarding pain is real — newcomers must locate code fast       | Codebase fits in one head                      |

**Smell test:** if you can't name three entities and three features for your app, FSD is overkill. Use a flat `src/components` + `src/pages` and re-evaluate at 50 components.

## Migration from `components/pages/utils`

1. **Inventory first.** Grep for top-level imports — what calls what. Steiger over the existing tree shows current violations to expect.
2. **Carve `shared/` first.** Move pure utilities, design-system primitives, axios setup. No business knowledge yet.
3. **Extract `entities/`.** For each domain noun (Report, User, Inspection): move its type, hooks, base UI (`ReportCard`, `ReportStatusBadge`), and api file.
4. **Pull `features/` out of `pages/`.** Each user action (`export-report-pdf`, `filter-reports`) becomes a slice. Move handlers + UI together.
5. **`widgets/` for composed blocks** used by 2+ pages.
6. **`pages/` becomes thin** — composition only, no business logic.
7. **Turn Steiger on per layer**, not all at once. Recommended order: shared → entities → features → widgets → pages.

Expect 2–4 weeks for a mid-size app. Doing it incrementally with a layer-at-a-time enable in CI is the only sane path.

## Anti-patterns

- **Sibling-feature imports.** `features/a/` importing from `features/b/`. If two features need the same logic, lift the shared piece to `entities/` or `shared/`.
- **Business logic in `widgets/`.** Widgets compose features and entities; they don't make API calls or own domain rules.
- **Business logic in `shared/`.** `shared/` knows nothing about "reports" or "inspections" — only generic primitives.
- **Reaching into segments.** `import X from '@/features/foo/model/X'` bypasses the public API. Steiger fails.
- **`utils/` or `helpers/` segment.** Not in the segment whitelist. Use `lib/`.
- **One mega-slice.** `features/reports/` containing every report-related action. Split per user action: `export-report-pdf`, `share-report-link`, `archive-report`.
- **Page logic in `app/`.** `app/` is providers + routing only. No business code.
- **Mixed naming.** `features/exportReportPdf/` (camelCase). Slices are kebab-case in 2.1+ — Steiger fails.

## Red flags

| Thought                                                  | Reality                                                                                                   |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| "I'll just import from this sibling feature, it's quick" | That import is the start of a coupling cycle. Lift it.                                                    |
| "I'll put the API client in `entities/`"                 | The axios instance is generic — `shared/api/`. Entity hooks (`useReport`) live in `entities/report/api/`. |
| "Every component is its own slice"                       | Then you have 200 slices and FSD is noise. Slice = user-meaningful action or domain noun.                 |
| "Steiger is too strict, let's disable it"                | Then you're using folder names, not FSD. Either keep the linter on or drop the methodology.               |
| "FSD will make us faster"                                | It makes a large team's code findable. It does nothing for a small team and adds ceremony. Be honest.     |

## Hand-off

For routing inside `pages/`: `Skill(frontend-react-router)`. For data-fetching hooks inside `entities/`: `Skill(frontend-tanstack-query)`. For mocking the `shared/api/` layer in tests: `Skill(frontend-msw)`. For React composition rules that FSD assumes: `Skill(react)`. For Tailwind tokens inside `shared/ui/`: `Skill(frontend-tailwind)`.
