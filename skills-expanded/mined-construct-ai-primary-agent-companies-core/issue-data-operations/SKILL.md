---
name: issue-data-operations
description: Routes database operations on issue tables (issues and 12 related tables) to Database Druid for FK-safe CRUD, bulk operations, deletions, and data migrations.
company: paperclipforge-ai
---

# Issue Data Operations

## Overview
This skill routes all database-level operations on the issue table ecosystem to the Database Druid agent. It handles FK-safe operations across the 13 issue-related tables in the Paperclip database, ensuring data integrity and referential consistency.

## Routing Criteria

Route to this skill when:
- **Bulk deletions** of issues or issue-related data
- **Data migrations** involving issue tables
- **FK-safe operations** across issue table relationships
- **Database cleanup** of orphaned issue records
- **Schema modifications** to issue tables
- **Performance optimization** of issue queries
- **Data integrity checks** across issue relationships
- **Backup and recovery** operations for issue data

## Issue Table Ecosystem (13 Tables)

### Core Table
1. **issues** - Main issue tracking table

### Relationship Tables
2. **issue_approvals** - Approval workflows for issues
3. **issue_attachments** - File attachments on issues
4. **issue_comments** - Comments and discussions
5. **issue_documents** - Document links
6. **issue_execution_decisions** - Agent execution decisions
7. **issue_inbox_archives** - Inbox management
8. **issue_labels** - Label/tag assignments
9. **issue_read_states** - Read/unread tracking
10. **issue_reference_mentions** - Cross-issue references
11. **issue_relations** - Issue relationships (blocks, depends on, etc.)
12. **issue_thread_interactions** - Thread/conversation tracking
13. **issue_work_products** - Work artifacts produced

## FK Dependency Map

### Tables Referencing Issues (Direct FKs)
- **cost_events** → issues.id (NO ACTION)
- **finance_events** → issues.id (NO ACTION)
- **feedback_votes** → issues.id (NO ACTION)
- **feedback_exports** → issues.id (CASCADE)
- **execution_workspaces** → issues.id (SET NULL)
- **workspace_runtime_services** → issues.id (SET NULL)
- **routine_runs** → issues.id (SET NULL)
- **routines** → issues.id (SET NULL)

### Self-Referencing FK
- **issues.parent_id** → issues.id (NO ACTION)

### Heartbeat Run Dependencies
Issues reference heartbeat_runs via:
- **checkout_run_id** (SET NULL)
- **execution_run_id** (SET NULL)

Multiple tables reference heartbeat_runs that are linked to issues, requiring cascading SET NULL operations.

## Required Procedures

**All agents using this skill MUST follow:**
- **SQL Generation Procedure**: `/docs-paperclip/procedures/database/sql-generation-procedure.md`
- **Schema Documentation**: `/docs-paperclip/schema/issues-schema.md`
- **FK Relationships**: `/docs-paperclip/schema/FK table relationships.csv`
- **Backup Procedures**: `/docs-paperclip/procedures/database/database-backup-recovery-procedure.md`

## Capabilities

### FK-Safe Deletion Operations
- **Single Issue Deletion**: Delete one issue with all child records
- **Bulk Issue Deletion**: Delete multiple issues by criteria
- **Complete Issue Purge**: Delete all issues from database
- **Orphan Cleanup**: Remove orphaned issue-related records
- **Cascade Analysis**: Identify all records affected by deletion

### Data Migration Operations
- **Issue Data Export**: Extract issue data for backup/migration
- **Issue Data Import**: Bulk import with FK validation
- **Schema Migration**: Modify issue table structures safely
- **Data Transformation**: Convert issue data formats
- **Relationship Rebuilding**: Reconstruct issue relationships after migration

### CRUD Operations
- **Bulk Insert**: Create multiple issues with FK validation
- **Bulk Update**: Update issue fields across multiple records
- **Conditional Delete**: Delete issues matching specific criteria
- **Relationship Management**: Create/update/delete issue relationships
- **Status Transitions**: Bulk status updates with validation

