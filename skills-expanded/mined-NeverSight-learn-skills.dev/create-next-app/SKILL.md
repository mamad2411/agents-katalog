---
name: create-next-app
description: "Create, initialize, restructure, or modernize production-grade Next.js App Router applications through guided architecture discovery, dependency review, scaffolding, documentation, and validation. Use when starting a Next.js project, establishing Next.js conventions, or modernizing an existing Next.js codebase."
argument-hint: 'Describe the application and its primary workflows (e.g. "a multi-tenant operations dashboard with authentication and realtime job updates")'
---

# Create Next App

Build modular, production-grade Next.js applications with explicit architecture decisions, minimal dependencies, useful documentation, and verified quality gates.

This skill supports every application category. Never infer the category or silently choose optional infrastructure. Discover the product requirements first, then scaffold only what the selected architecture needs.

## When to Use This Skill

- Creating or initializing a Next.js application
- Establishing architecture and coding conventions for a Next.js repository
- Restructuring an existing Next.js application
- Modernizing a legacy or Pages Router application
- Adding production-ready project governance, documentation, and boundaries
- Selecting data, authentication, API, realtime, email, upload, and deployment patterns

## Progressive Disclosure

Load the relevant reference before each stage instead of guessing:

- Discovery questions: [references/questionnaire.md](references/questionnaire.md)
- Defaults and conditional choices: [references/decision-matrix.md](references/decision-matrix.md)
- Step-by-step creation and Git checkpoints: [references/creation-workflow.md](references/creation-workflow.md)
- Existing projects and Pages Router migrations: [references/modernization.md](references/modernization.md)
- Folder ownership and component boundaries: [references/architecture.md](references/architecture.md)
- Server Actions, APIs, SWR, and external services: [references/api-standards.md](references/api-standards.md)
- Environment validation and synchronization: [references/env-standards.md](references/env-standards.md)
- Dependency selection: [references/package-policy.md](references/package-policy.md)
- Required and project-specific AI skills: [references/skills-policy.md](references/skills-policy.md)
- Security, accessibility, performance, errors, and documentation: [references/best-practices.md](references/best-practices.md)

Use the bundled checklists at project creation, code review, and release. Treat the bundled templates as adaptable references, not files to copy blindly.

## Operating Mode

Follow this sequence:

1. Read this file and the references relevant to the current stage.
2. Establish the Git baseline and checkpoint rules in [references/creation-workflow.md](references/creation-workflow.md). For an existing application, also establish the modernization baseline before proposing changes.
3. Ask the mandatory discovery questions one at a time; skip facts already supplied by the user.
4. Present a compact architecture summary and resolve corrections before implementation.
5. Initialize the application, configure tooling, establish architecture, and implement each selected workflow as separate validated phases. Commit every file-producing phase before starting the next one.
6. Generate or update `README.md`, `.env.example`, and relevant files under `docs/`, then validate and commit that documentation phase.
7. Invoke the installed `create-agentsmd` skill against the representative repository, reconcile its output with the accepted architecture and bundled Next.js guidance, verify its commands, and commit `AGENTS.md` separately.
8. Run formatting, linting, type checking, tests when present, a production build, bootstrap validation, and security checks. Commit any required fixes by concern and rerun the full gate.
9. Remove `create-agentsmd` and `create-next-app` through the Skills CLI, verify the final skill artifact contract, and commit the cleanup as the final file-producing phase.
10. Confirm the ordered commit history and report commits, assumptions, changed files, validation results, and unresolved risks.

Do not start scaffolding while required architecture decisions remain unresolved.

## Fixed Technical Defaults

These choices are non-negotiable unless the user explicitly asks to revise this skill itself:

- Next.js App Router only
- TypeScript with strict mode
- Tailwind CSS v4
- A `src/` directory
- The `@/` import alias
- Biome for linting and formatting
- No ESLint or Prettier
- Zod for runtime validation
- npm support in every project
- A committed `package-lock.json`
- Ask whether Bun package-manager commands should also be supported
- Bun's test runner when tests are requested or required, even when npm is the only supported package manager
- Server Components by default, with the smallest practical client boundaries
- No package merely because it is common
- No icon, UI, form, table, state, animation, or data-fetching package by default
- All AI-created temporary files under the project-root `docs/temp/` directory
- The root `.gitignore` rule `/docs/temp/` so temporary files are never committed
- The root `.gitignore` rule `/.agents/` so installed skill implementations remain local
- Committed root `skills-lock.json` and `AGENTS.md`; do not ignore either file
- A focused Git commit after every completed file-producing creation phase
- Removal of the setup-only `create-next-app` and `create-agentsmd` skills after the app and `AGENTS.md` are complete

