---
name: integrate-api-client
description: Connect frontend code to backend APIs by following the repo's request, caching, auth, error-handling, and state-management patterns. Use when a UI needs to read or mutate backend data.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, run_dev_server, execute_command]
---

# Integrate API Client

Use this skill when frontend code needs to call a backend API or when an existing integration must change.

## When to Use

- a UI needs to read backend data
- a UI needs to mutate backend state
- wiring auth, caching, or error handling for API calls
- following the repo's client/state patterns
- **Orval OpenAPI codegen pipeline**
- **React 19 `use()` for RSC streaming + TanStack Query for client**
- **React 19 `useActionState` for forms + `useMutation` for complex**
- **Streaming AI responses with `ReadableStream` + `useReducer`**

## Core Rules

- reuse the repo's existing data-fetching and mutation pattern
- keep transport details out of presentational components when possible
- make loading, error, and retry behavior explicit
- preserve auth and sensitive-data handling rules
- enforce type safety between API contract and frontend usage — use Zod schemas, generated types (Orval, openapi-typescript), or repo-local pattern; do not use untyped API responses
- avoid duplicated request logic when a shared client already exists
- for TanStack Query v5 codebases: centralize query keys and fetchers in `queryOptions` factories — scattered magic string query keys are an anti-pattern
- for optimistic mutations: implement the full lifecycle — `onMutate` (cancel in-flight queries + snapshot + update), `onError` (rollback from snapshot), `onSettled` (invalidate) — optimistic updates without rollback handlers are prohibited
- use functional updater syntax in `setQueryData((old) => ...)` to prevent stale state captures
- server state must stay in the query cache; do not duplicate server responses in local `useState`
- if any code in this change was AI-generated, validate it per the risk tier defined in the frontend-developer role before accepting
- **Stack-Adaptive Type-Safe Contract Pipeline**: match the repo's transport layer — use Orval (`OpenAPI -> TanStack Query v5 + MSW v2 + TS types`) when an OpenAPI spec exists, or tRPC / GraphQL codegen / typed Server Actions + Zod when matching the repo; never force Orval onto non-OpenAPI stacks or leave responses untyped
- **React 19 `use()` vs Client Query Cache**: read promises with `use()` in Server Components when RSC applies; use TanStack Query (`queryOptions` factories) for interactive client caching, background refetch, and deduplication
- **Form Actions vs Complex Mutations**: prefer React 19 `useActionState` + server validation for standard form submissions, and `useMutation` for cache-heavy/optimistic mutations
- **Streaming AI responses**: `ReadableStream` + `TextDecoderStream` + `useReducer` + `AbortController` cancellation hooks

## Suggested Process

### 1. Inspect Existing API Usage

Find how the repo currently handles:

- request construction
- auth headers or session context
- caching or stale-data behavior
- error normalization
- optimistic updates or invalidation

### 2. Define The Data Contract

Clarify:

- endpoint or operation used
- request payload
- response shape
- error cases the UI must handle
- whether the call is query, mutation, or streaming-like behavior

### 3. Add Or Update The Client Layer

Implement the narrowest useful integration:

- client helper or hook
- request serialization
- response mapping
- cache key or invalidation logic when the repo uses it

### 4. Connect The UI

Wire the integration into the right layer:

- page-level loader
- container or view-model layer
- mutation handler
- form submit or interaction callback

### 5. Check State And Failure Behavior

Verify:

- loading states are visible
- retries are appropriate
- stale data is invalidated correctly
- failure messages are useful but safe
- auth expiration or permission failures are handled intentionally

### 6. Add Tests

Use skill: `frontend-testing`

Cover:

- success path
- API failure path
- loading state
- mutation side effects or cache updates

## 2026 API Integration Standards

### Orval OpenAPI Codegen Pipeline

- Configure Orval as the code generation pipeline to automatically convert OpenAPI specifications into TanStack Query v5 queries, MSW (Mock Service Worker) mocks, and TypeScript types.
- Leverage the queryOptions pattern to write reusable, type-safe query configurations across components.
- Ensure that MSW mocks are updated and run in test and development environments when schemas change.

### React 19 use() vs TanStack Query

- Use React 19's `use()` hook to read promises directly in Server-rendered components, facilitating React Server Component (RSC) streaming and lazy data resolution.
- Keep TanStack Query for interactive client-side operations that require cache invalidation, background refetching, or request deduplication.
- Avoid nesting client-side query hooks when RSC-based streaming can resolve initial page load data.

### React 19 useActionState for Mutations

