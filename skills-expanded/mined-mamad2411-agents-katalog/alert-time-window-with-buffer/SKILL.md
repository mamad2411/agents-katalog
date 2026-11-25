---
name: alert-time-window-with-buffer
description: Compute a query time window that covers the alert plus a 30-min buffer by parsing startsAt from various schemas (Alertmanager nested, top-level, annotations.timestamp), with a 60-min minimum and a sentinel "0001-01-01" guard.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [time-window, alerting, alertmanager, observability]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/plan_actions/detect_sources.py
imported_at: 2026-04-18T00:00:00Z
---

# Alert Time Window with Buffer

## When to use
Your agent queries Loki/Datadog/Grafana with a `time_range_minutes` parameter. Use the alert's own start time so the window covers the relevant period, but add a buffer so context before and after the alert is included. Multiple alert schemas put the timestamp in different places.

## How it works
- Look for `startsAt` in three places: `alerts[0].startsAt` (Alertmanager nested), top-level `startsAt`/`timestamp`, then `annotations.timestamp`.
- Parse with `datetime.fromisoformat(starts_at.replace("Z", "+00:00"))` to handle the trailing-Z variant.
- Treat year `< 2000` as a zero-value sentinel ("0001-01-01" from Alertmanager when the field isn't populated).
- Window = `max(60, (now - alert_time_minutes) + 35)` so we always have at least an hour and always include 30+ min of post-alert context.

## Example
```python
def _alert_time_range_minutes(raw_alert):
    starts_at = None
    alerts = raw_alert.get("alerts", [])
    if alerts and isinstance(alerts, list):
        starts_at = alerts[0].get("startsAt")
    if not starts_at:
        starts_at = raw_alert.get("startsAt") or raw_alert.get("timestamp")
    if not starts_at:
        annotations = raw_alert.get("annotations") or raw_alert.get("commonAnnotations") or {}
        starts_at = annotations.get("timestamp")

    if not starts_at: return 60
    try:
        alert_time = datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
        if alert_time.year < 2000:           # zero-value sentinel
            return 60
        minutes_ago = int((datetime.now(UTC) - alert_time).total_seconds() / 60)
        return max(60, minutes_ago + 35)     # 5 min pre + 30 min post buffer
    except (ValueError, TypeError):
        return 60
```

## Gotchas
- `datetime.fromisoformat` in Python 3.11+ handles offset suffixes; for older Pythons, replace `"Z"` with `"+00:00"` first.
- The minimum 60-min window matters — many backends (e.g. Loki) won't return useful data for a 1-min window even if the alert just fired.
- Always parse annotations as a fallback; some alert sources put `timestamp` only in the human-readable annotations section.
