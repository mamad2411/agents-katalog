---
name: project-context-review
description: Auto-scans a project codebase and generates structured context (tech stack, patterns, conventions, architecture) so the AI understands the project before writing code. Replaces manual CLAUDE.md files with detected facts. Supports lenses (code, design, testing, docs) for focused context.
when_to_use: Trigger when starting work on an unfamiliar codebase, onboarding to a new project, before a major implementation task, when asked to review or document project context, or when the existing CLAUDE.md is outdated or missing.
---

# Project Context Review

This skill scans a project and generates structured context the AI can use to write better code. It extracts FACTS — tech stack, file patterns, naming conventions, architecture decisions — not opinions.

## Why This Exists

AI writes better code when it knows:
- What framework and tools the project uses (so it doesn't introduce incompatible dependencies)
- How existing code is structured (so new code matches the patterns)
- What conventions are followed (so it doesn't mix styles)
- Where things live (so it puts new files in the right places)

This skill automates that discovery instead of relying on a hand-written CLAUDE.md.

## How It Works

**Scan → Detect → Structure → Output**

1. **Scan** — Read key project files (package manifests, configs, entry points, directory tree)
2. **Detect** — Identify tech stack, patterns, and conventions from what actually exists
3. **Structure** — Organize findings into a consistent format
4. **Output** — Produce a context block the AI (or developer) can reference

## Activation

When this skill triggers, perform a context scan of the current project. The depth depends on the lens:

- **Full scan** (default): All lenses, complete project context
- **Code lens**: Tech stack + architecture + patterns + conventions
- **Design lens**: UI framework + component patterns + styling approach + tokens
- **Testing lens**: Test framework + patterns + utilities + coverage approach
- **Docs lens**: Documentation structure + API docs + README patterns

Load the relevant lens from `lenses/` for detailed scanning instructions.

## Scan Process

### Step 1: Project Identity

Read these files (whichever exist):
- `package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml` / `requirements.txt` / `Gemfile` / `pom.xml` / `build.gradle`
- `README.md` (first 50 lines for project description)
- `.gitignore` (reveals tooling and generated artifacts)

Extract: project name, language, runtime, primary framework, key dependencies.

### Step 2: Architecture Shape

Run a directory listing (depth 2-3) and identify:
- **Entry points**: `src/index.*`, `src/main.*`, `app.*`, `server.*`, `cmd/`
- **Routing**: `routes/`, `pages/`, `app/` (Next.js/Remix), `src/routes/`
- **Module boundaries**: Feature folders, domain folders, barrel files
- **Generated/build output**: `dist/`, `build/`, `.next/`, `target/`
- **Config layer**: root-level dotfiles and config directories

Classify the architecture pattern:
- Monolith / Monorepo / Microservice
- MVC / Feature-based / Domain-driven / Flat
- Client-only / Server-only / Full-stack / Serverless

### Step 3: Convention Detection

Sample 3-5 source files from different directories. Look for:
- **Naming**: camelCase / snake_case / PascalCase / kebab-case for files, functions, variables, components
- **Exports**: default vs named, barrel files, re-exports
- **Imports**: absolute paths, aliases (`@/`), relative only
- **File organization**: one component per file, co-located tests, co-located styles
- **Error handling**: try/catch patterns, Result types, error boundaries, custom error classes
- **Comments**: JSDoc, inline, none, header blocks
- **Formatting**: tabs/spaces, semicolons, quote style (check config or sample files)

### Step 4: Tooling & Config

Check for (file existence = fact):
- **Linter**: `.eslintrc*`, `biome.json`, `.ruff.toml`, `golangci.yml`
- **Formatter**: `.prettierrc*`, `rustfmt.toml`, `.editorconfig`
- **Type checking**: `tsconfig.json`, `mypy.ini`, type annotations
- **Build**: `vite.config.*`, `webpack.config.*`, `next.config.*`, `turbo.json`, `Makefile`
- **CI/CD**: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- **Package manager**: `pnpm-lock.yaml` / `yarn.lock` / `package-lock.json` / `bun.lockb`
- **Containerization**: `Dockerfile`, `docker-compose.yml`
- **Environment**: `.env.example`, `.env.local` patterns

### Step 5: Key Patterns

Detect from actual code (not assumptions):
- **State management**: Redux, Zustand, Pinia, Context, signals, MobX
- **Data fetching**: REST client, GraphQL, tRPC, server actions, SWR/React Query
- **Authentication**: JWT, session, OAuth provider, middleware patterns
- **Database**: ORM (Prisma, Drizzle, SQLAlchemy, GORM), raw queries, migrations
- **API style**: REST routes, RPC handlers, GraphQL resolvers, WebSocket handlers
- **Styling**: CSS modules, Tailwind, styled-components, SCSS, vanilla CSS

## Output Format

Structure the output as a context block. Use this template:

```markdown
## Project Context: [name]

**Stack**: [language] + [framework] + [runtime]
**Architecture**: [pattern] ([monolith/monorepo/etc])
**Package Manager**: [name] | **Build**: [tool] | **Deploy**: [target if detectable]

### Key Dependencies
- [dep1] — [what it's used for]
- [dep2] — [what it's used for]
- (list top 5-8 most important, skip utility libs)

### File Structure Pattern
- [describe the organization pattern in 2-3 lines]
- Entry: [path] | Routes: [path] | Components: [path]

### Conventions
- Naming: [files: x, functions: y, components: z]
- Imports: [style]
- Exports: [style]
- Formatting: [tool + key settings]

### Patterns In Use
- State: [approach]
- Data fetching: [approach]
- Styling: [approach]
- Testing: [approach]
- Error handling: [approach]

### Important Context
- [anything non-obvious that would trip someone up]
- [any documented decisions in ADRs, CONTRIBUTING.md, etc.]
- [active migrations, deprecations, or known tech debt if visible]
```

## Rules

1. **Report what IS, not what SHOULD BE.** This skill detects facts. Don't suggest improvements unless asked.
2. **Sample real files.** Don't guess conventions from config alone — read actual source code.
3. **Skip what's obvious.** If the project is a standard create-react-app with no customization, say that. Don't enumerate every default.
4. **Flag contradictions.** If conventions are inconsistent (some files use semicolons, others don't), report the inconsistency rather than picking one.
5. **Stay current.** Read the actual files NOW, not cached assumptions. Codebases evolve.
6. **Adapt depth to need.** A quick context check before a small fix needs 2 minutes. A full onboarding scan for a large monorepo might take 5+ minutes of reading.

## Lens Loading

For deeper scanning on a specific dimension, load the appropriate lens:
- `lenses/code.md` — Deep architecture and pattern analysis
- `lenses/design.md` — UI/styling/component library analysis
- `lenses/testing.md` — Test infrastructure and pattern analysis
- `lenses/docs.md` — Documentation structure and API surface analysis

See `detection/` for detailed file-matching rules used in each scan step.
