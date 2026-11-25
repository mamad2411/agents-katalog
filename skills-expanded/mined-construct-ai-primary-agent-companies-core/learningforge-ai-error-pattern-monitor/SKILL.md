---
name: learningforge-ai-error-pattern-monitor
description: >
  Use when monitoring for repeat errors across Paperclip companies,
  detecting recurring SQL validation failures, tracking cross-company
  error patterns, or alerting on systematic mistakes that need user attention.
triggers:
  - repeat error detection
  - error pattern analysis
  - cross-company error monitoring
  - SQL validation failure tracking
  - systematic mistake alerting
  - error recurrence monitoring
  - pattern-based error alerts
---

# Learning Forge AI - Error Pattern Monitor

## Overview

This skill monitors the Paperclip ecosystem for repeat errors and systematic mistakes across all companies. When the same error pattern occurs multiple times, it triggers user alerts and generates improvement recommendations.

## Purpose

**Problem Solved:** When the same SQL error (e.g., `slug` vs `title` column confusion) occurred across multiple agents/companies, no alerting mechanism triggered. This skill provides that missing link.

## When to Use

- When monitoring for repeat SQL validation errors across companies
- When detecting recurring mistake patterns in agent operations
- When alerting users about systematic errors needing attention
- When tracking error resolution progress
- When generating cross-company improvement recommendations

## Core Procedures

### Error Pattern Detection Workflow

1. **Error Collection** - Query activity_log for recent errors
2. **Pattern Analysis** - Identify recurring error messages
3. **Threshold Detection** - Flag patterns occurring 3+ times
4. **Alert Generation** - Create Paperclip issues for user review
5. **Recommendation Generation** - Propose template/skill improvements

### Repeat Error Detection Query

```sql
-- Detect repeat SQL errors across all companies
SELECT 
  details->>'error_message' AS error_pattern,
  COUNT(*) AS occurrence_count,
  array_agg(DISTINCT company_id) AS affected_companies,
  array_agg(DISTINCT actor_id) AS affected_agents,
  MIN(created_at) AS first_occurrence,
  MAX(created_at) AS last_occurrence
FROM activity_log
WHERE action = 'error'
  AND entity_type = 'agent'
  AND created_at > NOW() - INTERVAL '7 days'
GROUP BY details->>'error_message'
HAVING COUNT(*) >= 3
ORDER BY occurrence_count DESC;
```

### Cross-Company Error Correlation

```sql
-- Find errors that span multiple companies (indicates systemic issue)
SELECT 
  details->>'error_type' AS error_type,
  COUNT(DISTINCT company_id) AS company_count,
  COUNT(*) AS total_occurrences,
  string_agg(DISTINCT c.name, ', ') AS company_names
FROM activity_log al
JOIN companies c ON al.company_id = c.id
WHERE al.action = 'error'
  AND al.created_at > NOW() - INTERVAL '7 days'
GROUP BY details->>'error_type'
HAVING COUNT(DISTINCT company_id) >= 2
ORDER BY total_occurrences DESC;
```

## Error Categories to Monitor

### SQL Validation Errors
- Column name mismatches (e.g., `slug` vs `name` vs `title`)
- FK constraint violations
- Missing required fields
- Data type mismatches

### Naming Convention Violations
- Human name length > 22 characters
- Directory name pattern violations
- Inconsistent naming across companies

### Workflow Bypass Errors
- Validation steps skipped
- Template usage not followed
- Schema inspection bypassed

## Alert Thresholds

| Error Type | Threshold | Alert Level |
|------------|-----------|-------------|
| Same SQL error | 3+ occurrences | Warning |
| Cross-company error | 2+ companies | Critical |
| Naming violation | 5+ agents | Warning |
| Workflow bypass | 2+ occurrences | Critical |

## Output

### Paperclip Issue Creation
When threshold exceeded, create issue:
```yaml
title: "Repeat Error Alert: {error_type}"
description: "{occurrence_count} occurrences detected"
priority: high
labels: ["error-pattern", "repeat-error"]
assignee: paperclip-board-operations
```

### Improvement Recommendations
Generate recommendations for:
- Template updates
- Skill enhancements
- Validation workflow improvements
- Agent training needs

## Agent Assignment

**Primary Agent:** learningforge-ai-error-pattern-monitor (new agent)

**Supporting Agents:**
- learningforge-ai-feedback-synthesis (recommendation generation)
- learningforge-ai-workflow-coach (workflow improvement)

## Integration Points

### Activity Log Monitoring
- Query `activity_log` table for error entries
- Filter by time window (default: 7 days)
- Group by error pattern

### Paperclip Issue System
- Create issues for threshold-exceeded patterns
- Update issue status on resolution
- Track resolution metrics

### Template Registry
- Reference `docs-paperclip/schema/templates/`
- Identify which templates need updates
- Track template usage compliance

## Success Metrics

- **Detection Rate**: % of repeat errors caught within 24 hours
- **Alert Coverage**: % of threshold-exceeded patterns that generate alerts
- **Resolution Time**: Average time from detection to resolution
- **False Positive Rate**: % of alerts that are not actual errors

## Last Updated

2026-04-25
