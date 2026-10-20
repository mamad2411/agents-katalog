---
name: volcano-typescript
description: "Canonical TypeScript type definitions for the Volcano SDK: User, Session, AuthResponse, QueryBuilder, StorageObject, Realtime, Durable, and durable approval types, Function invocation generics, OAuth providers, middleware types, and utility types."
---
# Volcano TypeScript Types Skill

## Role
Provide the canonical TypeScript type definitions for every Volcano SDK surface. Use this skill whenever a task needs a precise type — including return shapes for auth/db/storage/realtime/functions, query builder generics, and middleware contracts. The SDK ships these types alongside the runtime, so `import type { ... } from '@volcano.dev/sdk'` works at compile time without any extra package.

## When to use
- Defining application data models that will go through `volcano.from<T>(...)` or `insert<T>(...)`.
- Reading or destructuring auth responses (`signIn`, `signUp`, `getUser`, `getSessions`).
- Typing realtime event handlers (`PostgresChange`, `PresenceState`).
- Typing function invocations with `invoke<P, R>(...)`.
- Typing durable handlers, contexts, and execution results.
- Writing middleware helpers that consume `getUser(token)` or `refreshToken(...)`.

## Importing
```ts
import { VolcanoAuth } from '@volcano.dev/sdk';
import type {
  User,
  Session,
  AuthResponse,
  UserResponse,
  SessionResponse,
  VolcanoAuthConfig,
} from '@volcano.dev/sdk';
```

## Core Types

### Configuration
```ts
interface VolcanoAuthConfig {
  /** API URL (defaults to https://api.volcano.dev) */
  apiUrl?: string;
  /** Project anon key (required) */
  anonKey: string;
  /** Access token for server-side use */
  accessToken?: string;
  /** Refresh token for server-side use */
  refreshToken?: string;
}
```

### User
```ts
interface User {
  id: string;
  email: string;
  user_metadata?: Record<string, JsonValue>;
  created_at: string;
  updated_at: string;
}
```
The `id` is the Volcano auth user_id; use it as the foreign key in your `users` application table.

### Session
```ts
interface Session {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}
```

### Auth response shapes
```ts
interface AuthResponse {
  user: User | null;
  session: Session | null;
  error: Error | null;
}

interface UserResponse {
  user: User | null;
  error: Error | null;
}

interface SessionResponse {
  session: Session | null;
  error: Error | null;
}
```
Returned from `signUp`, `signIn`, `getUser`, `refreshSession`, etc. Always check `error` before consuming `user`/`session` — they are `null` when `error` is set.

## Database Types

### Typed query results with generics
```ts
interface Post {
  id: string;
  title: string;
  content: string;
  status: 'draft' | 'published' | 'archived';
  user_id: string;
  created_at: string;
}

const { data, error } = await volcano
  .from<Post>('posts')
  .select('*')
  .eq('status', 'published');

if (data) {
  data.forEach(post => {
    // TypeScript knows post.title is string
    // and post.status is the union literal type
  });
}
```

### Insert / update with generics
```ts
const { data, error } = await volcano
  .insert<Post>('posts', {
    title: 'New Post',
    content: 'Content here',
    status: 'draft',
  });

const { data: updated } = await volcano
  .update<Post>('posts', { status: 'published' })
  .eq('id', postId);
```
TypeScript validates the partial shape against `Post`.

### QueryBuilder<T> contract
```ts
interface QueryBuilder<T> {
  select(columns: string): QueryBuilder<T>;
  eq(column: string, value: FilterValue): QueryBuilder<T>;
  neq(column: string, value: FilterValue): QueryBuilder<T>;
  gt(column: string, value: FilterValue): QueryBuilder<T>;
  gte(column: string, value: FilterValue): QueryBuilder<T>;
  lt(column: string, value: FilterValue): QueryBuilder<T>;
  lte(column: string, value: FilterValue): QueryBuilder<T>;
  like(column: string, pattern: string): QueryBuilder<T>;
  ilike(column: string, pattern: string): QueryBuilder<T>;
  is(column: string, value: null): QueryBuilder<T>;
  in(column: string, values: FilterValue[]): QueryBuilder<T>;
  order(column: string, options?: { ascending?: boolean }): QueryBuilder<T>;
  limit(count: number): QueryBuilder<T>;
  offset(count: number): QueryBuilder<T>;
  execute(): Promise<QueryResult<T>>;
}

interface QueryResult<T> {
  data: T[] | null;
  error: Error | null;
  count?: number;
}
```
The chain auto-resolves on `await` — you rarely need to call `.execute()` explicitly. `count` populates only when the query/result mode supports it.

