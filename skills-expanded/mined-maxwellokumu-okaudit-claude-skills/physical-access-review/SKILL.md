---
name: physical-access-review
description: Analyze badge or door access logs so Claude can explain after-hours activity, repeated failures, and other physical access anomalies clearly.
---

# Physical Access Review

Use this skill when the user wants to audit badge access logs, identify unusual physical entry patterns, or investigate after-hours and failed-access events.

## Goal

Help Claude review physical access activity, highlight suspicious or policy-relevant patterns, and summarize the findings in a practical audit-ready format.

## Workflow

1. Confirm the badge log file, business hours window, and any role or door access reference data.
2. Review the access events for after-hours activity, repeated failures, unusual door usage, or patterns that may suggest misuse.
3. Distinguish clear anomalies from events that may depend on role context or approved exceptions.
4. Highlight the most important access patterns and the likely follow-up actions.
5. Present a concise summary suitable for facilities, security, or audit stakeholders.

## Inputs

Expected inputs from the bundled tool metadata:
- logs: Path to the badge access log CSV.
- hours: Optional business hours window.
- roles: Optional path to badge role and door mapping data.
- failed-threshold: Optional failed-attempt threshold.

## Bundled Files

- main.py contains the executable access review logic.
- README.md provides guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative badge logs.

## Guidance

Preserve context and avoid overstating intent. Explain why a pattern is notable, and call out where role or facility context is needed before drawing stronger conclusions.