Do not ask whether the application should have a UI. Derive the required UI from its workflows. Select form and table tooling only when actual complexity justifies it.

## Conditional Defaults

Use these only after confirming that the concern exists and the user has not selected another option:

| Concern                 | Default                                               |
| ----------------------- | ----------------------------------------------------- |
| Database                | PostgreSQL                                            |
| ORM/query layer         | Prisma                                                |
| Authentication          | Better Auth                                           |
| Shared client state     | React Context                                         |
| URL-synchronized state  | `nuqs`                                                |
| Realtime                | Socket.IO, after deployment compatibility is verified |
| External service access | Official SDK, otherwise a shared typed adapter        |
| Client fetching         | SWR when client fetching is required                  |
| Testing                 | Bun test runner                                       |

Do not ask about payments, background jobs, internationalization, or analytics during initial discovery unless the product description requires them.

## Discovery and Architecture Confirmation

Use [references/questionnaire.md](references/questionnaire.md). Ask one question at a time, offer a recommendation when useful, and avoid repeating answered questions.

At minimum, resolve:

- Application type, users, workflows, and first-release modules
- npm-only package management or npm plus Bun commands
- Database, provider, data-access layer, and migration ownership
- Authentication, roles, and permissions
- Server Actions versus shared API/SWR strategy
- Internal HTTP APIs and external services
- Realtime, uploads/storage, and email
- Deployment target
- Security, privacy, compliance, and data-residency constraints

Before implementation, summarize every architecture category listed in the questionnaire's confirmation section. Record the accepted decisions in the generated README and relevant architecture documentation.

## Architecture Rules

Follow [references/architecture.md](references/architecture.md).

- Use technical layers at the top level and feature colocation inside routes.
- Keep route-specific components, actions, hooks, contexts, schemas, and types with their owning route.
- Promote code to a shared layer only after genuine reuse or a clear cross-cutting need.
- Avoid generic dumping grounds such as a large `utils.ts`.
- Keep secrets and privileged operations server-only.
- Use serializable DTOs instead of exposing database models to client components.
- Create only the infrastructure modules the confirmed project requires.

At the root App Router level, create meaningful implementations for `layout.tsx`, `page.tsx` when applicable, `loading.tsx`, `error.tsx`, `global-error.tsx`, `not-found.tsx`, `providers.tsx`, and `globals.css`. Never create empty route boundaries.

## Data and API Strategy

The Server Actions decision is mandatory. Follow [references/api-standards.md](references/api-standards.md).

### Server Actions primary

- Use Server Actions for authenticated UI mutations and form submissions.
- Use direct server functions for Server Component reads and reusable server-only domain operations.
- Use Route Handlers only when HTTP semantics are required, including auth endpoints, webhooks, callbacks, public APIs, streams, and file responses.
- Validate with Zod, authorize inside the operation, normalize expected errors, and revalidate affected paths or tags.

### Shared API and SWR

- Create typed client and server request utilities, normalized errors, shared contracts, and approved SWR hooks.
- Keep SWR keys stable and define mutation/revalidation behavior.
- Do not scatter raw `fetch()` calls through components.

In both modes, keep transport separate from domain logic. Wrap each external provider in one server-safe adapter, add timeouts, normalize provider errors, and validate untrusted responses when practical.

## Environment Contract

Follow [references/env-standards.md](references/env-standards.md). Every project must include:

- `src/lib/env/server.ts`
- `src/lib/env/client.ts`
- `.env.example`
- `.gitignore` rules that ignore `.env*`, preserve `!.env.example`, and ignore `/docs/temp/`

For every environment variable addition, removal, or rename, synchronize the correct schema, `.env.example`, README table, deployment and CI documentation, tests/mocks, and applicable Docker or platform configuration. Never place a production secret in a tracked file.

## AI Temporary Workspace

Every temporary, scratch, intermediate, generated-for-inspection, or disposable file created by an AI agent must be placed under the project-root `docs/temp/` directory.

- Create `docs/temp/` on demand before writing the first temporary file.
- Never create AI-owned temporary files at the project root, inside source directories, or elsewhere under `docs/`.
- Keep durable architecture and operational documentation elsewhere under `docs/`; `docs/temp/` is disposable and must not contain the only copy of required project information.
- Ensure the root `.gitignore` contains the exact `/docs/temp/` rule.
- Never force-add or commit anything under `docs/temp/`.
- Remove stale task artifacts when they are no longer useful, while leaving user-owned files untouched.

