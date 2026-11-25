---
name: engineer-discover
description: Scan the codebase and generate the technical-context briefing
---

# Discover

This skill analyzes the project automatically and generates a complete technical briefing in a modular format.

It is **optional** and can be run:
- Once, at the start of the project
- When ADRs change significantly
- When the codebase's architecture changes significantly — backend, frontend, or mobile

## Incremental behavior

This skill is **non-destructive**:
- If briefing files already exist: update them incrementally
- If they don't exist: create them from scratch
- Always preserve existing information

## Generated structure

```
docs/technical-context/
├── project-briefing.md              # Master index + summary
└── briefing/
    ├── critical-rules.md            # Non-negotiable rules
    ├── adrs-summary.md              # Consolidated ADRs (always created, even if empty)
    ├── backend-conventions.md       # Code conventions — only if a backend was detected
    ├── frontend-conventions.md      # Code conventions — only if a frontend was detected
    ├── mobile-conventions.md        # Code conventions — only if a mobile codebase was detected
    └── tech-stack.md                # Tech stack — one subsection per domain/service actually found
```

`backend-conventions.md`, `frontend-conventions.md`, and `mobile-conventions.md` are each
generated **only if that domain was actually detected** in this project — an empty
"no frontend found" file would be pure noise with no future value, unlike `adrs-summary.md` (which
documents "no ADRs yet" as a real, useful fact even when empty).

This conditional-generation rule applies only to *creating a new file this run*. If a prior run
already wrote one of these files and this run no longer detects that domain (e.g. a frontend was
removed from the project), leave the existing file alone per the non-destructive guarantee (Golden
Rule 2) — don't delete it automatically.

---

## Phase 1: ADR analysis (conditional)

### 1.1 Detect ADRs

```bash
paths_to_check = [
  "docs/technical-context/adr/",
  "docs/adr/",
  "adr/"
]
```

- If **none** of these paths exist: skip this phase entirely.
- If one exists: proceed with the analysis.

### 1.2 Process ADRs

For each `.md` file found in the ADR folder:

1. **Read the full file.**
2. **Extract:**
   - ADR number (e.g. ADR-001, ADR-015)
   - Title
   - Status (Accepted, Proposed, Rejected, Superseded)
   - Context/background
   - Core decision
   - Mandatory conventions (if any)
   - Consequences
   - Category (infer: database, API, code organization, security, etc.)
   - Impact (high/medium/low — infer from criticality)
3. **Identify critical rules**: look for keywords like "mandatory", "always", "never", "forbidden". Flag high-impact ADRs.

### 1.3 Consolidate ADRs

- Group by category (database, API, code organization, testing, security, etc.)
- Order by impact (high → medium → low)
- Build an index with links

### 1.4 Check existing code against the consolidated ADRs

Run the ADR Compliance Check (below) against the current codebase, now that the ADRs are consolidated. This matters most when onboarding an existing project — ADRs are often written after the fact, once a convention has already drifted, so this is the first chance to see where the code and the documented decisions disagree.

If Phase 2.0 below determines this is a monorepo, don't run this as a single generic pass — run the check once per workspace found in 2.0, the same way Phase 2's domain-specific analysis does, since a convention violation in `apps/api/` may not apply to `apps/web/` or `apps/mobile/` at all.

Advisory only: collect the findings for the Phase 4.2 report; don't block Phase 2-4 on them, and don't fix anything automatically.

#### ADR Compliance Check

You are validating code against the project's Architecture Decision Records (ADRs) — the documented, mandatory architectural rules and conventions the project has committed to.

**When this applies:**
- During `engineer-discover` (this skill) — check the existing codebase against the ADRs just cataloged, once per workspace in monorepo mode (backend, frontend, and mobile scopes alike, not just backend services). This is what surfaces drift when onboarding an existing project.
- During `engineer-work` — check newly created or modified files against relevant ADRs as they're written.
- On demand, for a compliance audit of a specific feature.

If the project has no ADRs (no `docs/technical-context/adr/` directory, no `docs/technical-context/briefing/adrs-summary.md`), say so and stop — there is nothing to validate.

**Mode**: Advisory by default — report possible violations and suggest fixes, but never block work — the engineer decides, since valid exceptions exist. Only switch to **strict mode** (block until fixed) if the project explicitly configures it, e.g. in a dedicated section of the project's `AGENTS.md` — Codex has no directory-of-files auto-load pattern the way Claude Code's `.claude/rules/` does, so there's no equivalent per-topic file to point to here.

