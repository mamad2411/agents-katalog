<!-- GSD:project-start source:PROJECT.md -->
## Project

**freerecipe.club**

A community-driven recipe website that's the antithesis of ad-bloated recipe sites. No accounts, no tracking, no dark patterns — just recipes. Contributors submit via GitHub PRs or issues, recipes get community annotations (inline substitutions and tips), and a full cooking mode guides you step by step. Themed packs transform the site's look alongside curated recipe collections. Open source, built transparently in a public repo. The October 2026 community effort is an independent Spooky Season recipe-pack drive, not a Hacktoberfest PR/reward program.

**Core Value:** Someone finds a recipe and actually cooks from it.

### Constraints

- **Framework**: Remix component + fetch-router packages; static output from `scripts/build-static.ts`
- **Hosting**: GitHub Pages (custom domain) is the planned free static host
- **Privacy**: Zero tracking, zero cookies beyond technical necessity, no third-party scripts
- **Data**: Recipes stored as flat files in the repo — no database
- **Accessibility**: Must work on phones in a kitchen (wet hands, small screen, distractions)
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages & Runtime
| Language | Version | Usage |
|----------|---------|-------|
| TypeScript | ^5.7.0 | Primary language — controllers, data layer, scripts |
| YAML | — | Recipe and pack data format |
## Framework
| Framework | Version | Role |
|-----------|---------|------|
| Remix packages | `@remix-run/*` | Fetch router, static middleware, component JSX and SSR |
| Tailwind CSS | v4 (CSS-first) | Utility-first styling via `@tailwindcss/cli` |
## Dependencies
### Production
| Package | Version | Purpose |
|---------|---------|---------|
| `@remix-run/fetch-router` | ^0.18.0 | Minimal, composable router for the web Fetch API |
| `@remix-run/node-fetch-server` | ^0.13.0 | Node.js server using the web fetch API |
| `@remix-run/static-middleware` | ^0.4.5 | Middleware for serving static files |
| `@remix-run/component` | ^0.6.0 | UI components / JSX runtime |
| `yaml` | ^2.7.0 | YAML parser for recipe/pack files |
| `zod` | ^3.24.0 | Schema validation for recipe and pack data |
### Dev-only
| Package | Version | Purpose |
|---------|---------|---------|
| `@tailwindcss/cli` | ^4.2.0 | Tailwind v4 CLI for CSS builds |
| `tailwindcss` | ^4.2.0 | Tailwind CSS engine |
| `@types/node` | ^22.0.0 | Node.js type definitions |
| `esbuild` | ^0.25.0 | Bundles client-side TypeScript scripts |
| `tsx` | ^4.19.0 | TypeScript execution for dev server and scripts |
| `typescript` | ^5.7.0 | Type checking |
## Build & Scripts
| Script | Command | Purpose |
|--------|---------|---------|
| `dev` | `dev:server & dev:css & dev:js` | Parallel dev server, CSS watch, JS watch |
| `dev:server` | `tsx watch server.ts` | Development server with hot reload |
| `dev:css` | `@tailwindcss/cli ... --watch` | Tailwind CSS watch mode |
| `dev:js` | `tsx scripts/build-scripts.ts --watch` | Client script rebuild on change |
| `start` | `tsx server.ts` | Production server |
| `build` | `build:css && build:js && build:static` | Full static site build |
| `build:static` | `tsx scripts/build-static.ts` | Static site generation → `dist/` |
| `validate` | `tsx scripts/validate-recipes.ts` | Recipe YAML validation |
## Configuration
- **TypeScript:** `tsconfig.json` — JSX via `@remix-run/component` (`jsxImportSource`)
- **Tailwind:** CSS-first config in `app/styles/input.css` (no JS config file)
- **No bundler:** No Vite/Webpack — Tailwind CLI + esbuild for client scripts
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Code Style
- **TypeScript** used throughout with strict config
- **JSX** via `@remix-run/component` (Preact-based, NOT React)
- **Single quotes** in TypeScript
- **No linter/formatter configured** (no ESLint, Prettier)
## Component Patterns
- **TSX server rendering:** Controllers return `new Response(html)` with TSX templates
- **No client-side framework:** Server-rendered HTML + vanilla TypeScript for interactivity
- **Controller pattern:** Route handlers in `app/controllers/` return Response objects
## Data Handling
- **File-based data:** Recipes/packs stored as YAML files in `data/`
- **Zod validation:** Schemas in `app/data/recipe-schema.ts` and `pack-schema.ts`
- **Loaders:** `app/data/recipes.ts` and `packs.ts` parse + validate at load time
## Styling
- **Tailwind v4 CSS-first:** Config via `@theme` in `app/styles/input.css`
- **CSS custom properties:** Pack themes use CSS variables for theming
- **Print stylesheet:** Strips chrome, shows link URLs
## Client Scripts
- **TypeScript source:** `app/assets/` compiled via esbuild to `public/`
- **Progressive enhancement:** JS enhances but is never required to read recipes
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern
Server-rendered TSX with Remix fetch-router. Controllers handle requests and return HTML Response objects; the same controllers are used by the local server and static builder.
## Data Flow
```
Request → @remix-run/fetch-router → controller → load data (YAML+Zod) → render TSX → Response
```
## Layers
| Layer | Technology | Files |
|-------|-----------|-------|
| Server | Node.js + `@remix-run/node-fetch-server` | `server.ts` |
| Router | `@remix-run/fetch-router` | `app/router.ts`, `app/routes.ts` |
| Controllers | TSX (@remix-run/component) | `app/controllers/` |
| Data | YAML + Zod schemas | `data/`, `app/data/` |
| Client scripts | TypeScript → esbuild | `app/assets/` → `public/` |
| Static Assets | CSS, images, JS | `public/` |
## Entry Points
- `server.ts` — HTTP server via `createRequestListener`
- `app/router.ts` — Route matching with static file middleware
- `app/routes.ts` — Explicit route definitions
## Key Abstractions
- **Recipe schema** (`app/data/recipe-schema.ts`): Zod schema with annotations, components, directions
- **Pack schema** (`app/data/pack-schema.ts`): Zod schema for themed recipe collections
- **Controller pattern**: Each route handler returns `new Response(renderToString(<Component />))`
- **Render helper** (`app/controllers/render.tsx`): Shared HTML shell for all pages
<!-- GSD:architecture-end -->

<!-- GSD:remix-skills-start -->
## Remix Agent Skills

This project includes Remix agent skills in `skills/`:

- `remix-project-layout` at `skills/remix-project-layout/SKILL.md`: Use when defining or scaffolding the on-disk layout and file conventions of a Remix app.
- `remix-ui` at `skills/remix-ui/SKILL.md`: Use when building pages, layouts, interactions, styling, navigation, and UI tests in a Remix app.
<!-- GSD:remix-skills-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
