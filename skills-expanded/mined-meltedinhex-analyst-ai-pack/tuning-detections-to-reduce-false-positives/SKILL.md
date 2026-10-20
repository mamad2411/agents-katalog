---
name: tuning-detections-to-reduce-false-positives
description: 'Tunes noisy detections by analyzing historical alert data to quantify false-positive
  sources, recommend allow-list filters and threshold adjustments, and measure precision impact.
  Activates for requests to tune a detection, reduce false positives, or analyze alert noise and
  recommend filters.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - detection-engineering
  - false-positives
  - tuning
  - alert-triage
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1071
  - T1053
d3fend:
  - D3-PSA
  - D3-NTA
references:
  - 'Sigma rule specification (filters/condition) — https://github.com/SigmaHQ/sigma-specification'
  - 'Detection engineering precision/recall concepts — https://attack.mitre.org/resources/'
---

# Tuning Detections to Reduce False Positives

## When to Use

- A detection generates excessive false positives and you want a data-driven tuning plan: which
  fields/values drive the noise, what filters to add, and the precision impact.
- You are balancing recall against alert fatigue.

**Do not use** tuning that suppresses true positives — filters must target benign noise, not the
malicious pattern. Always estimate the impact on true positives before applying.

## Prerequisites

- Labeled alert history (CSV/JSON) with at least an outcome/label field (true_positive vs
  false_positive) and the alert's distinguishing fields.

## Workflow

### Step 1: Quantify false-positive sources

```bash
python scripts/analyst.py analyze alerts.csv --label verdict --field ParentImage
```

Ranks field values by how much false-positive volume they drive and computes current
precision/false-positive rate.

### Step 2: Recommend filters

Suggest allow-list filters for values that are overwhelmingly benign (high FP, no/low TP), with the
projected precision gain.

### Step 3: Estimate impact

Report how many true positives would be lost (should be zero/near-zero for safe filters).

### Step 4: Apply and monitor

Add the safe filters to the rule's `filter`/exclusion and continue monitoring precision.

## Validation

- FP-driving values are ranked by their false-positive contribution.
- Recommended filters target values with negligible true-positive loss.
- Projected precision and TP-loss are reported.

## Pitfalls

- Filtering a value that also carries true positives, blinding the detection.
- Over-fitting to one time window's noise.
- Tuning by gut feel instead of measured FP/TP contribution.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the tuner.
- Sigma spec and detection-engineering references (linked in frontmatter).
