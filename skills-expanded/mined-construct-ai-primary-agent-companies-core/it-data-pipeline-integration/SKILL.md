---
title: IT Data Pipeline Integration
description: Skill for API integration, data synchronization, ETL workflows, and external system connectivity in the ConstructAI platform
frequency: Per integration requirement
success_rate: 90%
tags:
  - it-operations
  - data-pipeline
  - api-integration
  - data-synchronization
  - etl
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/prompts/02050_AI-NATIVE-INFORMATION-TECHNOLOGY-PROMPT.md
  - docs_construct_ai/skills/domainforge_ai/data-requirements-ui-design/SKILL.md
  - docs_construct_ai/skills/infraforge_ai/supply-chain-integration/SKILL.md
---

# IT Data Pipeline Integration

## Overview

This skill covers data pipeline integration for the ConstructAI platform. It encompasses API integration, data synchronization, ETL workflows, external system connectivity, data validation, and pipeline monitoring. Primary agent: 02050-010 Data Pipeline Builder. Supporting skills: `domainforge_ai/data-requirements-ui-design`, `infraforge_ai/supply-chain-integration`.

## Triggers

- New external API needs integration
- Data synchronization workflow required
- ETL pipeline needs to be built
- Existing integration requires enhancement
- Data format change in source system
- Integration error detected

## Prerequisites

- API documentation available
- Authentication credentials configured
- Data schema for source and target systems defined
- Network connectivity established
- Error handling strategy defined

## Steps

### Step 1: API Assessment
- Review API documentation (endpoints, methods, authentication)
- Identify rate limits and throttling behavior
- Identify pagination and filtering parameters
- Review error response format
- Test API connectivity and authentication

### Step 2: Data Schema Mapping
- Map source data fields to target schema
- Identify required vs optional fields
- Identify data type transformations needed
- Handle missing or null values
- Define data validation rules

### Step 3: Pipeline Design
- Design extraction strategy (full scan, incremental, event-driven)
- Design transformation rules (data type conversion, enrichment, filtering)
- Design loading strategy (upsert, append, merge)
- Define checkpoint and resume points
- Define error handling (retry, skip, escalate)

### Step 4: Implementation
- Generate API connector code with authentication
- Generate extraction logic with pagination handling
- Generate transformation functions with data validation
- Generate loading logic with conflict resolution
- Implement error handling and logging

### Step 5: Data Validation
- Implement pre-load validation (schema check, required fields)
- Implement post-load verification (record count, data integrity)
- Implement idempotency checks (no duplicate records)
- Implement reconciliation reports

### Step 6: Monitoring & Alerting
- Implement pipeline execution monitoring
- Implement data freshness monitoring
- Implement error rate monitoring
- Configure alerting for pipeline failures
- Configure execution summary reports

### Step 7: Testing & Deployment
- Test with sample datasets covering edge cases
- Test error handling scenarios
- Test idempotency (re-run produces same result)
- Test with production-scale data volume
- Deploy with monitoring enabled

## Success Criteria

- All API endpoints functional and authenticated
- Data mapping complete with all required fields
- Pipeline executes successfully with sample and production data
- Error handling covers all identified failure modes
- Idempotency guaranteed (re-run produces same result)
- Monitoring and alerting configured
- Documentation complete

## Common Pitfalls

1. **Ignoring rate limits**: Respect API rate limits — implement throttling
2. **Missing idempotency**: Re-running should not create duplicates
3. **Data type mismatches**: Always validate data types during transformation
4. **No checkpointing**: Long-running pipelines should resume from last checkpoint
5. **Missing reconciliation**: Always verify loaded data matches source
6. **Inadequate error handling**: Handle all API error codes, not just 200

## Cross-References

- `it-error-discovery-classification/SKILL.md` — Error classification for pipeline failures
- `it-log-analysis-monitoring/SKILL.md` — Pipeline execution log monitoring
- `domainforge_ai/data-requirements-ui-design/SKILL.md` — Data requirement input patterns
- `infraforge_ai/supply-chain-integration/SKILL.md` — External system integration patterns

## Usage

Apply this skill when integrating new external APIs, building data synchronization pipelines, creating ETL workflows, or enhancing existing integrations.

## Metrics

- **Pipeline Success Rate**: 95%+ of pipeline executions complete successfully
- **Data Accuracy**: 99%+ of records loaded correctly without transformation errors
- **Idempotency**: 100% of re-runs produce same result as initial execution
- **Error Recovery**: 90%+ of transient failures recovered through retry
- **Monitoring Coverage**: 100% of pipeline stages monitored and logged