# TypeScript Strict Soundness, Domain Modeling & Boundary Validation

## 1. Purpose
Author, refactor, and verify mission-critical systems written in modern **TypeScript (5.x+)**. This skill enforces complete compiler soundness (`strict: true`, `noUncheckedIndexedAccess: true`), absolute eradication of `any`, nominal domain modeling via Branded Types, exhaustive discriminated unions with `never` checks, modern `satisfies` expressions, and mandatory runtime schema validation (Zod/Valibot/TypeBox) at all external I/O boundaries.

---

## 2. Use When
- Developing frontend web applications, backend Node.js/Bun/Deno services, or fullstack TypeScript architectures.
- Defining strongly typed domain models, state machines, API contracts, or SDK client libraries.
- Ingesting untrusted external data (HTTP payloads, environment variables, IPC messages, WebSocket events).
- Refactoring legacy loosely typed JavaScript or unvalidated TypeScript codebases into sound type topologies.
- Operating in mode(s): `implementation`, `review`, `testing`, `audit`.

---

## 3. Do Not Use When
- Developing purely in vanilla JavaScript without build-step transpilation (use `lang-javascript`).
- Writing low-level systems kernels, native memory allocators, or graphics shaders in C/C++/Rust/WGSL.
- The project intentionally maintains a non-strict `tsconfig.json` with implicit `any` that cannot be upgraded.

---

## 4. Required Context
Before writing or modifying TypeScript code, verify:
- **TypeScript Version**: TypeScript 5.0+ with modern module resolution (`NodeNext` / `Bundler`).
- **Compiler Configuration (`tsconfig.json`)**:
  - `"strict": true`
  - `"noUncheckedIndexedAccess": true`
  - `"exactOptionalPropertyTypes": true`
  - `"noImplicitReturns": true`
  - `"noFallthroughCasesInSwitch": true`
- **Boundary Validation Library**: Zod, Valibot, ArkType, or TypeBox.
- **Linting & Code Quality**: `@typescript-eslint/strict-type-checked` with zero allowed warnings.

---

## 5. Procedure

```
[External Input / API Contract]
         |
         v
[1. Runtime Boundary Validation] ----> Parse via Zod/Valibot (Derive Type from Schema)
         |
         v
[2. Domain Modeling & Branding] -----> Nominal Branded Types & Discriminated Unions
         |
         v
[3. Business Logic Execution] -------> Immutability, `satisfies`, Exhaustive `never`
         |
         v
[4. Static Type Verification] -------> `tsc --noEmit` with zero diagnostics
         |
         v
[5. Dynamic Test Gauntlet] ----------> Vitest / Jest execution with typed mocks
```

### Step 1: Mandatory Boundary Validation (Never Cast with `as`)
1. Data crossing external boundaries (HTTP requests, environment variables, database records, file reads) must be treated as `unknown`.
2. Parse through a runtime schema validator that infers the static type automatically:
   ```typescript
   import { z } from "zod";

   export const UserPayloadSchema = z.object({
     id: z.string().uuid(),
     email: z.string().email(),
     role: z.enum(["admin", "operator", "viewer"]),
     retryCount: z.number().int().nonnegative().default(0),
   });

   export type UserPayload = z.infer<typeof UserPayloadSchema>;

   export function parseUserPayload(raw: unknown): UserPayload {
     return UserPayloadSchema.parse(raw);
   }
   ```
3. Type assertions (`raw as UserPayload`) without validation are strictly forbidden.

### Step 2: Nominal Domain Modeling with Branded Types
To prevent primitive obsession where IDs are accidentally swapped:
```typescript
declare const Brand: unique symbol;
export type Brand<T, B> = T & { readonly [Brand]: B };

export type UserId = Brand<string, "UserId">;
export type OrderId = Brand<string, "OrderId">;

export function makeUserId(id: string): UserId {
  if (!id.startsWith("usr_")) throw new Error("Invalid UserId format");
  return id as UserId;
}
```

### Step 3: Discriminated Unions & Exhaustiveness Checking
Model all stateful entities and multi-variant responses as discriminated unions:
```typescript
export type AsyncState<T> =
  | { readonly status: "idle" }
  | { readonly status: "loading" }
  | { readonly status: "success"; readonly data: T }
  | { readonly status: "error"; readonly error: Error };

export function assertNever(x: never): never {
  throw new Error(`Unexpected object: ${JSON.stringify(x)}`);
}

export function handleState<T>(state: AsyncState<T>): string {
  switch (state.status) {
    case "idle": return "Waiting...";
    case "loading": return "Loading...";
    case "success": return `Done: ${JSON.stringify(state.data)}`;
    case "error": return `Failed: ${state.error.message}`;
    default: return assertNever(state);
  }
}
```

### Step 4: Type Narrowing & `satisfies` Operator
- Use the `satisfies` operator to validate that an object conforms to a contract without widening literal types or losing autocomplete:
  ```typescript
  const config = {
    endpoint: "https://api.prumo.dev",
    retries: 3,
  } satisfies Record<string, unknown>;
  ```
- Narrow unknown types with user-defined type guards (`val is T`) or `typeof`/`instanceof` checks.

### Step 5: Static Analysis & Test Verification
1. Run `tsc --noEmit` across the entire project.
2. Run `eslint . --max-warnings=0`.
3. Run `vitest run` or `jest`.

---

## 6. Decision Rules & Invariants
- **RULE 1 (Zero `any`)**: The `any` type is completely prohibited. Unknown input must be typed as `unknown` and validated.
- **RULE 2 (No Non-Null Assertions)**: The non-null assertion operator `!` is forbidden in production code. Use optional chaining (`?.`), nullish coalescing (`??`), or explicit assertions (`assert(x !== undefined)`).
- **RULE 3 (No Silent Suppressions)**: `@ts-ignore` and `@ts-nocheck` are prohibited. If testing compiler diagnostic failures, use `@ts-expect-error` with a descriptive comment explaining the expected compiler error.
- **RULE 4 (Index Access Soundness)**: With `noUncheckedIndexedAccess: true`, array index accesses (`arr[i]`) return `T | undefined`. Always verify element existence before property access.

---

## 7. Evidence Required
- **Compiler Evidence**: `tsc --noEmit` completes with 0 errors under strict settings.
- **Linter Evidence**: ESLint reports 0 warnings with strict type-checking rules.
- **Boundary Test Evidence**: Unit tests proving invalid payload inputs are rejected at runtime with schema validation errors.

---

## 8. Output Contract
- Sound TypeScript source files (`.ts`, `.tsx`) with explicit type declarations.
- Fully configured `tsconfig.json` enforcing strict compiler invariants.
- TypeScript Verification Report (`templates/typescript-verification-report.md`).

---

## 9. Stop Conditions
- `tsc --noEmit` passes with 0 diagnostics.
- All boundary validation tests execute successfully.
- Token budget exhausted.
- Blocked on external dependency.

---

## 10. Escalation Rules
- Escalate immediately if an untyped legacy third-party dependency requires writing custom declaration files (`.d.ts`) that cannot be verified automatically.
- Escalate to tech lead if a library's generic types cause compiler recursion limits or excessive compile times ($> 30\text{s}$).