**Process:**

1. **Load ADRs**: read each ADR and extract its concrete, checkable rules (a location constraint, a required pattern, a forbidden dependency, a mandatory test, etc.).
2. **Match changed files to relevant ADRs**: use the file's path and content to determine which ADRs apply to it (e.g. a file under `/services/` is relevant to an ADR about a repository pattern; a file defining an enum is relevant to an ADR about shared-type location).
3. **Check for violations**: compare each relevant file against the rule it should follow.
4. **Report.**

**Output format** — for each violation found:

```
POSSIBLE ADR VIOLATION

File: <path>:<line>
ADR: <id> - <title>
Issue: <what's wrong>

Rule: "<the relevant ADR text>"

Suggested fix:
1. <step>
2. <step>

Ignore this if there's a valid, documented reason for the exception.
```

At the end of an `engineer-discover` or `engineer-work` run, summarize:

```
## ADR Compliance Report

Files checked: N
Violations found: N (N auto-fixable, N need discussion)
Warnings: N

- ADR-<id>: <title> — <status>
...

Compliance score: NN%
```

**What you can't detect:**
- Business-logic correctness (you check structure and convention, not whether the logic is right).
- Architectural decisions that were made but never written down as an ADR.

Say so explicitly rather than guessing.

---

## Phase 2: Codebase Domain Analysis (detection-gated)

Unlike ADR analysis (Phase 1, conditional on ADRs existing at all), this phase always runs its
detection step — but which domain-specific subsections actually execute depends entirely on what's
found. A project can be backend-only, frontend-only, mobile-only, or any combination — a Next.js
app, for instance, is legitimately both frontend and backend/API in the same codebase. Domains
aren't mutually exclusive; don't force a single classification.

### 2.0 Detect single-project vs. monorepo

Check for monorepo signals at the root: a `package.json` with a `workspaces` field, `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`, a `settings.gradle`/`settings.gradle.kts` with multiple `include(...)` modules, or multiple independent manifest files under `apps/*/` or `packages/*/` — "manifest" here means any of `package.json`, `pyproject.toml`, `pubspec.yaml`, `build.gradle`(.kts), `Package.swift`, `go.mod`, not just the JS-ecosystem ones.

- **If none of these exist**: single project. The "scope" for 2.0b below is the repo root.
- **If they do**: this is a monorepo. List every workspace/app/package that has its own manifest file (any of the types above) — don't just take the first match and stop. Each workspace becomes its own "scope" for 2.0b below. Keep each workspace's findings separate; don't merge them into one generic answer. A monorepo with `apps/api/`, `apps/web/`, `apps/mobile/`, and `packages/shared/` has four scopes; three of them (`apps/api/`, `apps/web/`, `apps/mobile/`) match a domain in 2.0b and get analyzed, the fourth matches none and is skipped — not one merged answer.

### 2.0b Detect which domain(s) each scope has

For each scope (the repo root in single-project mode, or each workspace in monorepo mode), check independently — a scope can match more than one domain, or none:

**Backend signals**: paths matching `apps/backend/`, `backend/`, `server/`, `api/`, `packages/backend/`, `src/backend/`, `src/` (with a server-side framework in the manifest — see 2.4), or the scope root itself when its manifest lists a server-side framework and no other backend path applies — same root-manifest fallback the frontend rule uses, for a Django/FastAPI/Rails-style repo with no dedicated backend subfolder.

**Frontend signals**: paths matching `apps/web/`, `frontend/`, `client/`, `web/`, `packages/frontend/`, or the scope root itself when its manifest lists a frontend framework (React, Vue, Svelte, Angular, Next.js, Nuxt, SvelteKit). Checked independently of the backend signal above, not exclusively — a scope root with `api/`-style routes *and* a frontend framework in its manifest (a typical Next.js app) correctly matches both, which is exactly the non-exclusivity this phase is built around.

