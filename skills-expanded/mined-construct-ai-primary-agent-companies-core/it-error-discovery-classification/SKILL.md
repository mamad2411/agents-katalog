---
title: IT Error Discovery & Classification
description: Skill for automated error detection, classification by severity and component, and prioritization of error resolution workflows in the ConstructAI platform
frequency: Per error event
success_rate: 95%
tags:
  - it-operations
  - error-management
  - error-discovery
  - error-classification
  - prioritization
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/prompts/02050_AI-NATIVE-INFORMATION-TECHNOLOGY-PROMPT.md
  - docs_construct_ai/skills/shared/systematic-debugging/SKILL.md
  - docs_construct_ai/skills/shared/build-error-fix/SKILL.md
---

# IT Error Discovery & Classification

## Overview

This skill covers the systematic discovery, classification, and prioritization of errors in the ConstructAI platform. It encompasses error detection from multiple sources (logs, user reports, monitoring alerts), classification by type/severity/component, and prioritization based on impact and frequency. Primary agent: 02050-002 Error Detective. Supporting skills: `shared/build-error-fix`, `shared/systematic-debugging`.

## Triggers

- New error detected in application logs
- User reports an issue via chatbot or error modal
- Monitoring system alerts on anomalous behavior
- Automated error discovery scan identifies new patterns
- 500-level server error occurs
- Client-side JavaScript exception is captured

## Prerequisites

- Access to error tracking system and logs
- Knowledge of system components and their criticality
- Understanding of severity classification matrix
- Access to 02050 domain knowledge for context

## Steps

### Step 1: Error Detection & Capture
- Ingest error from source (log, user report, monitoring alert)
- Capture full context: stack trace, component, user action, timestamp
- Extract structured fields: error type, message, severity indicators
- Tag with source system and environment (dev, staging, prod)

### Step 2: Component Identification
- Parse stack trace to identify originating component
- Map component to system module using component registry
- Identify affected subsystems and potential cascade effects
- Check if component is customer-facing or internal

### Step 3: Severity Classification
- Classify severity using matrix:
  - **P0 (Critical)**: System down, data loss, security breach
  - **P1 (High)**: Feature broken, significant degradation
  - **P2 (Medium)**: Minor feature impact, workaround available
  - **P3 (Low)**: Cosmetic, non-functional, edge case
- Use error type, user impact, and component criticality
- Assign confidence score to classification

### Step 4: Pattern Matching
- Search error history for similar patterns (last 30 days)
- Check if error is recurring or new
- Identify if same root cause has been resolved before
- Link related errors into pattern groups

### Step 5: Prioritization
- Apply prioritization rules:
  - P0 errors: immediate page/auto-escalate
  - P1 errors: same-day resolution target
  - P2 errors: next sprint resolution
  - P3 errors: backlog with trend monitoring
- Consider error frequency (high-frequency P2 → escalate to P1)
- Consider user impact scope (all users → escalate one level)

### Step 6: Assignment & Routing
- Route to appropriate agent based on component:
  - Frontend errors → UI/UX agent
  - API errors → Backend agent
  - Database errors → Data agent
  - AI/LLM errors → AI agent
- Include full context and classification in assignment
- Set SLA based on priority level

### Step 7: Documentation & Tracking
- Create error record in tracking system
- Record all classification decisions with reasoning
- Tag with component, severity, pattern group
- Log audit trail for all actions taken

## Success Criteria

- Error correctly identified and captured with full context
- Component accurately identified (95%+ accuracy)
- Severity classification matches actual impact
- Pattern matching identifies recurring issues
- Priority level matches severity and frequency
- Error routed to correct agent/team
- Complete audit trail maintained

## Common Pitfalls

1. **Incomplete stack trace**: Ensure full context is captured, not just error message
2. **Over-classification as Critical**: Not every 500 error is P0 — consider user impact
3. **Missing cascade effects**: Always check if error affects downstream systems
4. **Incorrect component mapping**: Verify component registry is up to date
5. **Ignoring error frequency**: High-frequency P2 errors should escalate
6. **Duplicate error creation**: Check pattern matching before creating new records

## Cross-References

- `shared/systematic-debugging/SKILL.md` — Root cause investigation for classified errors
- `shared/build-error-fix/SKILL.md` — Resolution workflow for build-related errors
- `it-log-analysis-monitoring/SKILL.md` — Ongoing error pattern monitoring
- `it-performance-monitoring-analytics/SKILL.md` — Error rate trend analysis

## Usage

Use this skill when any error is detected in the system that needs classification, prioritization, and routing. This is the first skill applied in the error management pipeline before resolution workflows.

## Metrics

- **Classification Accuracy**: 95%+ of errors correctly classified
- **Component Identification**: 95%+ accuracy in identifying error source
- **Routing Correctness**: 90%+ of errors routed to correct team
- **Pattern Detection**: 80%+ of recurring errors identified as patterns
- **Time to Classification**: <30 seconds for automated classification