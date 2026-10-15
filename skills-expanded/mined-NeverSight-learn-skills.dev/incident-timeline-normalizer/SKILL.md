---
name: incident-timeline-normalizer
description: Vendor-neutral skill to normalize incident event logs into an ordered timeline and compute phase durations.
---

## When to invoke
- You have incident notes/events from multiple systems and need a consistent timeline.
- You want basic metrics like time-to-detect and time-to-mitigate.

## Inputs needed
- `--events_json`: Path to input events JSON.
- `--out_json`: Path to write normalized timeline JSON.

Events JSON format (reference implementation)
- `incident_id` (string)
- `events[]`:
  - `timestamp` (string; ISO-8601, RFC-2822, or epoch seconds)
  - `type` (string; e.g., `detected`, `acknowledged`, `mitigated`, `resolved`, `note`)
  - `message` (string)

## Workflow
1. Parse timestamps with multiple fallbacks.
2. Sort events ascending.
3. Compute:
   - first event time
   - detected time (first `detected`)
   - mitigated time (first `mitigated`)
   - resolved time (first `resolved`)
   - durations in seconds for common phases (when possible)
4. Emit normalized timeline and computed metrics.

## Output format
JSON:
- `incident_id`
- `timeline[]`: `{ts_iso, type, message}`
- `metrics`: `time_to_detect_s`, `time_to_mitigate_s`, `time_to_resolve_s`

## Guardrails
- Timestamp parsing is best-effort; ambiguous formats may be skipped.
- Metrics are computed only when the required markers exist.

## Reference code
- `incident_timeline_normalizer.py`
