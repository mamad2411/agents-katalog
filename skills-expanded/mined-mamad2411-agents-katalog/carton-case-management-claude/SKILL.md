# carton-case-management Development Guidelines

## Skills

Before implementing any feature:
1. Review the skills table below and read relevant documentation in `.claude/skills/`
2. Apply skills that match your task (e.g., component-reuse before creating UI)
3. Follow skill workflows to prevent common mistakes

This project uses Agent Skills for specialized workflows. See `.claude/skills/`. Every skill in
that directory is listed below - if it isn't in this table, it isn't an active skill.

Agent Skills are an open standard, so `.claude/skills/` is read by both Claude Code and GitHub
Copilot. There is no second copy to keep in sync.

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `component-reuse` | Ensure existing UI components are reused before creating new ones | Before implementing any UI from Figma, tickets, or mockups |
| `validate-implementation` | Validate implementations for runtime errors, accessibility, and API compliance | Before marking any feature complete or committing code |
| `create-react-modlet` | Create React components following the modlet pattern | When creating any component in `packages/client/src/components/` |
| `cross-package-types` | Type flow between shared, server, and client packages | When working with types across package boundaries |
| `create-skill` | How to create new Agent Skills for this project | When asked to document a workflow or teach the agent a new capability |

### Optional plugins

Workflow skills that are not about this codebase live in `plugins/` and are dormant - nothing
loads them unless you ask. See each plugin's README for what it needs.

Plugins are a **Claude Code** feature. Copilot does not scan `plugins/`, so these are invisible to
it; the `SKILL.md` files inside are portable, but you would have to copy one into `.claude/skills/`
(which both tools read) to use it from Copilot.

| Plugin | Contains | Load with |
|--------|----------|-----------|
| `figma-workflow` | Figma-to-React skills (6): design analysis, implementation, design sync, Code Connect. Requires Figma access. | `claude --plugin-dir ./plugins/figma-workflow` |
| `cascade-workflow` | Jira story writing and Figma design-question skills (13). Requires Cascade + Atlassian MCP servers. | `claude --plugin-dir ./plugins/cascade-workflow` |

## Package-Specific Instructions

Each package has detailed instructions in its own `CLAUDE.md` file:

| Package | CLAUDE.md Location | Purpose |
|---------|-------------------|---------|
| `@carton/shared` | `packages/shared/CLAUDE.md` | Prisma schema, generated types, browser-safe utilities |
| `@carton/server` | `packages/server/CLAUDE.md` | tRPC router, API definitions, database operations |
| `@carton/client` | `packages/client/CLAUDE.md` | React components, UI, tRPC client usage |

### How these reach GitHub Copilot

Copilot reads this root `CLAUDE.md` directly, so there is no `.github/copilot-instructions.md` -
a root mirror would just be a second copy to keep in sync. Do not add one back.

What Copilot does not do is scope a nested `packages/<pkg>/CLAUDE.md` to just that package. That
scoping comes from the `applyTo` frontmatter on `.github/instructions/*.instructions.md`, which are
**generated** from the package CLAUDE.md files:

```bash
npm run sync:agent-docs         # regenerate after editing a package CLAUDE.md
npm run sync:agent-docs:check   # fails if they are stale - wire into CI if you add a workflow
```

Edit the `CLAUDE.md` files. Never edit anything in `.github/instructions/` - it will be overwritten.

## Active Technologies
- TypeScript 5.x, React 18.3.x + Shadcn UI components (Input, Select, Button), Radix UI primitives, Lucide icons, Tailwind CSS, Zod (validation)
- TypeScript 5.x / Node.js 24 + React 18, tRPC 11, @tanstack/react-query 5, Vite 6, Prisma (ORM)

## Project Structure

```text
packages/
  client/   # React frontend
  server/   # Express/tRPC backend
  shared/   # Shared types, Prisma schema, utilities
```

## Commands

### Running Tests
- **Unit Tests**: `npm test` - Runs all unit tests across workspaces (client, server, shared)
- **E2E Tests**: `npm run test:e2e` - Runs Playwright end-to-end tests (installs Chromium first if missing)
- **E2E Tests (UI mode)**: `npm run test:e2e:watch` - Opens Playwright UI for interactive test debugging
- **E2E Tests (pre-provisioned browsers)**: `npm run test:e2e:ci` - Skips the browser check; used by `docker-compose.test.yaml`, whose image already contains Chromium
- **Linting**: `npm run lint` - Runs ESLint across all packages
- **Type Checking**: `npm run typecheck` - Runs TypeScript type checking

### Before Submitting Code
Always ensure all tests pass before committing:
```bash
npm test && npm run test:e2e && npm run lint
```

## Code Style

TypeScript 5.x / Node.js 24: Follow standard conventions

## Coding Standards

