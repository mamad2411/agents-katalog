---
name: evidence-driven-claim-validator
description: Reject LLM-generated root-cause claims that aren't supported by the actual evidence dict — claim mentions "memory" but no host_metrics? mark not-validated. Uses a per-keyword evidence requirement table and outputs a confidence score.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [hallucination-defense, claim-validation, evidence, scoring]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/nodes/root_cause_diagnosis/claim_validator.py
imported_at: 2026-04-18T00:00:00Z
---

# Evidence-Driven Claim Validator

## When to use
Your LLM returns a list of "validated claims" (with `extract_evidence_sources` references) but you don't trust them. You want a deterministic post-filter: each claim is checked against the real evidence dict, and a weighted confidence score is computed so downstream nodes can decide whether to loop or publish.

## How it works
- Per-claim keyword detection: if claim mentions "memory" or "cpu", evidence must include `host_metrics.data` or RDS metrics; "log/error/fail" requires logs; "rds/postgres/database" requires RDS metrics or events; etc.
- `validate_claim(claim, evidence)` returns a bool; `validate_and_categorize_claims` reshuffles claims between `validated` and `non_validated` lists based on the actual check.
- `extract_evidence_sources(claim, evidence)` attaches a list of "real" sources (cloudwatch_logs, datadog_monitors, ...) to each validated claim — falls back to the generic `evidence_analysis` sentinel.
- `calculate_validity_score` weighs validated-with-real-sources at 1.0, validated-but-failed-our-check at 0.5, non-validated at 0.0, plus a +0.1 bonus when at least one claim has non-generic evidence sources.

## Example
```python
def validate_claim(claim, evidence):
    cl = claim.lower()
    has_dd = bool(evidence.get("datadog_logs") or evidence.get("datadog_error_logs"))

    if any(k in cl for k in ("log","error","fail")) and not _has_any_logs(evidence):
        return False
    if any(k in cl for k in ("memory","cpu")) and not (
        evidence.get("host_metrics", {}).get("data")
        or _has_rds_metrics(evidence) or _has_performance_insights(evidence)
        or (any(kw in cl for kw in ("monitor","datadog")) and has_dd)
    ):
        return False
    if any(k in cl for k in ("rds","postgres","database","replication","connection",
                              "storage","disk","failover","reboot")) and not (
        _has_rds_metrics(evidence) or _has_rds_events(evidence)
        or _has_performance_insights(evidence)
    ):
        return False
    # ... lambda, s3, schema, vendor, k8s checks ...
    return True

def calculate_validity_score(validated, non_validated):
    if not validated and not non_validated: return 0.0
    score = total = 0.0
    for c in validated:
        srcs = c.get("evidence_sources", [])
        has_real = any(s != "evidence_analysis" for s in srcs)
        if c.get("validation_status") == "validated":
            score += 1.0 if has_real else 0.8
        else:
            score += 0.5
        total += 1.0
    total += len(non_validated)
    base = score / total if total else 0.0
    has_real_evidence = any(
        s != "evidence_analysis" for c in validated for s in c.get("evidence_sources", [])
    )
    return min(1.0, round(base + (0.1 if has_real_evidence and validated else 0), 2))
```

## Gotchas
- Keep the keyword tables close to the evidence shape; if you add a new evidence key, add the corresponding claim-keyword check. Otherwise the validator silently rubber-stamps new categories.
- The 0.8 vs 1.0 split between "validated with generic sources" vs "validated with real sources" is what makes the score meaningful — without it, a model that always answers "evidence_analysis" gets perfect scores.
- Apply this AFTER masking is reversed; otherwise placeholder strings won't match keyword checks.
