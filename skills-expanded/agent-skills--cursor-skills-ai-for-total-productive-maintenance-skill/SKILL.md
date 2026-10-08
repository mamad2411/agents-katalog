# AI for Total Productive Maintenance

## Description

Predicts equipment failures, supports autonomous maintenance, and improves OEE across the eight TPM pillars.

## When to use

You are implementing Total Productive Maintenance and want to use AI to improve OEE, eliminate breakdowns, and empower operators to maintain equipment autonomously.

## Usage

- **Eight TPM pillars**: support autonomous, planned, quality, focused, early-equipment, training, safety, and office TPM.
- **OEE analytics**: measure and improve Availability x Performance x Quality.
- **Condition-based maintenance (CBM)**: monitor vibration, temperature, current, oil, and acoustics.
- **Autonomous maintenance**: enable operators to clean, inspect, and lubricate with AI-guided diagnostics.
- **Kaizen for equipment**: drive small, data-driven improvements to reduce minor stops and defects.

## Steps

1. Collect sensor, work-order, and OEE data for critical equipment.
2. Engineer condition indicators and OEE-loss labels from historical failures.
3. Train CBM and failure-risk models to prioritize maintenance actions.
4. Integrate alerts into operator rounds and maintenance planning systems.
5. Track OEE, MTBF, MTTR, and false-alarm rate to validate impact.

## Code pattern

```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Predict unplanned downtime from sensor features
X = df[["vibration_rms", "temperature", "motor_current", "cycle_count"]]
y = df["failure_next_24h"]
model = RandomForestClassifier(class_weight="balanced", random_state=42).fit(X, y)
```

## Tuning notes

- Balance recall for failure risk with false-alarm rate to avoid alert fatigue.
- Use OEE loss history to label maintenance priority, not just binary failure.
- Integrate operator annotations; domain knowledge is critical for the Autonomous Maintenance pillar.

## Verification

1. Train a failure-prediction model and measure lead time to the next breakdown.
2. Compare OEE before and after a pilot on one line or cell.
3. Verify that alerts lead to operator actions and track mean time to repair (MTTR).

## References

- https://doi.org/10.1016/j.eswa.2024.126283
- https://doi.org/10.1016/j.cie.2021.107267
- https://doi.org/10.3390/app11156953
- https://doi.org/10.1108/jqme-07-2022-0041
- https://hal.science/hal-05001680
