---
name: agent-reconciliation
description: >
  Audit filesystem agent definitions against database registrations
  (agents, agent_models, agent_api_keys tables). Identify missing
  registrations, invalid human names, and naming convention
  violations. Generate SQL fixes via collaboration with Database Druid
  and SQL experts. Also handles human name standardization and folder
  name alignment per AGENT-NAMING-STANDARD.md.
triggers:
  - agent reconciliation request
  - filesystem database audit
  - missing agent detection
  - naming convention validation
  - human name check
  - agent table reconciliation
  - database agent integrity check
  - rename agent folders
  - align folder names with human names
  - standardize agent human names
  - fix agent folder names
  - fresh reconciliation
  - full agent sync
  - sync agents to database
  - generate reconciliation SQL
---

# Agent Reconciliation Skill

## Overview

This skill enables systematic reconciliation between the filesystem agent definitions (AGENTS.md files under `docs-paperclip/companies/*/agents/`) and the database tables that power the Paperclip control plane (`agents`, `agent_models`, `agent_api_keys`).

## Trigger Conditions

- User asks to "reconcile agents"
- User asks to "check agents against database"
- User asks to "verify agent registrations"
- User asks to "audit agent names" or "check funky human names"
- User asks to "validate naming conventions"
- User asks to "find missing agents" or "find extra agents"
- User asks to "generate agent fix SQL"

## Execution Workflow

### Fresh Reconciliation Workflow (Recommended for Full Sync)

When doing a **complete sync** of all agents from filesystem to database:

1. **Run `fresh_reconciliation.py`**
   ```bash
   python3 fresh_reconciliation.py
   ```
   This will:
   - Scan all filesystem agents
   - Generate `fresh_reconciliation.sql` (DELETE + INSERT statements)
   - Generate `fresh_reconciliation_summary.json`
   - Warn that it will DELETE existing data

2. **Review Generated SQL**
   - Open `fresh_reconciliation.sql`
   - Verify DELETE statement targets correct tables
   - Verify INSERT statements have correct column values
   - Check for any unexpected DELETE operations

3. **Execute Against Database** (with user approval)
   ```bash
   # Apply the SQL (this DELETES all existing agents first!)
   psql $DATABASE_URL -f fresh_reconciliation.sql
   ```

4. **Post-Execution Verification**
   - Query agents table count
   - Verify sample agents have correct names/titles
   - Check agent_api_keys were created
   - Verify agent_models assignments

### Step 0: Schema Validation (MANDATORY)

Before generating ANY SQL, you MUST validate the schema:

1. **Run CHECK-column-existence.sql** template from `docs-paperclip/schema/templates/`
   ```sql
   SELECT column_name, data_type 
   FROM information_schema.columns 
   WHERE table_name = 'agents' 
   ORDER BY ordinal_position;
   ```

2. **Verify template compatibility** - Compare results against expected columns in template header comments

3. **CRITICAL**: The `agents` table has TWO name fields:
   - `name` = human-readable name (e.g., "SEO Strategist", "DB Specialist")
   - `title` = agent identifier/slug (e.g., "contentforge-ai-SEOStrategist")
   
   **DO NOT confuse `name` with `slug` - `slug` does NOT exist in the schema!**
   
   **CORRECT MAPPING**:
   ```sql
   -- ✅ CORRECT:
   INSERT INTO agents (name, title, ...) VALUES ('SEO Strategist', 'contentforge-ai-SEOStrategist', ...);
   
   -- ❌ WRONG - name should be human-readable, not the slug:
   INSERT INTO agents (name, title, ...) VALUES ('contentforge-ai-SEOStrategist', 'SEO Strategist', ...);
   ```

### Step 1: Filesystem Discovery
1. Scan `docs-paperclip/companies/{company}/agents/**/AGENTS.md`
2. Parse YAML frontmatter for each agent
3. Extract: `name`, `slug`, `reportsTo`, `team`, `skills`
4. Record directory name for naming convention checks
5. Build filesystem agent index

