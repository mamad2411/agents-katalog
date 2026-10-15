---
name: rexxars
description: Espen Hovlandsdal's opinionated tooling and conventions for JavaScript/TypeScript projects. Use when setting up new projects, configuring ESLint/Prettier alternatives, monorepos, library publishing, or when the user mentions Espen's preferences.
metadata:
  author: Espen Hovlandsdal
  version: "2026.05.01"
---

## Coding Practices

### Code Organization

- **Single responsibility**: Each source file should have a clear, focused scope/purpose
- **Split large files**: Break files when they become large or handle too many concerns
- **Type separation**: Always separate types and interfaces into `types.ts` or `types/*.ts`
- **Constants extraction**: Move constants to a dedicated `constants.ts` file
- **File extensions**: Use `.js`/`.ts` - only use `.mjs`/`.mts` when the project is not `"type": "module"`

### Runtime Environment

- **Prefer isomorphic code**: Write runtime-agnostic code that works in Node, browser, and workers whenever possible
- **Clear runtime indicators**: When code is environment-specific, add a comment at the top of the file:

```ts
// @env node
// @env browser
```

### TypeScript

- **Erasable syntax only**: avoid non-javascript features like enums, namespaces, decorators etc.
- **Never use type assertions** (`as`, `<Type>`) to silence type errors. Instead, use proper type narrowing (typeof, instanceof, `in` operator, discriminated unions) and user-defined type guards (`is` predicates).
- **Don't cast**: If a value's type isn't narrow enough, fix the upstream types or write a type guard function.
- **Prefer `unknown`** over `any`, and narrow from there.
- **Explicit return types**: Declare return types explicitly when possible
- **Avoid complex inline types**: Extract complex types into dedicated `type` or `interface` declarations

### Comments

- **Avoid unnecessary comments**: Code should be self-explanatory
- **Explain "why" not "how"**: Comments should describe the reasoning or intent, not what the code does

---

## Testing Practices

### Testing (Vitest)

- In success tests, use `if (error) throw error` - NOT `expect(error).toBeUndefined()`. It gives better stack traces on failure.
- Use `describe` + `test` API (not `it`), imported from `vitest` explicitly
- Use `toMatchSnapshot` for complex outputs

---

## Library authoring preferences

- **Pure ESM**: Always publish libraries as pure ESM.
- **tsdown**: Use `tsdown` for bundling libraries, unless in `@sanity/*` scopes where `@sanity/pkg-utils` is preferred.
- **TypeScript** with erasable syntax only, strict mode.
- **Isomorphic code**: Write runtime-agnostic code that works in Node, browser, and workers whenever possible.
- **Clear runtime indicators**: When code is environment-specific, add a comment at the top of the file:

```
// @env node
// @env browser
```

---

## Benchmarking

- When asked to benchmark javascript, use `mitata` package. Compare before/after changes.
