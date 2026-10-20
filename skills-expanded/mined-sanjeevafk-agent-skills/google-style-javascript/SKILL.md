---
name: google-style-javascript
description: >
  Apply Google's official JavaScript style guide when writing, reviewing,
  formatting, or linting JavaScript code. Use this skill whenever the user
  asks to review JavaScript for style, asks about JS naming conventions,
  module syntax, var vs let vs const, string formatting, JSDoc comments,
  or whether code follows Google JS conventions. Also triggers on: "clean
  up this JavaScript", "is this good JS?", "how do I format this JS function?",
  "should I use arrow functions here?", "how do I write JSDoc?", "what's the
  Google way to handle this in JS?". Note: for TypeScript (.ts/.tsx files)
  use google-style-typescript instead — this skill covers .js and .mjs files.
---

# Google JavaScript Style Guide

Google's JS style guide is used for all JavaScript in Google's open-source
projects. Key themes: ES2015+ features are encouraged, CommonJS (`require`) is
avoided in favour of ES modules, every file and public symbol needs JSDoc, and
`var` is permanently retired. It differs from the TypeScript guide mainly in
the absence of static types — JSDoc type annotations fill that role.

---

## Key Rules at a Glance

### Variables & scope
- **`const` by default**; `let` only when a variable must be reassigned; `var` never.
- Declare every variable — no implicit globals.
- One variable per declaration (`const a = 1, b = 2` — avoid).

### Functions
- Prefer **arrow functions** for non-method callbacks.
- Prefer **named function declarations** over `var f = function()` for top-level functions (enables hoisting and better stack traces).
- Default parameters: use `function f(x = 0)`, not `x = x || 0` inside the body.
- Rest params: use `...args`, never `arguments`.
- Spread: use `...arr`, never `.apply()`.

### Strings
- Use **single quotes** `'` for string literals (except to avoid escaping).
- Use **template literals** `` ` `` for any string with embedded expressions or multi-line content — never string concatenation.
- No `String()` constructor.

### Objects & arrays
- Use **object shorthand**: `{ x, y }` not `{ x: x, y: y }`.
- Use **computed property names** and **destructuring** freely.
- Use `Array.from()` or spread `[...iterable]` instead of `.slice()` to convert iterables.
- No `Object.prototype` method calls directly on instances (use `Object.keys(obj)` not `obj.hasOwnProperty(...)`).

### Classes & modules
- Use `class` syntax for OOP — no prototype manipulation.
- Use ES module `import`/`export` — never `require()` or `module.exports`.
- One class or closely related set of utilities per file.
- Prefer named exports; default exports are allowed but make re-exports harder.

### Naming conventions

| Entity | Style | Example |
|---|---|---|
| Variables & functions | `camelCase` | `getUserById()` |
| Classes | `PascalCase` | `UserService` |
| Constants (module-level) | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Private methods/props | leading `_` or `#` | `#cache`, `_helper` |
| Files | `kebab-case.js` | `user-service.js` |
| Enum-like objects | `PascalCase` | `Direction.Left` |

### Formatting
- **Line length**: 80 characters.
- **Indentation**: 2 spaces (not 4 — this is different from Python).
- **Semicolons**: Required at end of statements.
- **Trailing commas**: Required in multi-line arrays, objects, and parameter lists.
- **Braces**: Always use braces for `if`/`for`/`while` bodies, even single-line.
- **Blank lines**: One blank line between method definitions; two between top-level declarations.

### JSDoc (for public APIs)
```javascript
/**
 * Fetches a user by ID.
 *
 * @param {string} id The user's unique identifier.
 * @param {number=} timeout Optional timeout in milliseconds.
 * @return {!Promise<!User>} Resolves with the user record.
 */
async function getUser(id, timeout = 5000) { ... }
```
- Every module, class, and exported function needs a JSDoc comment.
- Use `{!Type}` for non-nullable, `{?Type}` for nullable.
- `@param`, `@return`, `@throws` sections mirror Python's Args/Returns/Raises.

---

## Mode: Reviewing JavaScript Code

When asked to review JS code for Google style compliance, work through:

1. **`var` / `let` / `const`** — any `var`? Any `let` that should be `const`?
2. **Strings** — any concatenation that should be a template literal? Any double quotes where single should be used?
3. **Functions** — named or arrow where appropriate? Any `arguments` use? Any `.apply()` that should be spread?
4. **Naming** — correct casing per the table above? No abbreviations beyond well-known ones?
5. **Modules** — any `require()` / `module.exports`? Any missing `export` keywords?
6. **JSDoc** — present on all public functions/classes? Correct `@param` / `@return` types?
7. **Braces** — any braceless control flow bodies?
8. **Line length** — any lines > 80 chars?
9. **Indentation** — 2 spaces (not 4)?

For each issue:
- Cite the section (e.g. "§Features: Variables", "§Naming")
- Show the problematic snippet and the corrected version

---

## Mode: Writing New JavaScript Code

When writing new JavaScript following Google style:

1. File starts with a `@fileoverview` JSDoc comment for non-trivial modules.
2. Imports at the top (ES module `import`), ordered: external → internal.
3. `const` everywhere; `let` only when mutation is unavoidable.
4. 2-space indentation, 80-char line limit.
5. Single quotes for strings; template literals for interpolation.
6. Add JSDoc to every exported function, class, and constant.
7. Use `class` for OOP; avoid prototype manipulation.
8. Arrow functions for callbacks; named function declarations for top-level.
9. Destructuring for multiple-value returns and parameter extraction.
10. Trailing commas in all multi-line structures.

---

## When to Load the Full Guide

Load `references/full_guide.md` when:
- The user asks about a specific rule not covered above (e.g. generator functions, `for...of` vs `forEach`, `Symbol`, `Proxy`)
- Doing a comprehensive file-level review
- Questions about specific sections: "Source File Basics", "Formatting", "Language Features", "Naming", "JSDoc"

The full guide is ~4,000 lines. The TOC in `references/TOC.md` lists all section headings with anchors.

**Overlap with TS**: This guide covers `.js` / `.mjs` files. For TypeScript, always use `google-style-typescript` instead.

**Also see**: `google-style-common` for cross-language naming and comment philosophy.
