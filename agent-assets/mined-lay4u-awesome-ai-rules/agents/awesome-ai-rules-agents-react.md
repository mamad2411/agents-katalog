# Codex React Rules

## Mission
- Produce production-ready React 19 code with strict TypeScript and reliable tests.
- Work autonomously: implement, verify, and report exact command outcomes.

## Execution Protocol
- Before edits: inspect existing component patterns, state model, and test setup.
- During edits: keep components focused and diffs behavior-oriented.
- After edits: run required checks and summarize concrete results.

## Required Verification Commands
- `pnpm -s exec prettier -c .` (or project formatter equivalent)
- `pnpm lint`
- `pnpm typecheck`
- `pnpm vitest run`
- `pnpm test:e2e` when UI flows were changed and suite exists.

## React 19 Component Standards
- Use functional components only; do not introduce class components.
- Keep component responsibilities narrow and composable.
- Prefer explicit props contracts and discriminated unions where needed.
- Avoid `any`; model uncertain data via validated types.

## Hooks and State
- Use hooks to isolate reusable behavior and side effects.
- Keep `useEffect` focused on external synchronization only.
- Prefer derived values over duplicated state.
- Use React 19 capabilities (`use`, `useOptimistic`, `useActionState`) intentionally.

## Data Flow and UX
- Handle loading, empty, success, and error states explicitly.
- Keep async boundaries clear and user-visible transitions predictable.
- Prevent stale UI with stable keys and deterministic state updates.
- Maintain accessibility with semantic markup and keyboard support.

## Testing Standards (Vitest + RTL)
- Write tests with Vitest and React Testing Library.
- Test user-observable behavior, not internal implementation details.
- Prefer `screen.getByRole`/`findByRole` over brittle selectors.
- Cover critical journeys, edge cases, and failure paths.

## Completion Criteria
- Lint, typecheck, and test commands pass.
- New logic includes tests aligned with user-facing behavior.
- Components remain typed, accessible, and maintainable.
