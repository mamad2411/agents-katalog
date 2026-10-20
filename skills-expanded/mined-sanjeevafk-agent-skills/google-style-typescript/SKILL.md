---
name: google-style-typescript
description: >
  Apply Google's official TypeScript style guide when writing, reviewing,
  formatting, or linting TypeScript code. Use this skill whenever the user
  asks to review TypeScript for style, asks about TypeScript naming conventions,
  module imports, type definitions, enums, decorators, or whether code follows
  Google TS conventions. Also triggers on: "clean up this TypeScript", "is this
  idiomatic TypeScript?", "how should I type this?", "should I use interface or
  type alias?", "are enums OK?", "how do I import in TS?", or any question about
  TypeScript code quality in a Google-style context. Note: Google's TS guide
  supersedes the JS guide for TypeScript projects — use this skill, not
  google-style-javascript, for .ts/.tsx files.
---

# Google TypeScript Style Guide

Google's TypeScript style guide is stricter than the JavaScript guide and
reflects TypeScript's additional capabilities around types. Key themes:
prefer explicit types over inference for public APIs, avoid language features
that transpile to surprising output (decorators, enums), and write TypeScript
that reads as clearly as well-typed Java or Go.

---

## Key Rules at a Glance

### Type system
- **Prefer interfaces** over type aliases for object shapes that may be extended. Use type aliases for unions, intersections, and utility types.
- **Avoid `any`** — use `unknown` when the type is genuinely unknown, then narrow it. `@ts-ignore` / `as any` are code smells.
- **No non-null assertion** (`!`) except in tests or when you have provably non-null values that TypeScript can't infer.
- **Enums**: Avoid `enum` — use string literal union types (`type Direction = 'left' | 'right'`) or `const` objects instead. Numeric enums are especially disallowed.
- **Decorators**: Avoid unless using a framework (Angular, NestJS) that requires them.

### Imports & modules
- Use ES module syntax (`import`/`export`), never `require()`.
- Only import from a path's index file or explicit file — no barrel-file chaining.
- Type-only imports: use `import type { Foo } from './foo'` for types that won't appear in the emitted JS.
- No namespace imports (`import * as foo`) unless the module has no default export.

### Naming conventions
| Category | Style | Example |
|---|---|---|
| Variables & functions | `camelCase` | `fetchUser()` |
| Classes & interfaces | `PascalCase` | `UserService` |
| Type aliases | `PascalCase` | `ResponseBody` |
| Enums (if used) | `PascalCase` members | `Direction.Left` |
| Constants | `UPPER_SNAKE_CASE` or `camelCase` | `MAX_RETRIES` |
| Private class members | prefix `#` (ES private) or `private` keyword | `#cache` |
| Files | `kebab-case.ts` | `user-service.ts` |

### Code style
- **Line length**: 80 characters.
- **Semicolons**: Required.
- **Trailing commas**: Required in multi-line structures.
- **Arrow functions**: Preferred for callbacks and short functions.
- **`var`**: Never. Use `const` by default; `let` when reassignment is needed.
- **Optional chaining**: Use `?.` instead of manual null checks.
- **Nullish coalescing**: Use `??` instead of `||` when differentiating null/undefined from falsy values.

### Visibility
- Prefer `private` (or `#` private fields) for class internals.
- Mark parameters as `readonly` when they shouldn't mutate.
- Avoid `public` keyword — it's the default and adds noise.

---

## Mode: Reviewing TypeScript Code

When asked to review TypeScript code for Google style compliance:

1. **Types** — any `any`? Any `!` non-null assertions? Should interfaces be used instead of type aliases?
2. **Enums** — are `enum` keywords present? Flag them and suggest union types.
3. **Imports** — ES module syntax? Type-only imports where appropriate? No `require()`?
4. **Naming** — correct casing per the table above? No abbreviations unless well-known?
5. **Visibility** — are class members appropriately `private`? Is `public` keyword being used unnecessarily?
6. **Null safety** — any risky `!` assertions or missing optional chaining?
7. **var/let/const** — any `var`? Any `let` that should be `const`?
8. **Line length** — any lines > 80 chars?

For each issue:
- Cite the rule (e.g. "§Enums", "§Imports")
- Show the problematic snippet
- Show the corrected version with a brief explanation

---

## Mode: Writing New TypeScript Code

When writing new TypeScript following Google style:

1. Use `const` for everything; `let` only when you must reassign; never `var`.
2. Prefer `interface` for object shapes, `type` for unions and computed types.
3. Add return type annotations to all exported functions.
4. Use `import type` for type-only imports.
5. Replace `enum` with string union types or `const` objects.
6. Use `#` private fields or the `private` keyword — never rely on naming conventions for privacy.
7. Add JSDoc comments to all exported symbols (one-line `/** */` at minimum).
8. Use optional chaining `?.` and nullish coalescing `??` freely.
9. Structure files as: imports → types/interfaces → constants → functions/classes → exports.

---

## When to Load the Full Guide

Load `references/full_guide.md` when:
- The user asks about a rule not covered above (e.g. decorators, module systems, generics constraints)
- Doing a comprehensive file-level review
- Questions about specific TypeScript-isms: conditional types, mapped types, template literal types

The full guide is ~4,000 lines. Search for section headings like `## Source Code Basics`, `## Type System`, `## Classes`, `## Imports`.

**Overlap with JS**: Google's TypeScript guide supersedes the JS guide for `.ts` files. For JavaScript-specific questions in a `.js` file, use `google-style-javascript` instead.

**Also see**: `google-style-common` for cross-language principles on naming and comments.
