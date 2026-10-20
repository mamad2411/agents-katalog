---
name: volcano-database
description: Use whenever a Volcano app stores or persists data, including CRUD, records, per-user data, migrations, RLS, todos, chat messages, polls, analytics, counters, click tracking, CMS content, feature flags, and leaderboards.
---
# Volcano Database Skill

## Role
Implement Volcano query-builder access with RLS-first authorization. All persistent data storage MUST use Volcano Databases. This skill is self-contained: the operators, mutation patterns, RLS examples, and error semantics are embedded below.

## Workflow
1. Initialize the client and call `volcano.database(databaseName)` BEFORE any query.
2. Use explicit column lists; avoid `select('*')` unless intentional.
3. Apply deterministic ordering and pagination for list views.
4. Handle mutation errors at every call site; refresh state after writes.

## Setup

### Browser / Client
```ts
import { VolcanoAuth } from '@volcano.dev/sdk';

const volcano = new VolcanoAuth({
  apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL!,
  anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
});
volcano.database(process.env.NEXT_PUBLIC_VOLCANO_DATABASE!);
```

### Function / Server-Side
```ts
function createClient(auth?: { access_token?: string }): VolcanoAuth {
  const volcano = new VolcanoAuth({
    apiUrl: process.env.VOLCANO_API_URL!,
    anonKey: process.env.VOLCANO_ANON_KEY!,
    accessToken: auth?.access_token,
  });
  volcano.database(process.env.VOLCANO_DATABASE!);
  return volcano;
}
```
Use the same request-scoped client pattern inside Functions handlers when server-side persistence is required.

## SELECT

### Basic
```ts
const { data, error, count } = await volcano.from('posts').select('*');
```

### Specific columns (preferred)
```ts
const { data } = await volcano.from('posts').select('id, title, created_at');
```

### Filter operators
```ts
volcano.from('t').select('*').eq('col', value);     // =
volcano.from('t').select('*').neq('col', value);    // !=
volcano.from('t').select('*').gt('col', n);         // >
volcano.from('t').select('*').gte('col', n);        // >=
volcano.from('t').select('*').lt('col', n);         // <
volcano.from('t').select('*').lte('col', n);        // <=
volcano.from('t').select('*').like('col', 'A%');    // case-sensitive
volcano.from('t').select('*').ilike('col', '%a%');  // case-insensitive
volcano.from('t').select('*').is('col', null);      // NULL check
volcano.from('t').select('*').in('col', [a, b, c]); // IN (...)
```
Pattern syntax: `%` matches any sequence, `_` matches any single character.

### Combine filters (AND)
```ts
const { data } = await volcano
  .from('products')
  .select('id, name, price')
  .eq('category', 'electronics')
  .gte('price', 100)
  .lte('price', 500)
  .eq('in_stock', true);
```

### Ordering
```ts
.order('created_at', { ascending: false })
.order('category', { ascending: true })
.order('created_at', { ascending: false }); // chain for multi-column
```

### Pagination
```ts
const pageSize = 10, page = 3;
const { data, count } = await volcano
  .from('posts')
  .select('id, title')
  .order('created_at', { ascending: false })
  .limit(pageSize)
  .offset((page - 1) * pageSize);
```

### Realistic example
```ts
async function getPublishedPosts(category: string, page = 1) {
  const pageSize = 20;
  const { data, error, count } = await volcano
    .from('posts')
    .select('id, title, excerpt, author_name, created_at')
    .eq('status', 'published')
    .eq('category', category)
    .is('deleted_at', null)
    .order('created_at', { ascending: false })
    .limit(pageSize)
    .offset((page - 1) * pageSize);
  if (error) throw new Error(`Failed to fetch posts: ${error.message}`);
  return { posts: data, totalPages: Math.ceil((count ?? 0) / pageSize), currentPage: page };
}
```

## INSERT
```ts
const { data, error } = await volcano.insert('posts', {
  title: 'My New Post',
  content: 'This is the content.',
  status: 'draft',
});
// data is an array; data[0] is the inserted row including any defaults.
```
If the table has a `user_id` column with default `auth.uid()`, the authenticated user's id is automatically associated.

## UPDATE
```ts
const { data, error } = await volcano
  .update('posts', {
    title: 'Updated Title',
    status: 'published',
    updated_at: new Date().toISOString(),
  })
  .eq('id', postId);
// data[0] is the updated row. Filter is REQUIRED.
```

Bulk update (multiple matching rows):
```ts
await volcano
  .update('posts', { status: 'archived' })
  .lt('created_at', oneYearAgo)
  .eq('status', 'published');
```

## DELETE
```ts
const { data, error } = await volcano.delete('posts').eq('id', postId);
```

### Soft-delete pattern
```ts
// Mark deleted
await volcano.update('posts', { deleted_at: new Date().toISOString() }).eq('id', postId);
// Filter from queries
await volcano.from('posts').select('*').is('deleted_at', null);
```

## Modifiers

