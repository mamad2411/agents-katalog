---
name: pericles-skill-registry
version: 2026.05.0
description: >
  How the Skill Registry resolves, validates, and composes Skills at runtime. Use
  this WHENEVER you build or change the registry loader, compose a Skill Stack,
  resolve dependencies, validate pipeline position, pin versions, or wire lineage.
  Encodes composition-time validation (<100ms/Skill), tenant→platform namespace
  resolution, the acyclic dependency graph, version pinning, and the link to
  per-invocation lineage. The registry is not built yet — this is the contract to build to.
doctrine_refs: [§1, §4, §8; Manifest Spec; Security §2, §8]
depends_on: [pericles-skill-authoring, pericles-tenant-isolation, pericles-functional-agent]
last_reconciled: 2026-05-28
---

# Pericles Skill Registry (build skill)

The registry is what makes "a deployment is a composed Skill Stack, not custom code"
true (§1). It loads manifests, validates them against each other, resolves
dependencies within a tenant's namespace, and hands the runtime a verified graph to
execute. **It is not built yet** — `DataSourceToolConfig` (per-org tool enablement) is
the closest existing primitive. Build to the contract below.

## When to use this skill

Building/changing the registry loader or resolver; composing a Skill Stack for a
deployment; adding dependency resolution, version pinning, or lineage; debugging a
composition failure.

## Responsibilities

1. **Load + validate manifests** (`pericles-skill-authoring`). Reject malformed
   manifests at load.
2. **Composition-time validation** — when a Skill Stack is composed, validate every
   Skill in **< 100 ms each** (`pericles-observability` SLA). Validation includes the
   pipeline-position rules below.
3. **Resolve dependencies** within the tenant namespace, producing an **acyclic** graph.
4. **Pin versions** per tenant so a deployment is reproducible and a retired version
   forces a bounded migration.
5. **Emit lineage** — record the resolved Skill IDs + versions for each invocation
   (`parent_invocation_id` chain, `pericles-observability`).

## Pipeline-position validation (§4)

The registry enforces `data_access.pattern` consistency at composition:

- A **`post_validation`** Skill may depend only on pipeline inputs / other
  post_validation Skills — **never** on a Topical/Regional/Industry Skill directly
  (that would re-query raw signal at action time).
- A **`pre_validation`** Skill may compose Topical/Regional/Industry Skills (it is
  establishing truth).
- A **`cross_pipeline`** Skill consumes pipeline inputs by default; if it composes a
  Topical/Regional/Industry Skill, the manifest MUST set `gateway_path: true` and the
  resolution goes through the **audited gateway path** (logged with reasons —
  `gateway_path_used` in the invocation log).

Reject composition if a Skill's declared pattern is inconsistent with its actual
dependencies. This is the mechanism that prevents the §4 misclassification failure.

## Namespace resolution (multi-tenant)

`resolve(skillId, tenant)`:

```
1. look up tenant/<tenant>/<id>      # tenant-scoped Custom Skill, if any
2. else look up platform/<id>        # platform Skill
3. else fail
```

A **platform**-visibility manifest may NOT reference a **tenant** Skill. A tenant
Skill depending on a platform Skill is the supported extension pattern (§8). Resolution
can never reach `tenant/<other>` (`pericles-tenant-isolation` guarantee 4).

## Version pinning & lifecycle interplay

- Each tenant Stack pins exact versions. New `published` versions don't auto-upgrade.
- `deprecated` resolves for already-pinned tenants; new pins discouraged.
- `retired` is unresolvable → pinned tenants must migrate within 7 days
  (`pericles-observability` incident flow). A post-promotion version tamper is P0
  (`pericles-tenant-isolation`).

## What this forbids

Composing a Stack without per-Skill validation; a `post_validation` Skill depending on
a Topical/Regional/Industry Skill; a `cross_pipeline` Skill reaching Topicals without
`gateway_path: true` + the audited path; cross-tenant resolution; cyclic dependencies;
silent version upgrades.

## Verification

Composition rejects pattern-inconsistent graphs and cycles; per-Skill validation meets
<100ms; resolution honors tenant→platform and never crosses tenants; pinned versions
are reproducible; every composed invocation emits lineage. Add tests for: a
post_validation→Topical dependency (must reject), a cross_pipeline→Topical without
gateway flag (must reject), and a cross-tenant resolution attempt (must fail).

## Existing standards (read alongside)

Skill Manifest Spec + Doctrine §4 (Notion); `DataSourceToolConfig` (the existing
per-org enablement primitive); `.claude/rules/11-security.md`.

## Open questions

- Where the registry runs (in-process module vs a service) and how manifests are
  packaged — decide with the platform team; affects `pericles-deployment-shapes`.
- Whether `DataSourceToolConfig` is subsumed by the registry's per-tenant Stack or
  remains a separate enablement layer.

## Changelog

- 2026.05.0 — Initial draft. Contract for an unbuilt registry; pipeline-position +
  namespace + pinning rules grounded in Doctrine §4/§8 and the Security spec.
