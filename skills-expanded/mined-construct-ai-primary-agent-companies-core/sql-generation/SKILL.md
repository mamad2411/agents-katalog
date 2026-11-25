---
name: sql-generation
description: Routes SQL script generation tasks to agents that follow the systematic SQL generation procedure for accurate database operations.
company: paperclipforge-ai
---

# SQL Generation

## Overview
This skill routes all SQL script generation tasks to agents that are required to follow the comprehensive SQL Generation Procedure. This ensures systematic, accurate, and validated SQL generation for all Paperclip database operations.

## Routing Criteria

Route to this skill when:
- SQL script generation is required for database operations
- Database schema modifications or data migrations
- Agent creation or management SQL scripts
- Complex database transactions or stored procedures
- Data validation or integrity checking scripts
- Backup or recovery SQL operations
- Any database operation requiring precise SQL syntax

## Required Procedures

**MANDATORY: All agents using this skill MUST follow:**
- **SQL Generation Procedure**: `/docs-paperclip/procedures/database/sql-generation-procedure.md`
- **Schema Documentation**: `/docs-paperclip/schema/` for all table and column references
- **Database Backup Procedures**: `/docs-paperclip/procedures/database/database-backup-recovery-procedure.md`

## SQL Templates (Required for Agent Operations)

**For agent-related SQL, use pre-validated templates from `docs-paperclip/schema/templates/`:**

| Template | Purpose | When to Use |
|---------|--------|-------------|
| `CHECK-column-existence.sql` | Schema validation | **Run FIRST** before any SQL |
| `VALIDATE-agent-exists.sql` | Agent verification | Before UPDATE/DELETE |
| `REGISTER-agent.sql` | Create new agents | Agent registration |
| `UPDATE-agent-title.sql` | Fix human names | Name corrections |
| `ADD-agent-api-keys.sql` | Add API keys | Key management |
| `DELETE-agent.sql` | Safe deletion | Agent removal |

**⚠️ CRITICAL SCHEMA WARNING**:
The `agents` table has TWO name fields:
- `name` = agent identifier (e.g., "infraforge-ai-supabase-specialist")
- `title` = human-readable name (e.g., "Supabase DB Specialist")

**Never use `slug`** - this column does NOT exist in the schema!

```sql
-- ✅ CORRECT:
UPDATE agents SET title = 'New Name' WHERE name = 'infraforge-ai-agent';

-- ❌ WRONG:
UPDATE agents SET slug = 'New Name' WHERE ...  -- 'slug' does NOT exist!
```

## Compliance Requirements

### Pre-Generation Checklist
- [ ] Reviewed relevant schema documentation in `/docs-paperclip/schema/`
- [ ] Verified all table and column names against actual database
- [ ] Checked foreign key relationships and constraints
- [ ] Confirmed PostgreSQL function availability
- [ ] Planned transaction boundaries and error handling

### Generation Standards
- [ ] Used verified column names (snake_case, not camelCase)
- [ ] Implemented proper foreign key constraint handling
- [ ] Applied correct PostgreSQL data types and functions
- [ ] Included transaction safety and rollback procedures
- [ ] Added comprehensive error handling

### Validation Requirements
- [ ] Syntax validation completed
- [ ] Schema compatibility verified
- [ ] Logic testing performed on development environment
- [ ] Performance implications assessed
- [ ] Rollback procedures documented

### Error Logging for LearningForge Integration

**IMPORTANT**: All SQL generation errors MUST be logged to activity_log for LearningForge AI error pattern monitoring.

When any of these errors occur, log to activity_log with proper error categorization:

```sql
-- Log SQL generation errors
INSERT INTO activity_log (
  id, company_id, actor_type, actor_id, action, entity_type, entity_id, details, created_at
) VALUES (
  gen_random_uuid(),
  (SELECT id FROM companies WHERE name = 'PaperclipForge AI'),
  'agent',
  'paperclipforge-ai-sql-generation',
  'error',
  'agent',
  NULL,
  '{
    "error_type": "sql_column_mismatch",
    "error_message": "Column X does not exist",
    "context": "SQL generation for [operation]",
    "remediation": "Use CHECK-column-existence.sql template"
  }'::jsonb,
  NOW()
);
```