### Step 2: Database Discovery
1. Query `companies` table → map name to `id`
2. Query `agents` table → all rows with `id`, `name`, `title`, `company_id`, `role`, `reports_to`, `status`
3. Query `agent_models` table → active model assignments by `agent_id` (TEXT type)
4. Query `agent_api_keys` table → API keys by `agent_id` (UUID type)
5. Build database agent index

### Step 3: Reconciliation Match
1. Match filesystem agents to database agents by `name` ↔ `name`
2. Identify **missing agents**: in filesystem, not in database
3. Identify **extra agents**: in database, not in filesystem
4. Identify **agents without API keys**
5. Identify **agents without model assignments**
6. Identify **invalid human names**: `title` ≥23 characters or invalid characters
7. Identify **naming convention violations**: directory doesn't follow `{company-slug}-{AgentName}`

### Step 4: SQL Fix Generation (Using Templates)

**ALWAYS use templates from `docs-paperclip/schema/templates/` as the source of truth.**

| Issue Type | Template to Use |
|------------|-----------------|
| Missing agent | `REGISTER-agent.sql` |
| Fix agent title (human name) | `UPDATE-agent-title.sql` |
| Add API key | `ADD-agent-api-keys.sql` |
| Delete agent | `DELETE-agent.sql` |
| Validate before modify | `VALIDATE-agent-exists.sql` |

**IMPORTANT**: For agent title/human name fixes, use `title` NOT `slug`:
```sql
-- ✅ CORRECT:
UPDATE agents SET title = 'Procurement' WHERE name = 'domainforge-ai-domainforge-ai-procurement';

-- ❌ WRONG - 'slug' column does NOT exist:
UPDATE agents SET slug = 'Procurement' WHERE ...
```

### Step 5: Collaboration Delegation
- **Complex schema queries** → delegate to `paperclipforge-ai-database-druid`
- **Agent creation logic** → delegate to `paperclipforge-ai-atlas-agent-creator`
- **Model assignment logic** → delegate to `paperclipforge-ai-model-assignment-specialist`

### Step 6: Report Output
- Save SQL to `reconciliation_fixes.sql`
- Save JSON report to `reconciliation_report.json`
- Print summary with counts per company

## SQL Template Location

All SQL generation MUST use templates from:
```
docs-paperclip/schema/templates/
```

Template files:
- `README.md` - Template registry documentation
- `CHECK-column-existence.sql` - Schema validation (run FIRST)
- `VALIDATE-agent-exists.sql` - Pre-modification validation
- `REGISTER-agent.sql` - Create new agents
- `UPDATE-agent-title.sql` - Fix human names (title field)
- `DELETE-agent.sql` - Safe deletion with FK cascade
- `ADD-agent-api-keys.sql` - Add API keys

## Single Source of Truth

The authoritative schema is in `packages/db/src/schema/*.ts`. Templates are validated against this source.
If template columns don't match actual schema, run `CHECK-column-existence.sql` and update template accordingly.

## Naming Convention Rules

### Human Name (Canonical Location: AGENTS.md YAML frontmatter)
- **Field**: `human_name` in AGENTS.md YAML frontmatter
- **Must be <23 characters**
- **Allowed characters**: `a-z`, `A-Z`, `0-9`, spaces, hyphens, underscores
- **Should be human-readable** (e.g., "Nexus", "Dataforge", "Recon")
- **Reference**: See `docs-paperclip/companies/shared/AGENT-NAMING-STANDARD.md`

### Directory Name
- Pattern: `{company-slug}-{HumanNameWithoutSpaces}`
- Examples: `devforge-ai-Nexus`, `measureforge-ai-CadOrchestrator`
- Must match the company slug prefix
- **Folder suffix should match `human_name` with spaces removed**

### File Name
- Always `AGENTS.md`
- Always inside the agent directory