## Storage Types
```ts
interface StorageObject {
  id: string;
  bucket_id: string;
  name: string;
  owner_id?: string;
  is_public: boolean;
  size: number;
  mime_type: string;
  etag?: string;
  metadata?: Record<string, JsonValue>;
  created_at: string;
  updated_at: string;
  public_url?: string;
}

interface StorageUploadOptions {
  contentType?: string;
}

interface StorageUploadResponse {
  data: StorageObject | null;
  error: Error | null;
}

interface StorageDownloadResponse {
  data: Blob | null;          // Blob in browser; convert with Buffer.from(await blob.arrayBuffer()) in Node
  error: Error | null;
}

interface StorageListResponse {
  data: StorageObject[] | null;
  error: Error | null;
  nextCursor: string | null;  // null on the final page
}
```

### Usage
```ts
const storage = volcano.storage.from('avatars');

const { data, error }: StorageUploadResponse = await storage.upload(
  'user/avatar.jpg',
  file,
  { contentType: 'image/jpeg' }
);

const { data: blob }: StorageDownloadResponse = await storage.download('user/avatar.jpg');

const { data: files, nextCursor }: StorageListResponse = await storage.list('user/', {
  limit: 100,
});
```

## Realtime Types
Import realtime types from the realtime module:
```ts
import { VolcanoRealtime, RealtimeChannel } from '@volcano.dev/sdk/realtime';
import type {
  PostgresChange,
  PresenceState,
  ConnectContext,
  DisconnectContext,
  ErrorContext,
  RealtimeConfig,
  ChannelOptions,
  WebSocketConstructor,
} from '@volcano.dev/sdk/realtime';
```

### Realtime configuration
```ts
interface RealtimeConfig {
  apiUrl: string;
  anonKey: string;
  accessToken?: string;
  getToken?: () => Promise<string>;
  volcanoClient?: VolcanoAuth;
  fetchConfig?: FetchConfig;
  webSocket?: WebSocketConstructor;
}

interface ChannelOptions {
  type?: 'broadcast' | 'presence' | 'postgres';
  autoFetch?: boolean;
  fetchBatchWindowMs?: number;
  fetchMaxBatchSize?: number;
}
```

### Event contexts
```ts
interface ConnectContext {
  client?: string;
  latency?: number;
}

interface DisconnectContext {
  code?: number;
  reason?: string;
  reconnect?: boolean;
}

interface ErrorContext {
  error?: Error;
  message?: string;
  code?: number;
}
```

### Postgres changes
```ts
interface PostgresChange {
  table: string;
  schema: string;
  type: 'INSERT' | 'UPDATE' | 'DELETE';
  record?: Record<string, unknown>;       // present on INSERT/UPDATE
  old_record?: Record<string, unknown>;   // present on UPDATE/DELETE
  columns?: string[];                     // changed columns, UPDATE only
  timestamp: string;
}
```

### Typed postgres listeners
```ts
interface Message {
  id: string;
  content: string;
  user_id: string;
  created_at: string;
}

channel.onPostgresChanges('INSERT', 'public', 'messages', (change: PostgresChange) => {
  const message = change.record as Message;
  // ...
});
```
The callback's `change.record` is `Record<string, unknown>`; cast to your row type at the boundary.

### Presence
```ts
interface PresenceState {
  [clientId: string]: Record<string, unknown>;
}

interface UserPresence {
  user_id: string;
  username: string;
  status: 'online' | 'away' | 'busy';
}

channel.onPresenceSync((state: PresenceState) => {
  const users = Object.values(state) as UserPresence[];
  // ...
});
```

## Functions Types

### Typed invocation with payload + response generics
```ts
interface InvokeParams {
  userId: string;
  action: 'fetch' | 'update' | 'delete';
}

interface InvokeResult {
  success: boolean;
  data?: Record<string, unknown>;
  message?: string;
}

const { data, error } = await volcano.functions.invoke<InvokeParams, InvokeResult>(
  'process-user',
  { userId: '123', action: 'fetch' }
);

if (data) {
  // TypeScript knows data.success is boolean, data.message is string | undefined
}
```
The full return tuple from `invoke<P, R>(...)` is `{ data: R | null; status: number; headers: Record<string, string>; version: string; error: Error | null }`.

## Durable Function Types

Authoring types come from the durable entry point:

