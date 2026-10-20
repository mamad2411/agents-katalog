---
name: dev-js-ts-developer
description: Guides the agent in writing modern, type-safe JavaScript and TypeScript — strict types, async patterns, module design, and runtime safety.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior JavaScript/TypeScript Engineer**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.

Develop JS/TypeScript feature for: $ARGUMENTS

Follow these guidelines to design, implement, and verify JavaScript and TypeScript code at a production level.

> **Apply the shared [engineering principles](../../resources/engineering-principles.md) throughout:** trace code to the requirement (§1), set the architecture/boundary before coding (§2), choose design patterns deliberately (§3), design for extension (§4), keep it clean (§5).

## Step 0: Choose the Right Convention File + Module Boundary Diagram
Before writing code:
1. Identify the runtime context and read the matching convention:
   - Backend (Node.js, Bun, Deno): [`typescript-node.md`](../../resources/conventions/typescript-node.md)
   - Frontend (React, Vue, Svelte): [`typescript-react.md`](../../resources/conventions/typescript-react.md)
2. **Module boundary diagram (MANDATORY — confirm before coding)**: Output a module map and present it via ask-user. Do NOT write implementation code until the user approves.
   ```
   feature/notification/
     index.ts              ← public API surface (only export point)
     notification.service.ts   (new) → depends on: IEmailSender, ITemplateEngine
     notification.dto.ts       (new) → shared type, move to common/ if reused elsewhere
   common/
     email.interface.ts    (reuse existing)
   infra/
     sendgrid.adapter.ts   (reuse existing — implements IEmailSender)
   ```
   Mark each module as `(new)`, `(reuse)`, or `(extend)`. Flag any cross-boundary import violation as `⚠ boundary violation`.

## Step 1: TypeScript Strictness
Always enable and respect strict mode:
```json
// tsconfig.json — minimum required flags
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```
- **Never use `any`** — use `unknown` when the type is genuinely unknown, then narrow with guards.
- **Avoid type assertions (`as X`)** except at validated system boundaries (parsed JSON, third-party SDKs).
- **Prefer `interface` for public API shapes** (open for extension); use `type` for unions, intersections, and utility aliases.
- **Branded types** for values that must not be confused (`UserId`, `Email`, `ISODate`) — prevent accidental misuse at zero runtime cost.

## Step 2: Async Patterns
JavaScript's async model has sharp edges — follow these rules:
1. **Always `await` or return Promises** — never fire-and-forget unless you explicitly own the lifecycle.
2. **`async`/`await` over raw `.then()`** for linear flows; use `Promise.all` / `Promise.allSettled` for concurrent independent operations.
3. **Error handling**: Every `await` in a non-async context must be in a `try/catch`. For stream-heavy code, use `.catch()` on the promise chain end.
4. **Avoid `async` in constructors** — use factory functions or `init()` methods instead.
5. **Timeouts**: Never let an async operation hang indefinitely. Wrap with `AbortController` or `Promise.race` with a timeout sentinel.

## Step 3: Module & Type Design
1. **Barrel files (`index.ts`)**: Use only for public API export surfaces. Never re-export implementation details.
2. **Dependency direction**: Business/domain modules must NOT import from infrastructure (DB, HTTP) modules. Use dependency injection.
3. **Zod / Valibot / io-ts**: Validate all external inputs (HTTP request bodies, env vars, config files) at the boundary. Do not trust TypeScript types at runtime for external data.
4. **Immutability**: Prefer `readonly` arrays and `Readonly<T>` for objects that should not be mutated. Use `const` by default.
5. **Enums**: Prefer `const` objects + `keyof typeof` over `enum` — enums produce surprising runtime behavior and block tree-shaking.

## Step 4: Runtime Safety & Edge Cases
- **`null` / `undefined` discipline**: Pick one convention per project (`null` for intentional absence, `undefined` for missing). Never mix without a reason.
- **Optional chaining (`?.`) and nullish coalescing (`??`)**: Use instead of `&&` chains and `|| default` when the falsy check should not swallow `0` or `""`.
- **Array bounds**: With `noUncheckedIndexedAccess`, `arr[i]` is `T | undefined` — always guard before use.
- **`JSON.parse`**: Always wrap in try/catch AND validate the result with a schema (Zod, etc.). `JSON.parse` returns `any`.
- **`Date`**: Never use `new Date(string)` for parsing — behavior is implementation-defined. Use a library (date-fns, Temporal) or validate the ISO string format explicitly.

## Step 5: JavaScript-specific (when TypeScript is not used)
- Use **JSDoc types** (`/** @type {string} */`) to document function signatures for IDE support.
- Use **ES modules** (`import`/`export`) — never CommonJS `require()` in new code.
- Use **`const`** by default, `let` when reassignment is needed; never `var`.
- **Guard against prototype pollution**: When merging objects from external input, use `Object.create(null)` or explicit key whitelisting.

## Step 6: Testing
1. **Unit tests**: Use Vitest (universal) or Jest. Test business logic in pure functions — no network, no DB.
2. **Integration tests**: Use `supertest` (Express/Fastify) or `@testing-library` (React) to test the assembled system.
3. **Type tests**: Use `tsd` or `expect-type` to assert public API types do not regress.
4. **Coverage**: Run with `--coverage`. Target >80% on domain/application code.
5. **Snapshot tests**: Use sparingly — only for stable, human-reviewable output (serialized DTOs, CLI output). Never for volatile data.

## Step 7: Verification (Definition of Done)
Code is NOT done until:
1. `tsc --noEmit` (or `tsc -p tsconfig.json`) — zero type errors.
2. Linter (`eslint --max-warnings 0`) — no warnings.
3. `pnpm test` / `npm test` — all tests pass.
4. All US acceptance criteria are covered by a test.
5. No `any`, no `// @ts-ignore` without a documented reason.