**Mobile signals** (check all four, but native iOS/Android are subordinate to React Native/Flutter — see the precedence note below):
- **React Native**: manifest has a `react-native` dependency (with or without `ios/`/`android/` host-project folders — Expo-managed projects have neither).
- **Flutter**: `pubspec.yaml` is present, listing `flutter` as a dependency or under `sdk:` — not just any Dart package.
- **Native iOS**: a `.xcodeproj` or `.xcworkspace` is present, with Swift/Objective-C source, **and it isn't the `ios/` host project of a scope already matched as React Native or Flutter above** — that folder is a build target of the cross-platform app, not a separate native codebase.
- **Native Android**: a `build.gradle`/`build.gradle.kts` is present, with the standard Android project structure and Kotlin/Java source, **and it isn't the `android/` host project of a scope already matched as React Native or Flutter above** — same reasoning.

A scope can still match more than one *real* combination (e.g. a standalone native Android library sitting alongside an unrelated Flutter app in a monorepo, in different scopes) — the precedence rule above only suppresses the false positive where React Native/Flutter's own host folders get double-counted as separate platforms in the *same* scope.

If a scope matches **zero** domains (e.g. a shared types/config-only package in a monorepo), skip it silently — that's expected, not an error.

If **every** scope across the whole project matches zero domains (nothing recognizable anywhere), don't silently produce empty briefings — **ask the human** where the code actually lives, per Golden Rule 1, then resume 2.0b treating whatever they point to as an additional scope before continuing to Phase 3. If only *some* scopes match nothing while at least one matches a domain, don't ask — that's the normal shared/config-only-package case — but note the count in the Phase 4.2 report (e.g. "2 of 5 scopes matched no domain") so a genuinely missed app doesn't disappear silently.

Run the domain-specific subsections below (2.1-2.4, 2.5-2.8, 2.9-2.12) only for the domains actually detected, scoped to the specific scope(s) where each was found.

### 2.1 Map the backend (for each scope where backend was detected)

Scan for:
- Controllers/routes → HTTP handlers
- Services → business logic
- Repositories/DAL → data access
- Models/entities → domain models
- Shared code (enums, types, validation schemas, utilities)
- Tests

### 2.2 Identify backend conventions

**Shared type/enum location**: find where the majority of enum/type definitions live; treat it as a convention if >80% share the same location. In monorepo mode, also check whether a `packages/shared/`-style package is where cross-service types actually live — that's itself a convention worth recording.

**Architectural patterns**: repository pattern? Service layer? MVC? — infer from which folders coexist.

**Naming**: sample 5-10 files to identify the dominant convention (kebab-case vs. camelCase vs. PascalCase, suffix conventions like `.controller.ts`/`.service.ts` or `_service.py`).

### 2.3 Detect the backend tech stack

Read the manifest file (`package.json`, `pyproject.toml`, etc.) — per scope, in monorepo mode, since different services in the same monorepo commonly run different stacks:
- Web framework (Express, Fastify, NestJS, Django, FastAPI, Flask, ...)
- Database/ORM (Prisma, TypeORM, Drizzle, SQLAlchemy, Mongoose, ...)
- Validation library (Zod, Joi, Pydantic, class-validator, ...)
- Test framework (Jest, Vitest, pytest, ...)
- Runtime/language version

### 2.4 (reference) Backend frameworks that confirm a backend signal

Used by 2.0b both to confirm a backend match when the path alone is ambiguous (e.g. a bare `src/`)
and to originate a root-scope match on its own: Express, Fastify, NestJS, Django, FastAPI, Flask,
Spring, Rails, Laravel, or an ORM/DB client. Checked independently of the frontend signal, not
exclusively — same non-exclusivity principle as 2.0b's frontend rule.

---

### 2.5 Map the frontend (for each scope where frontend was detected)

Scan for:
- Component structure/organization (feature-folder, atomic design, flat, etc.)
- Hooks/composables
- State management (Redux, Zustand, Pinia, Vuex, Context API, Signals, ...)
- Routing
- Styling approach (CSS modules, Tailwind, styled-components, vanilla CSS, ...)
- API-client layer — how the frontend talks to a backend, if any (fetch wrapper, generated client, GraphQL client, ...)
- Tests

### 2.6 Identify frontend conventions

**Naming**: sample 5-10 files to identify the dominant convention (kebab-case vs. camelCase vs. PascalCase, suffix conventions like `.component.tsx`, `.hook.ts`).

**Architectural patterns**: feature-folder vs. type-folder organization, atomic design, container/presentational split — infer from which folders coexist, same technique as 2.2.

### 2.7 Detect the frontend tech stack