## State, Search Parameters, and Providers

- Use React Context by default for genuinely shared client state.
- Every context needs a typed provider and a dedicated hook that throws clearly outside its provider.
- Split unrelated or frequently changing state to reduce rerenders.
- Colocate route-specific state with its route.
- Use `nuqs` for filters, sorting, pagination, tabs, search strings, and other URL-synchronized state.
- Add only providers selected by project requirements; do not create unused global providers.

## Optional Infrastructure

Create these modules only when selected during discovery:

### Realtime

Default to Socket.IO only after validating the deployment target. Define typed events, authentication, connection/reconnection state, cleanup, a context provider, and a dedicated hook. Do not initialize a global connection for an application that does not need realtime behavior.

### Email

Confirm provider and email types. Keep provider configuration server-only, centralize the send utility and templates, validate template inputs, document sender/domain variables, and never expose credentials to clients.

### Uploads and storage

Resolve accepted file types, size/count limits, visibility, provider, signed/direct upload flow, transformations, validation/scanning, and retention before implementation.

## Dependency and Skill Policy

Before installing a package, follow [references/package-policy.md](references/package-policy.md): verify the latest stable version, official documentation, maintenance, framework/runtime compatibility, necessity, and overlap with existing dependencies. Explain important architectural dependencies in README or docs.

Follow [references/skills-policy.md](references/skills-policy.md): install `find-skills` first, install the required skills, review every third-party `SKILL.md`, then add only project-relevant skills. A required AI skill does not automatically justify adding its corresponding runtime package.

Treat `create-next-app` and `create-agentsmd` as setup-only skills. Remove both with the Skills CLI only after the generated `AGENTS.md` and full application quality gate pass. Keep the resulting `skills-lock.json` and `AGENTS.md` in Git; keep `/.agents/` ignored.

## Bundled Assets

Use these after architecture confirmation:

- `templates/project/AGENTS.md` — provide as Next.js-specific input to `create-agentsmd`; do not copy it blindly or let it override facts discovered from the generated repository
- `templates/project/README.template.md` — fill with actual decisions and commands
- `templates/project/.env.example` — expand with safe documented placeholders
- `templates/project/.gitignore.fragment` — merge without discarding existing rules
- `templates/src/` — reference implementations for providers, context, API errors/fetching, env validation, search parameters, and realtime organization
- `examples/project-brief.example.md` — example architecture confirmation
- `scripts/install-required-skills.sh` — helper for required AI skills
- `scripts/bootstrap-check.sh` — required-file verification for a generated project

Adapt templates to the selected architecture and existing repository patterns. Do not overwrite user-owned files wholesale or add optional modules merely because a template exists.

## Documentation Requirements

Every generated project must contain `AGENTS.md`, `README.md`, `.env.example`, and relevant architecture/operations notes under `docs/`.

Generate or update the root `AGENTS.md` with the installed `create-agentsmd` skill only after the repository structure, package scripts, README, and architecture documentation are representative. Let that skill inspect the actual project, then incorporate the confirmed Next.js conventions from `templates/project/AGENTS.md`. Preserve its task execution workflow: inspect related code, read related installed skills, create an ordered plan, execute it step by step, validate each file-producing step, and commit that step before continuing. Keep only commands and workflows supported by repository evidence, and execute every documented validation command that is practical in the current environment.

The README must document the product, features, stack, accepted architecture, repository structure, setup, npm commands, Bun commands when enabled, environment variables, database/auth decisions when applicable, API patterns, external services, testing, build/deployment, installed AI skills, and troubleshooting.

Update documentation in the same change as behavior. Record durable architectural decisions under `docs/`.

## Completion Gates

Use:

- `checklists/project-creation.md` during scaffolding
- `checklists/code-review.md` before declaring implementation complete
- `checklists/release.md` before release

Do not call the work complete until:

- Biome passes
- Type checking passes
- Tests pass when present
- The production build passes
- Environment examples and documentation are synchronized
- No secret is tracked
- No unused package was introduced
- No AI-created temporary file exists outside `docs/temp/` or is tracked by Git
- Every completed file-producing phase has a focused commit and no unrelated user change was committed
- `/.agents/` is ignored and contains no tracked file
- Root `skills-lock.json` and `AGENTS.md` are tracked, not ignored
- `create-next-app` and `create-agentsmd` are absent from the final `skills-lock.json`
- Route boundaries and module ownership are clear

Report any pre-existing failure separately from failures introduced by the work.
