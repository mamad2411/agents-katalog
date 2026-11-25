---
name: tcx-source-gate
description: Route external investment evidence and preserve concise SourceSnapshot or Dataset provenance when a fixed-role analyst needs external facts, documents, prices, fundamentals, or time series.
---

# Data Source Routing

For each material missing fact or series:

1. Reuse an adequate supplied SourceSnapshot or Dataset.
2. Use one relevant enabled user Skill, Plugin, or MCP capability.
3. Use direct optional OpenBB when projected for this role.
4. Prefer an original public record when legal, accounting, regulatory,
   contractual, filing, or official-policy status is material.
5. Otherwise use a credible attributable source within its competence.
6. Preserve an explicit gap when adequate support is unavailable.

Check reusable current-workflow IDs before an external call. Use the smallest
call that can resolve the material gap. Do not repeat an unchanged successful
or terminal request. Retain valid partial results and fetch only missing
coverage. Do not recreate another role's data family or gather broad
just-in-case data.

Judge evidence against the claim, requested as-of, and consequence. OpenBB is
access to its returned provider, not a source class. Credible institutional,
provider-normalized, and reputable secondary evidence may support claims they
competently cover. Secondary does not mean screen-only. Independently check a
conclusion-driving claim when it is surprising, disputed, transformed, or
weakly attributed. Do not require a fixed source count.

A missing, stale, conflicting, or ambiguous field limits only dependent claims.
Evidence readiness, confidence, and action readiness remain separate; evidence
quality never creates order or execution authority.

Judge freshness against the requested as-of, publication or observation
cadence, and relevant market session. An unavailable future period is not a
gap. Preserve offset-free timestamps as ambiguous rather than inventing a
timezone, and convert epoch values exactly once. A timing ambiguity limits only
time-sensitive claims.

Use the current task's callable tools rather than a static inventory. Paid or
cost-unknown access requires user approval. If a named tool is deferred, use
one names-only exact-name lookup and inspect its schema once.

Continue only when another obtainable source has a credible path to changing
the conclusion, confidence, or readiness and its expected decision value
justifies the added work. Otherwise preserve the remaining gap and stop.

Use the active role skill for domain-specific filing, market-data, corporate
action, instrument, timezone, and macro-vintage requirements. When using direct
OpenBB, read [OpenBB MCP](references/openbb-mcp.md) before the call.

Record every external source actually used with `record_source_snapshot`.
Create a Dataset only for reusable structured rows or time series. Bind the
returned Snapshot and Dataset IDs to the consuming artifact.

Never install or configure providers, handle credential values, or treat
capability availability as evidence quality.
