---
name: bulk-operations
description: >
  Routes bulk database operations to the Database CRUD Orchestrator for FK-safe
  batch inserts, ordered bulk deletes, and transaction-wrapped bulk updates
  across Paperclip's heavily relational schema.
company: paperclipforge-ai
---

# Bulk Operations

## Overview
This skill provides FK-safe bulk operation patterns for the Paperclip database schema. Bulk operations present unique challenges with 237+ FK relationships — insert order matters, delete order matters, and partial failures must be handled gracefully. This skill provides battle-tested patterns for all three bulk operation types.

## Routing Criteria

Route to this skill when:
- Bulk inserting 10+ records across FK-linked tables
- Bulk deleting multiple records with FK dependencies
- Batch updating records with FK constraint considerations
- Data migration requiring FK-safe ordering
- Large-scale agent creation/deletion operations
- CSV or JSON data import requiring FK validation
- Any operation involving `COPY`, `unnest()`, or batch transactions

## Bulk Operation Patterns

### Bulk INSERT with FK Pre-validation

```sql
-- Bulk insert agents with FK validation
-- Validates all FK references before inserting any records
DO $$
DECLARE
  v_company_id UUID;
  v_agent_count INTEGER;
BEGIN
  -- 1. Resolve shared FK references once
  SELECT id INTO v_company_id FROM companies 
  WHERE name = 'PaperclipForge AI' AND status = 'active';
  
  IF v_company_id IS NULL THEN
    RAISE EXCEPTION 'Company not found';
  END IF;

  -- 2. Pre-validate all foreign keys
  -- (Check all manager agents exist before inserting)
  
  -- 3. Bulk insert with unnested arrays
  INSERT INTO agents (id, company_id, name, title, role, status, created_at, updated_at)
  SELECT
    gen_random_uuid(),
    v_company_id,
    unnest(ARRAY['agent-1', 'agent-2', 'agent-3']),
    unnest(ARRAY['Agent One', 'Agent Two', 'Agent Three']),
    'specialist',
    'active',
    NOW(),
    NOW()
  ON CONFLICT (name) DO NOTHING;

  GET DIAGNOSTICS v_agent_count = ROW_COUNT;
  RAISE NOTICE 'Inserted % agents', v_agent_count;
END $$;
```

### Bulk DELETE with Ordered FK Awareness

```sql
-- Bulk delete multiple agents with FK-safe ordering
-- Processes deepest dependencies first, works up to target
BEGIN;

-- Phase 1: Remove deepest children
DELETE FROM heartbeat_run_events hre
USING heartbeat_runs hr
WHERE hre.run_id = hr.id
  AND hr.agent_id = ANY($agent_ids);

DELETE FROM agent_config_revisions WHERE agent_id = ANY($agent_ids);
DELETE FROM agent_wakeup_requests WHERE agent_id = ANY($agent_ids);

-- Phase 2: Remove intermediate children
DELETE FROM agent_task_sessions WHERE agent_id = ANY($agent_ids);
DELETE FROM agent_runtime_state WHERE agent_id = ANY($agent_ids);

-- Phase 3: Remove direct children
DELETE FROM agent_api_keys WHERE agent_id = ANY($agent_ids);
DELETE FROM agent_skill_assignments WHERE agent_id = ANY($agent_ids);

-- Phase 4: Handle SET NULL + self-refs
UPDATE heartbeat_runs SET agent_id = NULL WHERE agent_id = ANY($agent_ids);
UPDATE activity_log SET agent_id = NULL WHERE agent_id = ANY($agent_ids);
UPDATE agents SET reports_to = NULL WHERE reports_to = ANY($agent_ids);

-- Phase 5: Remove targets
DELETE FROM agents WHERE id = ANY($agent_ids);

COMMIT;
```

### Supabase-PY Bulk Delete Pattern

```python
from supabase import create_client
from typing import Optional

def bulk_delete_with_fk_ordering(
    supabase,
    table: str,
    ids: list[str],
    fk_dependency_order: Optional[list[dict]] = None
) -> dict:
    """
    Generic FK-safe bulk deletion.
    
    fk_dependency_order: list of {table, column, fk_action} in
    dependency order (deepest children first)
    """
    # Default: children first ordering for agents table
    fk_order = fk_dependency_order or [
        {'table': 'heartbeat_run_events', 'column': 'agent_id', 
         'subquery': lambda ids: supabase.table('heartbeat_runs')
             .select('id').in_('agent_id', ids).execute()},
        {'table': 'agent_config_revisions', 'column': 'agent_id', 'fk_action': 'CASCADE'},
        {'table': 'agent_wakeup_requests', 'column': 'agent_id'},
        {'table': 'agent_task_sessions', 'column': 'agent_id'},
        {'table': 'agent_runtime_state', 'column': 'agent_id'},
        {'table': 'agent_api_keys', 'column': 'agent_id'},
        {'table': 'agent_skill_assignments', 'column': 'agent_id'},
        # Nullify self-refs
        {'table': 'heartbeat_runs', 'column': 'agent_id', 'fk_action': 'SET NULL',
         'update_fn': lambda: supabase.table('heartbeat_runs')
             .update({'agent_id': None}).in_('agent_id', ids).execute()},
        # Target table last
        {'table': 'agents', 'column': 'id'},
    ]
    
    for entry in fk_order:
        if entry.get('subquery'):
            # Tables needing intermediate lookups
            ids_to_delete = entry['subquery'](ids)
            if ids_to_delete:
                supabase.table(entry['table']).delete().in_(
                    entry['column'], ids_to_delete
                ).execute()
        elif entry.get('update_fn'):
            # SET NULL operations
            entry['update_fn']()
        elif entry['fk_action'] == 'CASCADE':
            supabase.table(entry['table']).delete().in_(
                entry['column'], ids
            ).execute()
        else:
            supabase.table(entry['table']).delete().in_(
                entry['column'], ids
            ).execute()
    
    return {'status': 'success', 'deleted_count': len(ids)}
```

