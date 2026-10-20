---
description: RLS migration and policy patterns
globs:
  - "**/migrations/**"
alwaysApply: false
---

# RLS (Row-Level Security) Patterns

## Every tenant-scoped table
- ALTER TABLE public.[name] ENABLE ROW LEVEL SECURITY;
- tenant_id column: uuid NOT NULL REFERENCES public.tenants(id) ON DELETE CASCADE
- CREATE INDEX CONCURRENTLY idx_[name]_tenant_id ON public.[name] (tenant_id); all indexes in migrations MUST use CONCURRENTLY
- Composite index for time-ordered queries: (tenant_id, created_at DESC)

## Policy checklist
- Prefer public.tenant_id() (STABLE PARALLEL SAFE) for tenant-scoped policies — see 005_auth_tenant_id_helper.sql and 007_refactor_rls_use_tenant_id_helper.sql
- SELECT: USING (tenant_id = public.tenant_id()) or for tenants table: (id = public.tenant_id())
- INSERT: WITH CHECK (tenant_id = public.tenant_id())
- UPDATE: USING (tenant_id = public.tenant_id()) WITH CHECK (tenant_id = public.tenant_id())
- DELETE: USING (tenant_id = public.tenant_id())

## Performance
- public.tenant_id() is evaluated once per query (initplan); every tenant_id column must have an index — without it RLS causes full table scans
- Verify with EXPLAIN (ANALYZE, BUFFERS); see docs/security/MULTI_TENANT_SECURITY.md and supabase/verify-rls-indexes.sql