## Directory Name Alignment Workflow

When user asks to "align folder names with human names" or "rename agent folders":

### Step 1: Scan All Agents
1. Scan `docs-paperclip/companies/*/agents/**/AGENTS.md`
2. Extract `human_name` from YAML frontmatter
3. Record current folder name

### Step 2: Identify Mismatches
For each agent:
- Expected folder: `{company-slug}-{human_name_without_spaces}`
- If current folder doesn't match expected → flag for rename

### Step 3: Generate Rename Commands
```bash
mv "old-folder-name" "expected-folder-name"
```

### Step 4: Execute Renames (with user confirmation)
- Present dry-run first showing all planned renames
- Execute only after user approval

### Step 5: Update register-agent.sql files
After folder rename, update any `register-agent.sql` files to reference new folder path.

## Human Name Standardization Workflow

When user asks to "standardize human names" or "fix agent human names":

### Step 1: Scan All Agents
1. Find all AGENTS.md files
2. Extract current `human_name` values
3. Identify issues: missing, truncated, >22 chars

### Step 2: Fix Issues
- **Missing**: Derive from folder name (convert CamelCase to spaces)
- **Truncated**: Expand to full meaningful name (max 22 chars)
- **Too long**: Truncate intelligently, preserve key words

### Step 3: Validate
- All names <23 characters
- All names human-readable
- All names match folder suffix pattern

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `companies_dir` | string | No | Path to companies directory (default: `docs-paperclip/companies`) |
| `output_sql_path` | string | No | Path for SQL output (default: `reconciliation_fixes.sql`) |
| `output_json_path` | string | No | Path for JSON report (default: `reconciliation_report.json`) |
| `dry_run` | boolean | No | If true, only report without generating SQL |

## Output Format

### Console Summary
```
COMPANIES:
  - In filesystem: 16
  - In database: 16
AGENTS:
  - In filesystem: 496
  - In database: 548
  - Missing in database: 344
  - Extra in database: 402
  - Without API keys: 84
  - Without models: 159
VALIDATION ISSUES:
  - Invalid names: 70
  - Naming convention issues: 0
```

### JSON Report Structure
```json
{
  "companies_in_filesystem": [...],
  "companies_in_database": [...],
  "missing_companies": [...],
  "missing_agents": [{"name": "...", "slug": "...", "company": "..."}],
  "extra_agents_in_database": [{"id": "...", "name": "..."}],
  "agents_without_api_keys": [{"id": "...", "name": "..."}],
  "agents_without_models": [{"id": "...", "name": "..."}],
  "invalid_names": [{"name": "...", "reason": "..."}],
  "naming_convention_issues": [...],
  "sql_count": 657
}
```

## Error Handling

- **Missing companies directory**: Report error and exit
- **Database connection failure**: Report error with connection details
- **Malformed AGENTS.md**: Log warning, skip file, continue
- **No database agents**: Report warning but continue with filesystem scan

## Error Logging for LearningForge Integration

**IMPORTANT**: All errors MUST be logged to activity_log for LearningForge AI error pattern monitoring.

### Required Error Logging

When any of these errors occur, log to activity_log with proper error categorization:

```sql
-- Log SQL validation errors
INSERT INTO activity_log (
  id, company_id, actor_type, actor_id, action, entity_type, entity_id, details, created_at
) VALUES (
  gen_random_uuid(),
  (SELECT id FROM companies WHERE name = 'PaperclipForge AI'),
  'agent',
  'paperclipforge-ai-agent-reconciler',
  'error',
  'agent',
  NULL,
  '{
    "error_type": "sql_validation",
    "error_message": "Column slug does not exist in agents table",
    "context": "reconciliation SQL generation",
    "remediation": "Use title field instead of slug"
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

---

**Skill Name**: agent-reconciliation
**Version**: 1.0
**Owner**: paperclipforge-ai-agent-reconciler
**Created**: 2026-04-24