### Error Categories for Logging

| Error Type | details->>'error_type' | Threshold |
|------------|------------------------|-----------|
| Column name mismatch | `sql_column_mismatch` | 3+ |
| FK constraint violation | `fk_violation` | 2+ |
| Naming violation | `naming_violation` | 5+ |
| Template bypass | `workflow_bypass` | 2+ |

### Integration with LearningForge AI

The `learningforge-ai-error-pattern-monitor` agent monitors activity_log for these error patterns and creates alerts when thresholds are exceeded.

## Capabilities

### SQL Script Generation
- **Schema-Driven Generation**: All SQL based on verified schema documentation
- **Transaction Management**: Proper transaction boundaries and isolation levels
- **Error Handling**: Comprehensive error trapping and recovery
- **Performance Optimization**: Efficient query structures and indexing considerations
- **Data Integrity**: Constraint validation and referential integrity maintenance

### Database Operation Types
- **Data Manipulation**: INSERT, UPDATE, DELETE operations with proper constraints
- **Schema Modifications**: ALTER TABLE, CREATE INDEX with migration safety
- **Bulk Operations**: Efficient batch processing with error recovery
- **Complex Transactions**: Multi-table operations with rollback capabilities
- **Data Validation**: Integrity checks and business rule enforcement

### Quality Assurance
- **Syntax Validation**: Automated SQL syntax checking
- **Schema Compatibility**: Verification against live database structure
- **Logic Testing**: Business logic validation and edge case handling
- **Performance Testing**: Query optimization and resource usage analysis
- **Documentation**: Comprehensive script headers and usage instructions

## Procedure Integration

### Phase 1: Requirements Analysis
- Define operation scope and data dependencies
- Review schema documentation for all referenced tables
- Identify foreign key relationships and cascading effects
- Assess transaction requirements and isolation levels

### Phase 2: SQL Development
- Use verified column names from schema documentation
- Implement proper constraint handling and validation
- Apply correct PostgreSQL functions and data types
- Structure transactions with appropriate error handling

### Phase 3: Validation & Testing
- Perform syntax validation and schema compatibility checks
- Test logic on development environment with sample data
- Analyze performance implications and optimization opportunities
- Document rollback procedures and failure recovery

### Phase 4: Documentation & Review
- Include comprehensive script headers with all metadata
- Document dependencies, prerequisites, and post-conditions
- Provide clear rollback and recovery instructions
- Undergo peer review for schema compliance and logic validation

### Phase 5: Deployment & Monitoring
- Execute pre-deployment validation checks
- Monitor script execution with proper logging
- Perform post-deployment data integrity verification
- Document execution results and any issues encountered

## Common SQL Patterns

### Agent Creation Template
```sql
-- Follow SQL Generation Procedure Phase 2.4: Transaction Safety
DO $$
DECLARE
  company_id UUID;
  agent_id UUID;
BEGIN
  -- Phase 1.2: Review Schema Documentation
  -- Verified: companies.name, agents table structure

  -- Get company ID safely (Phase 2.2: Handle Foreign Key Constraints)
  SELECT id INTO company_id
  FROM companies
  WHERE name = 'Target Company Name'
    AND status = 'active';

  IF company_id IS NULL THEN
    RAISE EXCEPTION 'Company not found or not active';
  END IF;

  -- Check for existing agent (Phase 2.2: Constraint Handling)
  IF EXISTS (SELECT 1 FROM agents WHERE name = 'Agent Name') THEN
    RAISE NOTICE 'Agent already exists, skipping creation';
    RETURN;
  END IF;

  -- Create agent with verified column names (Phase 2.1: Verified Column Names)
  INSERT INTO agents (
    id, company_id, name, role, title, status,
    adapter_type, adapter_config, runtime_config,
    permissions, created_at, updated_at
  ) VALUES (
    gen_random_uuid(), company_id, 'Agent Name', 'agent-role', 'Agent Title', 'active',
    'process', '{"model": "glm-5.1"}'::jsonb, '{"config": "data"}'::jsonb,
    '{"permissions": "data"}'::jsonb, NOW(), NOW()
  ) RETURNING id INTO agent_id;

  -- Log creation (Phase 4.1: Documentation)
  INSERT INTO activity_log (
    company_id, actor_type, actor_id, action, entity_type, entity_id, agent_id, details, created_at
  ) VALUES (
    company_id, 'system', 'atlas-agent-creator', 'create', 'agent', agent_id, agent_id,
    '{"description": "Agent created via SQL Generation Procedure"}'::jsonb, NOW()
  );

  RAISE NOTICE 'Agent created successfully with ID: %', agent_id;
END $$;
```

