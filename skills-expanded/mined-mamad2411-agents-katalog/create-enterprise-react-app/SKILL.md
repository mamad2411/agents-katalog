---
name: create-enterprise-react-app
description: "Scaffold and verify a production-ready enterprise React application shell. Use when creating a new React admin project, initializing a blank Vite workspace, or applying the React 19, Ant Design 6, React Router 7, TanStack Query, Zustand, Axios, Tailwind CSS 4, Storybook, Vitest, and Playwright architecture baseline."
---

# React企业级空白项目创建 / Enterprise React Blank Project Creator

## Overview

Create a new, blank enterprise React project with clear UI, routing, state,
request, security, testing, and build boundaries. Use the bundled deterministic
template for an empty destination; adapt the process instead of overwriting
files when the user asks to apply the baseline to an existing project.

## Typical Requests

- "Create a blank enterprise React admin project in this directory."
- "Initialize a Vite 8 + React 19 project using Ant Design and TanStack Query."
- "Use the enterprise React baseline for a new back-office application."

## Inputs And Outputs

Require a target directory. Accept an optional npm package name and display
title. Infer the package name from the target directory and the title from the
package name when they are omitted.

Deliver a runnable project containing:

- a responsive blank application shell and route-level lazy page;
- Ant Design theme tokens plus Tailwind layout utilities without Preflight;
- TanStack Query, Zustand, and a typed Axios boundary;
- Vitest, Storybook accessibility checks, and Playwright browser checks;
- strict TypeScript, ESLint flat config, Prettier, and production build scripts.

Treat successful dependency installation, typecheck, lint, tests, production
build, and a nonblank browser render as completion. Report any check that could
not run instead of claiming success.

## Workflow

1. Inspect the target directory, its nearest `package.json`, Node version, package
   manager configuration, and existing user changes. Require Node.js 20.19+ before
   installing the baseline; stop with the exact detected version when the runtime
   is older. Do not overwrite a nonempty directory.
2. Read [references/architecture.md](references/architecture.md) before changing
   dependency versions, project boundaries, security behavior, styling strategy,
   or quality gates.
3. For a new empty target, run the bundled `scripts/create_project.py` using its
   path inside this Skill package. Pass the target directory, plus `--name` or
   `--title` only when the user supplied them. Use `--dry-run` when destination
   safety is uncertain.
4. For an existing project, inspect its architecture first and apply only the
   requested compatible changes. Do not run the template script against it.
5. Enable Corepack when available, install with the generated project's pinned
   pnpm version, and preserve the generated lockfile. Dependency installation in
   the requested project is a normal implementation step; ask only when the user
   explicitly requested files without installation or installation would affect
   another project.
6. Run `pnpm typecheck`, `pnpm lint`, `pnpm test`, `pnpm build`, and
   `pnpm build-storybook`. Run `PW_PORT=<available-port> pnpm test:e2e` when a
   compatible Playwright browser is already installed. Installing a new browser
   binary requires explicit user approval.
7. Start the development server on an available port. Verify the desktop and a
   narrow mobile viewport, the sidebar toggle, semantic heading/navigation
   structure, visible keyboard focus, browser console, and nonblank rendering.
8. Report the project path, URL, commands run, real results, compatibility
   fallbacks, and remaining warnings. Do not commit, push, deploy, or publish
   without an explicit request.

## Decision Rules

- Keep TanStack Query as the owner of server state. Keep Zustand limited to
  navigation state, display preferences, and other client-only state.
- Keep Axios inside `src/services`; pages and presentational components must not
  import it directly.
- Prefer route-level lazy loading before `manualChunks`. Add ECharts, XLSX,
  drag-and-drop, editors, and similar large packages only when a feature needs
  them.
- Prefer `HttpOnly + Secure + SameSite` cookies. Do not persist access tokens in
  `localStorage`. Treat frontend permissions as visibility controls, never as the
  security boundary.
- Let Ant Design own complex interactive widgets. Use Tailwind for layout,
  spacing, and responsive utilities, and do not globally reset Ant Design
  controls.
- Keep the pinned compatible baseline unless the user asks for newer versions.
  When updating a major version, verify ecosystem peer compatibility and rerun
  every quality gate.

## Guardrails

- Refuse to scaffold over existing files. If the target is nonempty, stop and
  inspect whether the request is an integration task.
- Do not invent backend contracts, authentication endpoints, organization rules,
  tokens, private registries, or remote repository URLs.
- Do not initialize Git, commit, push, install global tools, install browser
  binaries, deploy, or publish unless the user explicitly authorizes that action.
- Do not hide build-size, peer-dependency, browser, or accessibility warnings.

## Validation

When changing this Skill itself, run:

```bash
python3 scripts/test_create_project.py
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

Also parse `agents/openai.yaml` as YAML and scan the package for absolute home
paths, secrets, TODO markers, and unused resource directories.