### Data Integrity Operations
- **FK Validation**: Verify all foreign key relationships
- **Orphan Detection**: Find records without valid parent references
- **Circular Reference Detection**: Identify circular parent_id chains
- **Constraint Verification**: Check all database constraints
- **Data Consistency Checks**: Validate business rule compliance

### Performance Operations
- **Index Analysis**: Identify missing or inefficient indexes
- **Query Optimization**: Optimize slow issue queries
- **Partition Management**: Manage table partitioning for large datasets
- **Statistics Update**: Refresh query planner statistics
- **Vacuum Operations**: Reclaim storage and update statistics

## Operation Templates

### Delete All Issues (FK-Safe)
```sql
-- See: /docs-paperclip/sql/delete-all-issues.sql
-- 5-phase deletion:
-- 1. SET NULL for nullable FKs
-- 2. DELETE child records
-- 3. Clear self-referencing parent_id
-- 4. DELETE all issues
-- 5. Verify deletion
```

### Delete Issues by Criteria
```sql
-- Delete issues matching specific conditions
DO $$
DECLARE
    target_issues UUID[];
BEGIN
    -- Identify target issues
    SELECT ARRAY_AGG(id) INTO target_issues
    FROM issues
    WHERE status = 'cancelled' 
      AND cancelled_at < NOW() - INTERVAL '90 days';
    
    -- Phase 1: SET NULL for nullable FKs
    UPDATE execution_workspaces 
    SET source_issue_id = NULL 
    WHERE source_issue_id = ANY(target_issues);
    
    -- Phase 2: DELETE child records
    DELETE FROM issue_comments WHERE issue_id = ANY(target_issues);
    DELETE FROM issue_attachments WHERE issue_id = ANY(target_issues);
    -- ... (all child tables)
    
    -- Phase 3: Clear parent references
    UPDATE issues SET parent_id = NULL WHERE parent_id = ANY(target_issues);
    
    -- Phase 4: DELETE target issues
    DELETE FROM issues WHERE id = ANY(target_issues);
    
    RAISE NOTICE 'Deleted % issues', array_length(target_issues, 1);
END $$;
```

### Orphan Cleanup
```sql
-- Find and remove orphaned issue-related records
DO $$
DECLARE
    orphan_count INTEGER;
BEGIN
    -- Find issue_comments without valid issue_id
    DELETE FROM issue_comments
    WHERE issue_id NOT IN (SELECT id FROM issues);
    GET DIAGNOSTICS orphan_count = ROW_COUNT;
    RAISE NOTICE 'Deleted % orphaned comments', orphan_count;
    
    -- Repeat for all child tables
    DELETE FROM issue_attachments
    WHERE issue_id NOT IN (SELECT id FROM issues);
    GET DIAGNOSTICS orphan_count = ROW_COUNT;
    RAISE NOTICE 'Deleted % orphaned attachments', orphan_count;
    
    -- ... (all child tables)
END $$;
```

### Bulk Status Update
```sql
-- Update issue status with validation
DO $$
DECLARE
    updated_count INTEGER;
BEGIN
    -- Validate transition is allowed
    UPDATE issues
    SET status = 'done',
        completed_at = NOW(),
        updated_at = NOW()
    WHERE status = 'in_progress'
      AND assignee_agent_id IS NOT NULL
      AND id IN (
          -- Only issues with all work products completed
          SELECT i.id FROM issues i
          LEFT JOIN issue_work_products iwp ON i.id = iwp.issue_id
          GROUP BY i.id
          HAVING COUNT(iwp.id) > 0
      );
    
    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RAISE NOTICE 'Updated % issues to done', updated_count;
END $$;
```

## Data Integrity Checks