Read the manifest file, per scope in monorepo mode:
- Framework (React, Vue, Svelte, Angular, Next.js, Nuxt, SvelteKit, ...)
- State management library
- Styling approach/library
- Build tool (Vite, Webpack, Turbopack, ...)
- Test framework (Vitest, Jest, Testing Library, Playwright/Cypress for e2e, ...)
- Runtime/language version

### 2.8 (reference) Frontend frameworks that confirm a frontend signal

Used by 2.0b: React, Vue, Svelte, Angular, Next.js, Nuxt, SvelteKit. Checked independently of
the backend signal, not exclusively — same non-exclusivity principle as
2.0b's frontend rule.

---

### 2.9 Map each detected mobile platform (React Native, Flutter, native iOS, native Android)

For each platform actually detected in 2.0b, scan for:
- Screens/views organization
- Navigation pattern (stack/tab/drawer — whichever navigation library or native pattern is in use)
- State management
- Native module / platform-channel usage (React Native and Flutter only — where platform-specific code is bridged)
- Architectural pattern (MVVM, MVC, MVI — infer from which folders/files coexist, same technique as 2.2)

If a scope matches more than one mobile platform (e.g. a native Android library alongside a
Flutter app in the same monorepo), map each platform separately — don't merge them.

### 2.10 Identify mobile conventions (per platform)

**Naming**: sample 5-10 files per platform to identify the dominant convention.

**Screen/navigation organization**: how screens are grouped (by feature, by flow, flat) and how navigation is wired (declarative route table, programmatic, native storyboard/nav-graph).

### 2.11 Detect the mobile tech stack (per platform)

- React Native / Flutter version, or native SDK/minimum-OS-version target
- Key libraries (navigation library, state management library, native-module bridges)
- Test framework (if any)

### 2.12 (reference) Mobile detection signals