```ts
import { durable, type DurableContext, type DurableHandler } from '@volcano.dev/sdk/durable';

interface OrderInput {
  order_id: number;
}

interface OrderResult {
  order_id: number;
  outcome: 'shipped' | 'refunded';
}

const run: DurableHandler<OrderInput, OrderResult> = async (input, ctx) => {
  const order = await ctx.step('load', () => loadOrder(input.order_id));
  await ctx.wait('settle', '30s');
  return { order_id: order.id, outcome: 'shipped' };
};

export const handler = durable(run);
```

`DurableContext`, `StepOptions`, `WaitUntilOptions`, `BatchOptions`,
`BatchResult`, `Retry`, and `DurableDuration` describe authoring. Execution
client types come from the main entry point:

```ts
import type { DurableExecution, DurableExecutionStatus } from '@volcano.dev/sdk';

const status: DurableExecutionStatus = 'running';
const { data } = await volcano.durable.list(projectId, 'order-pipeline', { status });
const execution: DurableExecution | undefined = data?.data[0];
```

`DurableExecution` uses the API's snake-case fields. Its `result` is `unknown`,
so narrow it before use.

`ctx.waitForApproval` takes `WaitForApprovalOptions` and resolves with an
`ApprovalDecision`, both from the durable entry point:

```ts
import type { ApprovalDecision, WaitForApprovalOptions } from '@volcano.dev/sdk/durable';

const request: WaitForApprovalOptions = { title: 'Ship order 4417?', timeout: '3d' };
const decision: ApprovalDecision = await ctx.waitForApproval('ship-order', request);
// decision.status is 'approved' | 'denied' | 'expired'; decidedBy is null on expiry.
```

Reading and deciding approvals uses the main entry point's `DurableApproval`,
`DurableApprovalStatus`, `PaginatedDurableApprovals`, and `DurableApprovalStats`,
with `DurableApprovalListOptions` and `DurableApprovalStatsOptions` for filters:

```ts
import type { DurableApproval, DurableApprovalListOptions } from '@volcano.dev/sdk';

const options: DurableApprovalListOptions = { status: 'pending', function: 'order-pipeline' };
const { data } = await volcano.durable.approvals.list(projectId, options);
const approval: DurableApproval | undefined = data?.data[0];
```

Like `DurableExecution`, `DurableApproval` uses snake-case fields
(`requested_at`, `expires_at`, `decision.decided_by`).

## OAuth Types
```ts
type OAuthProviderName = 'google' | 'github' | 'microsoft' | 'apple';

interface OAuthProvider {
  provider: OAuthProviderName;
  linked_at: string;
  updated_at: string;
}

interface OAuthAPIParams {
  endpoint: string;
  method?: string;
  body?: JsonValue;
}
```

```ts
volcano.auth.signInWithOAuth('google');     // OK
volcano.auth.signInWithOAuth('invalid');    // Compile error: not in OAuthProviderName

const { providers } = await volcano.auth.getLinkedOAuthProviders();
providers?.forEach((p: OAuthProvider) => { /* ... */ });
```

## Session Management Types
```ts
interface AuthSession {
  id: string;
  user_id: string;
  provider: 'email' | 'google' | 'github' | 'microsoft' | 'apple' | 'anonymous';
  user_agent?: string;
  ip_address?: string;
  last_ip_address?: string;
  expires_at: string;
  last_activity_at?: string;
  session_started_at?: string;
  is_active: boolean;
  is_current: boolean;
  created_at: string;
  updated_at: string;
}

interface SessionsResponse {
  sessions: AuthSession[] | null;
  total: number;
  page: number;
  limit: number;
  total_pages: number;
  error: Error | null;
}
```
Returned from `volcano.auth.getSessions({ page, limit })`. `is_current` flags the calling client's own session.

## Middleware Types
```ts
import type {
  ServerClientConfig,
  ServerClient,
  User,
  GetUserResult,
  RefreshTokenResult,
} from '@volcano.dev/sdk/next/middleware';

interface ServerClientConfig {
  anonKey: string;
  apiUrl?: string;
  accessToken?: string;
}

interface ServerClient {
  getUser(accessToken: string): Promise<GetUserResult>;
  refreshToken(refreshToken: string): Promise<RefreshTokenResult>;
}

interface GetUserResult {
  user: User | null;
  error: Error | null;
}

interface RefreshTokenResult {
  accessToken: string | null;
  refreshToken: string | null;
  error: Error | null;
}
```

## Utility Types

### JsonValue
Recursive JSON-serializable type. Used throughout the SDK for `user_metadata`, OAuth bodies, function payloads, and realtime broadcast payloads:
```ts
type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };
```

