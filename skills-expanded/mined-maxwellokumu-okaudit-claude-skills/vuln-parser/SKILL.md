---
name: vuln-parser
description: Parse vulnerability scan results into a risk-ranked view so Claude can explain which hosts, findings, and remediation actions deserve attention first.
---

# Vulnerability Parser

Use this skill when the user has scan output that needs triage, prioritization, or summarization for remediation planning or audit review.

## Goal

Help Claude convert raw vulnerability scan data into a clearer, risk-focused analysis that highlights the most important remediation priorities.

## Workflow

1. Review the scan result file and confirm the format is readable enough to analyze.
2. Identify hosts, findings, severity levels, and any concentration of critical issues.
3. Rank the results by likely risk and remediation urgency rather than just listing raw counts.
4. Highlight the most exposed systems, recurring weakness patterns, and immediate next actions.
5. Present a concise triage summary that supports remediation planning or audit reporting.

## Inputs

Expected inputs from the bundled tool metadata:
- scan: Path to the vulnerability scan results file.
- output: Optional output format.
- top-hosts: Optional limit for the highest-risk hosts to highlight.

## Bundled Files

- main.py contains the executable parsing and ranking logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example scan outputs.

## Guidance

Keep the emphasis on prioritization. Separate raw severity from practical business risk when possible, and make it easy for the user to see what should be fixed first.
