---
title: HSE Safety Performance Monitoring
description: Monitor and analyze safety performance metrics including TRIFR, LTIFR, near-miss rates, incident trends, leading indicators, and safety culture assessment with automated data collection and trend analysis
version: 1.0
frequency_percent: 95.0
success_rate_percent: 94.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00885_hse-director/hse-safety-performance-monitoring
gigabrain_tags: disciplines, 00885_hse-director, safety-performance, trifr, ltifr, incident-trends, leading-indicators, safety-culture
openstinger_context: hse-director, safety-monitoring, performance-analytics
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00885_hse-director/agent-data/domain-knowledge/00885_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00885_hse-director/agent-data/prompts/00885_AI-NATIVE-HSE-DIRECTOR-PROMPT.md
  - docs_construct_ai/disciplines/00885_hse-director/agent-data/domain-knowledge/00885_GLOSSARY.MD
related_skills:
  - pre-task-assessment-readiness
  - hse-incident-investigation
  - hse-executive-reporting
---

# HSE Safety Performance Monitoring

## Overview

Monitor and analyze safety performance metrics from incident management systems, site logs, and safety observation databases. Calculate TRIFR (Total Recordable Injury Frequency Rate), LTIFR (Lost Time Injury Frequency Rate), near-miss rates, and leading indicators. Perform incident trend analysis to identify patterns by location, activity type, time, and personnel. Generate safety performance dashboards and alerts for executive monitoring.

**Announce at start:** "I'm using the hse-safety-performance-monitoring skill to analyze safety performance data and calculate HSE metrics."

## When to Use This Skill

**Trigger Conditions:**
- Daily/weekly safety KPI dashboard updates
- Monthly safety performance reports for management
- Incident trend analysis after new incidents
- Safety culture assessment from survey data
- Leading indicator monitoring (near-miss, observations, audits)
- Board-level HSE briefing preparation
- Contractor safety performance scoring

**Prerequisites:**
- Access to incident management system (incident database)
- Site incident logs and near-miss reports
- Workforce exposure hours data (for frequency rate calculation)
- Time range defined for analysis
- Safety observation and audit data

## Step-by-Step Procedure

### Step 1: Data Source Validation

Verify all safety data sources are current and reconciled:

| Data Source | Purpose | Required Fields | Update Frequency |
|-------------|---------|----------------|------------------|
| **Incident Management System** | Incident records, classification, investigation status | Incident ID, date, severity, location, personnel, root cause | Real-time |
| **Site Incident Logs** | Field incident capture | Incident details, witness statements, immediate actions | Daily |
| **Near-Miss Reports** | Leading indicator tracking | Near-miss details, potential severity, corrective actions | Daily |
| **Workforce Hours** | Exposure hours for frequency calculations | Work hours by project/contractor/location | Weekly |
| **Safety Observations** | Proactive hazard identification | Observation type, location, corrective action | Daily |
| **Safety Audit Results** | Compliance verification | Audit findings, corrective actions, closure status | Weekly/Monthly |

**Data Reconciliation Check:**
```
IF incident_system.count ≠ site_logs.count THEN
    FLAG discrepancy for investigation
    REPORT missing incidents to HSE Director
END IF
```

### Step 2: Safety Frequency Rate Calculation

Calculate TRIFR and LTIFR using standard formulas:

**TRIFR (Total Recordable Injury Frequency Rate):**
```
TRIFR = (Total Recordable Injuries / Total Hours Worked) × 1,000,000
```

**LTIFR (Lost Time Injury Frequency Rate):**
```
LTIFR = (Lost Time Injuries / Total Hours Worked) × 1,000,000
```

**Injury Classification:**
| Classification | Definition | TRIFR | LTIFR |
|---------------|------------|-------|-------|
| **First Aid** | Minor injury, no lost time | No | No |
| **Medical Treatment** | Requires medical attention | Yes | No |
| **Restricted Work** | Modified duties, no lost time | Yes | No |
| **Lost Time Injury** | Cannot work next shift | Yes | Yes |
| **Permanent Disability** | Permanent impairment | Yes | Yes |
| **Fatality** | Death | Yes | Yes |

**Calculation Example:**
```
Period: Q1 2026
Total Hours Worked: 500,000 hours
Recordable Injuries: 3 (1 medical treatment, 1 restricted work, 1 LTI)
Lost Time Injuries: 1

TRIFR = (3 / 500,000) × 1,000,000 = 6.0
LTIFR = (1 / 500,000) × 1,000,000 = 2.0
```

