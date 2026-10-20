---
name: healthy-short-circuit-skip-llm
description: Bypass an expensive LLM diagnosis when an alert is provably healthy (resolved/info severity, no error annotations, evidence-investigated-and-empty), guarded behind an env-var kill switch in case the heuristic misfires.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [optimization, short-circuit, llm-cost, healthy-finding]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/root_cause_diagnosis/evidence_checker.py
imported_at: 2026-04-18T00:00:00Z
---

# Healthy Short-Circuit: Skip the LLM

## When to use
Many alerts are noise (scheduled health checks, "resolved" notifications). Calling a reasoning LLM on each one wastes tokens and adds latency. You can prove an alert is non-actionable using four cheap checks; only when all four pass do you skip the LLM and emit a deterministic "healthy" report.

## How it works
- All four conditions must hold:
  1. `state ∈ {"normal","resolved","ok"}` (covers Grafana, CloudWatch, PagerDuty).
  2. `severity ∈ {"info","none",""}` (rules out resolved-critical that still warrants RCA).
  3. No error-signal annotations populated (`error`, `error_message`, `log_excerpt`, `failed_steps`).
  4. At least one investigation evidence key is present in `evidence` (proves we actually queried the systems and found nothing).
- A `HEALTHY_SHORT_CIRCUIT` env var (default `"true"`) lets ops disable the optimization without a deploy if it ever misfires.
- The "evidence key present even if empty" check is the trick — empty `grafana_logs: []` is itself a health signal ("we queried Loki, no errors").

## Example
```python
_HEALTHY_STATES     = frozenset({"normal","resolved","ok"})
_HEALTHY_SEVERITIES = frozenset({"info","none",""})
_ERROR_ANNOTATION_KEYS = ("error","error_message","log_excerpt","failed_steps")
_INVESTIGATED_EVIDENCE_KEYS = frozenset({
    "grafana_logs", "grafana_metrics", "grafana_alert_rules",
    "aws_cloudwatch_metrics", "aws_rds_events", "datadog_logs",
    "datadog_monitors", "eks_pods", "eks_events", ...
})

def is_clearly_healthy(raw_alert, evidence) -> bool:
    if not isinstance(raw_alert, dict): return False
    state = str(raw_alert.get("state","")).lower().strip()
    if state not in _HEALTHY_STATES: return False

    labels = raw_alert.get("commonLabels", raw_alert.get("labels", {})) or {}
    severity = str(labels.get("severity", raw_alert.get("severity",""))).lower().strip()
    if severity not in _HEALTHY_SEVERITIES: return False

    annotations = raw_alert.get("commonAnnotations", raw_alert.get("annotations", {})) or {}
    if any(annotations.get(k) for k in _ERROR_ANNOTATION_KEYS): return False

    return any(k in evidence for k in _INVESTIGATED_EVIDENCE_KEYS)

def diagnose_root_cause(state):
    if _short_circuit_enabled() and is_clearly_healthy(state.get("raw_alert", {}),
                                                       state.get("evidence", {})):
        return _handle_healthy_finding(state, ...)   # no LLM call
    # else proceed with normal LLM diagnosis
```

## Gotchas
- Always document the "blast radius if this misfires" — for a healthy short-circuit, the worst case is a real incident gets reported as healthy. Defend with the severity gate (firing critical never satisfies condition 2) plus the env kill switch.
- Use `frozenset` for the membership lookups — they're hot path.
- The "key present" check is subtly different from "key truthy". `grafana_logs: []` is a positive signal; `evidence.get("grafana_logs")` would treat it as missing.