### Data Migration Template
```sql
-- Data migration with transaction safety and error handling
DO $$
DECLARE
  migrated_count INTEGER := 0;
  error_count INTEGER := 0;
BEGIN
  -- Phase 1.3: Identify Dependencies - Check source and target tables exist

  -- Create savepoint for rollback capability
  SAVEPOINT migration_start;

  -- Process migration in batches for safety
  FOR record IN SELECT * FROM source_table WHERE migrated = false LIMIT 1000 LOOP
    BEGIN
      -- Phase 2.3: Use Proper Data Types and Functions
      INSERT INTO target_table (
        id, company_id, name, status, created_at, updated_at
      ) VALUES (
        gen_random_uuid(),
        record.company_id,
        record.name,
        COALESCE(record.status, 'active'),
        COALESCE(record.created_at, NOW()),
        NOW()
      );

      -- Mark as migrated
      UPDATE source_table SET migrated = true, migrated_at = NOW()
      WHERE id = record.id;

      migrated_count := migrated_count + 1;

    EXCEPTION WHEN OTHERS THEN
      error_count := error_count + 1;

      -- Log error but continue (Phase 3.3: Logic Testing)
      UPDATE source_table SET migration_error = SQLERRM, migrated_at = NOW()
      WHERE id = record.id;

      -- Continue processing other records
    END;
  END LOOP;

  -- Phase 5.3: Post-Deployment Validation
  RAISE NOTICE 'Migration completed: % migrated, % errors', migrated_count, error_count;

  -- Rollback on excessive errors (Phase 5.4: Incident Response)
  IF error_count > migrated_count * 0.1 THEN
    ROLLBACK TO SAVEPOINT migration_start;
    RAISE EXCEPTION 'Migration failed: too many errors (%)', error_count;
  END IF;

  -- Commit successful migration
  COMMIT;
END $$;
```

## Error Prevention

### Schema Reference Discipline
- **Always consult schema documentation first**
- **Never assume column names or data types**
- **Verify foreign key constraints exist and are correct**
- **Test with actual database before production deployment**

### Transaction Safety
- **Use explicit transactions for multi-step operations**
- **Implement proper savepoints for partial rollback**
- **Test transaction behavior under failure conditions**
- **Document transaction boundaries and isolation requirements**

### Data Integrity
- **Validate all input data before insertion**
- **Implement constraint checking in application logic**
- **Use database constraints as final safety net**
- **Test edge cases and boundary conditions thoroughly**

## Quality Metrics

### Generation Quality
- **Schema Compliance**: 100% of generated SQL uses verified schema references
- **Syntax Accuracy**: 0 syntax errors in production deployments
- **Constraint Adherence**: 100% foreign key and constraint compliance
- **Function Compatibility**: 100% use of available PostgreSQL functions

### Process Efficiency
- **Development Time**: Average time to generate and validate SQL scripts
- **Review Cycle Time**: Time from generation to approval
- **Error Detection**: Percentage of errors caught in validation phase
- **Deployment Success**: Percentage of successful SQL deployments

## Related Skills

- `database-schema-inspection` - Schema analysis and validation
- `agent-creation-management` - Agent lifecycle SQL operations
- `nimbus-infraforge-supabase-specialist` - Database execution and monitoring

## Training Requirements

### Required Knowledge
- Complete PostgreSQL syntax and function reference
- Paperclip database schema structure and relationships
- Transaction management and isolation levels
- SQL performance optimization techniques

### Certification
- SQL Generation Procedure compliance test
- Schema documentation navigation assessment
- PostgreSQL function and data type proficiency
- Transaction safety and error handling validation

---

*This skill ensures all SQL generation follows systematic procedures for accuracy, safety, and maintainability.*