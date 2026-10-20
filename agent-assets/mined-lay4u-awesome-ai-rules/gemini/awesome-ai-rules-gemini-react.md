# Gemini CLI React Rules

## CLI-First Workflow
- Use terminal-driven development with explicit command output.
- Iterate in short loops: implement -> lint -> typecheck -> test.
- Keep diffs small and tied to observable behavior.

## Standard Command Set
- `pnpm lint`
- `pnpm typecheck`
- `pnpm vitest run`
- `pnpm test -- --watch=false` when Vitest script is absent.
- `pnpm -s exec prettier -w .` for formatting updates.

## React 19 Baseline
- Use functional components and strict TypeScript throughout.
- Prefer explicit props typing and narrow component contracts.
- Avoid class components and opaque abstraction layers.
- Use React 19 APIs (`use`, `useOptimistic`, `useActionState`) with intent.

## Hooks and State
- Extract reusable logic into focused custom hooks.
- Keep side effects in `useEffect` only for external synchronization.
- Favor derived state over duplicated mutable state.
- Model async state transitions explicitly to avoid UI ambiguity.

## Component and Styling Conventions
- Keep components single-purpose and composition-friendly.
- Prefer semantic HTML and accessible form/control patterns.
- Use project-standard styling approach consistently (Tailwind/CSS Modules/etc).
- Keep visual states clear for loading, empty, success, and error cases.

## Testing (Vitest + RTL)
- Use Vitest with React Testing Library for component behavior tests.
- Query by role, label, and visible text before test IDs.
- Assert user-visible outcomes, not hook internals.
- Cover interaction paths, edge states, and error handling.

## Delivery Expectations
- Lint, typecheck, and tests must pass for touched scope.
- Add or update tests alongside behavior changes.
- Preserve readability and maintainability over cleverness.
