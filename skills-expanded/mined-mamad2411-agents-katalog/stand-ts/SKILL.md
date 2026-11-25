---
name: stand-ts
description: >-
  TypeScript and JavaScript standards. Use when writing TS/JS code. Covers strict
  mode, type patterns, error handling, imports, naming, testing, React conventions,
  and package management with bun.
---

# TypeScript / JavaScript Standards

Standards for TypeScript and JavaScript code.

## Package Manager

- Prefer `bun` over `npm`
- Use `bun install` instead of `npm install`
- Use `bun run` instead of `npm run`
- Use `bunx` instead of `npx`

## Strict Mode

- Enable `strict: true` in `tsconfig.json`
- No `any` escape hatches without justification — if unavoidable, add a comment
  explaining why

## Type Patterns

- Prefer `interface` for object shapes; use `type` for unions, intersections, and
  mapped types
- Use `satisfies` over `as` for type narrowing — preserves the inferred type while
  validating the shape
- Avoid `enum` — use `as const` objects instead:

  ```typescript
  // Good
  const Status = {
    Active: "active",
    Inactive: "inactive",
  } as const;
  type Status = (typeof Status)[keyof typeof Status];

  // Avoid
  enum Status {
    Active = "active",
    Inactive = "inactive",
  }
  ```

- Prefer discriminated unions over optional fields for state modeling

## Error Handling

- Use `unknown` in catch clauses, not `any`:

  ```typescript
  // Good
  catch (err: unknown) {
    if (err instanceof SpecificError) { ... }
  }

  // Bad
  catch (err: any) { ... }
  ```

- Never swallow errors with empty catch blocks
- Prefer typed error results (`Result<T, E>` pattern) over thrown exceptions for
  expected failure paths

## Imports

- Use type-only imports for types: `import type { Foo } from "./foo";`
- Avoid barrel files (`index.ts` re-exports) in libraries — they defeat tree-shaking
  and obscure dependency graphs

## Naming

- `PascalCase` for types, interfaces, classes, and React components
- `camelCase` for variables, functions, and methods
- `UPPER_SNAKE_CASE` for constants and environment variable names
- Prefix boolean variables/props with `is`, `has`, `should`, `can`

## Formatting Rules

- More than 1 arg/param requires a trailing comma (consistent with the `stand-py` skill)
- Be explicit with named arguments in object parameters when more than 1 property

## Linting

Follow the `lint` skill for linting and formatting workflow.

## Testing

- Prefer Vitest over Jest
- Use test functions, not test classes
- Leverage `describe` blocks for grouping, not class hierarchies
- Use `beforeEach` / `afterEach` for shared setup/teardown
- Use `it.each` or `test.each` for parameterized tests

```typescript
// Good
describe("parseConfig", () => {
  it("returns defaults for empty input", () => {
    expect(parseConfig({})).toEqual(defaults);
  });

  it.each([
    { input: "yes", expected: true },
    { input: "no", expected: false },
  ])("parses '$input' as $expected", ({ input, expected }) => {
    expect(parseBoolean(input)).toBe(expected);
  });
});
```

## React

When working in React codebases:

- Function components only — no class components
- Prefer hooks over HOCs and render props
- Named exports for components (no `export default`)
- Co-locate component, styles, and tests in the same directory
- Extract custom hooks when logic is reused across components
