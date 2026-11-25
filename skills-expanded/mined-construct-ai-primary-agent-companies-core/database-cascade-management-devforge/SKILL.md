---
name: database-cascade-management-devforge
description: >
  Use when database foreign key cascade issues occur, deletion operations fail with
  constraint violations, or data model changes require cascade path updates. Handles
  company deletion CASCADE failures, orphaned records, and migration planning.
---

# Database Cascade Management - DevForge AI

## Overview
Handles database foreign key cascade issues in the Paperclip codebase. Resolves deletion operation failures caused by missing CASCADE constraints, plans safe migration paths for schema changes, and ensures data integrity during company/agent lifecycle operations.

## When to Use
- When `DELETE /api/companies/:id` fails with FK constraint violations
- When orphaned records remain after parent entity deletion
- When schema migrations need CASCADE path additions
- When activity_log, cost_events, issue_read_states block deletion
- **Don't use when:** It's a query performance issue (use schema-devforge-data-schema-management)

## Core Procedures
### Cascade Fix Workflow
1. **Identify Blocking Constraints** - Run deletion, capture FK violation errors
2. **Map Dependency Graph** - Trace all tables referencing the target entity
3. **Determine Cascade Strategy** - Decide CASCADE vs SET NULL vs manual deletion order
4. **Write Migration** - Add ON DELETE CASCADE to appropriate FK constraints
5. **Test Deletion** - Verify full cascade works with realistic test data
6. **Add Integration Test** - Ensure deletion path is covered

### Common Blocking Tables
- `activity_log.run_id` → `heartbeat_runs.id`
- `cost_events.heartbeat_run_id` → `heartbeat_runs.id`
- `issue_read_states.issue_id` → `issues.id`
- `agent_wakeup_requests` → `agents` / `heartbeat_runs`
- `goals` → blocked by `projects.goal_id`

## Agent Assignment
**Primary Agent:** devcore-devforge-core-development
**Company:** DevForge AI
**Role:** Database Cascade Specialist
**Reports To:** devcore-devforge-core-development
**Backup Agents:** schema-devforge-data-schema-management, database-infraforge-database-infrastructure

## Success Metrics
- Company deletion completes without manual SQL intervention
- All dependent tables properly cascaded
- No orphaned records after deletion
- Deletion covered by integration tests

## Error Handling
- **Error:** CASCADE would delete unintended data
  **Response:** Use soft delete pattern or manual ordered deletion instead
- **Error:** Circular FK prevents CASCADE
  **Response:** Break circular dependency, use deferred constraints

## Cross-Team Integration
**Gigabrain Tags:** devforge, database, cascade, foreign-key, migration, deletion
**Related Skills:** devcore-devforge-core-development, schema-devforge-data-schema-management, database-infraforge-database-infrastructure
**Last Updated:** 2026-04-07