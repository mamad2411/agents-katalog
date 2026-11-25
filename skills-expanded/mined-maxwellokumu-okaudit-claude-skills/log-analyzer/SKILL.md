---
name: log-analyzer
description: Review log data for suspicious events and help Claude explain what stands out, why it matters, and which findings deserve escalation or follow-up.
---

# Log Analyzer

Use this skill when the user wants to review security logs for suspicious activity, apply known event patterns, or summarize noteworthy events from CloudTrail or similar sources.

## Goal

Help Claude identify suspicious log events, explain their likely significance, and present findings in a concise format suitable for investigation or audit review.

## Workflow

1. Confirm whether the user is analyzing local log files or using a live mode such as AWS.
2. Review the log source and any custom pattern library the user wants applied.
3. Identify suspicious events, severity patterns, and time-bounded activity relevant to the request.
4. Distinguish clear findings from low-confidence or context-dependent matches.
5. Summarize the key events, likely risks, and recommended follow-up actions.

## Inputs

Expected inputs from the bundled tool metadata:
- logs: Optional path to a local JSON-lines log file.
- patterns: Optional path to custom suspicious-event patterns.
- mode: Optional execution mode such as local or aws.
- start: Optional ISO timestamp filter start.
- end: Optional ISO timestamp filter end.

## Bundled Files

- main.py contains the executable log analysis logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative log data and patterns.

## Guidance

Prioritize clarity over volume. Surface the most important suspicious events first, explain the reasoning, and note when additional context is needed before drawing conclusions.