Used by 2.0b — repeated here for completeness, including the precedence rule (native iOS/Android
don't separately match inside a scope already identified as React Native or Flutter):
- React Native: `react-native` in the manifest (host `ios/`/`android/` folders optional — Expo-managed projects have neither).
- Flutter: `pubspec.yaml` listing `flutter` as a dependency or under `sdk:`.
- Native iOS: `.xcodeproj`/`.xcworkspace` present, Swift/Objective-C source, not a React Native/Flutter host project.
- Native Android: `build.gradle`(.kts) present with standard Android structure, Kotlin/Java source, not a React Native/Flutter host project.

---

## Phase 3: Generate the briefing files

### 3.1 Create the folder if it doesn't exist

```bash
mkdir -p docs/technical-context/briefing/
```

### 3.2 `project-briefing.md` (master index)

Include: an executive-summary project status, an index of the briefing files **actually generated
this run** (not a fixed list — see 3.5-3.8 below), a usage guide by feature type, and maintenance
instructions. Target size: ~150 lines.

### 3.3 `briefing/critical-rules.md`

The 3-5 most critical rules from the ADRs, mandatory conventions, and a compliance checklist. **This file gets copied in full into every `context.md`.** Target size: ~80 lines.

### 3.4 `briefing/adrs-summary.md`

If ADRs exist: an index by category, each ADR summarized with title, status, impact, decision, mandatory conventions, and a link to the full ADR. If no ADRs exist: create the file anyway with a note that none are defined yet. Target size: scales with ADR count.

### 3.5 `briefing/backend-conventions.md` (only if backend was detected — see 2.0b)

Folder structure (ASCII tree), file/class/method naming, code patterns (controller/service/repository or equivalent), and a couple of representative code examples. In monorepo mode, use one subsection per service instead of collapsing them into a single generic answer — a convention that holds in `apps/api/` may not hold elsewhere. Target size: ~150 lines (scales with the number of services). Skip this file entirely if no backend was detected anywhere in the project.

### 3.6 `briefing/frontend-conventions.md` (only if frontend was detected — see 2.0b)

Folder/component structure (ASCII tree), naming, state management approach, styling approach, and a couple of representative code examples. In monorepo mode, one subsection per frontend workspace. Target size: ~150 lines. Skip this file entirely if no frontend was detected anywhere in the project.

### 3.7 `briefing/mobile-conventions.md` (only if any mobile platform was detected — see 2.0b)

One subsection per platform detected (React Native, Flutter, native iOS, native Android), and — same as 3.5/3.6 — one subsection per scope within a platform if more than one scope matches it (e.g. two separate Flutter apps in a monorepo don't collapse into one subsection): screen/navigation organization, naming, architectural pattern, and a couple of representative code examples per platform/scope. Target size: ~150 lines (scales with the number of platforms and scopes). Skip this file entirely if no mobile codebase was detected anywhere in the project.

### 3.8 `briefing/tech-stack.md`

One subsection per domain actually found (backend/frontend/mobile), and within a domain, one subsection per service/workspace/platform if more than one was found for that domain (same pattern already used for monorepo backend services, extended to also mean "per domain"). Include a line noting which package manager/workspace tool ties a monorepo together (pnpm workspaces, Nx, Turborepo, Lerna), if applicable. Target size: ~100-150 lines (scales with the number of domains/services/platforms).

---

## Phase 4: Validation and wrap-up

### 4.1 Sanity check

- All files created successfully?
- Do cross-links between files resolve?
- No unexpectedly empty file?
- No domain-conventions file newly created for a domain that wasn't actually detected this run (3.5-3.7 are conditional — double-check none were created "just in case"; this doesn't apply to a file that already existed from a prior run, which is left untouched per the non-destructive guarantee)?

### 4.2 Report to the human

Build this report dynamically — the file list and the summary lines each reflect only what was
actually found and generated this run. Example shape (a real report omits any line for a domain
that wasn't detected):

```
✅ Project Discovery complete.

📁 Files generated:
- docs/technical-context/project-briefing.md (master index)
- docs/technical-context/briefing/critical-rules.md
- docs/technical-context/briefing/adrs-summary.md
- docs/technical-context/briefing/backend-conventions.md   [only if backend was detected]
- docs/technical-context/briefing/frontend-conventions.md  [only if frontend was detected]
- docs/technical-context/briefing/mobile-conventions.md    [only if mobile was detected]
- docs/technical-context/briefing/tech-stack.md

📊 Summary:
- ADRs analyzed: X
- Critical rules: X
- Backend framework(s): [name, or one per service — omit this line if no backend was found]
- Frontend framework(s): [name, or one per workspace — omit this line if no frontend was found]
- Mobile platform(s): [e.g. "React Native", "Flutter + native Android" — omit this line if no mobile codebase was found]
- Database/ORM: [name, if a backend was found]
- ADR compliance: [no ADRs to check / N violations found, listed below / clean — one line per scope in monorepo mode]
- Scopes with no domain match: [N of M — omit this line if 0, expected for shared/config-only packages]

[If violations were found, list each: which ADR, where in the code, and the suggested fix.]

💡 Next steps:
1. Review project-briefing.md for accuracy.
2. Review critical-rules.md (it gets copied into every context.md).
3. Run `engineer-context` when ready to start a feature.

ℹ️  This briefing is loaded automatically by `engineer-context` to enrich context.
🔄 To update it, re-run this skill (incremental, non-destructive).
```

⛔ **After reporting to the human, STOP. Don't automatically proceed to `engineer-context` or any other skill. Wait for feedback.**

---

## Tools used

- **Glob**: to find files (ADRs, manifest files, source files).
- **Read**: to read file contents.
- **Write**: to create/update the briefing files.

---

## Error handling

- **Malformed ADR**: warn the human ("ADR X is malformed, skipping"), continue with the others, and list what was skipped at the end.
- **Unrecognized structure for a detected domain**: if a scope clearly matches a domain (backend/frontend/mobile) but its internal structure can't be mapped confidently (2.1/2.5/2.9), ask the human where the relevant folders/files live instead of guessing — same treatment for all three domains, not backend-only.
- **No manifest file found**: warn that analysis will be limited and document what could be inferred from the folder structure alone.

---

## Detailed vs. summarized progress

If the user asks for a detailed or verbose run, show detailed progress (each ADR processed, each scope's domain detection, each file scanned, each generated file). The default is a summarized progress report with only warnings/errors shown.

---

## Golden rules

1. **Never assume** — if something can't be found, ask the human. If every scope in the project matches zero domains (2.0b), don't silently generate empty briefings — ask where the code lives.
2. **Be incremental** — don't overwrite existing information without reason.
3. **Be explicit** — cross-links between files must resolve.
4. **Be resilient** — an error in one phase shouldn't stop the whole process.