### Step 3: Near-Miss Rate Calculation

Calculate near-miss reporting rate as leading indicator:

**Near-Miss Rate:**
```
Near-Miss Rate = (Near-Miss Reports / Total Hours Worked) × 1,000,000
```

**Target:** Increasing near-miss rate indicates improving safety culture (more reporting, not more incidents)

**Trend Analysis:**
- Compare month-over-month near-miss rate
- Identify if trend is increasing (positive - more reporting) or decreasing (negative - potential underreporting)
- Flag if near-miss rate drops significantly (may indicate reporting fatigue)

### Step 4: Incident Trend Analysis

Analyze incidents to identify patterns and root causes:

**Pattern Detection Dimensions:**
| Dimension | Analysis | Action |
|-----------|----------|--------|
| **Location** | Cluster incidents by work area, site zone | Focus safety resources on high-risk areas |
| **Activity Type** | Group by activity (excavation, working at height, lifting) | Review method statements for high-incident activities |
| **Time** | Analyze by time of day, day of week, season | Adjust workforce scheduling, manage fatigue |
| **Personnel** | Track incidents by crew, supervisor, contractor | Identify training needs, competency gaps |
| **Root Cause** | Categorize by root cause theme | Target systemic improvements |

**Root Cause Categories:**
- Inadequate training or competency
- Inadequate procedures or method statements
- Inadequate supervision or monitoring
- Equipment failure or inadequacy
- Human error or behavior
- External factors (weather, third party)

**Trend Identification:**
```
FOR each dimension:
    COUNT incidents by dimension value
    RANK dimension values by incident count
    IDENTIFY top 3 high-incident values
    CALCULATE trend direction (increasing/stable/decreasing)
    FLAG if significant increase detected
END FOR
```

### Step 5: Leading Indicator Monitoring

Monitor leading indicators for proactive safety management:

| Leading Indicator | Target Trend | Calculation | Warning Threshold |
|------------------|--------------|-------------|-------------------|
| **Near-Miss Reporting Rate** | Increasing | Per Step 3 | Decrease >20% month-over-month |
| **Safety Observation Rate** | Increasing | Observations / exposure hours × 1,000,000 | <100 per million hours |
| **Safety Audit Compliance** | >95% | (Compliant items / total items) × 100 | <90% |
| **Corrective Action Closure** | >90% on time | (On-time closures / total actions) × 100 | <85% |
| **Safety Training Compliance** | 100% | (Trained personnel / total personnel) × 100 | <95% |
| **Management Safety Walks** | Increasing | Walks completed / planned walks × 100 | <80% |

### Step 6: Safety Culture Assessment

Assess safety culture from survey data and behavioral indicators:

**Survey Analysis:**
- Collect anonymous safety climate survey responses
- Calculate average scores by dimension (leadership, communication, hazard recognition, reporting)
- Identify trend direction (improving, stable, declining)
- Flag significant gaps between perception and reality

**Behavioral Indicators:**
- Near-miss reporting rate (proxy for reporting culture)
- Safety observation quality (detailed vs. generic)
- Stop-work authority use (empowered workforce)
- Incident reporting timeliness (delays indicate fear)

**Culture Gap Identification:**
```
IF survey_score.leadership > 4.0 AND near_miss_rate < 50 THEN
    FLAG "Disconnect between perceived and actual reporting culture"
END IF
```

### Step 7: Contractor Safety Performance

Score contractor safety performance for commercial and HSE oversight:

**Contractor Safety Scorecard:**
| Metric | Weight | Calculation |
|--------|--------|-------------|
| **Contractor TRIFR** | 30% | TRIFR for contractor workforce |
| **Contractor LTIFR** | 30% | LTIFR for contractor workforce |
| **Safety Audit Compliance** | 20% | Audit compliance rate |
| **Corrective Action Closure** | 10% | On-time closure rate |
| **Incident Investigation Quality** | 10% | Investigation thoroughness score |

**Overall Contractor Score:**
```
Score = Σ(metric_score × weight)
```

**Performance Bands:**
| Score | Band | Action |
|-------|------|--------|
| >90% | Excellent | Recognition, use as benchmark |
| 80-90% | Good | Continue monitoring |
| 70-80% | Acceptable | Improvement plan required |
| <70% | Poor | Escalate, consider contract review |

### Step 8: Safety Performance Dashboard Generation

Generate safety performance dashboard for executive monitoring:

