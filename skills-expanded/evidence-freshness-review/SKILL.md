---
name: evidence-freshness-review
description: Check supplier evidence ages against the 365-day policy, preserve evidence identifiers, and classify expired records as blocking findings.
tools: [validate_evidence_freshness]
---

# Evidence freshness review

## When to use

Use this procedure whenever a supplier case contains certificates, attestations, audit records, or other dated control evidence.

## Steps

1. Pass the complete control list to `validate_evidence_freshness`.
2. Use `maximum_age_days=365`; do not silently change the policy threshold.
3. Preserve every `control_id`, `evidence_id`, original status, and evidence age.
4. Treat a record older than the limit as expired and blocking.
5. Return both the normalized findings and the identifiers of blocking controls.

## Do not use

Do not use freshness as a substitute for sanctions screening, risk scoring, or human publication authority.
