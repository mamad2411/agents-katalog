---
name: log-error-analyzer
description: Analyze log files to extract errors, warnings and generate summary
---

# Log Error Analyzer

Analyze log files to extract errors, warnings and generate summary

## When to Use

- User wants to analyze logs
- User wants to log analysis
- Keywords: log, error, analysis, debug

## Required Parameters

- **log_path** (string): Path to log file

## Output

- **errors** (array): Extracted error lines
- **warnings** (array): Extracted warning lines
- **summary** (string): LLM summary of issues

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `read_log` -> 7 steps -> Exit: `ret_ok`, `ret_fail`