### FilterValue
Values accepted by query filter operators (`eq`/`neq`/`gt`/etc.):
```ts
type FilterValue = string | number | boolean | null | Date;
```

### UserMetadata
Convenience alias when typing user_metadata records:
```ts
type UserMetadata = Record<string, JsonValue>;
```

## Best Practices

### Define your data models once
Centralize entity types in one application-owned shared model file and import them everywhere they're used. In the canonical `web/` frontend this lives under `web/types/` (e.g. `web/types/models.ts`); in a non-web app, use that app's existing shared types path instead of creating `web/` just for types.
```ts
// web/types/models.ts, or your existing shared application types path
export interface User {
  id: string;
  email: string;
  display_name?: string;
  created_at: string;
}

export interface Post {
  id: string;
  user_id: string;
  title: string;
  content: string;
  published: boolean;
  created_at: string;
}
```

### Use type guards for narrowing on union return types
```ts
function isError<T>(result: { data: T | null; error: Error | null }): result is { data: null; error: Error } {
  return result.error !== null;
}

const result = await volcano.from('posts').select('*');
if (isError(result)) {
  console.error(result.error.message);
  return;
}
// result.data is non-null here
```

### Handle null on success-side too
Even with `error` null, `data` can be empty (e.g., `select` with no matches returns `[]`, not `null`; but `update`/`delete` returning no rows returns `[]` or `null` depending on the call). Always handle both:
```ts
const { data, error } = await volcano.update('posts', { ... }).eq('id', id);
if (error) return handleError(error);
if (!data || data.length === 0) return notFound();
const updated = data[0];
```

### Type your realtime callbacks at the boundary
The SDK gives you `Record<string, unknown>`; cast to your row type once at the entry of the handler:
```ts
channel.onPostgresChanges('INSERT', 'public', 'posts', (change) => {
  const post = change.record as Post;
  setPosts(prev => [post, ...prev]);
});
```

### Use strict mode
`tsconfig.json` should have `"strict": true` (the volcano-standard scaffold sets this by default). It surfaces null/undefined mistakes at compile time:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```
`noUncheckedIndexedAccess` is optional but catches subtle bugs with `data[0]` after a query.

## Quick Reference — what type do I need?

| Domain | Most useful type | Where it appears |
|---|---|---|
| Auth | `User`, `Session`, `AuthResponse` | `signIn`/`signUp`/`getUser` returns |
| Database | `QueryResult<T>`, `FilterValue` | `from<T>(...).select(...)` chain |
| Storage | `StorageObject`, `StorageUploadResponse`, `StorageListResponse` | `storage.from(...)` operations |
| Realtime | `PostgresChange`, `PresenceState`, `ConnectContext` | Channel callbacks |
| Functions | `invoke<P, R>(...)` generic params | Both ends of an invocation |
| Durable | `DurableHandler`, `DurableContext`, `DurableExecution`, `ApprovalDecision`, `DurableApproval` | Durable authoring, approvals, and execution clients |
| OAuth | `OAuthProviderName`, `OAuthProvider` | Provider name validation |
| Sessions | `AuthSession`, `SessionsResponse` | Multi-device session UI |
| Middleware | `ServerClient`, `GetUserResult` | Next.js middleware/route handlers |
| Utility | `JsonValue`, `FilterValue`, `UserMetadata` | Anywhere user-supplied JSON-shaped data flows |

## Verification Checklist
- `tsconfig.json` has `"strict": true`.
- All `data` consumption is guarded by an `if (error)` (or equivalent) check first.
- Application data models are centralized (one source of truth) and imported, not redeclared.
- `volcano.from<T>(...)`, `volcano.insert<T>(...)`, `volcano.update<T>(...)` use generic parameters where they apply.
- Realtime callbacks cast `change.record` to a typed row type at the entry boundary.
- Function invocations use `invoke<Params, Result>(...)` generics, not `invoke(...)`.
- Durable handlers use `DurableHandler<Input, Result>` when their input and result are known.
- OAuth provider names are typed as `OAuthProviderName`, not `string`.

## Companion Skills
- `volcano-sdk` — top-level orientation and mandatory usage.
- `volcano-platform` — project shape, Volcano Functions runtime contract, build pipeline.
- Domain and interface skills (`volcano-auth`, `volcano-database`, `volcano-functions`, `volcano-durable`, `volcano-storage`, `volcano-realtime`, `volcano-nextjs`, `volcano-uiux`) — pair with this skill when implementing.
