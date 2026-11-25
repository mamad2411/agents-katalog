---
title: IT Log Analysis & Monitoring
description: Skill for log aggregation pipelines, pattern detection, anomaly identification, and alert configuration in the ConstructAI platform
frequency: Continuous (real-time monitoring)
success_rate: 90%
tags:
  - it-operations
  - log-analysis
  - monitoring
  - anomaly-detection
  - alerting
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/prompts/02050_AI-NATIVE-INFORMATION-TECHNOLOGY-PROMPT.md
  - docs_construct_ai/skills/domainforge_ai/it-error-discovery-classification/SKILL.md
---

# IT Log Analysis & Monitoring

## Overview

This skill covers log aggregation, pattern detection, anomaly identification, and monitoring alert configuration for the ConstructAI platform. It encompasses log ingestion pipelines, structured query generation, pattern matching algorithms, anomaly detection thresholds, and alert routing. Primary agent: 02050-004 Log Analyst. Supporting skills: `it-error-discovery-classification`.

## Triggers

- New log source needs monitoring
- Alert thresholds require configuration or tuning
- Log patterns indicate potential systemic issues
- New component deployment requires monitoring setup
- Error rate exceeds configured thresholds
- Periodic log analysis audit is due

## Prerequisites

- Access to log aggregation system
- Known baseline metrics for normal operation
- Component topology documentation
- Understanding of error classification from `it-error-discovery-classification`
- Alert routing configuration access

## Steps

### Step 1: Log Source Identification
- Identify all log sources (application logs, server logs, database logs, API logs, infrastructure logs)
- Verify log format and parsing capabilities
- Confirm log ingestion pipeline connectivity
- Map log sources to system components

### Step 2: Pattern Definition
- Define known normal patterns for each log source
- Define error patterns requiring alerting
- Define anomaly patterns indicating potential issues
- Create pattern match rules (regex, structured queries, ML-based detection)

### Step 3: Baseline Establishment
- Collect baseline metrics for normal operation periods
- Establish normal error rate ranges per component
- Establish normal response time distributions
- Establish normal request volume patterns by time

### Step 4: Threshold Configuration
- Configure error rate thresholds (warning at 2x baseline, critical at 5x baseline)
- Configure response time thresholds (warning at 150% baseline, critical at 300% baseline)
- Configure volume thresholds (warning at 150% expected, critical at 300% expected)
- Configure cascading failure detection rules

### Step 5: Anomaly Detection
- Implement statistical anomaly detection (Z-score, IQR methods)
- Implement time-series anomaly detection (sudden spikes, gradual drifts)
- Implement correlation-based anomaly detection (multiple anomalies coinciding)
- Implement seasonal adjustment for periodic patterns

### Step 6: Alert Configuration
- Configure alert levels (info, warning, critical, emergency)
- Configure alert routing (on-call, team leads, engineering director by level)
- Configure alert deduplication rules (same pattern, same component, same time window)
- Configure alert escalation rules (no acknowledgment within SLA → escalate)

### Step 7: Dashboard Configuration
- Configure real-time dashboards with key metrics
- Configure trend charts for historical analysis
- Configure component health dashboards
- Configure business-relevant dashboards (user impact, revenue impact)

### Step 8: Analysis & Action
- When anomaly detected, run root cause correlation
- When threshold breached, create error classification task
- When pattern indicates systemic issue, generate incident report
- When alert fires, provide context to responding team

## Success Criteria

- All log sources identified and being ingested
- Pattern definitions cover 90%+ of known error scenarios
- Baseline metrics established for all components
- Thresholds configured and tuned (few false positives)
- Anomaly detection identifies 85%+ of real anomalies
- Alerts route correctly with appropriate deduplication
- Dashboards provide real-time visibility

## Common Pitfalls

1. **Alert fatigue**: Too many non-actionable alerts — tune thresholds regularly
2. **Missing context**: Alerts without component or user impact context — enrich alert data
3. **Baseline staleness**: Baselines drift over time — update baselines quarterly
4. **Log gaps**: Not all components logging at appropriate levels — verify coverage
5. **Deduplication failures**: Same alert firing repeatedly — improve deduplication windows
6. **No seasonal adjustment**: Normal traffic patterns flagged as anomalies — implement seasonality

## Cross-References

- `it-error-discovery-classification/SKILL.md` — Error classification for detected anomalies
- `it-performance-monitoring-analytics/SKILL.md` — Performance metrics integration
- `shared/systematic-debugging/SKILL.md` — Root cause investigation from detected anomalies

## Usage

Apply this skill when setting up monitoring for new components, configuring alert thresholds, investigating anomalous patterns, or performing periodic log analysis. This runs continuously for production monitoring as well as on-demand for investigations.

## Metrics

- **Pattern Coverage**: 90%+ of known error patterns detected
- **Anomaly Detection Rate**: 85%+ of real anomalies detected
- **False Positive Rate**: <10% of alerts are false positives
- **Alert Response Time**: 95%+ of critical alerts acknowledged within SLA
- **Log Coverage**: 100% of critical components producing structured logs