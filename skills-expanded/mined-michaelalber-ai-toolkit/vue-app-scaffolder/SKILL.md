---
name: vue-app-scaffolder
audience: team
description: >
  Scaffolds a production-ready Vue 3 + TypeScript application skeleton with Vite, Vue Router,
  strict TypeScript, Vitest + Vue Testing Library, ESLint (vue + a11y plugins), Prettier,
  environment handling, app-level error handling, and a feature-folder layout. Vue analog of
  an app/project scaffolder. Use when starting a new Vue app, bootstrapping a Vite + Vue +
  TypeScript project, setting up the testing/lint toolchain, or establishing the base folder
  structure and app shell.
---

# Vue App Scaffolder

> "Make the right thing the easy thing. A project's defaults become its culture."
> -- Adapted from engineering practice

> "Strict from day one is cheaper than strict retrofitted."
> -- Adapted from TypeScript adoption experience

## Core Philosophy

The first commit sets the project's defaults, and defaults are sticky: a project that starts without
`strict` TypeScript, without a test runner, or without lint rarely gains them later without pain. This
skill stands up the skeleton with the non-negotiables already on — strict types, Vitest, ESLint with the
vue and a11y plugins, Vue Router, app-level error handling, and a feature-folder layout — so the first
real feature drops into a structured, tested, type-safe project.

Vite is the default bundler (fast, modern, ESM-native, the official Vue tooling recommendation). The
legacy Vue CLI is in maintenance mode and is never the target for a new project — if an existing Vue CLI
app is in play, route to `vue-modernization-analyzer`.

> **Grounding note:** the KB has a Vue 2/3 corpus under `collection="javascript"` (alongside TS/tooling).
> Cite **vuejs.org** / Vite + Vitest docs as the authority. Never invent a `vue` collection.

**Non-Negotiable Constraints:**
1. **Vite + TypeScript `strict`** — `strict: true` in `tsconfig` from the first commit
2. **Test runner wired** — Vitest + Vue Testing Library with a `test` script and a passing smoke test
3. **Lint + format wired** — ESLint (`eslint-plugin-vue` + `vuejs-accessibility`) and Prettier with scripts
4. **Router from the start** — Vue Router with a typed route table and a not-found route
5. **App-level error handling** — `app.config.errorHandler` so one throw does not blank the app
6. **Env via Vite convention** — only `VITE_*` exposed to the client; secrets stay server-side

**What this skill is NOT:**
- It is NOT a feature generator — use `vue-feature-slice` / `vue-component-scaffolder` for that
- It is NOT a deployment/CI guide — it covers the application skeleton; CI is a follow-up
- It is NOT a styling-framework decision — leave styling choice to the team

The 10 domain principles, knowledge-base lookups, discipline rules, the anti-pattern catalog, and
error-recovery procedures live in `references/conventions.md`.

## Workflow

### Phase 1: DETECT

```bash
node -v && npm -v
ls package.json 2>/dev/null && echo "existing project — confirm before overwriting"
# If a Vue CLI project exists, STOP and route to vue-modernization-analyzer.
grep -l "@vue/cli-service" package.json 2>/dev/null && echo "Vue CLI detected → modernization, not fresh scaffold"
```

If `package.json` already exists, do not clobber it — scaffold missing pieces only, and confirm first.

### Phase 2: CREATE

```bash
npm create vite@latest <app-name> -- --template vue-ts
cd <app-name>
npm install
npm install -D vitest @testing-library/vue @testing-library/user-event jsdom \
  eslint-plugin-vue eslint-plugin-vuejs-accessibility prettier
npm install vue-router@4
```

### Phase 3: CONFIGURE

Apply the structure and config. See `references/project-structure.md` for full file contents.

```
src/
  app/
    App.vue             # shell: router-view + error handling wiring
    routes.ts            # typed route table (home, layout, 404)
  features/              # feature slices land here (vue-feature-slice)
  shared/                # cross-cutting UI + utilities (http client, etc.)
  test/setup.ts          # RTL + jest-dom setup
  main.ts                # createApp + errorHandler
  vite-env.d.ts           # typed VITE_* env
eslint.config.js
vitest.config.ts
.env.example
.prettierrc
tsconfig.json            # strict
```

See `references/toolchain-config.md` for `tsconfig`, `eslint.config.js`, `vitest.config.ts`, and scripts.

### Phase 4: VERIFY

```bash
npm run typecheck      # vue-tsc --noEmit, strict
npm run lint           # eslint clean
npm run test           # smoke test green
npm run build          # production build succeeds
npm run dev            # dev server boots
```

## State Block

```xml
<vue-app-scaffold-state>
  phase: DETECT | CREATE | CONFIGURE | VERIFY | COMPLETE
  app_name: [name]
  existing_project: true | false
  vue_cli_detected: true | false
  strict_ts: true | false
  router_configured: true | false
  test_harness_configured: true | false
  lint_configured: true | false
  error_handler_added: true | false
  last_action: [description]
  next_action: [description]
</vue-app-scaffold-state>
```

## Output Template

Emit the scaffold checklist (Toolchain · App Shell · Scripts · Verification) as the progress report.
Full markdown checklist: `references/conventions.md` → "Scaffold Checklist (Output Template)".

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `vue-feature-slice` | The first thing to use after the skeleton — adds feature slices into `src/features/`. |
| `vue-component-scaffolder` | Generates individual components/routes within the scaffolded app. |
| `vue-modernization-analyzer` | For an existing Vue CLI / legacy app, assess and plan the move to this Vite skeleton instead of scaffolding fresh. |
| `vue-security-review` | Run once features land to verify CSP, env exposure, and dependency posture. |
| `tdd-loop` | Drive the first features test-first on top of the scaffolded Vitest harness. |
