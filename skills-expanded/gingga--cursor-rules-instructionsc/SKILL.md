---
description: General instructions and standards to follow for our project
globs: *
alwaysApply: false
---
# Agent Behaviour Guide

## Core Tech Stack

<tech_stack>
- **Monorepo Management**: [Turbo](mdc:https:/turbo.build)
- **Package Manager**: [pnpm](mdc:https:/pnpm.io)
- **Primary Languages**: TypeScript (strict mode) / JavaScript (ES6+)
- **Runtime**: API ([Workerd](mdc:https:/developers.cloudflare.com/workers/runtime-apis/workerd)), Web ([Node.js](mdc:https:/nodejs.org) >= 20)
- **UI Framework**: React 19+ (Functional Components + Hooks)
- **Web Framework**: React Router 7
- **API Framework**: [Hono](mdc:https:/hono.dev)
- **RPC**: [tRPC](mdc:https:/trpc.io)
- **State/Routing**: TanStack Ecosystem (Query, Router, Table, Form)
- **Styling**: Tailwind CSS v4+ with Shadcn/UI components
- **Database**: [Turso](mdc:https:/turso.tech) (Serverless SQLite)
- **ORM**: [Drizzle ORM](mdc:https:/orm.drizzle.team)
- **Authentication**: [Better Auth](mdc:https:/better-auth.com)
- **Validation**: Zod 3.22+
- **Form**: React Hook Form / TanStack Form
- **Animation**: Motion and GSAP
</tech_stack>

## Agent Operating Protocol

<agent_rules>
1. Mandatory Planning Phase:
- Always work in English, even if you receive instructions in Spanish. Think, develop, and give responses in English.
- Always start with RFC-style plan containing:
-- Affected components/files
-- Data flow diagram (mental model)
-- Potential breaking changes
-- Alternative approaches considered

2. Implementation Standards:
- When developing features, refer to [features.mdc](mdc:.cursor/rules/features.mdc)
- When working on UI/UX, refer to [design.mdc](mdc:.cursor/rules/design.mdc)
- When working with forms, refer to [forms.mdc](mdc:.cursor/rules/forms.mdc)
- Project vision → [agents-vision.mdc](mdc:.cursor/rules/agents-vision.mdc) (project general purpose)
- Explicitly list ALL referenced sections from any instruction file at the end of the response. Just as an extra commentary.
</agent_rules>

## Code Style Guide

<code_style>
**Naming Conventions:**
-- Boolean vars: hasXxx/isXxx/shouldXxx (e.g. isReady)
-- Event handlers: handle[Element][Action] (e.g. handleFormSubmit)
-- Prefer kebab-case for file names, PascalCase for component names, and camelCase for the rest.
-- Prefer using named exports over default exports.
</code_style>

## Quality Enforcement

<best_practices>
1. Do not add unnecessary comments to the generated code. Only add comments for complex business logic.
2. Always implement proper error boundaries and loading states.
3. Use TypeScript's strict mode and avoid any type.
4. Follow React's functional component patterns.
5. Implement proper prop validation.
6. Use consistent naming conventions.
7. Write self-documenting code with clear function and variable names.
8. Follow accessibility best practices.
9. Do not add descriptions to your response, unless it is explicitly asked for. Just write the code.
10. Use Tailwind CSS, and import the `cn()` utility for conditional classes only if you need to. Import it from `~/lib/utils`.
11. Keep component files focused and single-responsibility
12. Use early returns whenever possible to make the code more readable.
13. Prefer using the "Icon" suffix whenever using icons from `lucide-react`. E.g., import `ExternalLinkIcon` instead of `ExternalLink`.
14. Prioritize using destructuring and other modern JavaScript functions whenever possible.
</best_practices>

## Project Anatomy

<project_structure>
The application follows a monorepo structure managed by Turbo:
```
.
├── apps/
│   ├── api/        # Cloudflare Worker API (Hono, tRPC)
│   └── client/        # Web Application (React Router, React)
├── packages/
│   ├── db/         # Drizzle ORM schema, migrations (Turso/SQLite)
│   ├── ui/         # Shared React components (Shadcn/UI based)
│   └── tsconfig/   # Shared TypeScript configurations
├── pnpm-lock.yaml
├── package.json    # Root dependencies and scripts
└── turbo.json      # Turbo configuration
```
- Features within `apps/web` generally follow the structure outlined in [features.mdc](mdc:.cursor/rules/features.mdc).
- API routes and logic reside within `apps/api`.
</project_structure>

## Monorepo Workflow

<monorepo_workflow>
- **Running Commands**: Use `pnpm run <script>` from the root directory. Turbo will execute the script across the relevant workspaces (e.g., `pnpm run dev`, `pnpm run build`, `pnpm run lint`).
- **Package-Specific Commands**: For scripts not defined in the root `package.json` (e.g., `db:migrate`, `cf-typegen`), either:
    - Run the command from within the specific package directory (`cd packages/db && pnpm run db:migrate`).
    - Use the `--filter` flag with Turbo from the root (`pnpm run db:migrate --filter=@gingga/db...`).
</monorepo_workflow>

## Return Types

When declaring functions on the top-level of a module,
declare their return types. This will help future AI
assistants understand the function's purpose.

```ts
const myFunc = (): string => {
  return "hello";
};
```

One exception to this is components which return JSX.
No need to declare the return type of a component,
as it is always JSX.

```tsx
const MyComponent = () => {
  return <div>Hello</div>;
};
```

