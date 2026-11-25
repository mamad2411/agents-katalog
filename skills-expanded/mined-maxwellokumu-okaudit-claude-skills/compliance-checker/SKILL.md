---
name: compliance-checker
description: Compare system configuration evidence against common control frameworks and produce a concise compliance assessment with gaps and remediation priorities.
---

# Compliance Checker

Use this skill when the user needs to assess configuration evidence against a named compliance framework such as CIS, SOC2, ISO27001, or PCI-DSS.

## Goal

Help Claude review configuration inputs, identify failed or missing controls, explain what the gaps mean, and present practical remediation guidance.

## Workflow

1. Confirm which framework or standard the user wants to assess.
2. Review the provided configuration evidence and note any missing or malformed input data.
3. Compare the evidence against the requested control expectations.
4. Summarize passing controls, failing controls, and the highest-priority remediation actions.
5. Present the result in a way that is easy for an auditor or system owner to act on.

## Inputs

Expected inputs from the bundled tool metadata:
- config: Path to a JSON file describing the system configuration to assess.
- standard: Target framework or standard to compare against.

## Bundled Files

- main.py contains the executable checker logic.
- README.md provides human-facing usage notes and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example evidence files for testing and demonstration.

## Guidance

Prefer concise compliance language. Call out control failures clearly, explain why they matter, and separate confirmed findings from assumptions caused by missing evidence.