### `.single()`
Return a single row (not an array). Errors if zero or more-than-one row matches.
```ts
// After a unique-filter select
const { data: post, error } = await volcano
  .from('posts')
  .select('*')
  .eq('id', postId)
  .single();
// data is the row, not data[0]

// Inserts (and updates/deletes) do NOT support .select()/.single() chaining —
// they return { data, error } with data as an array. Take data[0]:
const { data, error } = await volcano.insert('tasks', { title, user_id });
const task = data?.[0];
```

## Limitations
The query builder does NOT currently expose:
- **Joins / nested embedded selects** (e.g., `select('*, comments(*)')`).
- **Upserts** (insert-on-conflict-update).
- **Multi-statement transactions.**
- **`.select()` / `.single()` chained onto a mutation.** `insert()`, `update()`, and `delete()` return a `MutationBuilder` that supports only filters (`.eq()`, `.neq()`, `.in()`, … — the update/delete WHERE clause) and resolves to `{ data, error }` with `data` as an **array**. There is no `.select()` or `.single()` on a mutation: `await volcano.insert(...)` (or `.update(...).eq(...)`) and read `data[0]` for the written row. Chaining `.select()` fails at runtime with `volcano.insert(...).select is not a function`.

When the work genuinely requires one of these, treat **direct Postgres access** (see below) as a last resort, not the default next step — first check whether the feature can be reshaped to fit the query builder (e.g., denormalize, add a lookup column, split into two queries client-side) before reaching for a raw connection. Consult the fallback reference if the SDK has gained these capabilities since this skill was last updated.

## Direct Postgres Access (discouraged — last resort only)

**Prefer the query builder (`volcano.from(...)`) for essentially everything.** Direct Postgres access inside a Function is an escape hatch for the three specific query-builder gaps above, not a general-purpose alternative data-access layer. Treat every use as exceptional and narrow:

- Do NOT adopt a direct-connection/ORM layer as the project's default architecture. Introducing `pg`, Prisma, Sequelize, TypeORM, etc. opens unbounded surface area (arbitrary SQL, connection lifecycle, pooling bugs, migrations drift) that this skill cannot fully cover or guarantee support for.
- Reach for it only when a specific piece of work is provably impossible with the query builder (a genuine join/upsert/multi-statement transaction), and scope the raw-SQL usage to that one function/query — not a rewrite of existing query-builder code.
- Before using it, confirm with the user that this is a deliberate, scoped exception, since it carries more manual RLS-safety responsibility (see the `application_name` rewrite below) than the query builder, which enforces RLS automatically.

**Never browser-side.** Direct connections are Function-only; `DATABASE_URL` is never exposed to browser code.

### The `application_name` rewrite is mandatory
`DATABASE_URL` is auto-injected into every function's environment, but it already carries `application_name=volcano_full_access` — full admin access that **bypasses RLS**. To scope a connection to the calling user (and get RLS enforcement), you MUST rewrite `application_name` to `volcano_user_access:{user_id}` before connecting:

```js
// functions/get-posts-with-authors.js
const { Pool } = require('pg');

// One pool per auth user — the RLS identity is fixed at connection
// startup, so a shared pool can't switch users per request. Capped so a
// warm instance can't accumulate unbounded connections.
const MAX_POOLS = 50;
const poolsByUser = new Map();

function poolForUser(userId) {
  let pool = poolsByUser.get(userId);
  if (pool) return pool;

  // NOTE: FIFO eviction (oldest-inserted), not true LRU — swap in an
  // LRU cache if recency (not insertion order) matters for your traffic.
  if (poolsByUser.size >= MAX_POOLS) {
    const oldestUserId = poolsByUser.keys().next().value;
    poolsByUser.get(oldestUserId).end().catch((err) => console.error('pool.end() failed:', err)); // close before evicting; log instead of crashing on a disconnect error
    poolsByUser.delete(oldestUserId);
  }

  const url = new URL(process.env.DATABASE_URL);
  url.searchParams.set('application_name', `volcano_user_access:${userId}`); // REPLACE, don't append
  pool = new Pool({ connectionString: url.toString(), max: 5 });
  poolsByUser.set(userId, pool);
  return pool;
}

exports.handler = async (event) => {
  const auth = event.__volcano_auth;
  if (!auth) return { statusCode: 401, body: JSON.stringify({ error: 'Unauthorized' }) };

  const client = await poolForUser(auth.user_id).connect();
  try {
    // RLS is active: auth.uid() resolves to auth.user_id inside this query.
    const { rows } = await client.query(`
      SELECT p.*, u.name AS author_name
      FROM posts p JOIN users u ON p.user_id = u.id
      WHERE p.status = $1
    `, ['published']);
    return { statusCode: 200, body: JSON.stringify({ posts: rows }) };
  } finally {
    client.release();
  }
};
```

