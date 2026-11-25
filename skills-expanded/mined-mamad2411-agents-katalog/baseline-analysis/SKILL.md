# Baseline Analysis

## Skill: `nmon_baseline_analysis`

Establish normal network traffic patterns, detect anomalies through statistical and ML-based approaches, and leverage baselines for capacity planning. This skill covers time-series baseline computation, dynamic threshold configuration, seasonal adjustment, and trend extrapolation.

---

## Establishing Normal Traffic Patterns

Baselines capture the expected behavior of network metrics under normal operating conditions. For Azure flow-log baselines, use VNet flow logs and current Traffic Analytics schemas by default; examples using `AzureNetworkAnalytics_CL` are legacy/schema examples that must be validated in the target workspace. NSG flow logs are legacy/migration-only (new creation blocked after 2025-06-30; retire 2027-09-30). Effective baselines must account for multiple temporal dimensions:

### Time-of-Day Analysis

Network traffic exhibits strong diurnal patterns. Business applications peak during working hours (08:00-18:00 local time), while batch processing and backup traffic may peak overnight. Compute hourly averages over a multi-week window to establish the daily profile:

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(28d)
| where SubType_s == "FlowLog"
| extend HourOfDay = hourofday(TimeGenerated)
| summarize AvgBytesMB = round(avg(InboundBytes_d + OutboundBytes_d) / 1048576, 2),
            StdDevMB = round(stdev(InboundBytes_d + OutboundBytes_d) / 1048576, 2)
    by HourOfDay
| order by HourOfDay asc
```

### Day-of-Week Patterns

Weekday traffic typically differs significantly from weekend traffic. E-commerce workloads may spike on weekends, while enterprise SaaS applications are quiet. Compute per-day-of-week baselines:

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(28d)
| where SubType_s == "FlowLog"
| extend DayOfWeek = dayofweek(TimeGenerated) / 1d
| summarize AvgFlows = avg(FlowCount_d),
            P95Flows = percentile(FlowCount_d, 95)
    by DayOfWeek
| order by DayOfWeek asc
```

### Seasonal Variations

Monthly and quarterly cycles affect traffic: end-of-quarter reporting surges, holiday retail peaks, fiscal year-end processing. Capture at least 3-6 months of data before establishing seasonal baselines. Use time-series decomposition to separate trend, seasonal, and residual components.

---

## Anomaly Detection Approaches

### Statistical Methods (Standard Deviation)

The simplest anomaly detection flags data points that deviate by more than N standard deviations from the rolling mean. A 2-sigma threshold catches ~5% of normal variation as anomalous; 3-sigma catches ~0.3%.

```kql
let baseline = AzureNetworkAnalytics_CL
| where TimeGenerated between (ago(28d) .. ago(1d))
| where SubType_s == "FlowLog"
| extend HourOfDay = hourofday(TimeGenerated)
| summarize BaselineMean = avg(InboundBytes_d), BaselineStdDev = stdev(InboundBytes_d) by HourOfDay;
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(1h)
| where SubType_s == "FlowLog"
| extend HourOfDay = hourofday(TimeGenerated)
| summarize CurrentBytes = sum(InboundBytes_d) by HourOfDay
| join kind=inner baseline on HourOfDay
| extend Deviation = (CurrentBytes - BaselineMean) / BaselineStdDev
| where abs(Deviation) > 3
| project HourOfDay, CurrentBytes, BaselineMean, BaselineStdDev, Deviation
```

### ML-Based Detection (Azure Monitor Smart Detection)

Azure Monitor dynamic thresholds use machine learning models that automatically learn the seasonal and trend patterns of each metric. The model requires a minimum of 3 days of data (10 days recommended) to calibrate.

Sensitivity levels:

- **High**: Detects small deviations. More alerts, fewer missed anomalies. Use for critical security metrics.
- **Medium**: Balanced detection. Recommended starting point for most network metrics.
- **Low**: Only large deviations trigger. Fewer alerts, potential to miss subtle degradation. Use for noisy metrics.

---

## Deviation Alerting

### Dynamic Threshold Configuration

Configure dynamic thresholds in Azure Monitor to automatically alert when metrics deviate from learned patterns:

```bash
az monitor metrics alert create \
  --name "DynamicBaseline-VNetThroughput" \
  --resource-group MyRG \
  --scopes <vnet-gateway-resource-id> \
  --condition "avg ExpressRouteGatewayBitsPerSecond > dynamic medium 4 of 5 since 2024-01-01T00:00:00Z" \
  --window-size 15m \
  --evaluation-frequency 5m \
  --action-group <action-group-id> \
  --severity 2
```

The `4 of 5` parameter means the condition must be true in 4 of the last 5 evaluation periods before firing, reducing transient false positives.

### Sensitivity Tuning

Start with medium sensitivity and adjust based on alert volume:

- If receiving >5 false positives per day on a metric, reduce to low sensitivity.
- If missing known degradation events, increase to high sensitivity.
- Review and re-tune monthly as traffic patterns evolve.

---

## Seasonal Adjustment for Business Cycles

Adjust baselines for known business events that cause legitimate traffic changes:

- **Retail**: Black Friday, Cyber Monday, holiday season (November-January). Pre-adjust baselines upward by expected growth factor.
- **Financial**: Quarter-end reporting (last week of March, June, September, December). Expect 2-3× batch processing traffic.
- **SaaS**: Product launch events, marketing campaigns. Coordinate with business teams to tag expected traffic surges.

Use Azure Monitor alert processing rules to suppress or adjust alert thresholds during known events rather than permanently widening baselines.

---

## Capacity Planning from Baselines

### Trend Extrapolation

Use linear regression on monthly peak throughput to project when capacity limits will be reached:

```kql
AzureMetrics
| where ResourceProvider == "MICROSOFT.NETWORK"
| where MetricName == "BitsInPerSecond"
| where TimeGenerated > ago(180d)
| summarize MonthlyPeakBps = max(Maximum) by Month = startofmonth(TimeGenerated)
| order by Month asc
| serialize
| extend MonthIndex = row_number()
| extend ProjectedGrowth = MonthlyPeakBps * 1.0
| render timechart
```

For programmatic forecasting, export monthly peaks and fit a linear or exponential growth model. If peak throughput is growing at 8% per month and current ExpressRoute circuit is at 60% utilization, the circuit will reach 80% in approximately 4 months — triggering a capacity upgrade decision.

### Growth Modeling

Account for both organic growth and step-function changes:

- **Organic growth**: Gradual increase in users, devices, or transaction volume. Model with linear or low-order polynomial regression.
- **Step-function changes**: New application onboarding, office openings, acquisition integration. Add known future loads to the trend projection.
- **Cloud migration traffic**: Workloads moving to/from cloud generate temporary high traffic during migration windows, followed by a new steady state.

### Capacity Threshold Recommendations

| Utilization Level | Action |
|---|---|
| < 50% | Monitor. No action needed. |
| 50-70% | Plan. Begin evaluating upgrade options and lead times. |
| 70-85% | Prepare. Initiate procurement or provisioning of additional capacity. |
| > 85% | Act. Execute capacity expansion immediately to avoid congestion. |

For ExpressRoute circuits, lead time for provisioning can be 2-8 weeks depending on the provider. For VPN gateways, scaling is faster (hours) but still requires planned maintenance windows for active-active reconfiguration.

**Analysis only — verify against vendor documentation before applying.**
