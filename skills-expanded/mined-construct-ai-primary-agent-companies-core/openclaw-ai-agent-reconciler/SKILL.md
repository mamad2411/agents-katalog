---
name: openclaw-ai-agent-reconciler
description: >
  Audit filesystem agent definitions (AGENTS.md) against the OpenClaw SQLite database (openclaw_agents, openclaw_agent_skills, openclaw_agent_models, openclaw_agent_capabilities tables). Identify missing registrations, extra database entries, field mismatches, and naming convention violations. Generate SQL fixes via collaboration with SQLite Manager.
triggers:
  - agent reconciliation request
  - filesystem database audit
  - missing agent detection
  - naming convention validation
  - agent table reconciliation
  - database agent integrity check
  - fresh reconciliation
  - full agent sync
  - sync agents to database
  - generate reconciliation SQL
---

# OpenClaw Agent Reconciliation Skill

## Overview

This skill enables systematic reconciliation between the filesystem agent definitions (AGENTS.md files under `agent-companies-core/agents/openclawforge-ai/agents/`) and the OpenClaw SQLite database tables (`openclaw_agents`, `openclaw_agent_skills`, `openclaw_agent_models`, `openclaw_agent_capabilities`) that power the OpenClaw control plane.

## Trigger Conditions

- User asks to "reconcile agents"
- User asks to "check agents against database"
- User asks to "verify agent registrations"
- User asks to "audit agent names"
- User asks to "validate naming conventions"
- User asks to "find missing agents" or "find extra agents"
- User asks to "generate agent fix SQL"
- User asks to "sync agents to database"

## Execution Workflow

### Step 0: Schema Validation (MANDATORY)

Before generating ANY SQL, validate the schema:

1. Query the `openclaw_agents` table schema:
   ```sql
   PRAGMA table_info(openclaw_agents);
   ```

2. Verify columns match expected from `schema/create-openclaw-tables.sql`:
   - `id`, `name`, `slug`, `role`, `reports_to`, `description`, `skills`, `company`, `status`, `adapter_type`, `adapter_config`, `runtime_config`, `budget_monthly_cents`, `spent_monthly_cents`, `last_heartbeat_at`, `capabilities`, `metadata`, `created_at`, `updated_at`

3. **CRITICAL**: The `openclaw_agents` table has:
   - `name` = human-readable agent name (e.g., "OpenClaw Agent Reconciler")
   - `slug` = agent identifier (e.g., "openclaw-ai-agent-reconciler")
   - `company` = company namespace (e.g., "openclawforge-ai")

### Step 1: Filesystem Discovery

1. Scan `agent-companies-core/agents/openclawforge-ai/agents/**/AGENTS.md`
2. Parse YAML frontmatter for each agent
3. Extract: `name`, `slug`, `reportsTo`, `role`, `description`, `skills`
4. Build filesystem agent index

### Step 2: Database Discovery

1. Query `openclaw_agents` table → all rows
2. Query `openclaw_agent_skills` table → skill assignments by `agent_id`
3. Query `openclaw_agent_models` table → model assignments by `agent_id`
4. Build database agent index

### Step 3: Reconciliation Match

1. Match filesystem agents to database agents by `slug` ↔ `slug`
2. Identify **missing agents**: in filesystem, not in database
3. Identify **extra agents**: in database, not in filesystem
4. Identify **field mismatches**: name, role, reports_to, description differences
5. Identify **missing skill assignments**
6. Identify **missing model assignments**
7. Identify **naming convention violations**

### Step 4: SQL Fix Generation

Generate SQL INSERT/UPDATE/DELETE statements:

| Issue Type | SQL Operation |
|------------|---------------|
| Missing agent | INSERT INTO openclaw_agents |
| Extra agent | DELETE FROM openclaw_agents (FK cascade) |
| Field mismatch | UPDATE openclaw_agents |
| Missing skill | INSERT INTO openclaw_agent_skills |
| Missing model | INSERT INTO openclaw_agent_models |

### Step 5: Collaboration Delegation

- **Database operations** → delegate to `openclaw-ai-sqlite-manager`
- **Agent creation logic** → delegate to `openclaw-ai-agent-creator`
- **Model assignment logic** → delegate to `openclaw-ai-model-assigner`

### Step 6: Report Output

- Save SQL to `reconciliation_fixes.sql`
- Save JSON report to `reconciliation_report.json`
- Print summary with counts per table

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agents_dir` | string | No | Path to agents directory (default: `agent-companies-core/agents/openclawforge-ai/agents`) |
| `db_path` | string | No | Path to SQLite database (default: `schema/openclaw-app.db`) |
| `output_sql_path` | string | No | Path for SQL output (default: `reconciliation_fixes.sql`) |
| `dry_run` | boolean | No | If true, only report without generating SQL |

## Error Handling

- **Missing agents directory**: Report error and exit
- **Database connection failure**: Report error with connection details
- **Malformed AGENTS.md**: Log warning, skip file, continue
- **No database agents**: Report warning but continue with filesystem scan

---

**Skill Name**: openclaw-ai-agent-reconciler
**Version**: 1.0
**Owner**: openclaw-ai-agent-reconciler
**Created**: 2026-05-01