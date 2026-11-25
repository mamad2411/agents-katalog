---
name: clean-code
description: Clean code and structure standards for this repo. Use when writing or refactoring any TypeScript/React code — covers naming, file layout, typing, and testing discipline.
---

# Clean Code

Optimize for the next reader. This repo is a template people clone repeatedly — every
pattern in it gets copied, so every pattern must be worth copying.

## TypeScript discipline

- Strict mode is on; keep it meaningful: **no `any`**, no `as unknown as`, no `!`
  non-null assertions to silence errors you should fix.
- Derive types instead of duplicating them: `z.infer<typeof Schema>`,
  `ComponentProps<typeof Button>`, `ReturnType<...>`.
- Type function boundaries (params, return values); let inference handle locals.
- Model states that can't coexist as discriminated unions, not boolean soup
  (`status: "idle" | "loading" | "error"` beats `isLoading` + `isError`).

## Naming

- Components: `PascalCase`. Hooks: `useCamelCase`. Everything else: `camelCase`.
  Files: match the main export (`user-card.tsx` exporting `UserCard` — kebab-case files,
  per shadcn convention).
- Names say **what**, not **how**: `activeUsers`, not `filteredArr`.
- Booleans read as predicates: `isOpen`, `hasAccess`, `canEdit`.
- No abbreviations that save three characters at the cost of a mental lookup.

## Structure

- `src/app/` — routes only (pages, layouts, route handlers).
- `src/components/ui/` — shadcn primitives (managed by the CLI, don't hand-edit).
- `src/components/` — shared feature components composed from primitives.
- `src/lib/` — pure utilities, schemas, clients. No React in `lib/`.
- Small components: when a component needs a scroll to read, extract pieces.
- Co-locate what changes together; extract only on the second use, not speculatively.

## Functions & flow

- Early returns over nested `if`/`else` pyramids.
- No dead code, no commented-out code, no `console.log` left behind — git remembers.
- Comments explain **why** (constraints, gotchas), never **what** the next line does.
- Don't catch errors you can't handle; let them reach the error boundary with context.

## Testing discipline

- Test behavior, not implementation: query by role/label (`getByRole("button",
{ name: /save/i })`), never by class names or test IDs when a semantic query exists.
- Every bug fix gets a test that fails without the fix.
- Tests live in `src/__tests__/` or co-located as `*.test.tsx`.

## Commits

- Conventional Commits, enforced by commitlint: `feat:`, `fix:`, `docs:`, `refactor:`...
- One logical change per commit; subject in imperative mood, ≤ 72 chars.
