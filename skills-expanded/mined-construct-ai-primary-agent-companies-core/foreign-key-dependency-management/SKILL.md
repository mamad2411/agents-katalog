---
name: foreign-key-dependency-management
description: >
  Routes tasks related to foreign key dependencies, FK constraint violations,
  cascade deletes, and database dependency management to agents with appropriate
  database schema and deletion workflow expertise.
triggers:
  - "foreign key"
  - "fk constraint"
  - "cascade delete"
  - "delete order"
  - "dependency levels"
  - "referential integrity"
  - "orphan records"
  - "constraint violation"
  - "fk dependency"
---

# Foreign Key Dependency Management Skill

## Purpose

This skill provides comprehensive knowledge of the Paperclip database's foreign key dependencies and the correct procedures for safe deletion and insertion operations.

## Core Knowledge

### Actual Tables Referencing `agents.id`

Based on `packages/db/src/schema/index.ts`:

| Table | FK Column | Notes |
|-------|-----------|-------|
| `heartbeat_runs` | `agent_id` | |
| `heartbeat_run_events` | `run_id` → `heartbeat_runs.id` | Chained FK |
| `agent_task_sessions` | `agent_id` | |
| `execution_workspaces` | `agent_id` | |
| `agent_runtime_state` | `agent_id` | |
| `agent_wakeup_requests` | `agent_id` | |
| `agent_config_revisions` | `agent_id`, `created_by_agent_id` | Multiple FKs |
| `agent_api_keys` | `agent_id` | |
| `issues` | `assignee_id` | Nullable FK |
| `agents` (self-ref) | `reports_to` | Nullable FK |
| `activity_log` | `actor_id` | Nullable FK |

**Note**: There is NO `agent_skills` or `agent_models` table in the current schema.

### Deletion Order Rules

**Critical**: Always delete from highest level (children) to lowest level (parents).

#### Agent Deletion Order (10 steps)

1. `heartbeat_run_events` → `run_id → heartbeat_runs.id` (chained)
2. `heartbeat_runs` → `agent_id → agents.id`
3. `agent_task_sessions` → `agent_id → agents.id`
4. `agent_runtime_state` → `agent_id → agents.id`
5. `agent_wakeup_requests` → `agent_id → agents.id`
6. `agent_config_revisions` → `agent_id → agents.id`, `created_by_agent_id → agents.id`
7. `agent_api_keys` → `agent_id → agents.id`
8. `agents.reports_to` → SET NULL (nullable FK, self-ref) - if column exists
9. `agents` → `company_id → companies.id`

**NOTE**: `issues.assignee_id` and `activity_log.actor_id` may NOT exist in production schema. Always wrap in DO $$ block for safety.

### Type Casting Requirement

PostgreSQL does not allow direct comparison between UUID and VARCHAR types. **Always cast to TEXT**:

```sql
-- Correct: Cast to TEXT for comparison
WHERE agent_id::TEXT IN (SELECT id FROM to_delete)

-- Incorrect: Will cause "operator does not exist" error
WHERE agent_id IN (SELECT id FROM to_delete)
```

## Standard SQL Templates

### Temp Table Pattern for Batch Deletion

```sql
-- Step 1: Create temp table of records to delete
CREATE TEMP TABLE to_delete (id TEXT);
INSERT INTO to_delete SELECT id::TEXT FROM agents WHERE [condition];

-- Step 2: Delete in correct FK order

-- 1. Delete heartbeat events (chained via heartbeat_runs)
DELETE FROM heartbeat_run_events 
WHERE run_id IN (
    SELECT hr.id::TEXT FROM heartbeat_runs hr 
    WHERE hr.agent_id::TEXT IN (SELECT id FROM to_delete)
);

-- 2. Delete heartbeat runs
DELETE FROM heartbeat_runs WHERE agent_id::TEXT IN (SELECT id FROM to_delete);

-- 3. Delete agent task sessions
DELETE FROM agent_task_sessions WHERE agent_id::TEXT IN (SELECT id FROM to_delete);

-- 4. Delete agent runtime state
DELETE FROM agent_runtime_state WHERE agent_id::TEXT IN (SELECT id FROM to_delete);

-- 5. Delete agent wakeup requests
DELETE FROM agent_wakeup_requests WHERE agent_id::TEXT IN (SELECT id FROM to_delete);

-- 6. Delete agent config revisions (both FKs)
DELETE FROM agent_config_revisions 
WHERE agent_id::TEXT IN (SELECT id FROM to_delete)
   OR created_by_agent_id::TEXT IN (SELECT id FROM to_delete);

-- 7. Delete agent API keys
DELETE FROM agent_api_keys WHERE agent_id::TEXT IN (SELECT id FROM to_delete);

-- 8. Clear self-referential nullable FK (agents.reports_to)
-- NOTE: issues.assignee_id and activity_log.actor_id may NOT exist - use safe DO block
DO $$ BEGIN
    UPDATE agents SET reports_to = NULL WHERE reports_to::TEXT IN (SELECT id FROM to_delete);
EXCEPTION WHEN undefined_column THEN
    RAISE NOTICE 'Column reports_to does not exist, skipping';
END $$;

-- 9. Delete the agents
DELETE FROM agents WHERE id::TEXT IN (SELECT id FROM to_delete);

-- Cleanup
DROP TABLE to_delete;
```

### Duplicate Agent Removal Pattern

```sql
-- Find duplicates
SELECT name, company_id, COUNT(*) as cnt
FROM agents GROUP BY name, company_id HAVING COUNT(*) > 1;

-- Create temp table keeping most recent
CREATE TEMP TABLE duplicates_to_delete (id TEXT);
INSERT INTO duplicates_to_delete
SELECT id::TEXT FROM (
    SELECT id, updated_at,
           ROW_NUMBER() OVER (PARTITION BY name, company_id ORDER BY updated_at DESC) as rn
    FROM agents
) ranked WHERE rn > 1;

-- Execute deletion using the template above
```

## Common Errors and Solutions

### Error: "relation does not exist"

**Cause**: Table name incorrect or table doesn't exist in schema  
**Solution**: Verify table exists in `packages/db/src/schema/index.ts`

### Error: "violates foreign key constraint"

**Cause**: Deleting parent before children  
**Solution**: Add the missing level to deletion order

### Error: "operator does not exist: uuid = varchar"

**Cause**: Mixed UUID/VARCHAR types in comparison  
**Solution**: Cast to TEXT: `column::TEXT IN (...)`

### Error: "null value in column violates not-null constraint"

**Cause**: FK column doesn't allow NULL but parent deleted  
**Solution**: Update child records to NULL before deletion:
```sql
UPDATE issues SET assignee_id = NULL WHERE assignee_id::TEXT IN (SELECT id FROM to_delete);
```

## Reference Documentation

- `docs-paperclip/schema/constraints/FK-DEPENDENCY-LEVELS.md` - Complete FK dependency hierarchy
- `docs-paperclip/schema/constraints/foreign-keys.md` - Detailed FK constraint mappings
- `docs-paperclip/procedures/agents/fk-deletion-procedure.md` - Detailed deletion procedure
- `packages/db/src/schema/index.ts` - Source of truth for actual table names

## Related Skills

- `agent-creation-management` - For agent lifecycle including creation and deletion
- `database-schema-inspection` - For querying actual database structure
- `sql-generation` - For generating compliant SQL scripts
- `duplicate-prevention` - For identifying and handling duplicate records
