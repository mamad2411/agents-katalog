---
name: capacitor-source-curation
description: Use when CapacitorJS guidance must be grounded in authoritative, current sources and converted into reusable, agent-usable patterns with freshness and drift controls.
---

# Capacitor Source Curation

## Specialization

Curate and validate CapacitorJS guidance against authoritative primary sources so that downstream skills, instructions, and agents produce code and decisions aligned with current Capacitor behavior — not stale documentation or community drift.

## Scope Boundaries

In scope:

- Authoritative source identification, freshness verification, and version pinning.
- Source catalog creation and maintenance for the Capacitor skill family.
- Identification of deprecated APIs, migration-breaking changes, and drift from official patterns.
- Mapping official sources to specific skill or guidance domains.

Out of scope:

- Implementation of Capacitor features.
- Plugin authoring or native bridge code.
- Release or store submission decisions.

## Trigger Conditions

- A new CapacitorJS skill, instruction, or guidance asset is being authored.
- An existing Capacitor skill is being updated and source freshness must be verified.
- A major Capacitor version release (e.g., v5 → v6 → v7) has occurred and drift must be assessed.
- Guidance is producing unexpected or incorrect Capacitor behavior in a target project.
- An agent requests a source check before implementing Capacitor-specific patterns.

## Inputs

- Target skill or guidance domain (e.g., plugin authoring, native APIs, release readiness).
- Evaluation date in ISO format (`YYYY-MM-DD`) for freshness calculations.
- Freshness threshold in days (default: 30).
- Known Capacitor version in use or target version range.
- Existing source catalog path when one exists (default: `./references/source-catalog.md`).

## Required Outputs

- Confirmed authoritative source list with URLs, access dates, and version scope.
- Freshness assessment: current, stale, or expired for each source.
- Drift log: deprecated APIs, changed behaviors, or breaking changes found.
- Recommended source-to-skill domain mappings.
- Updated or new `source-catalog.md` entry set.

## Authoritative Source Registry

| Source | Domain | URL | Notes |
|---|---|---|---|
| Capacitor Docs (Official) | All | https://capacitorjs.com/docs | Primary reference; check version selector |
| Capacitor GitHub | Core behavior, issues | https://github.com/ionic-team/capacitor | Source of truth for bugs and releases |
| Capacitor Plugins (Official) | Native APIs | https://capacitorjs.com/docs/apis | Core plugin API contracts |
| Capacitor Community Plugins | Extended APIs | https://github.com/capacitor-community | Community plugin registry |
| Capacitor Blog | Migration, releases | https://capacitorjs.com/blog | Release notes and deprecation announcements |
| Capacitor Config Reference | Configuration | https://capacitorjs.com/docs/config | `capacitor.config.ts` schema |
| Ionic Blog | Integration patterns | https://ionic.io/blog | Ionic + Capacitor cross-stack guidance |

## Deterministic Workflow

1. Lock the target domain, evaluation date, Capacitor version, and freshness threshold.
2. Retrieve the current authoritative source list from the registry above.
3. For each source: check version alignment, access the current docs, and record the last-verified date.
4. Flag sources as current (within threshold), stale (beyond threshold), or expired (missing or removed).
5. Scan the Capacitor GitHub releases and blog for breaking changes or deprecations since the last catalog entry.
6. Build or update the drift log with: deprecated API names, replacement patterns, and migration notes.
7. Map each source to the relevant downstream skill domain.
8. Publish the updated source catalog with all freshness, drift, and domain-mapping entries.

## Freshness Rules

- Sources accessed within the threshold are current; include them with no action.
- Sources beyond the threshold but accessible must be re-verified before use.
- Sources that return 404, redirect to a different version, or are no longer maintained must be marked expired and replaced with current equivalents.
- Drift identified in the changelog that is not yet reflected in any skill constitutes a skill-update obligation; record it explicitly.

## Quality Gates

- No guidance asset references a source marked stale or expired without an explicit owner-acknowledged exception.
- Every source in the catalog has an access date within the freshness threshold or an explicit exception.
- Drift log entries have one-to-one mapping to the downstream skill or instruction that needs updating.

## Done Criteria

- All target-domain sources are verified current or explicitly excepted.
- Drift log is complete and traceable to downstream update obligations.
- Source catalog is updated and reflects evaluation date.
- Every downstream skill depending on curated sources is listed with its update status.
