---
name: backward-compatibility
version: 1.0.0
description: Preserving compatibility for existing consumers/data/config across a change — beyond API versioning, covering data format, config, and behavioral compatibility. Load when a change could affect anything already depending on current behavior. Do NOT use for explicit API contract versioning schemes and sunset policy — that is `api-versioning`; this skill covers everything else something might depend on.
---

# Backward Compatibility

## Broader than API versioning

`api-versioning` covers explicit API contracts; backward compatibility covers everything else that something else might depend on: on-disk data formats, configuration file formats, CLI argument behavior, exported library interfaces, even implicit behavioral guarantees (ordering, timing, error conditions) that were never formally documented but are relied upon anyway.

## Assume something depends on current behavior

Unless you can verify otherwise, assume existing behavior has a dependent — a config format change that "shouldn't matter" can break someone's automation script that parses it. Check for actual consumers before assuming a change is safe, rather than assuming safety because the change looks internal.

## Compatibility strategies

Additive change over modification (new field/flag alongside the old, not replacing it); a compatibility shim/adapter layer during a transition period; feature-flagged behavior change so consumers can opt in rather than being forced; clear deprecation warnings before removal, with a real runway.

## When compatibility must break

Sometimes breaking compatibility is the right call (a security fix, a fundamentally broken behavior) — when it is, say so explicitly, document the migration path for affected consumers, and treat it with release-gate rigor (see `release-engineering`, `governance`) rather than as a routine change.

## Testing compatibility

Test old-format inputs/data against the new code, not just new-format inputs — this is the direction most likely to be skipped and most likely to actually break in production.
