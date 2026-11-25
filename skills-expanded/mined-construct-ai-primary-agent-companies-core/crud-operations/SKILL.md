---
name: crud-operations
description: >
  Routes CRUD operations requiring FK-safe programmatic database access to the
  Database CRUD Orchestrator. Handles insert/update/delete/select operations
  with automatic foreign key dependency resolution, transaction wrapping, and
  rollback support across Paperclip's FK-heavy schema.
company: paperclipforge-ai
---

# CRUD Operations

## Overview
This skill routes all programmatic CRUD operations on Paperclip's FK-heavy database schema to the Database CRUD Orchestrator agent. It handles the complexity of FK dependency resolution, safe deletion ordering, and transaction-safe inserts/updates.

## Routing Criteria

Route to this skill when:
- **INSERT** operations requiring FK parent lookups (e.g., creating agents with company_id, reports_to)
- **DELETE** operations where child records must be removed first
- **UPDATE** operations on FK-linked columns
- **SELECT** with complex JOINs across FK relationships
- Any CRUD involving 3+ FK constraints in a single operation
- Bulk inserts/updates/deletes needing FK-aware batching
- Data migration requiring FK-safe ordered operations

## FK-Aware Operation Patterns

### Safe DELETE Sequences

The Paperclip schema has a dense FK graph. Deletions must follow child-to-parent ordering:

```sql
-- Generic FK-safe deletion pattern
-- 1. Delete deepest children first
-- 2. Delete intermediate children
-- 3. Delete parent records last
BEGIN;

-- Step 1: Handle CASCADE-able children (these go first)
-- Tables with ON DELETE CASCADE will auto-clean, but explicit control is safer
DELETE FROM heartbeat_run_events WHERE run_id IN (
  SELECT id FROM heartbeat_runs WHERE agent_id = $target_id
);
DELETE FROM agent_task_sessions WHERE agent_id = $target_id;
DELETE FROM agent_runtime_state WHERE agent_id = $target_id;

-- Step 2: Handle SET NULL children (nullify references first)
UPDATE heartbeat_runs SET agent_id = NULL WHERE agent_id = $target_id;
UPDATE activity_log SET agent_id = NULL WHERE agent_id = $target_id;

-- Step 3: Handle NO ACTION children (must delete explicitly)
DELETE FROM agent_api_keys WHERE agent_id = $target_id;
DELETE FROM agent_config_revisions WHERE agent_id = $target_id;
DELETE FROM agent_skill_assignments WHERE agent_id = $target_id;
DELETE FROM agent_wakeup_requests WHERE agent_id = $target_id;

-- Step 4: Handle self-referencing FK (reports_to)
UPDATE agents SET reports_to = NULL WHERE reports_to = $target_id;

-- Step 5: Delete the target record
DELETE FROM agents WHERE id = $target_id;

COMMIT;
```

### Safe INSERT with FK Lookups

```sql
-- INSERT pattern with FK validation
DO $$
DECLARE
  v_company_id UUID;
  v_manager_id UUID;
  v_agent_id UUID;
BEGIN
  -- Validate FK references first
  SELECT id INTO v_company_id FROM companies 
  WHERE name = 'Target Company' AND status = 'active';
  
  IF v_company_id IS NULL THEN
    RAISE EXCEPTION 'Company "Target Company" not found or inactive';
  END IF;
  
  SELECT id INTO v_manager_id FROM agents 
  WHERE name = 'manager-agent-name' AND company_id = v_company_id;
  -- manager_id is optional, no exception if NULL

  -- Insert with validated FK references
  INSERT INTO agents (id, company_id, name, title, reports_to, ...)
  VALUES (gen_random_uuid(), v_company_id, 'new-agent', 'New Agent', v_manager_id, ...)
  RETURNING id INTO v_agent_id;
  
  RAISE NOTICE 'Agent created: %', v_agent_id;
END $$;
```

## Capabilities

### FK Graph Analysis
- Scan `information_schema.table_constraints` and `information_schema.referential_constraints` for live FK definitions
- Build ordered dependency lists for any target table
- Identify CASCADE vs SET NULL vs RESTRICT/NO ACTION rules
- Detect circular FK references and self-referencing FKs

### CRUD Template Generation
- Generate Drizzle ORM TypeScript templates for type-safe CRUD
- Generate supabase-py Python templates for programmatic access
- Generate raw SQL templates for manual execution
- Each template includes FK validation, transaction wrapping, and error handling

### Bulk Operation Patterns
- **Bulk Insert**: Validates all FK references upfront, batches with `unnest()`, wraps in transaction
- **Bulk Delete**: Orders by FK dependency depth, deletes in reverse-dependency batches
- **Bulk Update**: Uses temporary tables for atomic updates, SAVEPOINT per batch for partial rollback

## Related Procedures

- **SQL Generation Procedure**: `/docs-paperclip/procedures/database/sql-generation-procedure.md`
- **FK Dependency Map**: `/docs-paperclip/schema/FK table relationships.csv`
- **Schema Documentation**: `/docs-paperclip/schema/` for all table references
- **Backup Procedures**: `/docs-paperclip/procedures/database/database-backup-recovery-procedure.md`

## Drizzle ORM Integration

When generating Drizzle ORM templates, use these patterns:

```typescript
// TypeScript Drizzle ORM - FK-safe insert
import { db } from './db';
import { agents, companies } from './schema';
import { eq } from 'drizzle-orm';
import { z } from 'zod';

async function createAgentWithFks(data: {
  name: string;
  companyName: string;
  reportsTo?: string;
  title: string;
}) {
  return await db.transaction(async (tx) => {
    // Validate FK references
    const company = await tx.query.companies.findFirst({
      where: eq(companies.name, data.companyName),
    });
    if (!company) throw new Error(`Company not found: ${data.companyName}`);

    // Optional manager reference
    let managerId: string | null = null;
    if (data.reportsTo) {
      const manager = await tx.query.agents.findFirst({
        where: eq(agents.name, data.reportsTo),
      });
      if (!manager) throw new Error(`Manager not found: ${data.reportsTo}`);
      managerId = manager.id;
    }

    // Insert with resolved FKs
    const [agent] = await tx.insert(agents).values({
      id: crypto.randomUUID(),
      companyId: company.id,
      name: data.name,
      title: data.title,
      reportsTo: managerId,
      status: 'active',
      createdAt: new Date(),
      updatedAt: new Date(),
    }).returning();

    return agent;
  });
}
```

## Related Skills

- `database-schema-inspection` - Schema analysis for FK validation
- `sql-generation` - Raw SQL generation for verified operations
- `foreign-key-dependency-management` - Shared FK mapping and deletion ordering
- `fk-dependency-graph` - Detailed FK graph analysis
- `drizzle-crud-templates` - Type-safe ORM template generation
- `bulk-operations` - FK-safe bulk operation patterns

---

*This skill ensures all CRUD operations on FK-heavy tables are safe, ordered, and transaction-protected.*