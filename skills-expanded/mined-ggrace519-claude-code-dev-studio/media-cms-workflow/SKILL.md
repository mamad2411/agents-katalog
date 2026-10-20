---
name: media-cms-workflow
description: CMS / editorial workflow specialist. Owns asset ingest, metadata model, rights windows, scheduling / publishing, and editorial review. Auto-invoked for CMS schema, workflow, rights, or scheduling work.
---

# Media CMS Workflow

If editors can't ship on schedule, nothing else matters — and a title served outside
its rights window is legal exposure, not a bug ticket. Metadata, rights, and
publishing workflows are the editorial productivity *and* compliance layer.

## When to reach for this

- Designing the asset ingest workflow, status machine, or auto-QC gates
- Modeling metadata (titles / seasons / episodes / cast) or rights windows (territory, language, license period, exclusivity)
- Implementing scheduled publish / unpublish, embargoes, or editorial review and approval
- Building asset search, filtering, or bulk-edit tooling for editors

## Principles

1. **Rights are first-class data, enforced at playback auth.** Territory, language,
   window start/end, and exclusivity live in the schema and gate the entitlement
   check — the CMS UI surfacing them is necessary but never sufficient.
2. **Workflow is an explicit state machine.** Named states, allowed transitions,
   guards — not a pile of boolean flags (`is_published`, `is_qc_passed`) that drift
   into impossible combinations.
3. **Bulk operations everywhere.** Editors never hand-click 500 titles. Every list
   view needs multi-select edit, schedule, and rights-assignment.
4. **Audit log on every editorial action.** Who changed what, when, and the prior
   value — rights disputes and publish incidents are settled from this log.
5. **Unpublish must be at least as reliable as publish.** A failed publish is a
   missed slot; a failed unpublish at rights expiry is a license breach. Expiry jobs
   alert on failure and a serving-side window check backstops them.
6. **Store schedule times in UTC, display in the editor's locale.** Embargo bugs are
   almost always timezone bugs.

## Asset state machine (starting point)

| State | Enters via | Guard to leave |
|---|---|---|
| `ingesting` | upload / feed delivery | media + required metadata present |
| `qc` | ingest complete | auto-QC pass (black frames, silence, sync) + manual approval if flagged |
| `ready` | QC pass | rights window assigned, artwork present |
| `scheduled` | editor sets publish time | publish time reached **and** rights window open |
| `live` | scheduler fires | — |
| `expired` | rights window end / manual unpublish | re-license → back to `ready` |

Transitions are append-only events (actor, timestamp, from → to), which gives the
audit log for free. Rejections route back to `ingesting` or `qc` with a reason code.

## Pitfalls

- Rights checked in the CMS but not at the playback-auth / manifest layer — expired titles still stream
- Unpublish implemented as soft-delete while CDN-cached manifests keep serving; purge or short-TTL the manifest
- Free-text fields where controlled vocabularies belong (genres, territories, languages) — breaks filtering and rights queries
- Episode/season hierarchy modeled as string prefixes instead of real relations
- Scheduler that silently skips a missed tick after downtime — catch-up logic and alerting are part of the design
- QC gates that block on manual review for every asset — auto-pass the clean ones, queue only flagged

---
*Related: `media-transcode` (ingest QC signals), `media-drm-cdn` (rights enforcement
at delivery), `media-live` (live event scheduling) · domain agent: `media-architect` ·
output/ADR format: `playbook-conventions`*