- Utilize React 19's `useActionState` hook for handling straightforward form actions and state updates.
- Keep `useMutation` from TanStack Query for complex mutations that require advanced cache manipulation, pagination updates, or optimistic UI responses.
- Ensure validation errors returned from actions are correctly bound back to the UI inputs.

### Streaming AI Responses

- Handle streaming responses using `ReadableStream` and `TextDecoderStream` to parse chunked responses.
- Implement token-by-token UI updates via a `useReducer` pattern to avoid unnecessary re-renders during rapid stream updates.
- Provide clear cancellation hooks to allow users to abort active stream requests.

## Checklist

- [ ] local data-fetching pattern reviewed
- [ ] Repo-aligned type-safe contract pipeline active (Orval for OpenAPI, or tRPC/GraphQL/Zod Server Actions)
- [ ] `queryOptions` factories used when TanStack Query v5 is active (no magic string keys)
- [ ] Server-rendered initial data hoisted to RSC `use()` / route loaders where applicable; client cache used for interactivity
- [ ] Standard form mutations use `useActionState` / native form actions; complex cache/optimistic mutations use `useMutation` (`onMutate`/`onError`/`onSettled`)
- [ ] Functional updater syntax: `setQueryData((old) => ...)` — no stale captures
- [ ] Server state stays in query cache; no `useState` duplication
- [ ] Streaming AI responses: `ReadableStream` + `TextDecoderStream` + `useReducer`
- [ ] Cancellation hooks for active streams (`AbortController`)
- [ ] Validation errors from actions bound to UI inputs
- [ ] MSW v2 mocks auto-generated and updated with Orval pipeline
- [ ] Idempotency keys on every non-idempotent mutation (POST/DELETE)
- [ ] Explicit error code handling (4xx vs 5xx differentiated)
- [ ] tests added or updated
- [ ] `implementation-result.json` emitted

## Failure Modes

- **API client widens auth scope**: the client requests a token scope broader than the feature needs. Mitigation: validate every client against the feature's declared auth scope; reject clients that request broader scopes.
- **AI-suggested client widens dependency surface**: an AI-suggested client pattern imports libraries outside the feature's interface. Mitigation: validate AI-generated code against the feature's narrow interface; reject patterns that deviate.
- **Client retries non-idempotent mutations**: a POST or DELETE is retried without an idempotency key. Mitigation: require an explicit idempotency key on every non-idempotent mutation; reject retries without the key.
- **Client ignores error codes**: the client treats 4xx and 5xx identically. Mitigation: require explicit handling for every documented error code; reject clients that lump error codes together.
- **Orval spec drift**: OpenAPI spec changes but generated code not updated. Mitigation: CI step running Orval; fail if generated code differs from committed.
- **RSC/TanStack Query boundary confusion**: client query hooks nested in Server Components. Mitigation: lint rule banning `useQuery` in `"use client"` components that are RSC children; use `use()` in RSC.
- **`useActionState` for complex mutations**: simple form hook used for paginated cache updates. Mitigation: lint rule: `useActionState` only for forms; `useMutation` for cache manipulation.
- **Streaming re-render storm**: `useState` updated per token. Mitigation: `useReducer` pattern; batch updates; `React.startTransition` for non-urgent.
- **Missing cancellation**: user cannot abort slow AI stream. Mitigation: `AbortController` wired to cancel button; cleanup on unmount.
- **Stale state capture**: `setQueryData(newData)` captures stale closure. Mitigation: functional updater `setQueryData((old) => ...)` mandatory.
- **MSW mock divergence**: mocks not updated with schema changes. Mitigation: Orval generates MSW handlers; CI verifies mocks match spec.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: change_summary, files_touched[], and validation_run. Set produced_by_role to the emitting developer role. Include: Orval config, `queryOptions` factories, RSC/Client boundary, streaming handler, cancellation infrastructure.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: API clients must follow least-privilege auth scopes; reject requests with unscoped tokens.
- **ASI05 RCE Guard**: never construct API payloads, headers, or auth tokens from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the client contract is consumed by frontend and backend roles; emit a structured spec so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the client as "secure" without the actual auth and error-handling gates; surface the residual risk.

## Related Skills

- **add-page-route**: Place the data integration into route flow
- **add-ui-component**: Render the integrated state in reusable UI
- **frontend-testing**: Add coverage for network-driven states
- **review-code**: Review data flow, auth, and error handling risk
- **commit-code**: Prepare the integration for delivery
- **develop-mobile-app**: Connect mobile clients with offline-first persistence (MMKV, WatermelonDB) and NetInfo synchronization
- Companion reference: `references/orval-tanstack-query-and-streaming-specs.md`
- Companion example: `examples/orval-query-and-streaming-mutation.ts`

Last updated: 2026-11-08