**Dashboard Components:**
1. **KPI Summary:** TRIFR, LTIFR, Near-Miss Rate (current period vs. target vs. prior period)
2. **Trend Charts:** 12-month rolling TRIFR/LTIFR trend line
3. **Incident Heatmap:** Incidents by location and time
4. **Leading Indicators:** Near-miss rate, observation rate, audit compliance, training compliance
5. **Contractor Performance:** Top 5 and bottom 5 contractors by safety score
6. **Alerts:** Overdue corrective actions, declining trends, data anomalies

**Alert Thresholds:**
- TRIFR/LTIFR exceeds target
- Incident trend increasing (>20% increase month-over-month)
- Near-miss rate decreasing (>20% decrease - potential underreporting)
- Corrective actions overdue (>7 days past due date)
- Data reconciliation failure (site logs ≠ incident system)

## Success Criteria

- [ ] All data sources validated and reconciled
- [ ] TRIFR and LTIFR calculated correctly with documented formulas
- [ ] Near-miss rate calculated and trend direction identified
- [ ] Incident trend analysis identifies top 3 patterns by each dimension
- [ ] Leading indicators monitored and warnings flagged
- [ ] Safety culture assessment includes survey and behavioral indicators
- [ ] Contractor safety performance scored for all active contractors
- [ ] Dashboard generated with all components and alerts
- [ ] Data accuracy matches source system values (100% reconciliation)

## Common Pitfalls

1. **Incorrect Exposure Hours** — Using headcount instead of actual hours worked leads to incorrect frequency rates. Always use verified hours from timekeeping systems.
2. **Inconsistent Classification** — Incident classification must be consistent (medical treatment vs. first aid). Borderline cases require HSE director decision.
3. **Underreporting Detection Failure** — If TRIFR is significantly lower than industry benchmarks or historical average without explanation, investigate for underreporting.
4. **Incomplete Data Reconciliation** — Site logs and incident system must reconcile. Missing incidents in either source invalidate all metrics.
5. **Lagging Indicator Only Focus** — TRIFR/LTIFR are lagging indicators. Leading indicators (near-miss, observations) provide proactive insight.
6. **Ignoring Near-Miss Decline** — Declining near-miss rate is often negative (reporting fatigue, fear) not positive (fewer hazards).

## Cross-References

### Related Skills
- `hse-incident-investigation` — Provides root cause data for trend analysis
- `hse-executive-reporting` — Uses safety performance data for board briefings
- `hse-audit-management` — Provides audit compliance data as leading indicator
- `hse-training-compliance` — Provides training compliance data as leading indicator

### Related Agents
- `Safety Performance Agent` (HSE-SAF-001) — Primary owner of this skill
- `Incident Investigation Agent` (HSE-INC-001) — Provides root cause analysis
- `HSE Executive Reporting Agent` (HSE-RPT-001) — Consumes safety performance data

## Example Usage

**Scenario:** Generate Q1 2026 safety performance dashboard for board HSE briefing

1. **Data Validation:** Incident system (45 incidents), site logs (45 incidents) — reconciled ✓
2. **TRIFR Calculation:** 12 recordable injuries / 1,200,000 hours × 1,000,000 = 10.0 (target: <5.0) ❌
3. **LTIFR Calculation:** 4 LTIs / 1,200,000 hours × 1,000,000 = 3.3 (target: 0) ❌
4. **Near-Miss Rate:** 150 near-misses / 1,200,000 hours × 1,000,000 = 125 (prior period: 110) — increasing trend ✓
5. **Incident Trends:** Top location: Structural zone (8 incidents), Top activity: Working at height (6 incidents), Top root cause: Inadequate supervision (7 incidents)
6. **Leading Indicators:** Audit compliance 92% (target >95%), Corrective actions 87% on-time (target >90%)
7. **Contractor Performance:** Contractor A (95% - Excellent), Contractor B (68% - Poor, escalate)
8. **Alerts:** TRIFR above target, LTIFR above target, Contractor B poor performance
9. **Output:** Dashboard with red alerts on lagging indicators, amber on leading indicators, recommendation to focus on structural zone working at height supervision

## Performance Metrics

**Target Performance:**
- Data accuracy: 100% (perfect reconciliation between site logs and incident system)
- Calculation accuracy: 100% (correct frequency rate formulas applied)
- Dashboard generation time: <2 minutes for full refresh
- Data freshness: <1 hour (real-time incident updates)
- Alert detection: 100% (all threshold breaches detected and flagged)