### FK Validation Query
```sql
-- Verify all FK relationships are valid
SELECT 
    'issue_comments' AS table_name,
    COUNT(*) AS orphaned_records
FROM issue_comments
WHERE issue_id NOT IN (SELECT id FROM issues)
UNION ALL
SELECT 'issue_attachments', COUNT(*)
FROM issue_attachments
WHERE issue_id NOT IN (SELECT id FROM issues)
-- ... (repeat for all child tables)
HAVING COUNT(*) > 0;
```

### Circular Reference Detection
```sql
-- Find circular parent_id chains
WITH RECURSIVE issue_hierarchy AS (
    SELECT id, parent_id, ARRAY[id] AS path, 1 AS depth
    FROM issues
    WHERE parent_id IS NOT NULL
    
    UNION ALL
    
    SELECT i.id, i.parent_id, ih.path || i.id, ih.depth + 1
    FROM issues i
    JOIN issue_hierarchy ih ON i.parent_id = ih.id
    WHERE NOT (i.id = ANY(ih.path))  -- Prevent infinite recursion
      AND ih.depth < 100
)
SELECT id, parent_id, path, depth
FROM issue_hierarchy
WHERE id = ANY(path[1:array_length(path, 1)-1])  -- Circular reference detected
ORDER BY depth DESC;
```

## Performance Optimization

### Index Recommendations
```sql
-- Analyze query patterns and recommend indexes
SELECT 
    schemaname,
    tablename,
    attname AS column_name,
    n_distinct,
    correlation
FROM pg_stats
WHERE tablename LIKE 'issue%'
  AND n_distinct > 100  -- High cardinality columns
  AND correlation < 0.5  -- Low correlation (good index candidates)
ORDER BY tablename, n_distinct DESC;
```

### Query Performance Analysis
```sql
-- Identify slow queries on issue tables
SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
WHERE query LIKE '%issues%'
  AND mean_exec_time > 100  -- Queries taking >100ms on average
ORDER BY mean_exec_time DESC
LIMIT 20;
```

## Related Skills

- `sql-generation` - SQL script generation for verified operations
- `crud-operations` - FK-safe CRUD operation patterns
- `database-schema-inspection` - Schema analysis and validation
- `bulk-operations` - FK-safe bulk operation patterns
- `fk-dependency-graph` - Detailed FK graph analysis

## Coordination with Other Agents

### Issue Generator (`paperclipforge-ai-issuegenerator`)
- **Database Druid**: Handles bulk issue creation at database level
- **Issue Generator**: Manages issue lifecycle and workflow

### Assignment Specialist (`paperclipforge-ai-assignmentspecialist`)
- **Database Druid**: Performs bulk assignment updates
- **Assignment Specialist**: Manages assignment logic and validation

### Issue Batch Importer (`issue-batch-importer-paperclipforge`)
- **Database Druid**: Provides FK-safe import templates
- **Batch Importer**: Orchestrates import workflow

## Quality Metrics

### Operation Safety
- **FK Compliance**: 100% of operations respect FK constraints
- **Transaction Safety**: 100% of operations wrapped in transactions
- **Rollback Capability**: 100% of operations have documented rollback procedures
- **Validation Coverage**: 100% of operations include pre/post validation

### Performance Standards
- **Bulk Operations**: Process >1000 records/second
- **Query Optimization**: Reduce slow queries by >50%
- **Index Efficiency**: Improve query performance by >80%
- **Storage Efficiency**: Reclaim >90% of orphaned storage

## Training Requirements

### Required Knowledge
- Complete understanding of issue table ecosystem (13 tables)
- FK dependency graph and cascade rules
- PostgreSQL transaction management
- Query optimization techniques
- Backup and recovery procedures

### Certification
- Issue table schema proficiency test
- FK-safe deletion procedure validation
- Bulk operation safety assessment
- Performance optimization competency

---

*This skill ensures all database operations on issue tables are FK-safe, performant, and maintain data integrity across the complex issue table ecosystem.*
