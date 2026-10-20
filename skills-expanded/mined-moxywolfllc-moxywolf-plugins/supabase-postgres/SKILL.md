---
name: supabase-postgres
description: >
  This skill should be used when the user asks to "write a Supabase query",
  "set up RLS policies", "create a migration", "optimize Postgres queries",
  "design a database schema", "use edge functions", "configure realtime",
  "fix database performance", or needs guidance on Supabase patterns,
  Row Level Security, connection management, indexing strategies,
  or Postgres best practices for SaaS applications.
version: 0.1.0
---

# Supabase & Postgres Best Practices

Patterns for building performant, secure applications with Supabase and PostgreSQL. Covers query performance, RLS, connection management, schema design, and advanced features.

## 1. Query Performance

### Use Appropriate Indexes

Create indexes based on actual query patterns, not just column existence:

```sql
-- For exact lookups
CREATE INDEX idx_users_email ON users (email);

-- For range queries and sorting
CREATE INDEX idx_orders_created ON orders (created_at DESC);

-- For composite lookups
CREATE INDEX idx_orders_user_status ON orders (user_id, status);

-- Partial indexes for common filters
CREATE INDEX idx_active_subscriptions ON subscriptions (user_id)
  WHERE status = 'active';
```

### Avoid N+1 Queries

Use Supabase's nested selects instead of looping:

```typescript
// BAD: N+1 — one query per user
const users = await supabase.from('users').select('id');
for (const user of users.data) {
  const posts = await supabase.from('posts').select('*').eq('user_id', user.id);
}

// GOOD: Single query with join
const { data } = await supabase
  .from('users')
  .select('id, name, posts(id, title, created_at)')
  .order('created_at', { foreignTable: 'posts', ascending: false });
```

### Use `explain analyze` for Slow Queries

```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 'abc' AND status = 'pending'
ORDER BY created_at DESC
LIMIT 20;
```

Look for: Seq Scan (needs index), Nested Loop (potential N+1), high actual rows vs. estimated.

## 2. Row Level Security (RLS)

### Always Enable RLS on Public Tables

```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Users can only read their own documents
CREATE POLICY "Users read own documents"
  ON documents FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own documents
CREATE POLICY "Users insert own documents"
  ON documents FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own documents
CREATE POLICY "Users update own documents"
  ON documents FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
```

### Organization-Based Access

```sql
-- Check membership through a join
CREATE POLICY "Org members access"
  ON projects FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM org_members
      WHERE org_members.org_id = projects.org_id
      AND org_members.user_id = auth.uid()
    )
  );
```

### Performance Tip: Use Security Definer Functions

For complex RLS policies, wrap the check in a function to avoid repeated subquery execution:

```sql
CREATE OR REPLACE FUNCTION is_org_member(org uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM org_members
    WHERE org_id = org AND user_id = auth.uid()
  );
$$;

CREATE POLICY "Org access" ON projects
  FOR ALL USING (is_org_member(org_id));
```

## 3. Connection Management

### Use Connection Pooling

Supabase provides PgBouncer connection pooling. Use the pooled connection string for application queries:

- **Direct connection**: For migrations, DDL, and administrative tasks
- **Pooled connection (port 6543)**: For all application queries
- **Transaction mode**: Default. Each transaction gets a dedicated connection
- **Session mode**: Use when you need prepared statements or session variables

### Edge Functions: Use Supabase Client

```typescript
// In edge functions, use the Supabase client — it handles pooling
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
);
```

## 4. Schema Design

### Use UUIDs for Primary Keys

```sql
CREATE TABLE items (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);
```

### Timestamps with Timezone

Always use `timestamptz`, never `timestamp`:

```sql
-- GOOD
created_at timestamptz DEFAULT now() NOT NULL

-- BAD: Loses timezone information
created_at timestamp DEFAULT now() NOT NULL
```

### Soft Deletes for Audit Trails

```sql
ALTER TABLE documents ADD COLUMN deleted_at timestamptz;

-- RLS policy excludes soft-deleted rows
CREATE POLICY "Hide deleted" ON documents
  FOR SELECT USING (deleted_at IS NULL);
```

## 5. Migrations

### One Change Per Migration

```sql
-- migrations/20240101_add_user_status.sql
ALTER TABLE users ADD COLUMN status text DEFAULT 'active' NOT NULL;
CREATE INDEX idx_users_status ON users (status);
```

### Always Add Down Migrations

Keep a corresponding rollback for every migration in case of issues.

### Test Migrations on a Branch

Use Supabase branching to test migrations before applying to production.

## 6. Realtime

### Subscribe to Specific Filters

```typescript
// GOOD: Subscribe only to relevant changes
const channel = supabase
  .channel('user-notifications')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'notifications',
    filter: `user_id=eq.${userId}`,
  }, handleNotification)
  .subscribe();

// Always clean up
return () => supabase.removeChannel(channel);
```

### Use Broadcast for Ephemeral Data

For presence, cursor positions, or typing indicators — use Broadcast, not database changes:

```typescript
const channel = supabase.channel('room-1');
channel.on('broadcast', { event: 'cursor' }, handleCursor);
channel.subscribe();
channel.send({ type: 'broadcast', event: 'cursor', payload: { x, y } });
```

## 7. Edge Functions

### Keep Functions Focused

Each edge function should do one thing. Compose complex workflows by calling multiple functions.

### Use Service Role Key Carefully

The service role key bypasses RLS. Only use it in edge functions for admin operations, never expose it to clients.

### Handle Errors Explicitly

```typescript
Deno.serve(async (req) => {
  try {
    const { data, error } = await supabase.from('items').select('*');
    if (error) throw error;
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});
```

## Quick Reference Checklist

- [ ] RLS enabled on all public-facing tables
- [ ] Indexes match actual query patterns
- [ ] Using pooled connections for application queries
- [ ] `timestamptz` used everywhere (not `timestamp`)
- [ ] UUIDs for primary keys
- [ ] N+1 queries replaced with joins or nested selects
- [ ] Realtime subscriptions include filters
- [ ] Edge functions use error handling and focused scope
- [ ] Migrations are single-purpose and reversible

For detailed patterns on each topic, see `references/`.

## Restraint layer (ponytail)

Prefer a DB constraint or built-in over app code; climb the ladder before adding a table, trigger, or dependency. See the `ponytail` skill — the YAGNI ladder (does it need to exist; stdlib before custom; native before dependency; one line before fifty), never cutting validation, error handling, security, or accessibility.
