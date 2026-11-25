---
name: anomaly-detector
description: Compare recent activity against a historical baseline to identify behavioral anomalies and help Claude explain which users or patterns warrant deeper investigation.
---

# Anomaly Detector

Use this skill when the user wants to compare current log activity against a baseline, identify unusual behavior, or investigate whether user activity has deviated from normal patterns.

## Goal

Help Claude highlight meaningful anomalies, explain why they stand out from the baseline, and present the results in a way that supports security review or audit follow-up.

## Workflow

1. Confirm the baseline log source, the test period log source, and any tuning preferences such as sensitivity.
2. Review whether the baseline has enough activity to support a credible comparison.
3. Compare the test period against the baseline to identify users or patterns that exceed expected thresholds.
4. Separate strong anomaly candidates from weak signals caused by sparse data or noisy inputs.
5. Present a concise anomaly summary with likely priorities for investigation.

## Inputs

Expected inputs from the bundled tool metadata:
- logs: Path to the historical baseline log file.
- test: Path to the test period log file.
- sensitivity: Optional threshold sensitivity.
- min_events: Optional minimum baseline event count.

## Bundled Files

- main.py contains the executable anomaly detection logic.
- README.md provides usage notes and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative baseline and test logs.

## Guidance

Treat anomaly detection as a triage aid rather than definitive proof of malicious behavior. Call out data quality limits and explain why each anomaly is notable.