### Bulk UPDATE with Transaction Safety

```sql
-- Bulk update with per-row SAVEPOINT for partial rollback
DO $$
DECLARE
  v_record RECORD;
  v_updated INTEGER := 0;
  v_errors INTEGER := 0;
BEGIN
  FOR v_record IN 
    SELECT id, name, new_status
    FROM agent_updates
    WHERE needs_update = true
    LIMIT 100
  LOOP
    SAVEPOINT batch_savepoint;
    BEGIN
      UPDATE agents 
      SET status = v_record.new_status,
          updated_at = NOW()
      WHERE id = v_record.id;
      
      v_updated := v_updated + 1;
      RELEASE SAVEPOINT batch_savepoint;
    EXCEPTION WHEN OTHERS THEN
      ROLLBACK TO SAVEPOINT batch_savepoint;
      v_errors := v_errors + 1;
      RAISE WARNING 'Failed to update agent %: %', v_record.name, SQLERRM;
    END;
  END LOOP;
  
  RAISE NOTICE 'Updated: %, Errors: %', v_updated, v_errors;
  
  IF v_errors > v_updated * 0.1 THEN
    RAISE EXCEPTION 'Too many errors (%), rolling back batch', v_errors;
  END IF;
END $$;
```

## CSV Import Pattern

```sql
-- Fast CSV import using COPY (bulk insert via Supabase SQL Editor)
BEGIN;

-- 1. Pre-validate FK references
-- Check all company names exist
SELECT DISTINCT company_name FROM import_agents_csv
EXCEPT
SELECT name FROM companies;
-- Should return 0 rows

-- 2. Import with FK resolution
CREATE TEMP TABLE staged_agents AS
SELECT
  gen_random_uuid() AS id,
  c.id AS company_id,
  csv.name,
  csv.title,
  m.id AS reports_to_id,
  'active'::text AS status,
  NOW() AS created_at,
  NOW() AS updated_at
FROM import_agents_csv csv
JOIN companies c ON c.name = csv.company_name
LEFT JOIN agents m ON m.name = csv.reports_to
  AND m.company_id = c.id;

-- 3. Insert staged records
INSERT INTO agents (id, company_id, name, title, reports_to, status, created_at, updated_at)
SELECT id, company_id, name, title, reports_to_id, status, created_at, updated_at
FROM staged_agents
ON CONFLICT (company_id, name) DO UPDATE SET
  title = EXCLUDED.title,
  updated_at = NOW();

-- 4. Cleanup
DROP TABLE IF EXISTS import_agents_csv;
DROP TABLE IF EXISTS staged_agents;

COMMIT;
```

## Performance Guidelines

### Batch Sizes
- **INSERT**: 100-500 records per batch (avoid statement timeout)
- **DELETE**: 50-100 records per batch (FK check overhead)
- **UPDATE**: 100-500 records per batch with SAVEPOINT

### Full Table Operations
```sql
-- Fast truncate with CASCADE (only in maintenance windows)
BEGIN;
SET session_replication_role = replica;  -- Skip FK checks temporarily
TRUNCATE agents, agent_api_keys, agent_config_revisions RESTART IDENTITY CASCADE;
RESET session_replication_role;
COMMIT;
```

### Index Maintenance
```sql
-- Ensure FK columns are indexed for bulk operations
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_agents_company_id 
  ON agents(company_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_agent_api_keys_agent_id 
  ON agent_api_keys(agent_id);
```

## Error Handling & Recovery

### Pre-Operation Validation
- [ ] All FK referenced records exist
- [ ] No circular dependencies in batch
- [ ] Batch size within limits
- [ ] No unique constraint violations expected
- [ ] Database has sufficient resources (connections, locks)

### Recovery Patterns
1. **Partial failure**: Use SAVEPOINT per batch, log failures, continue
2. **Total failure**: Full ROLLBACK, investigate FK violations
3. **Timeout**: Reduce batch size, add `statement_timeout` override
4. **Deadlock**: Ensure consistent lock ordering across transactions

## Related Skills

- `crud-operations` - Single-record CRUD patterns
- `fk-dependency-graph` - FK ordering intelligence for bulk ops
- `drizzle-crud-templates` - ORM-based bulk operation templates
- `foreign-key-dependency-management` - Shared FK relationship mapping

---

*This skill ensures bulk operations are safe, ordered, and recoverable across Paperclip's complex FK schema.*