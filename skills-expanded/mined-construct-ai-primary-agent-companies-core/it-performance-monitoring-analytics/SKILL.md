---
title: IT Performance Monitoring & Analytics
description: Skill for system metrics tracking, trend analysis, dashboard configuration, capacity forecasting, and performance optimization recommendations in the ConstructAI platform
frequency: Continuous monitoring, weekly analysis
success_rate: 90%
tags:
  - it-operations
  - performance-monitoring
  - analytics
  - capacity-forecasting
  - trend-analysis
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/prompts/02050_AI-NATIVE-INFORMATION-TECHNOLOGY-PROMPT.md
  - docs_construct_ai/skills/domainforge_ai/it-log-analysis-monitoring/SKILL.md
---

# IT Performance Monitoring & Analytics

## Overview

This skill covers system performance monitoring, analytics, trend analysis, and capacity forecasting for the ConstructAI platform. It encompasses metric collection, performance trend analysis, dashboard configuration, capacity forecasting, and optimization recommendations. Primary agent: 02050-008 Performance Monitor. Supporting skills: `it-log-analysis-monitoring`.

## Triggers

- New component deployment requires monitoring
- Performance degradation alert received
- Capacity planning review scheduled
- New dashboard or report needed
- Traffic pattern change detected
- System scaling decision required

## Prerequisites

- Metrics collection infrastructure in place
- Baseline performance metrics established
- Component topology and dependency map available
- Business traffic patterns and growth projections available
- Access to monitoring platform and dashboards

## Steps

### Step 1: Metrics Definition & Collection
- Define key performance metrics (response time, throughput, error rate, resource usage)
- Verify metrics collection for all critical components
- Check metric collection frequency and granularity
- Ensure custom business metrics are being tracked

### Step 2: Performance Trend Analysis
- Calculate trends for key metrics (weekly, monthly, quarterly)
- Identify degrading performance patterns
- Correlate performance changes with code deployments
- Identify capacity bottlenecks

### Step 3: Dashboard Configuration
- Configure component-level dashboards
- Configure system-level dashboards
- Configure business-impact dashboards
- Set up alert thresholds based on trends
- Configure executive summary views

### Step 4: Capacity Forecasting
- Project resource needs based on traffic trends
- Model scaling scenarios (2x, 5x, 10x traffic)
- Identify approaching capacity limits
- Generate infrastructure scaling recommendations

### Step 5: Bottleneck Identification
- Analyze response time distribution by component
- Identify slow queries and database bottlenecks
- Identify resource saturation (CPU, memory, connections, IOPS)
- Analyze network latency between services

### Step 6: Optimization Recommendations
- Generate specific optimization recommendations
- Estimate impact of each recommendation
- Prioritize by effort and impact
- Create implementation roadmap

### Step 7: Reporting & Action
- Generate weekly performance report
- Generate monthly capacity planning report
- Present findings to engineering leadership
- Track optimization actions and results

## Success Criteria

- All critical components have performance metrics
- Trends accurately forecast future capacity needs
- Dashboards provide actionable insights
- Optimization recommendations are specific and actionable
- Capacity forecasts have 80%+ accuracy
- Performance degradation detected before user impact

## Common Pitfalls

1. **Metric silos**: Don't analyze metrics in isolation — always correlate across components
2. **Baseline drift**: Performance baselines change — update them regularly
3. **Missing business metrics**: Technical metrics alone don't show business impact
4. **Dashboard overload**: Focus on actionable metrics, not vanity metrics
5. **Forecast overconfidence**: Include confidence ranges — don't project single values

## Cross-References

- `it-log-analysis-monitoring/SKILL.md` — Log data integration for performance analysis
- `it-error-discovery-classification/SKILL.md` — Error rate trend integration
- `shared/systematic-debugging/SKILL.md` — Root cause investigation for performance issues

## Usage

Apply this skill for performance monitoring, capacity planning, system optimization, and executive reporting. Run weekly trend analysis and quarterly capacity reviews.

## Metrics

- **Metric Coverage**: 100% of critical components have performance metrics
- **Forecast Accuracy**: 80%+ of capacity forecasts within 20% of actual
- **Detection Time**: 95%+ of performance degradation detected before user reports
- **Dashboard Currency**: Dashboards updated within 24 hours of system changes
- **Optimization Impact**: Measurable improvement after implementing recommendations