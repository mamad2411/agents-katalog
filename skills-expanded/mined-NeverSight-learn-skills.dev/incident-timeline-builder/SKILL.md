---
name: incident-timeline-builder
description: Vendor-neutral skill to turn semi-structured incident logs into a normalized chronological timeline with clusters and gaps.
---

## When to invoke
- When writing an incident postmortem and you need a clean timeline.
- When you have log lines or chat exports with timestamps and need ordering and clustering.

## Inputs needed
- `--input`: Path to a text file with one event per line.
  - Each line should start with an ISO-8601 timestamp like `2026-05-10T12:34:56Z`.
- Optional `--out`: Path to write a JSON timeline.
- Optional `--gap-minutes`: Threshold to flag gaps (default 20).

## Workflow
1. Parse timestamps and messages; drop lines without a parseable timestamp.
2. Sort events.
3. Cluster events when adjacent messages are within N minutes.
4. Identify gaps larger than the threshold.

## Output format
JSON with:
- `events`: ordered list of `{ts, message}`.
- `clusters`: list of `{start_ts, end_ts, count}`.
- `gaps`: list of `{from_ts, to_ts, minutes}`.

## Guardrails
- Never change the meaning of messages; only normalize timestamp and ordering.
- If timezones are missing, treat times as UTC.

## Reference code
- `incident_timeline_builder.py`