- When creating new React files ensure to follow the modlet pattern in `packages/client/CLAUDE.md`.
- No tsx or ts files should have inline comments.
- All styling should be done using Tailwind CSS classes in an external CSS file.
- Responsive designing should be implemented using Tailwind CSS utilities.
- Extract complex logic into custom hooks when it can be reused or when it bloats the component file.

### Component Architecture

- **Component Structure**: Follow the recursive modlet pattern (as demonstrated by CaseDetails component)
- **Component Testing & Documentation**:
  - Every component must have accompanying tests (`.test.tsx` files)
  - Every component should have Storybook stories (`.stories.tsx` files) for documentation and visual testing
  - Tests should cover main functionality, edge cases, and user interactions
- **Custom Hooks - when**:
  - Component has >3 pieces of related state
  - Logic involves complex calculations/transformations
  - Logic could be reused elsewhere
  - Component file exceeds ~100 lines
  - Examples: `useCaseFilters`, `useFormValidation`, `useDebounce`
- **Shadcn UI Components**:
  - Always prioritize using Shadcn UI components over native HTML elements (e.g., use Shadcn Select instead of `<select>`, Shadcn Input instead of `<input>`, etc.)
  - If a needed component is not available, install the Shadcn equivalent using `npx shadcn@latest add [component-name]`
  - Shadcn components should be installed to `packages/client/src/components/ui/` directory and exported via `packages/client/src/components/ui/index.ts`
- **Custom Components**: If a custom component must be built on top of underlying Shadcn components (e.g., EditableSelect, ConfirmationDialog), it should go in `packages/client/src/components/common/`
- **Domain Wrapper Components**: When using generic/common components in a specific domain context:
  - Create a domain-specific wrapper component in the domain's `components/` folder
  - The wrapper encapsulates domain logic (hooks, state management, data fetching)
  - The wrapper passes domain data to the generic component
  - Example structure:
    ```
    components/common/GenericComponent/        # Generic, reusable
    components/FeatureName/
      components/FeatureGenericComponent/      # Domain wrapper
    ```
  - Example implementation:
    ```tsx
    // Domain wrapper
    export function FeatureGenericComponent({ open, onOpenChange }) {
      const { data, handleAction, handleClear } = useFeatureData();
      return (
        <GenericComponent
          open={open}
          onOpenChange={onOpenChange}
          data={data}
          onAction={handleAction}
          onClear={handleClear}
        />
      );
    }
    ```
  - Benefits: Generic components stay reusable, domain logic stays in domain folders, easier testing, clear separation of concerns

### UX Patterns

- **Creating**: Use dedicated create pages (not modals) for creating new entities
- **Editing**: Implement "click to edit" functionality on view pages with inline editing
- **Deleting**: Always use a confirmation modal (ConfirmationDialog) before deleting entities

### Data Layer

- **Prisma Schema in Shared**: Prisma schema lives in `packages/shared/prisma/schema.prisma` - the data model is a shared concern
- **Database Operations in Server**: Database file (`dev.db`), seed script, and constants live in `packages/server/db/`
- **Prisma Client Import**: Server imports Prisma Client from `@carton/shared`, e.g., `import { prisma } from '@carton/shared'`
- **Zod Schemas from Prisma**: Use auto-generated Zod schemas from `@carton/shared` for validation - do not manually duplicate Prisma enums
- **Database Commands** (all run from project root):
  - `npm run db:generate` - Generate Prisma Client and Zod types
  - `npm run db:push` - Push schema changes to the database
  - `npm run db:seed` - Seed the database with test data
  - `npm run db:setup` - Combined push + seed (use for initial setup or reset)
  - `npm run db:studio` - Open Prisma Studio to browse data
- **Environment Config**: Single `.env` file at project root. `DATABASE_URL` must be `file:../../server/db/dev.db`, which points at `packages/server/db/dev.db`.
- **DATABASE_URL is schema-relative**: Prisma resolves relative `file:` paths against the directory holding the schema (`packages/shared/prisma/`) — **not** the project root and **not** the process CWD. This is the single most common source of "why is there a stray `dev.db`?" confusion in this repo. A value like `file:./packages/server/db/dev.db` silently creates `packages/shared/prisma/packages/server/db/dev.db` instead of failing, so mistakes are easy to miss.
  - Use the same value in **every** environment (host, devcontainer, `docker-compose*.yaml`, `Dockerfile*`, CI). Because the path is relative to the schema file, one value is correct regardless of the absolute root — `/workspaces/carton-case-management` and `/app` both work.
  - When a container persists the database via a volume, mount it at `<WORKDIR>/packages/server/db` and confirm `<WORKDIR>` matches the `WORKDIR` in the Dockerfile being built.
- **Cascading Deletes**: Always configure cascading deletes (`onDelete: Cascade`) in Prisma schema when an entity has related data that should be removed when the parent is deleted
