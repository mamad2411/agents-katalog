---
name: vendor-type-dedup
description: Deduplicate TS types between vendored upstream and client.
license: MIT
metadata:
  hermes:
    tags:
    - typescript
    - vendor
    - dedup
    - migration
    related_skills: []
  source_frontmatter:
    version: 1.0.0
    author: hermes-agent
  imported_from: hermes
---

# Vendor Type Deduplication

When a project vendors upstream source code and defines its own types that overlap with upstream exports, use this skill to systematically deduplicate.

## When to Use

- Project has `vendor/` with upstream TypeScript source
- Local type files re-implement upstream types
- Vendor rev upgrades cause silent protocol drift
- Need to import types from vendor packages in nested workspaces

## Core Strategy: D→C Boundary Migration

Don't choose between "keep all local" (A) and "re-export everything" (C). Use boundary-based migration:

```
Protocol boundary types → re-export upstream (exact)
Application domain types → keep local (ergonomic)
```

Decision rule: **does this type belong to the wire protocol or to the application domain?**

| Protocol (re-export) | Application (keep local) |
|-----------------------|--------------------------|
| RPC envelope types | UI message types |
| Frame unions | Session state |
| Branded IDs (via factory) | Domain-specific DTOs |
| Error codes | Webview bridge types |

## Phase Checklist

**Before each phase**: Write a detailed prompt to `docs/chatgpt-prompt-m<phase>-<topic>.md` with exact type definitions and specific questions. Get ChatGPT confirmation before executing. This catches architectural mistakes (e.g. creating unnecessary adapter layers, modifying upstream classes) before code changes. See `references/migration-phase-prompts.md` for templates.

### Phase 1: Infrastructure
1. Add tsconfig paths pointing to vendor source `.ts` files
2. Add esbuild alias (matching tsconfig paths) to build config
3. Add `allowImportingTsExtensions: true` to tsconfig (upstream uses `.ts` extension imports)
4. Verify typecheck passes

### Phase 2: Safe Re-exports + Factory
1. Identify types with ZERO compatibility issues (no branded fields, no generic mismatch, no discriminated union conflict)
2. Re-export those from upstream
3. Create factory functions for branded types (e.g. `createRpcId()`)
4. Centralize construction sites to use factories

### Phase 3: Union Boundary Split
1. Split combined switch handlers into per-union handlers
2. Define union composition types if needed (e.g. `type IncomingFrame = MuxFrame | HostFrame`)

### Phase 4: Exact Union Migration
1. Re-export upstream discriminated unions (e.g. `SessionEvent`, `SessionEventMap`)
2. Update consumers to use narrowing (`switch (event.type)` auto-narrows `event.data`)
3. Remove old loose types

### Phase 5: Generic Alignment (No Adapter Layer)
1. Re-export upstream non-generic wire types (`ClientRequest`, `ServerResponse`, `ServerRequest`) — do NOT create `TypedClientRequest<P>` adapters
2. Wire types carry `unknown` payload/result — this is correct wire-level semantics
3. Keep generics ONLY at business function signatures: `request<T>()` returns `RpcResult<T>`
4. At extraction boundary, cast: `parseServerResponse(text).result as RpcResult<T>`
5. `rpc.ts` local types (e.g. `RpcEnvelope`, webview-side `RpcResult`) stay local if they serve a different abstraction layer (webview vs extension process)

**Why no TypedXxx adapters**: If no call site actually uses `ClientRequest<SomeSpecificPayload>` (all构造都是 `payload: unknown`), the generic adds no value. Upstream's non-generic type is the correct wire-level representation. Generics belong at the business API boundary, not the wire type.

## Compatibility Pre-Check

Before re-exporting any upstream type, verify:

| Check | Fail means |
|-------|-----------|
| No branded fields used as plain `string` | Need factory or adapter |
| No generic vs non-generic mismatch | Usually OK — wire types stay non-generic, generics at business function level only |
| No discriminated union conflicting with `switch/default:break` | Need union split first |
| Shape fields match (same names, same types) | Keep local or adapter |
| `readonly` modifiers compatible | Usually OK (readonly assignable to mutable) |

## Branded Type Consumption Patterns

When upstream re-exports a discriminated union containing branded fields (e.g. `SessionId = string & { readonly [BRAND]: 'SessionId' }`):

**Source code is usually safe without changes:**
- `typeof frame.sessionId !== 'string'` → works (branded string IS a string at runtime)
- `someMethod(frame.sessionId)` where param is `string` → works (branded is subtype of string)
- `Map<string, ...>.get(frame.sessionId)` → works (string key accepts branded)
- Only breaks when you try to assign plain string TO branded: `'s1' as SessionId` needed

