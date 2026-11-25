---
name: segmentation-validator
description: Validate zone isolation and cross-zone traffic controls so Claude can explain where segmentation rules may allow unauthorized or risky network flows.
---

# Segmentation Validator

Use this skill when the user wants to check whether firewall rules align with defined network zones and whether segmentation boundaries are being enforced properly.

## Goal

Help Claude analyze zone definitions and traffic rules, detect problematic cross-zone paths, and explain segmentation weaknesses in a practical, audit-ready way.

## Workflow

1. Confirm the zone definition file and the firewall rule file to review.
2. Normalize the zones and traffic flows so cross-zone paths can be evaluated consistently.
3. Identify unauthorized, risky, or unexpected flows between zones.
4. Highlight whether the issue is a direct rules problem, a missing zone assignment, or unclear network design.
5. Present the findings with enough context for remediation or audit reporting.

## Inputs

Expected inputs from the bundled tool metadata:
- zones: Path to the JSON zone definition file.
- rules: Path to the CSV firewall rules file.

## Bundled Files

- main.py contains the executable segmentation analysis logic.
- README.md provides guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative zone and rule data.

## Guidance

Stay focused on trust boundaries and unauthorized movement risk. Explain which zones are involved, what traffic is allowed, and why the flow may violate segmentation intent.
