---
name: react-app-scaffolder
audience: team
description: >
  Scaffolds a production-ready React + TypeScript application skeleton with Vite, a router,
  strict TypeScript, Vitest + React Testing Library, ESLint (hooks + jsx-a11y), Prettier,
  environment handling, an error boundary, and a feature-folder layout. React analog of an
  app/project scaffolder. Use when starting a new React app, bootstrapping a Vite + React +
  TypeScript project, setting up the testing/lint toolchain, or establishing the base folder
  structure and app shell.
---

# React App Scaffolder

> "Make the right thing the easy thing. A project's defaults become its culture."
> -- Adapted from engineering practice

> "Strict from day one is cheaper than strict retrofitted."
> -- Adapted from TypeScript adoption experience

## Core Philosophy

The first commit sets the project's defaults, and defaults are sticky: a project that starts without
`strict` TypeScript, without a test runner, or without lint rarely gains them later without pain. This
skill stands up the skeleton with the non-negotiables already on — strict types, Vitest, ESLint with the
hooks and a11y plugins, a router, an error boundary, and a feature-folder layout — so the first real
feature drops into a structured, tested, type-safe project.

Vite is the default bundler (fast, modern, ESM-native). Create React App is deprecated and is never the
target for a new project — if an existing CRA app is in play, route to `react-modernization-analyzer`.

> **Grounding note:** the KB has no React corpus. Use `collection="javascript"` for TS/tooling and cite
> **react.dev** / Vite + Vitest docs as the authority. Never invent a `react` collection.

**Non-Negotiable Constraints:**
1. **Vite + TypeScript `strict` + React Compiler** — `strict: true` in `tsconfig` from the first commit, and React Compiler wired (stable since 1.0, Oct 2025; by 2026 the default assumption for a new project, not an opt-in experiment)
2. **Test runner wired** — Vitest + React Testing Library with a `test` script and a passing smoke test
3. **Lint + format wired** — ESLint (react-hooks + jsx-a11y) and Prettier with scripts
4. **Router from the start** — a router with a typed route table and a not-found route
5. **Error boundary at the shell** — a top-level error boundary so one throw does not blank the app
6. **Env via Vite convention** — only `VITE_*` exposed to the client; secrets stay server-side

**What this skill is NOT:**
- It is NOT a feature generator — use `react-feature-slice` / `react-component-scaffolder` for that
- It is NOT a deployment/CI guide — it covers the application skeleton; CI is a follow-up
- It is NOT a styling-framework decision — leave styling choice to the team

The 10 domain principles, knowledge-base lookups, discipline rules, the anti-pattern catalog, and
error-recovery procedures live in `references/conventions.md`.

## Workflow

### Phase 1: DETECT

```bash
node -v && npm -v
ls package.json 2>/dev/null && echo "existing project — confirm before overwriting"
# If a Create React App project exists, STOP and route to react-modernization-analyzer.
grep -l "react-scripts" package.json 2>/dev/null && echo "CRA detected → modernization, not fresh scaffold"
```

If `package.json` already exists, do not clobber it — scaffold missing pieces only, and confirm first.

### Phase 2: CREATE

```bash
npm create vite@latest <app-name> -- --template react-ts
cd <app-name>
npm install
npm install -D vitest @testing-library/react @testing-library/user-event jsdom \
  eslint-plugin-react-hooks eslint-plugin-jsx-a11y prettier babel-plugin-react-compiler
npm install react-router-dom
```

### Phase 3: CONFIGURE

Apply the structure and config. See `references/project-structure.md` for full file contents.

```
src/
  app/
    App.tsx            # shell: providers + router + error boundary
    routes.tsx         # typed route table (home, layout, 404)
    ErrorBoundary.tsx  # top-level error boundary
  features/            # feature slices land here (react-feature-slice)
  shared/              # cross-cutting UI + utilities (http client, etc.)
  test/setup.ts        # RTL + jest-dom setup
  main.tsx             # createRoot
  vite-env.d.ts        # typed VITE_* env
eslint.config.js
vitest.config.ts
.env.example
.prettierrc
tsconfig.json          # strict
```

See `references/toolchain-config.md` for `tsconfig`, `eslint.config.js` (incl. compiler lint rules),
`vite.config.ts` (React Compiler babel plugin), `vitest.config.ts`, and scripts.

### Phase 4: VERIFY

```bash
npm run typecheck      # tsc --noEmit, strict
npm run lint           # eslint clean
npm run test           # smoke test green
npm run build          # production build succeeds
npm run dev            # dev server boots
```

## State Block

```xml
<react-app-scaffold-state>
  phase: DETECT | CREATE | CONFIGURE | VERIFY | COMPLETE
  app_name: [name]
  existing_project: true | false
  cra_detected: true | false
  strict_ts: true | false
  router_configured: true | false
  test_harness_configured: true | false
  lint_configured: true | false
  error_boundary_added: true | false
  compiler_enabled: true | false
  last_action: [description]
  next_action: [description]
</react-app-scaffold-state>
```

## Output Template

Emit the scaffold checklist (Toolchain · App Shell · Scripts · Verification) as the progress report.
Full markdown checklist: `references/conventions.md` → "Scaffold Checklist (Output Template)".

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `react-feature-slice` | The first thing to use after the skeleton — adds feature slices into `src/features/`. |
| `react-component-scaffolder` | Generates individual components/routes within the scaffolded app. |
| `react-modernization-analyzer` | For an existing CRA / legacy app, assess and plan the move to this Vite skeleton instead of scaffolding fresh. |
| `react-security-review` | Run once features land to verify CSP, env exposure, and dependency posture. |
| `tdd-loop` | Drive the first features test-first on top of the scaffolded Vitest harness. |
