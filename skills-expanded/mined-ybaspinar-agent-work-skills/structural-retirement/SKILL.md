---
name: structural-retirement
description: Use when deprecating, removing, deleting, retiring, sunsetting, cleaning up, or decommissioning APIs, features, flags, services, tables, datasets, jobs, configs, docs, or code paths.
---

# Structural Retirement

Removal is safe only when the signals earned it and the irreversible step is hard to take by accident.

Core rule:

> Prove nothing still depends on it, contract in reverse, split delete decision from delete act, and leave nothing behind that names or resurrects it.

## Default output

```md
## Removal proof
- Live usage telemetry:
- Observation window / usage cycle:
- Dependency search:
- Slowest consumer:

## Retirement sequence
- Deprecation / sunset:
- Reverse contraction:
- Tombstone / compatibility:
- Irreversible delete plan:

## Cleanup
- Derivations / consumers:
- Data retention / hard-delete duty:
- Code/config/docs/tests:
- Resurrection guard:
```

## Retirement checks

- Prove zero use from live telemetry over the real usage cycle; grep is only a sample.
- Deprecate additively with a window for consumers you cannot force to upgrade.
- Contract in reverse: switch reads, stop writes, observe cold, then drop. Every intermediate step should be runnable and reversible.
- Separate the deletion decision from deletion: manifest/dry-run/review, then apply; four-eyes for irreversible/wide drops.
- Remove or re-home derivations, caches, indexes, exports, consumers, and in-flight obligations before killing the owner.
- Honour hard-delete duties for regulated or rights-bearing data; soft-delete is not destruction.
- Delete code, config, flags, tests, dashboards, runbooks, docs, and SDK references together once rollback is no longer needed.
- Confirm it stays gone with an alert/test/lint rule while resurrection remains plausible, and give that guard an expiry.

## Red flags

- “I grepped the main repo” as deletion proof.
- Public API hard cut with no Sunset/deprecation window.
- Drop-and-rename or `rm -rf` fused with selection logic.
- Derived data answering queries after source deletion.
- Archive used to avoid a duty to forget.
- Dead docs/config/flags still naming the removed thing.