**Test construction sites always break:**
- `{ sessionId: 's1' }` in inline MuxFrame literals → TS error: `Type 'string' is not assignable to type 'SessionId'`
- Fix: import the branded type's factory function and wrap: `{ sessionId: SessionId('s1') }`
- Factory is zero-cost compile-time cast (no runtime overhead)

**Diagnostic shortcut:** `npx tsc --noEmit 2>&1 | grep -i '<BrandName>'` isolates branded-type errors from unrelated noise (SessionEvent mismatches, argument count errors, etc.)

**Scope discipline:** branded type fixes are narrow — only construction sites and explicit `=== string` comparisons that TypeScript treats as always-true. Don't expand to `Map<SessionId, ...>` or change function signatures unless the full migration phase calls for it.

## References

- `references/session-event-boundary-cast.md` — Full error transcripts + fix pattern for upstream SessionEvent → local SessionEvent boundary casting, including test fixture patterns and subagent coordination pitfalls.
- `references/migration-phase-prompts.md` — ChatGPT prompt templates for each migration phase (M3-M6), including decision questions and expected answers.
- `templates/vitest.config.ts` — Starter vitest config with upstream package aliases mirroring tsconfig paths. Adapt package paths to your project.

## Pitfalls

- **`.ts` extension imports**: Upstream source uses `from './foo.ts'`. TypeScript requires `allowImportingTsExtensions` + `noEmit` in tsconfig.
- **Nested pnpm workspace**: Vendor packages NOT in outer `node_modules`. MUST use tsconfig paths + esbuild alias. Cannot add as npm dependency.
- **Branded type downgrade**: Never `type RpcId = string` to fix incompatibility. This destroys the compile-time boundary. Use factory pattern instead. See "Branded Type Consumption Patterns" above for what actually breaks and the fix pattern.
- **RpcResult pulls RpcError**: Upstream `RpcResult<T>` references upstream `RpcError` (discriminated union ~40 codes). Re-exporting brings the discriminated union — conflicts with local loose `{code: string}`.
- **Cross-union switch**: If switch on `MuxFrame` handles `host/agent-error`, that's a `HostFrame` variant. Split the handler.
- **@ts-expect-error format**: Use `// @ts-expect-error UPSTREAM-MIGRATION(TypeName): reason`. Never `@ts-ignore`. Labels are searchable: `rg "UPSTREAM-MIGRATION" src/`.
- **Consumer narrowing**: Upstream `SessionEvent<'turn/end'>` has `data.reason: TurnEndReason` (discriminated union), not `string`. Consumers narrow via `switch (event.type)` — no manual assertion needed.
- **Vitest can't resolve tsconfig paths**: `tsconfig.json` `paths` works for `tsc --noEmit` but vitest uses vite's resolver which ignores them. Test files that `import { Foo } from '@vendor-pkg/types'` will typecheck green but fail at vitest runtime with "Cannot find package". Workaround: use `as unknown as` casts in tests, or add a vitest `resolve.alias` in `vitest.config.ts` mirroring the tsconfig paths.
- **Dead event-type branches**: When upstream `SessionEvent` becomes a precise discriminated union (no longer `type: string`), any `if (event.type === 'session/title')` or similar for types NOT in the upstream union becomes a compile error — comparison always false, body narrowed to `never`. These dead paths must be removed. Often the feature works differently in upstream (e.g., titles ride `session/projection` frames, not a dedicated event type).
- **Test fixtures for branded fields**: Upstream `JobView.id` is branded `JobId`, not `string`. Test object literals like `{ id: 'bash-1' }` fail. Fix: `'bash-1' as unknown as JobView['id']` or import the branded factory `JobId('bash-1')`.
- **Test helpers for mapped union types**: When `MuxFrame.event` carries upstream `SessionEvent` (a complex mapped type over `SessionEventMap`), you can't trivially construct matching objects. The pattern: write an `ev()` helper that accepts partial fields and casts via `as unknown as SessionEvent`. Callers also need `as unknown as MuxFrame` on frame literals since inline objects don't satisfy the discriminated union.
- **Boundary cast → local variable**: When casting `frame.event` at the upstream→local boundary, extract to a local variable once: `const localEvent = frame.event as unknown as SessionEvent;` then use `localEvent` throughout the case block. Avoids repetitive casts and makes the boundary explicit in code review.
- **Subagent coordination on shared type files**: When multiple subagents work on vendor dedup simultaneously, **each subagent MUST modify a DIFFERENT file**. If two agents modify `wire.ts` simultaneously, they produce conflicting changes (one removes local types while another adds casts against them). **Rule**: before dispatching parallel subagents, assign each a unique target file. If a phase requires modifying the same file (e.g. wire.ts re-export + consumer adaptation), serialize: do the re-export first (single agent), then dispatch parallel agents for consumer adaptation in different files. If parallel execution is mandatory for the same file, use worktree isolation.
- **Patch tool false-positive on concurrent edits**: The `patch` tool can report a successful diff output while the actual file on disk reverts. This happens when another process (LSP auto-save, parallel subagent, formatter) modifies the file between the read and write of a `patch` call. The `patch` tool's diff is computed against a stale snapshot, so the replacement lands against old content and gets overwritten. **Diagnostic**: if `tsc --noEmit` still shows errors the patch was supposed to fix, re-read the file to confirm the change persisted. **Fix**: use `write_file` with the full corrected file content instead of targeted `patch` edits when the file is under concurrent modification, or `execute_code` with the `patch()` helper which re-reads before writing.
- **`verbatimModuleSyntax` re-export pattern**: When tsconfig has `"verbatimModuleSyntax": true` (common in ESM strict projects), `export type { X } from '...'` does NOT make `X` available in the local module scope — it only re-exports. Any local code referencing `X` (e.g. `SessionHistoryResponse.events: Array<{ event: SessionEvent }>`) will error `TS2304: Cannot find name`. **Fix**: use a two-step pattern:
  ```typescript
  import type { X, Y } from '@vendor-pkg/types'
  export type { X, Y }
  ```
  This imports into local scope (for use in this file) AND re-exports (for consumers). Single `export type` re-exports are only correct when nothing in the same file references the type locally.
