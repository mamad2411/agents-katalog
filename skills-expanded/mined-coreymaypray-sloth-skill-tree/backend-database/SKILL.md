---
name: backend-database
description: "Use when designing or reviewing a Postgres/Supabase schema, writing RLS policies, planning migrations or indexes, choosing a Supabase plan, or diagnosing slow queries."
---

# Backend Database

## Overview

PostgreSQL/Supabase database design, schema setup, RLS policies, performance optimization, and pricing guidance for Corey's projects.

## Schema Design Principles

1. **Normalize first, denormalize for performance** — Start with 3NF, add materialized views or denormalized columns only when query patterns demand it
2. **UUIDs for primary keys** — Use `gen_random_uuid()` as default
3. **Timestamps on everything** — `created_at`, `updated_at` with triggers
4. **Soft deletes by default** — `deleted_at` timestamp, never hard delete in application layer
5. **Audit trail** — Track who changed what and when

## Standard Table Template

```sql
CREATE TABLE public.table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- columns here
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ
);

-- Auto-update timestamp
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON public.table_name
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- RLS
ALTER TABLE public.table_name ENABLE ROW LEVEL SECURITY;
```

## RLS Policy Patterns

### User-Owned Data
```sql
CREATE POLICY "Users can view own data"
  ON public.table_name FOR SELECT
  USING (auth.uid() = user_id);
```

### Organization-Scoped (Multi-Tenant)
```sql
CREATE POLICY "Members can view org data"
  ON public.table_name FOR SELECT
  USING (
    org_id IN (
      SELECT org_id FROM public.org_members
      WHERE user_id = auth.uid()
    )
  );
```

### Role-Based
```sql
CREATE POLICY "Admins can update"
  ON public.table_name FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM public.org_members
      WHERE user_id = auth.uid()
        AND org_id = table_name.org_id
        AND role IN ('admin', 'owner')
    )
  );
```

## Multi-Tenant Architecture

### Core Tables
- `organizations` — Tenant container
- `org_members` — User-to-org mapping with roles
- `org_invitations` — Pending invites
- `org_settings` — Per-tenant configuration

### RBAC Roles
- `owner` — Full access, billing, can delete org
- `admin` — Manage members, settings, all data
- `member` — Standard access to org data
- `viewer` — Read-only access

## Performance Optimization

### Indexing Strategy
- Index all foreign keys
- Index columns used in WHERE clauses
- Composite indexes for multi-column lookups
- Partial indexes for filtered queries
- GIN indexes for JSONB and full-text search

### Query Optimization
- Use `EXPLAIN ANALYZE` before and after
- Avoid N+1 queries — use joins or Supabase's `select('*, relation(*)')`
- Materialized views for complex aggregations
- Connection pooling via Supabase's built-in pgBouncer

## Supabase Plan Guidance

| Plan | Monthly | Best For |
|------|---------|----------|
| Free | $0 | Prototyping, demos |
| Pro | $25 | Client apps, small SaaS |
| Team | $599 | Multi-tenant, TIE Platform |
| Enterprise | Custom | Large-scale deployments |

## Rules

- RLS on every table, no exceptions
- Never expose service_role key to client
- Use database functions for complex business logic
- Migrations tracked in version control
- Test RLS policies with pgTAP or manual testing
- Document every table and column purpose
- Review schema before any production deployment
