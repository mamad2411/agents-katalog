---
name: source-detection-from-alert-annotations
description: Auto-detect which observability backends to query for a given alert by scanning annotations + raw payload for source-specific keys (cloudwatch_log_group, s3_bucket, lambda_function, eks_cluster) plus URL-based heuristics on externalURL/generatorURL.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [alert-routing, multi-source, observability, planner]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/plan_actions/detect_sources.py
imported_at: 2026-04-18T00:00:00Z
---

# Source Detection from Alert Annotations

## How it works
Given a raw alert + investigation context + resolved integrations, build a `sources: dict[str, dict]` of "which backend should the planner consider, and with what extracted parameters". Two layers of heuristics:

1. **Structural source detection** (what platform fired the alert): inspect `externalURL`, `generatorURL`, `alerts[0].generatorURL`, `alert_source` field. URL substrings `grafana`, `honeycomb`, `coralogix` etc. select the backend even when an LLM extraction couldn't.
2. **Resource detection** (which resources to query): scan annotations for `cloudwatch_log_group`/`log_group`/`cloudwatchLogGroup`/`lambda_log_group` aliases, `s3_bucket`/`bucket`/`s3Bucket`/`landing_bucket`, etc. Same alias-set pattern repeats per resource type.

## When to use
You have many possible observability backends and many possible alert sources, and you want a planner to query only the relevant ones (don't hammer Datadog when the alert came from Grafana).

## Example
```python
def detect_sources(raw_alert, context, resolved_integrations=None):
    sources = {}
    if isinstance(raw_alert, str): raw_alert = {}

    alert_source = raw_alert.get("alert_source","").lower()
    if not alert_source:
        urls = [raw_alert.get("externalURL",""), raw_alert.get("generatorURL","")]
        if (alerts := raw_alert.get("alerts", [])): urls.append(alerts[0].get("generatorURL",""))
        if any("grafana" in str(u).lower() for u in urls):    alert_source = "grafana"
        elif any("honeycomb" in str(u).lower() for u in urls): alert_source = "honeycomb"
        elif any("coralogix" in str(u).lower() for u in urls): alert_source = "coralogix"

    annotations = {}
    if isinstance(raw_alert, dict):
        nested = raw_alert.get("annotations", {}) or raw_alert.get("commonAnnotations", {}) or {}
        annotations = {**nested, **{k: v for k, v in raw_alert.items() if v and k not in nested}}

    cloudwatch_log_group = (
        annotations.get("cloudwatch_log_group")
        or annotations.get("log_group")
        or annotations.get("cloudwatchLogGroup")
        or annotations.get("lambda_log_group")
    )
    if cloudwatch_log_group:
        sources["cloudwatch"] = {"log_group": cloudwatch_log_group, "region": ...}

    # Suppress real Grafana when the alert came from a non-Grafana platform unless a
    # synthetic backend is injected for testing
    if grafana_int and not (has_injected_backend or alert_source in ("grafana","")):
        grafana_int = None

    return sources
```

## Gotchas
- Always merge nested annotations + top-level enriched fields (LLM extracts may inject top-level keys).
- The "suppress backend X when alert source is Y" pattern keeps the planner honest — querying Datadog for a Grafana alert wastes calls and confuses the LLM with irrelevant logs.
- For each resource type, accept multiple casings of the same key (`cloudwatch_log_group`, `cloudwatchLogGroup`, `log_group`) — alert payloads come from many tools and conventions vary.
- For backends that need a credential-injected fixture in tests, look for a sentinel (`_backend` key) and bypass the alert-source filter so synthetic tests work.