- **Non-generic wire types + generic business functions**: When upstream wire types are non-generic (`ClientRequest` with `payload: unknown`) but business functions need typed responses (`request<T>()` returns `RpcResult<T>`), remove generics from wire parsing functions and cast at the extraction boundary:
  ```typescript
  // Wire function: non-generic
  parseServerResponse(text): ServerResponse { ... }
  // Business function: generic via cast
  async request<T>(method: string, payload: unknown): Promise<RpcResult<T>> {
    return parseServerResponse(await res.text()).result as RpcResult<T>;
  }
  ```
  Don't create `TypedClientRequest<P>` / `TypedServerResponse<T>` adapter types — they add complexity without value if no call site uses the request generic.
- **Transport convergence: wrapper not replacement**: When replacing local transport (e.g. `runtime.ts`) with upstream (`ConnectionController`), don't modify the upstream class. Create a thin adapter/wrapper that handles host-specific semantics (rebase, multi-subscribe, status snapshot, connect-Promise lifecycle). The wrapper should implement the same interface as the old local class so callers don't change.
- **Shared file split for multi-runtime code**: When a file (e.g. `rpc.ts`) serves both extension process and webview, split during migration: keep webview-side code in `webview/rpc.ts`, replace extension-side with upstream API client. Don't leave a shared file that mixes both abstractions.
- **Vendor barrel export for missing classes**: When upstream packages don't export a class you need to subclass (e.g. `WebApiClient` was internal in `@deepseek-ai/dsh-client-connection/client`), add the export to the vendor barrel file (`packages/.../src/client/index.ts`). This is a non-breaking additive change but **must be re-applied when vendor rev bumps**. Track in dedup plan checkboxes. The vendor change is in a git submodule — `git add` will fail with "Pathspec is in submodule". Commit only the extension-side files; note the vendor barrel change in the commit message.
- **Runtime deletion pattern**: When deleting a local transport module (e.g. `runtime.ts`, `rpc.ts`), first inline its helper functions into remaining consumers (e.g. `bootstrap.ts`), then delete. Check for test file imports before deleting — `grep -rn "from.*<module>" src/ test/` to find all references.

## Parallel Subagent Execution

User prefers parallel subagents for migration phases, with **separate commits per subagent**. Key rules:
1. **Assign each subagent a DIFFERENT file** — never two agents modifying the same file
2. Each subagent commits independently before returning
3. If a phase requires modifying one file first (e.g. wire.ts re-export), do that with a single agent, then dispatch parallel agents for consumer adaptation in different files
4. After all subagents return, verify `tsc --noEmit` passes and commit any remaining fixes

