---
name: database-schema-inspection
description: Routes database schema inspection and SQL generation tasks to the Atlas Agent Creator for accurate database operations.
company: paperclipforge-ai
---

# Database Schema Inspection

## Overview
This skill routes all database schema inspection and SQL generation tasks to the Atlas Agent Creator, enabling accurate database operations by querying actual table structures, column names, and constraints rather than relying on assumptions.

## Routing Criteria

Route to this skill when:
- Database schema inspection is needed for SQL generation
- Table structure validation for agent creation
- Column name verification for database operations
- Constraint and relationship analysis
- Function availability checking
- SQL syntax validation against live schema
- Database compatibility verification

## Required Procedures

**All agents using this skill MUST follow:**
- **SQL Generation Procedure**: `/docs-paperclip/procedures/database/sql-generation-procedure.md`
- **Schema Documentation**: `/docs-paperclip/schema/` for all table references
- **Backup Procedures**: `/docs-paperclip/procedures/database/database-backup-recovery-procedure.md` for data safety

## Capabilities

### Schema Inspection
- **Table Structure Analysis**: Query information_schema for actual table definitions
- **Column Metadata**: Retrieve column names, types, constraints, and defaults
- **Relationship Mapping**: Identify foreign keys and table relationships
- **Index Analysis**: Examine existing indexes and performance structures
- **Constraint Validation**: Check primary keys, unique constraints, and check constraints

### SQL Generation
- **Dynamic Query Building**: Generate SQL using real column names and functions
- **Syntax Validation**: Validate SQL against actual database capabilities
- **Function Compatibility**: Use database-specific functions (digest vs sha256, etc.)
- **Constraint Awareness**: Generate SQL that respects database constraints
- **Performance Optimization**: Create efficient queries based on actual indexes

### Database Compatibility
- **PostgreSQL Functions**: Use correct PostgreSQL functions and syntax
- **Data Type Mapping**: Ensure proper data type usage and casting
- **Transaction Safety**: Generate transaction-safe SQL operations
- **Error Handling**: Include proper error handling for database operations

## Template Reference

For SQL generation tasks, use validated templates from `docs-paperclip/schema/templates/`:

| Template | Purpose |
|---------|---------|
| `CHECK-column-existence.sql` | **Use this first** - validates table columns |
| `VALIDATE-agent-exists.sql` | Verify agents before modification |
| `REGISTER-agent.sql` | Create new agents |
| `UPDATE-agent-title.sql` | Fix agent human names |
| `ADD-agent-api-keys.sql` | Add API keys |
| `DELETE-agent.sql` | Safe deletion with FK cascade |

**⚠️ CRITICAL**: Always run `CHECK-column-existence.sql` before generating SQL to verify columns exist.

## Related Skills

- `agent-creation-management` - Agent creation with database integration
- `nimbus-infraforge-supabase-specialist` - Database operations execution
- `database-infraforge-database-infrastructure` - Database infrastructure management

## Examples

### Schema Inspection Query
```sql
-- Inspect agents table structure
SELECT
  column_name,
  data_type,
  is_nullable,
  column_default,
  character_maximum_length
FROM information_schema.columns
WHERE table_name = 'agents'
  AND table_schema = 'public'
ORDER BY ordinal_position;
```

### Dynamic SQL Generation
```sql
-- Generate INSERT using real schema
INSERT INTO agents (
  id, company_id, name, role, title, status,
  capabilities, adapter_type, adapter_config,
  runtime_config, permissions, metadata,
  created_at, updated_at
) VALUES (
  gen_random_uuid(),
  (SELECT id FROM companies WHERE name = 'PromptForge AI'),
  'Agent Name',
  'agent-role',
  'Agent Title',
  'active',
  'Capabilities description',
  'process',
  '{"model": "claude-3"}'::jsonb,
  '{"config": "data"}'::jsonb,
  '{"permissions": []}'::jsonb,
  '{"metadata": {}}'::jsonb,
  NOW(),
  NOW()
);
```

### Function Compatibility Check
```sql
-- Check available functions
SELECT
  routine_name,
  routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name LIKE '%digest%'
  OR routine_name LIKE '%encode%';
```

---

*This skill routes to Atlas for intelligent database schema inspection and accurate SQL generation, preventing schema mismatch errors.*