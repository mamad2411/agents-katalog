---
name: openclaw-ai-document-completeness-checker
description: >
  Audit OpenClaw tasks to verify that all required documents have been generated. Check for completeness of skills (SKILL.md), agent definitions (AGENTS.md), project docs (PROJECT.md), issue files, orchestration docs, migration docs, schema definitions, trigger definitions, and adapter configs. Report missing or incomplete documents with actionable paths.
triggers:
  - document completeness check
  - document generation audit
  - task readiness validation
  - missing document detection
  - skill file verification
  - agent documentation audit
  - cross-reference validation
  - pre-execution document check
  - document readiness report
  - verify all docs exist
---

# OpenClaw Document Completeness Checker Skill

## Overview

This skill enables systematic auditing of OpenClaw tasks to verify that all required supporting documents have been generated before execution. It checks the filesystem against a comprehensive document type inventory, identifying gaps in skills, agent definitions, project documentation, issue files, orchestration docs, migration docs, schema definitions, trigger definitions, and adapter configurations.

## Trigger Conditions

- User asks to "check document completeness" for a task
- User asks to "verify all docs exist" for a task
- User asks to "audit document generation" or "find missing documents"
- User asks to "validate task readiness" or "check if all docs are generated"
- User asks to "verify skill files exist" or "check agent documentation"
- User asks to "run document readiness check" before task execution
- User asks to "verify cross-references" in issue files

## Execution Workflow

### Step 1: Task Context Resolution

1. Identify the task or issue being checked (by issue ID, project code, or description)
2. Resolve the task's project path under `agent-companies-core/projects/`
3. Parse the issue file's YAML frontmatter to extract:
   - `id` — issue identifier
   - `title` — issue title
   - `phase` — task phase
   - `status` — current status
   - `priority` — task priority
   - `Assigned Company & Agent` — from body section
   - `Required Skills` — from body section
   - `Dependencies` — from body section
4. Build a document requirement profile based on task type and phase

### Step 2: Document Type Inventory

Check for the presence of each required document type:

| Document Type | Path Pattern | Required For |
|--------------|--------------|--------------|
| **Issue File** | `projects/{project-code}/issues/{issue-id}.md` | All tasks |
| **Issue Generation Status** | `projects/{project-code}/ISSUE-GENERATION-STATUS.md` | Multi-issue projects |
| **Project Charter** | `projects/{project-code}/PROJECT.md` | All projects |
| **Agent Definition** | `agents/{company}/agents/{agent-slug}/AGENTS.md` | Assigned agent |
| **Agent Skill** | `skills/{company}/skills/{skill-slug}/SKILL.md` | Each required skill |
| **Company Definition** | `companies/{company}/COMPANY.md` | Assigned company |
| **Orchestration Doc** | `orchestration/OVERVIEW.md` | Cross-agent tasks |
| **Execution Tracker** | `orchestration/EXECUTION-TRACKER.md` | Multi-step tasks |
| **Risk Tracker** | `orchestration/RISK-TRACKER.md` | High-risk tasks |
| **Learning Integration** | `orchestration/LEARNING-INTEGRATION.md` | Learning tasks |
| **Migration Plan** | `migration/CONCEPT-MAPPING.md` | Migration tasks |
| **Schema Definition** | `schema/create-tables.sql` | Database tasks |
| **Trigger Definition** | `triggers/TRIGGER-README.md` | Automation tasks |
| **Adapter Config** | `adapters/README.md` | Adapter tasks |

### Step 3: Document Existence Verification

1. For each required document type, check if the file exists at the expected path
2. For existing files, verify they contain valid YAML frontmatter (where applicable)
3. For existing files, check that frontmatter fields are populated (not empty)
4. For existing files, verify required sections are present:
   - **AGENTS.md**: Overview, When To Use, Core Procedures
   - **SKILL.md**: Overview, Execution Workflow, Error Handling
   - **PROJECT.md**: Project Overview, Scope, Objectives
   - **COMPANY.md**: Company Overview, Agents, Services
   - **Issue files**: Description, Acceptance Criteria, Required Skills
5. Log each check result: ✅ Present, ⚠️ Present but incomplete, ❌ Missing

### Step 4: Skill Completeness Check

1. For each skill referenced in the task's `Required Skills` section:
   - Verify the SKILL.md file exists at `skills/{company}/{skill-slug}/SKILL.md`
   - Verify the skill has a `description` field in its frontmatter
   - Verify the skill has `related_skills` and `related_docs` if applicable
   - Check that the skill is assigned to the correct agent in the agent's AGENTS.md
2. Report any missing or incomplete skill definitions

### Step 5: Agent Readiness Check

1. Verify the assigned agent's AGENTS.md exists
2. Verify the agent has the required skills listed in its frontmatter `skills` array
3. Verify the agent has a valid `reportsTo` field
4. Verify the agent has a `description` field
5. Check that the agent's slug matches the directory name
6. Report any agent documentation gaps

### Step 6: Cross-Reference Validation

1. Verify that issue file references (dependencies, related tickets) point to existing documents
2. Verify that skill references in issue files point to existing SKILL.md files
3. Verify that agent references in issue files point to existing AGENTS.md files
4. Verify that company references point to existing COMPANY.md files
5. Report any broken cross-references

### Step 7: Report Generation

1. Generate a completeness report with:
   - **Summary**: Total required docs, present, incomplete, missing
   - **By Category**: Skills, Agents, Projects, Companies, Orchestration, Schema, Triggers, Adapters
   - **Missing Documents**: List of paths that need to be created
   - **Incomplete Documents**: List of paths with missing content
   - **Broken References**: List of cross-reference issues
2. Save report to `reports/document-completeness/{task-id}-completeness-report.md`
3. Print summary with pass/fail status per category

### Step 8: Collaboration Delegation

- **Missing agent creation** → delegate to `openclaw-ai-agent-creator`
- **Agent reconciliation** → delegate to `openclaw-ai-agent-reconciler`
- **Documentation content generation** → delegate to `documenter-qualityforge-documentation-specialist`
- **Skill file creation** → delegate to `openclaw-ai-agent-creator`

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | string | Yes | Issue ID or task identifier (e.g., `PROC-000`) |
| `project_code` | string | Yes | Project code (e.g., `01900-procurement`) |
| `agents_dir` | string | No | Path to agents directory (default: `agent-companies-core/agents`) |
| `projects_dir` | string | No | Path to projects directory (default: `agent-companies-core/projects`) |
| `skills_dir` | string | No | Path to skills directory (default: `agent-companies-core/skills`) |
| `companies_dir` | string | No | Path to companies directory (default: `agent-companies-core/companies`) |
| `output_report_path` | string | No | Path for completeness report output |
| `strict_mode` | boolean | No | If true, fail on any missing optional doc (default: false) |

## Error Handling

- **Task not found**: Report error with available project codes
- **Project directory missing**: Report error and list available projects
- **Malformed issue file**: Log warning, attempt partial parsing, continue
- **No required skills listed**: Report warning, check agent's default skills
- **Circular references**: Detect and report, skip affected checks
- **Permission denied**: Log error with file path, continue with remaining checks

---

**Skill Name**: openclaw-ai-document-completeness-checker
**Version**: 1.0
**Owner**: openclaw-ai-document-completeness-checker
**Created**: 2026-05-01