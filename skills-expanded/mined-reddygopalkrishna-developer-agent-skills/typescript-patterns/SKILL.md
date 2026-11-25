---
name: typescript-patterns
description: Writes and reviews type-safe TypeScript - strict compiler settings, unknown plus narrowing instead of any, discriminated unions with exhaustive checks, satisfies and as const, branded types, and runtime validation at trust boundaries with schema-inferred types. Use when writing or reviewing TypeScript, creating or tightening tsconfig, removing any, type assertions or non-null assertions, modeling domain types, or typing API, form, env or JSON data. Not for plain JavaScript projects.
license: MIT
---

# TypeScript Patterns

Types are only as true as the data that reaches them. Make the compiler as strict as the codebase can bear, validate everything that crosses a trust boundary at runtime, and never silence an error you have not understood.

## When to use

- Writing new TypeScript or reviewing a TypeScript diff.
- Creating `tsconfig.json` or tightening an existing one.
- Code with `any`, `as`, `!` or `@ts-ignore` scattered around.
- Typing data from HTTP APIs, forms, env vars, `localStorage`, queues, webhooks or `JSON.parse`.

## Workflow

1. **Read the config first.** Open `tsconfig.json` and its `extends` chain. Run `npx tsc --showConfig` to see the effective settings. Note `strict`, `noUncheckedIndexedAccess`, `module`, `moduleResolution` and `verbatimModuleSyntax`.
2. **Check the TypeScript version** (`npx tsc -v`) before using newer syntax. `satisfies` needs 4.9+, `const` type parameters 5.0+, `NoInfer` 5.4+, inferred type predicates 5.5+.
3. **Type-check before and after.** Run `npx tsc --noEmit` (or the project's `typecheck` script). A change that adds errors is not done.
4. **Model the domain with unions and literal types** before writing logic (see below).
5. **Put a runtime validator at every trust boundary** and derive the static type from the schema.
6. **Remove escape hatches** (`any`, `as`, `!`, `@ts-ignore`) in code you touch and replace them with narrowing. If one must stay, add a comment saying why it is safe.
7. Re-run the type checker, the linter and the tests.

## Compiler settings

For new code, `strict: true` is non-negotiable. Add the extra flags below by default; see [references/tsconfig.md](references/tsconfig.md) for full configs per project type and a migration plan for existing code.

| Option | What it buys | Cost |
|---|---|---|
| `strict` | `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `useUnknownInCatchVariables` and more | Required |
| `noUncheckedIndexedAccess` | `arr[i]` and `record[key]` become `T \| undefined` | Extra checks in index-heavy code; worth it |
| `exactOptionalPropertyTypes` | `{ a?: string }` stops accepting an explicit `a: undefined` | Noisy with some libraries; adopt in new code |
| `noImplicitOverride` | Subclass overrides must say `override` | Low |
| `noFallthroughCasesInSwitch` | Catches missing `break`/`return` | Low |
| `verbatimModuleSyntax` | Type-only imports must say `import type`; predictable output | Use with ESM; in CommonJS output it forces `import x = require()` |
| `isolatedModules` | Each file can be compiled alone (esbuild, swc, Babel, Vite) | Bans a few constructs such as cross-file `const enum` |

Do not flip `strict` on a large existing codebase in one PR. Follow the incremental plan in the reference.

## Core patterns

### `unknown` over `any`, then narrow

```ts
function parseConfig(raw: string): Config {
  const data: unknown = JSON.parse(raw);
  return ConfigSchema.parse(data); // validated, typed
}

try {
  await save();
} catch (err: unknown) {
  const message = err instanceof Error ? err.message : String(err);
  logger.error({ message }, "save failed");
}
```

Narrowing toolkit: `typeof`, `instanceof`, `in`, `Array.isArray`, discriminant checks, type predicates (`(x): x is User`) and assertion functions (`asserts x is User`). From 5.5, `.filter((x) => x !== undefined)` narrows the array type on its own.

### Make illegal states unrepresentable

Replace bags of optional fields with a discriminated union, and make the compiler prove every case is handled.

```ts
// Bad: loading, data and error can all be set at once
type State<T> = { loading: boolean; data?: T; error?: Error };

// Good
type State<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`);
}

function render<T>(state: State<T>): string {
  switch (state.status) {
    case "idle": return "Start";
    case "loading": return "Loading...";
    case "success": return `Got ${String(state.data)}`;
    case "error": return state.error.message;
    default: return assertNever(state); // compile error if a case is added and not handled
  }
}
```

### Literal unions and `as const` objects instead of `enum`

```ts
export const Role = { Admin: "admin", Member: "member", Viewer: "viewer" } as const;
export type Role = (typeof Role)[keyof typeof Role]; // "admin" | "member" | "viewer"
```

Plain string unions are erasable, tree-shake cleanly and work with Node's type stripping and `erasableSyntaxOnly`. Keep an existing `enum` if the codebase standardizes on it; don't mix both styles in one module.

### `satisfies` to check without widening

```ts
const routes = {
  home: "/",
  userDetail: "/users/:id",
} as const satisfies Record<string, `/${string}`>;

routes.userDetail; // type is "/users/:id", not string
```

Use `satisfies` instead of a type annotation when you want the value checked against a type but keep its precise inferred type.

### Branded types for IDs and validated values

```ts
type Brand<T, B extends string> = T & { readonly __brand: B };
export type UserId = Brand<string, "UserId">;
export type OrderId = Brand<string, "OrderId">;

export function toUserId(raw: string): UserId {
  if (!raw.startsWith("usr_")) throw new Error(`Invalid user id: ${raw}`);
  return raw as UserId; // the only place this assertion is allowed
}

declare function getOrder(id: OrderId): Promise<Order>;
// getOrder(userId) is now a compile error
```

Use brands for IDs that are easy to mix up, money in minor units, sanitized HTML, and validated emails or URLs.

### Validate at trust boundaries, infer the type from the schema

Write the shape once as a schema (zod, valibot, arktype, typebox, or whatever the project uses) and derive the type from it. Never cast `await res.json()` to a type.

```ts
import { z } from "zod";

const User = z.object({
  id: z.string().min(1),
  name: z.string(),
  role: z.enum(["admin", "member", "viewer"]),
});
export type User = z.infer<typeof User>;

export async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${encodeURIComponent(id)}`);
  if (!res.ok) throw new Error(`GET /api/users failed: ${res.status}`);
  const parsed = User.safeParse(await res.json());
  if (!parsed.success) throw new Error(`Unexpected user payload: ${parsed.error.message}`);
  return parsed.data;
}
```

Boundaries that need validation: HTTP responses and request bodies, env vars (validate once at startup and export a typed `env` object), `JSON.parse`, `localStorage`, URL and query params, `postMessage`, webhooks, queue messages, and rows from loosely typed DB drivers.

### Generics that earn their keep

- A type parameter should relate two or more things (an input to an output, two arguments). One that appears once is `any` in disguise; use the concrete type or `unknown`.
- Constrain parameters: `function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K>`.
- Use `const` type parameters (5.0+) to infer literal types from arguments without forcing callers to write `as const`.
- Use `NoInfer<T>` (5.4+) when one argument should not drive inference, such as a default value.

### Utility types worth knowing

| Type | Use |
|---|---|
| `Pick`, `Omit` | Derive view types from a model. `Omit` is not distributive over unions; write a distributive helper if needed |
| `Partial`, `Required`, `Readonly` | Patch objects, config with defaults, immutable inputs |
| `Record<K, V>` | Maps with known key sets (`Record<Role, Permission[]>`) |
| `ReturnType`, `Parameters`, `Awaited` | Derive types from functions you don't own |
| `Extract`, `Exclude`, `NonNullable` | Filter unions |

### Imports and exports

Use `import type { User } from "./user"` and `export type { User }` for types. It keeps runtime output predictable and is required under `verbatimModuleSyntax`.

### Public API types

Annotate return types of exported functions and public methods so the API cannot change by accident. Let local variables and private helpers infer.

## Anti-patterns

- **`as` to make an error go away.** It hides the bug the compiler found. Narrow or validate instead. `as unknown as T` is always a red flag.
- **Non-null `!`.** Replace with a check and an early return or a thrown error that says what was missing.
- **`@ts-ignore`.** If you truly cannot fix it, use `// @ts-expect-error <reason>`, which fails once the error is gone.
- **Trusting `JSON.parse`, `res.json()` or `any`-typed library output.** Validate it.
- **Bags of optional properties** where a discriminated union fits.
- **`Function`, `Object` or `{}` as types.** Use a real signature, `Record<string, unknown>` or `unknown`.
- **Duplicated types** that drift from the schema, the DB model or the API contract. Derive them.
- **Type-level cleverness** that nobody on the team can read. Prefer a simple type plus a runtime check.
- **Turning off strict flags** to get a build green.

## Done when

- `tsc --noEmit` passes with no new errors and no new `any`, `as`, `!` or `@ts-ignore` without a comment justifying it.
- Every value that crosses a trust boundary is validated at runtime, and its type is inferred from the schema.
- Every union `switch` has an exhaustive `never` check.
- Exported functions have explicit return types.

## References

- [references/tsconfig.md](references/tsconfig.md) — read when creating or changing `tsconfig.json`, choosing `module`/`moduleResolution`, or migrating an existing codebase to stricter settings.
