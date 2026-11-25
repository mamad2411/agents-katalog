---
title: IT Agent Coordination
description: Skill for multi-agent workflow orchestration, structured data handoffs, error recovery, and agent lifecycle management in the ConstructAI platform
frequency: Per workflow execution
success_rate: 95%
tags:
  - it-operations
  - multi-agent-orchestration
  - workflow-management
  - agent-handoffs
  - error-recovery
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/prompts/02050_AI-NATIVE-INFORMATION-TECHNOLOGY-PROMPT.md
---

# IT Agent Coordination

## Overview

This skill covers multi-agent workflow orchestration for IT operations. It encompasses workflow definition, agent-to-agent handoffs with structured data, error recovery patterns, workflow monitoring, and agent lifecycle management. Primary agent: 02050-006 AI Orchestrator. Supporting skills: All domainforge_ai IT skills.

## Triggers

- Multi-agent workflow needs to be initiated
- Agent execution failure requires recovery
- New workflow needs to be orchestrated
- Existing workflow requires monitoring or intervention
- Agent lifecycle event detected (start, complete, fail, timeout)

## Prerequisites

- Agents defined and available in agent registry
- Workflow schema and handoff definitions established
- Error handling and recovery patterns defined
- Monitoring and alerting configured
- Agent communication channels established

## Steps

### Step 1: Workflow Definition
- Define workflow stages and agent sequence
- Define data schema for each handoff
- Define success criteria for each stage
- Define failure handling (retry, alternative, escalation)
- Define timeout thresholds for each stage

### Step 2: Agent Assignment & Validation
- Verify all required agents are available
- Confirm agent capabilities match workflow requirements
- Assign primary and backup agents for each stage
- Validate agent environment connectivity
- Confirm agent authentication and authorization

### Step 3: Handoff Configuration
- Define data format for each agent handoff (structured JSON, not free text)
- Define validation rules for handoff data
- Define data transformation rules between incompatible formats
- Set up handoff monitoring and logging

### Step 4: Workflow Initiation
- Trigger workflow with initial data
- Verify first agent receives correct input
- Monitor first agent execution progress
- Validate first agent output against expected schema

### Step 5: Handoff Execution
- Pass validated output from Agent A to Agent B
- Verify Agent B acknowledges receipt and begins processing
- Monitor execution time against thresholds
- Check output quality against success criteria

### Step 6: Error Handling & Recovery
- Detect agent execution failure (error, timeout, invalid output)
- Apply error recovery strategy (retry, alternative path, human escalation)
- Log recovery action with reasoning
- Resume workflow from last valid checkpoint

### Step 7: Workflow Monitoring
- Track workflow progress through stages
- Monitor stage durations against baselines
- Detect stalled workflows
- Alert on workflow failures or SLA breaches

### Step 8: Workflow Completion
- Validate final output against workflow success criteria
- Generate workflow execution summary
- Log audit trail for all actions and decisions
- Update workflow analytics and metrics

## Success Criteria

- All workflow stages complete successfully
- Data handoffs use validated structured JSON (no free text between agents)
- Error recovery succeeds for all recoverable failures
- Workflow completes within defined SLA
- Complete audit trail maintained
- All stages logged with execution metrics

## Common Pitfalls

1. **Unvalidated handoffs**: Always validate handoff data before passing to next agent
2. **Missing backups**: Define alternative paths for critical agent failures
3. **Timeout storms**: Set appropriate timeouts — too short causes cascading failures, too long wastes resources
4. **Free text handoffs**: Use structured JSON — free text loses schema guarantees
5. **No monitoring**: Always monitor workflow progress and stages
6. **Orphaned workflows**: Define cleanup for stuck or failed workflows

## Cross-References

- `it-error-discovery-classification/SKILL.md` — Error classification for agent failures
- `it-log-analysis-monitoring/SKILL.md` — Workflow execution log monitoring

## Usage

Apply this skill when setting up or monitoring multi-agent workflows, handling agent failures during workflow execution, or designing new orchestrated workflows.

## Metrics

- **Workflow Completion Rate**: 95%+ of workflows complete successfully
- **Handoff Accuracy**: 100% of handoffs use validated structured JSON
- **Error Recovery Rate**: 90%+ of recoverable failures resolved without human intervention
- **SLA Compliance**: 95%+ of workflows complete within SLA
- **Audit Trail**: 100% of workflow actions logged with source, timestamp, and decision