---
name: ics-detection-anomaly
description: "Ics Ics Detection Anomaly."
domain: cybersecurity
---

|
| Deterministic Traffic | ICS networks exhibit highly predictable communication patterns where the same master polls the same slaves at fixed intervals with identical function codes |
| Isolation Forest | Unsupervised machine learning algorithm that isolates anomalies by randomly partitioning feature space, effective for OT traffic with low anomaly rates |
| Polling Interval | Time between consecutive SCADA master requests to a slave device, typically fixed and configurable (100ms to 10s) |
| Function Code Allowlist | Set of permitted industrial protocol operations for each communication pair, enforced by anomaly detection rules |
| Topology Baseline | Complete map of all authorized device-to-device communication paths in the OT network |
| Physics-Based Detection | Using physical process models (thermodynamics, fluid dynamics) to detect attacks that manipulate the process while spoofing sensor data |

## Tools & Systems

- **Nozomi Networks Guardian**: OT anomaly detection with AI-powered baseline learning and industrial protocol analysis
- **Dragos Platform**: Threat detection using behavioral analytics and threat intelligence specific to ICS environments
- **Scikit-learn**: Python ML library with Isolation Forest, One-Class SVM, and Local Outlier Factor for anomaly detection
- **Zeek with OT plugins**: Network security monitor with Modbus, DNP3, and BACnet protocol analyzers for baseline building

## Output Format

```
ICS Anomaly Detection Report
==============================
Detection Period: YYYY-MM-DD to YYYY-MM-DD
Baseline Size: [N] communication profiles

ANOMALIES DETECTED: [N]
  Critical: [N]  High: [N]  Medium: [N]  Low: [N]

[SEVERITY] ANOMALY_TYPE
  Source: [IP] -> Target: [IP]:[Port]
  Detail: [Description of deviation from baseline]
  Baseline: [Expected behavior]
  Observed: [Actual behavior]
```
