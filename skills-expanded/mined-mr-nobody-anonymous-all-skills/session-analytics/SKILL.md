---
name: session-analytics
description: Parse developer and agent session traces into productivity telemetry, decision trails, time allocation, and cognitive bottleneck metrics.
category: productivity
aliases:
- developer-telemetry
- productivity-analytics
- session-metrics
- work-log-parser
triggers:
- parse session analytics
- analyze my productivity session
- extract decision trail from working session
- summarize developer time allocation
- identify cognitive bottlenecks in work log
keywords:
- analytics
- session
- metrics
- telemetry
- time
- productivity
- bottlenecks
- decisions
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- session-trace-parsing
- decision-extraction
- bottleneck-detection
- time-auditing
inputs:
- session_log
- command_history
- agent_transcript
outputs:
- productivity_report
- time_breakdown
- decision_log
- bottleneck_recommendations
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- analytics
- metrics
- productivity
- session
- telemetry
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Session Analytics

## Purpose
Parses developer command logs, shell histories, and agent interaction transcripts into actionable productivity analytics. Extracts decision trails, quantifies focus vs. context-switching intervals, and pinpoints cognitive friction points.

## When to Use
- Reviewing end-of-day or end-of-sprint developer session logs.
- Identifying recurring friction points, slow commands, or debugging loops.
- Extracting architecture and design decisions made during an exploratory agent pair-programming session.
- Optimizing focus time and eliminating unnecessary context switching.

## When NOT to Use
- Micromanaging individual engineers with punitive surveillance metrics.
- Parsing real-time production server access telemetry (use `utilities.system-monitor`).

## Capabilities
- **Transcript & Log Parsing**: Process agent transcripts, bash histories, and git logs into unified timelines.
- **Decision Extraction**: Surface explicit architectural choices, discarded alternatives, and trade-offs.
- **Context-Switch Detection**: Measure time gaps and frequency of task switching.
- **Productivity Scoring**: Quantify deep-work duration, compilation latency, and iteration speed.

## Inputs
- `session_data` (required) — Terminal log, transcript JSONL, or work diary text.
- `focus_interval` (optional) — Expected time window for analysis (e.g., 2 hours, 1 day).

## Workflow
1. Ingest session event data, normalizing timestamps and action categories.
2. Group actions into focus blocks: coding, testing, debugging, research, and idle intervals.
3. Identify looping behavior (e.g., repeating the same failing test 8 times without progress).
4. Extract explicit rationale statements and decisions logged during the session.
5. Generate a concise visual summary report with specific optimization recommendations.

## Tools
- Text and log parsing utilities.

## Examples
- "Parse session analytics from today's transcript and summarize my deep-work hours."
- "Extract the decision trail from this 3-hour agent pair programming session."
- "Identify cognitive bottlenecks and repetitive loops in my development workflow."

## Safety
- Strip all credentials, API keys, and private customer information during transcript ingestion.
- Preserve privacy of developer logs.

## Source
Custom skill maintained in this library for developer productivity telemetry.

## Notes
Pairs with `utilities.agent-transcript` and `productivity.daily-journal`.
