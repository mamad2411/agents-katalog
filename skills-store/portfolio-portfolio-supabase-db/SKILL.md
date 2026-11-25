---
name: portfolio-supabase-db
description: >-
  Assign this skill to a sub-agent for database migrations, Supabase CLI operations, and Row Level Security (RLS) policies.
---

# Supabase Database Guidelines

## Best Practices
1. **Migrations**: Always use the Supabase CLI to generate and apply migrations. Do not make manual changes to the production schema via the dashboard.
   - Command: `supabase migration new <name>`
2. **Row Level Security (RLS)**: By default, tables should have RLS enabled. Write explicit policies for SELECT, INSERT, UPDATE, and DELETE.
   - Example: `ALTER TABLE my_table ENABLE ROW LEVEL SECURITY;`
3. **Roles**: Understand the difference between `anon` (unauthenticated), `authenticated` (logged-in users), and `service_role` (bypass RLS, used by FastAPI backend).
4. **Local Dev**: Use the Supabase CLI for local development to ensure a reproducible environment.

## Command Reference
- Start Local DB: `supabase start`
- Stop Local DB: `supabase stop`
- Create Migration: `supabase migration new <name>`
- Apply Migrations: `supabase db reset`
- Generate Types: `supabase gen types typescript --local > types/supabase.ts`
