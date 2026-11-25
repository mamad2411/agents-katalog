---
name: skill-supabase-rls
description: Design and review defensive Supabase/Postgres Row Level Security for SaaS systems. Use for RLS policies, auth-aware tenant isolation, storage policies, service-role boundaries, migrations, indexes, positive/negative access tests, and data-isolation security reviews.
category: security
risk: high
source: supabase-rls-docs-plus-local-patterns
---

# skill-supabase-rls

## Authorization gate

Use this skill for projects the user owns or is authorized to modify. For production databases, do not run migrations, resets, destructive SQL, or policy changes without explicit approval in the current task.

Record:

- Project and environment: local, staging, preview, or production.
- Tables, schemas, buckets, and tenants in scope.
- Whether changes are advisory, migration-ready, or approved for execution.

## Core rules

1. Enable RLS on every user-facing table in exposed schemas.
2. Browser clients must use anon/user auth, never service-role keys.
3. Service-role keys are allowed only in server functions, controllers, jobs, or trusted backends.
4. Policies must include user ownership, tenant membership, or explicit role checks.
5. Admin cross-tenant reads should go through backend routes or RPC with explicit authorization.
6. Add indexes that match policy predicates and dashboard filters.
7. Avoid new `select('*')` reads in application code when sensitive columns exist.
8. Test positive and negative access cases before claiming security is complete.
9. Remember that after RLS is enabled, API access with browser-safe keys returns no rows until explicit policies exist.
10. For SQL-created tables in exposed schemas, enable RLS deliberately; do not rely on dashboard defaults.

## Severity and gates

- Critical: service-role key exposed to client code, RLS disabled on user-facing sensitive tables, cross-tenant read/write, public write access to sensitive data. Block release.
- High: missing tenant predicate, admin bypass without server-side authorization, storage bucket policy exposing private files, unsafe `SECURITY DEFINER` function. Block merge until fixed or risk-accepted.
- Medium: missing policy indexes, broad `select('*')`, ambiguous anonymous access, missing negative tests. Require ticketed remediation.
- Low/Info: naming, documentation, policy simplification, performance tuning without direct exposure. Track without blocking.

## Policy patterns

Use direct ownership when a row belongs to a user:

```sql
CREATE POLICY "users_read_own_rows" ON table_name
  FOR SELECT
  TO authenticated
  USING ((SELECT auth.uid()) = user_id);
```

Use membership checks for tenant/workspace data:

```sql
CREATE POLICY "members_read_tenant_rows" ON table_name
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1
      FROM tenant_members tm
      WHERE tm.tenant_id = table_name.tenant_id
        AND tm.user_id = (SELECT auth.uid())
    )
  );
```

Use `WITH CHECK` for write policies:

```sql
CREATE POLICY "members_create_tenant_rows" ON table_name
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1
      FROM tenant_members tm
      WHERE tm.tenant_id = table_name.tenant_id
        AND tm.user_id = (SELECT auth.uid())
        AND tm.role IN ('owner', 'admin')
    )
  );
```

Add supporting indexes:

```sql
CREATE INDEX IF NOT EXISTS idx_table_name_tenant_id ON table_name(tenant_id);
CREATE INDEX IF NOT EXISTS idx_table_name_user_id ON table_name(user_id);
CREATE INDEX IF NOT EXISTS idx_tenant_members_user_tenant ON tenant_members(user_id, tenant_id);
```

## Validation queries

Check exposed tables without RLS:

```sql
SELECT n.nspname AS schema_name, c.relname AS table_name
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
  AND n.nspname IN ('public', 'storage')
  AND c.relrowsecurity = false
ORDER BY 1, 2;
```

List policies for review:

```sql
SELECT schemaname, tablename, policyname, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname IN ('public', 'storage')
ORDER BY schemaname, tablename, policyname;
```

For access tests, prove both cases:

- Positive: an authorized user can read/write only the intended row or object.
- Negative: another user or tenant cannot read/write the same row or object.

## Related files

- Read `RULES.md` for detailed SQL patterns.
- Read `TROUBLESHOOTING.md` for common RLS failures and diagnostics.

## Related skills

- `skill-saas-factory`
- `skill-saas-core-limits`
- `skill-saas-security-scan`
- `skill-security-hooks`

