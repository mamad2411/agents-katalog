---
name: structural-integrating
description: Use when wiring a feature, service, worker, pipeline, dependency, API, model, adapter, or migration into a larger system or cross-team boundary.
---

# Structural Integrating

Local correctness stops at the seam. Integration proves the whole still works when the part joins it.

Core rule:

> Guard your part from the whole, guard the whole from your part, and give every cross-part invariant an explicit home.

## Default output

```md
## Whole-system map
- Shared substrate:
- Cycles / cold-start risks:
- Existing control loops:

## Boundary contract
- Producer / consumer contract:
- Parser and compatibility:
- Contract test:

## Bidirectional blast radius
- What the whole can do to this part:
- What this part can do to the whole:
- Fallback / rate / quota / breaker:

## Integration proof
- Dark launch / ramp:
- End-to-end probe:
- Edge owner / expiry:
```

## Integration checks

- Learn the whole before wiring in: DNS, config, identity, zones, shared pools, queues, tables, deploy steps, and boot cycles.
- Pin the boundary contract with schema and contract tests. Reject invariant violations; tolerate unknown additive fields where safe.
- Bound waits, retries, and fallbacks so the whole's bad day does not freeze this part.
- Bound emitted load, fan-out, retries, and resource share so this part cannot melt the whole.
- Give distributed invariants a home: coordinator, owner, saga, quorum, idempotency key, or explicit reconciliation.
- Compose control loops deliberately. Separate timescales or assign one loop authority over a shared lever.
- Wire in dark, fallback first, then ramp traffic.
- Prove the whole path works with an end-to-end request and a fault, not only component health.
- Give every new edge an owner, contract test, and sunset/review date.

## Red flags

- “They are separate services” used as proof they fail independently.
- Contract described in Slack but not enforced by tests or schemas.
- Retrying into a struggling dependency without cap, jitter, deadline, or breaker.
- A new adapter, shim, or edge with no owner and no removal plan.
- Green components but no whole-path probe.
