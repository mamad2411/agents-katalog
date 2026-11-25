---
name: ml-monitoring
version: 1.0.0
min_mindforge_version: 10.6.0
status: stable
triggers: ML model monitoring, model drift detection, data quality monitoring, performance degradation alert, retraining trigger, model decay detection, prediction monitoring, feature drift, concept drift detection, model health dashboard, ML observability, model performance SLA
---

# Skill — ML Monitoring

## When this skill activates
This skill activates when implementing production ML observability, drift detection systems, or automated retraining pipelines. Use when models are deployed and require continuous performance tracking and health monitoring.

## Mandatory actions when this skill is active

### Before writing any code
1. Define model performance SLAs with business stakeholders: accuracy thresholds, latency requirements, prediction volume expectations, and acceptable degradation rates
2. Establish baseline distributions for all features, predictions, and evaluation metrics from training data and initial production period
3. Select drift detection methods appropriate to data types: KS test for continuous, chi-square for categorical, PSI for binned distributions
4. Design alerting strategy with severity levels: critical (immediate intervention), warning (investigate within 24h), informational (track trend)

### During implementation
- Log 100% of predictions with model version, feature values, timestamp, and prediction context for forensic analysis
- Implement statistical drift detection on feature distributions comparing rolling windows to baseline (typically 7d vs 30d trailing)
- Track concept drift by monitoring model performance metrics on recent predictions with ground truth labels when available
- Calculate prediction drift metrics: distribution shifts, confidence score changes, class imbalance variations over time
- Monitor data quality indicators: missing value rates, out-of-range values, schema violations, duplicate records, freshness delays
- Implement shadow scoring for challenger models to compare performance against production champion model continuously
- Create automated retraining triggers based on drift thresholds, performance degradation, or calendar schedule with approval gates

### After implementation
- Build real-time dashboards showing model health: prediction volume, latency p95/p99, error rates, drift scores, and performance metrics
- Set up alerting channels integrated with on-call rotation: PagerDuty, Slack, email with runbook links for common issues
- Generate weekly model health reports with drift analysis, performance trends, data quality issues, and recommended actions
- Document incident response procedures: model rollback process, emergency retraining workflow, and escalation paths

## Self-check before task completion
- [ ] All predictions logged with sufficient context for debugging and audit requirements
- [ ] Drift detection implemented for top 10 most important features with statistical significance testing
- [ ] Performance monitoring tracks all business-critical metrics with automated alerting on degradation
- [ ] Retraining pipeline tested end-to-end with rollback capability and A/B testing framework
- [ ] Dashboard provides visibility into model health for both technical teams and business stakeholders