### Rules
- **Rewrite `application_name`, never append** — a duplicate parameter leaves the startup mode up to the driver's dupe handling. Use `url.searchParams.set(...)`, not string concatenation.
- **Never trust a client-supplied user id** — only use `event.__volcano_auth.user_id` (server-verified), never a value from the request body.
- **The identity is fixed at connection startup** — `SET application_name` after `connect()` has no effect on RLS scoping. Pool per user (as above); don't share one pool across users.
- **The per-user pool cache is capped** (`MAX_POOLS`, oldest-evicted with `pool.end()` before removal) — an unbounded cache lets total open connections grow as (distinct users served by this warm instance) × `max` and can exhaust the database's connection limit. Tune `MAX_POOLS × max` against the database's connection limit rather than removing the cap.
- **Admin/bypass access** (background jobs, migrations, cross-user aggregation) uses the connection string as-is (`volcano_full_access`) or a dedicated service-role connection string — never expose this path to user-triggered requests.
- **Default to the query builder.** Re-check this section's "discouraged" framing before writing new raw-SQL code — direct access should stay the exception, not grow into a parallel data layer.

## Row-Level Security (RLS)

### How it works
1. Sign-in produces an access token containing the user's id.
2. Every database call includes that token.
3. Volcano sets the user context in the DB session.
4. RLS policies use `auth.uid()` to reference the current user.

### Example policies
```sql
-- Users can only read their own posts
CREATE POLICY "Users can read own posts"
ON posts FOR SELECT
USING (user_id = auth.uid());

-- Users can only update their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (user_id = auth.uid());

-- Users can only insert posts owned by themselves
CREATE POLICY "Users can insert own posts"
ON posts FOR INSERT
WITH CHECK (user_id = auth.uid());

-- Public-read pattern
CREATE POLICY "Published posts are public"
ON posts FOR SELECT
USING (status = 'published');
```

### Owner column & inserts

Pair every owner-scoped `WITH CHECK (user_id = auth.uid())` insert policy with a `DEFAULT auth.uid()` on the column it checks (`user_id uuid NOT NULL DEFAULT auth.uid()`) so the server fills the owner from the token. Otherwise every client insert must set `user_id` itself, and one that omits it is rejected with `new row violates row-level security policy` (`42501`) — Postgres evaluates the RLS `WITH CHECK` before the column's `NOT NULL` constraint, so the missing owner surfaces as a policy violation, not a not-null error. With the default, `insert('posts', { title })` works for the signed-in user without passing `user_id`, and the policy still enforces ownership.

RLS only takes effect once the table has `ALTER TABLE <table> ENABLE ROW LEVEL SECURITY`. For the full `CREATE TABLE` + enable + policy sequence, follow the canonical `posts` migration in the `volcano-platform` skill ("Canonical migration with RLS") rather than re-declaring the table here. For a child table (e.g. `comments`), the FK (`post_id`) comes from the client while the owner (`user_id`) still defaults to `auth.uid()`.

The same client query returns different rows depending on the signed-in user. Do NOT emulate authorization in client code; rely on RLS.

## TypeScript
```ts
interface Post {
  id: string;
  title: string;
  status: 'draft' | 'published' | 'archived';
  created_at: string;
}
const { data } = await volcano.from<Post>('posts').select('*').eq('status', 'published');
// data: Post[] | null
```

## Error Handling
All operations return `{ data, error }`. Common messages:
- `column does not exist` — invalid column name (developer error).
- `permission denied` — RLS policy blocked the operation.
- `No active session` — user not authenticated.
- `Database name not set` — forgot `volcano.database(...)`.
- `violates unique constraint` — duplicate value on insert.
- `violates foreign key` — bad reference.
- `violates check constraint` — invalid input.

## Functions Integration
When persistence belongs in a function, keep the same client pattern inside the handler:
```ts
// Client side
const { data, error } = await volcano.functions.invoke('get-dashboard-stats', { timeframe: 'last-30-days' });

// Function side: same query-builder flow with a request-scoped client
export const handler = async (event: { __volcano_auth?: { access_token?: string } }) => {
  const auth = event.__volcano_auth;
  if (!auth) return { statusCode: 401, body: JSON.stringify({ error: 'Unauthorized' }) };
  const volcano = createClient(auth);
  const { data, error } = await volcano.from('posts').select('id, title, created_at').order('created_at', { ascending: false });
  if (error) return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
  return { statusCode: 200, body: JSON.stringify({ posts: data ?? [] }) };
};
```

## Best Practices
- Always set the database name once after init.
- Sign in (or accept anonymous) before queries that depend on RLS-bound rows.
- Select only the columns you need.
- Paginate large lists (`.limit(50)` is a sensible default).
- Filter server-side; never fetch everything then filter in JS.
- Return the `error` object from server handlers as `{ statusCode, body: JSON.stringify({ error: error.message }) }`.

## Verification Checklist
- `volcano.database(name)` is called before any query.
- Filter, order, and pagination intent matches the request.
- RLS policies are assumed to exist; no client-side pseudo-authorization.
- Mutations have explicit error handling at the call site.
- Functions doing persistence use a request-scoped client built from `event.__volcano_auth`.
- The query builder was confirmed insufficient (a genuine join/upsert/multi-statement transaction) before reaching for direct Postgres access — it is not used as a default data-access layer.
- If using direct Postgres access, `application_name` is rewritten to `volcano_user_access:{user_id}` before connecting — never a bare `DATABASE_URL` for user-scoped queries.

## Optional Fallback Reference
