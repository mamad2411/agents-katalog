---
name: validating-detections-with-atomic-tests
description: 'Validates detection coverage by mapping Atomic Red Team tests to ATT&CK techniques,
  checking which of your detections cover each tested technique, and reporting coverage gaps.
  Activates for requests to validate detections with atomic tests, map Atomic Red Team to coverage,
  or find detection gaps against tested techniques.'
domain: cybersecurity
subdomain: threat-hunting
tags:
  - threat-hunting
  - detection-engineering
  - atomic-red-team
  - coverage
  - validation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1059
  - T1003
  - T1053
d3fend:
  - D3-PSA
  - D3-NTA
references:
  - 'Atomic Red Team — https://github.com/redcanaryco/atomic-red-team'
  - 'MITRE ATT&CK techniques — https://attack.mitre.org/techniques/'
---

# Validating Detections With Atomic Tests

## When to Use

- You want to validate that your detections fire for specific ATT&CK techniques by correlating
  Atomic Red Team test definitions with your detection inventory.
- You are measuring coverage and identifying gaps before or after running atomics.

**Do not use** the atomics themselves on production systems without authorization and isolation —
they execute adversary behaviors. This skill performs mapping/coverage analysis offline.

## Prerequisites

- An export of Atomic test→technique mappings (CSV/JSON) and your detection inventory mapped to
  ATT&CK techniques.

## Workflow

### Step 1: Compute coverage

```bash
python scripts/analyst.py coverage --atomics atomics.json --detections detections.json
```

Joins atomic-tested techniques with your detections' covered techniques and reports covered vs
uncovered techniques.

### Step 2: Prioritize gaps

Rank uncovered techniques by the number of atomic tests (more atomics → more validated adversary
behavior you currently miss).

### Step 3: Validate live (authorized/isolated)

For covered techniques, run the corresponding atomic in an isolated range and confirm the detection
fires; record results.

### Step 4: Close gaps

Author detections for high-priority uncovered techniques and re-run coverage.

## Validation

- Coverage join keys on ATT&CK technique IDs (including sub-techniques).
- Covered and uncovered technique lists are complete and disjoint.
- Gap prioritization reflects atomic-test counts.

## Pitfalls

- Sub-technique vs parent-technique mismatch (T1059 vs T1059.001) skewing coverage.
- Claiming coverage from a rule that exists but is disabled/untuned.
- Running atomics outside an isolated, authorized range.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the coverage tool.
- Atomic Red Team and ATT&CK references (linked in frontmatter).
