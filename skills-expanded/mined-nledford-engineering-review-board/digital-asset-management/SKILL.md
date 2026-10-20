---
name: digital-asset-management
description: Digital asset management (DAM) engineering guidance for photo and video ingest, asset identity, immutable originals, derivatives, metadata, non-destructive edits, organization, smart collections, hierarchies, viewing, sharing, and validation. Use when building, changing, reviewing, or testing a photo/video catalog, media library, asset browser, editing workflow, or related API and data model. Do not use for standalone codec implementation, generic SQL/API/CSS work, or non-media document management without a DAM lifecycle.
---

# Digital Asset Management

Use this skill for the media-specific lifecycle and vocabulary that connect a
photo/video catalog, its viewers, its editing workflow, and its storage. Inspect
the product's supported formats, storage model, existing media libraries, and
privacy policy before choosing representations or changing behavior.

## Scope And Vocabulary

- **Asset:** the logical, user-visible media item. Do not equate it with a path,
  filename, byte sequence, or rendered file.
- **Media file:** stored bytes associated with an asset, with a role such as
  original, imported copy, sidecar, derivative, proxy, preview, or export.
- **Original:** immutable source bytes and their import provenance. Preserve them
  unless the product explicitly defines replacement semantics.
- **Rendition:** generated output for a defined purpose, such as a thumbnail,
  preview, video proxy, or export.
- **Edit recipe:** versioned, ordered operation parameters that can reproduce a
  rendition from a source. It is not the same as an undo history or an asset
  version.
- **Asset version:** a user-visible revision or branch that can be restored. Keep
  it distinct from metadata revisions, edit-recipe revisions, and renderer
  versions.
- **Folder:** a physical/import location or hierarchy. **Manual collection:** a
  user-managed membership list. **Smart collection:** a saved, validated query.
  **Tag/keyword:** a reusable classification. Do not collapse these concepts.

## Workflow

1. Identify supported image/video formats, storage topology, media-processing
   libraries, source-of-truth locations, and background-worker boundaries.
2. State lifecycle rules before editing: ingest, duplicate detection, metadata
   extraction/write-back, editing, rendition generation, sharing, deletion,
   retention, and restore.
3. Define domain nouns and invariants before choosing tables, endpoints, or UI
   controls. Model an original, an edit recipe, a rendition, and a user-visible
   version independently when the product needs each one.
4. Define authority and conflict behavior for embedded metadata, sidecars,
   catalog edits, external file changes, concurrent edits, and ACL changes.
5. Define viewer and organization behavior for loading, unsupported media,
   orientation, color, keyboard interaction, hierarchy moves, and selection.
6. Route implementation mechanics to the owning skills, then add focused tests
   for the invariants and user-visible workflow that changed.

## Ingest And Identity

- Preserve immutable original bytes, source location/provenance, extraction
  result, and import failure separately from generated output.
- Treat byte hash, perceptual similarity, filename, and logical asset identity as
  different facts. Define duplicate, re-import, moved-file, and replacement
  behavior explicitly and make ingestion idempotent where retries are possible.
- Treat uploaded/imported media as untrusted input. Determine format from byte
  signatures and parser-confirmed structure against an allowlist; do not trust
  extensions or caller-supplied MIME types, and reject material mismatches.
- Bound compressed and expanded bytes, dimensions/pixels, duration, streams,
  frame count, metadata depth/count/value size, CPU/wall time, memory, temporary
  and output storage, and queueing per item and per tenant or workload boundary.
- Process risky formats and codecs with least privilege and operating-system,
  container, or VM isolation proportionate to the threat model. Do not expose
  ambient credentials or unnecessary filesystem/network access. Invoke reviewed
  external tools with structured argument APIs, never through a shell command
  assembled from media paths or metadata.
- Model asynchronous extraction/rendition work with observable states,
  cancellation, retry, and terminal failure behavior.

## Metadata And Interpretation

- Preserve raw embedded and sidecar metadata where interoperability requires it;
  extract normalized values for search/display without losing provenance.
- Define field-level precedence and conflict handling among EXIF, IPTC, XMP, ICC,
  sidecars, catalog edits, and later external changes. Do not overwrite a whole
  metadata block merely to change one field.
- Apply orientation consistently to previews, viewer dimensions, crop coordinates,
  exports, and API values. Distinguish stored from display dimensions.
- Make timestamp timezone assumptions, repeatable values, legacy encodings, GPS
  precision, and missing values explicit.
- For video, distinguish the container from video, audio, subtitle, and data
  streams. Record timebase, display rotation, duration, codecs, HDR/color data,
  and keyframe limits only when the product needs them.

Read [metadata and interoperability](references/metadata-and-interoperability.md)
when this boundary is material.

## Non-Destructive Editing And Renditions

- Store validated operation parameters and their order as an edit recipe; retain
  original bytes. A preview, proxy, or export is generated output, not authority
  for future edits.
- Define a canonical coordinate space for crop/geometry after orientation policy.
  State units, ranges, defaults, and rounding.
- For automatic operations, persist resolved parameters and algorithm/model
  version. An unversioned `auto` flag cannot reproduce a result.
- Include source identity, recipe revision, presentation-affecting metadata,
  color/output profile, and renderer/codec version in rendition-cache decisions.
  Invalidate atomically and do not serve stale or unauthorized output.
- Define whether undo/redo, restoring an asset version, and branching edits move
  pointers or create new immutable revisions.

Read [editing and rendering](references/editing-and-rendering.md) for operation,
cache, export, and video-specific details.

## Organization, Hierarchies, And Viewing

- Give manual collections, folders, tags, and smart collections separate
  semantics. Specify ordering, membership, root, delete, and authorization rules.
- Give smart collections a versioned, validated query language. Define supported
  fields/operators, null versus absent data, timezone/collation/full-text rules,
  live versus snapshot membership, deterministic sorting, and schema evolution.
- Prevent hierarchy cycles, including concurrent self/descendant moves. Define
  sibling names, reparenting, subtree deletion, and parent authorization.
- Use thumbnails/proxies appropriate to the view; do not decode originals for
  catalog browsing by default. Define progressive loading, cancellation, error,
  unsupported-media, and stale-preview states.
- Verify orientation and color correctness, virtualized grid/filmstrip behavior,
  zoom/pan, accessible selection, keyboard tree navigation, and video playback
  controls/captions where applicable.

Read [catalog, persistence, and organization](references/catalog-and-persistence.md)
and [viewer, organization, and testing](references/viewer-organization-and-testing.md)
when designing these areas.

## Sharing And Read Paths

- Enforce tenant and object authorization on originals, metadata, renditions,
  exports, search/index results, background jobs, and cache hits. Client-visible
  identifiers, collection membership, or possession of an old URL are not
  authorization.
- Treat signed/share URLs as bearer capabilities. Bind them to the tenant,
  asset/version/rendition, purpose, method, and a short lifetime; define
  revocation and do not put capability values in logs, analytics, referrers, or
  durable client-visible locations beyond the intended handoff.
- Propagate ACL, privacy, version, and deletion transitions to every normal read
  path and generated representation. Expire capabilities and purge or deny stale
  caches/exports; keep retained backups inaccessible to normal reads and remove
  them under the documented retention schedule.
- Serve only allowlisted response media types. Set `X-Content-Type-Options:
  nosniff`, an appropriate `Content-Disposition`, and cache directives matching
  sensitivity and revocation needs; do not render attacker-controlled active
  content inline merely because it was uploaded as media.
- Test access before and after tenant, ACL, privacy, version, share, and deletion
  transitions, including direct IDs, old capabilities, caches, indexes, workers,
  thumbnails, previews, proxies, and exports.

## Skill Routing

- Use [`domain-driven-design`](../domain-driven-design/SKILL.md) for bounded
  contexts/invariants and [`domain-modeling`](../domain-modeling/SKILL.md) for an
  implemented model review.
- Use [`sql-engineering`](../sql-engineering/SKILL.md), then
  [`postgresql-sql-engineering`](../postgresql-sql-engineering/SKILL.md),
  [`mysql-mariadb-sql-engineering`](../mysql-mariadb-sql-engineering/SKILL.md),
  or [`sqlite-sql-engineering`](../sqlite-sql-engineering/SKILL.md), for
  schema, migration, query, and transaction mechanics.
- Use [`api-design`](../api-design/SKILL.md) for ingest, metadata, edit,
  collection, rendition, pagination, and concurrency contracts.
- Use [`css-scss-styling`](../css-scss-styling/SKILL.md) for viewer styling,
  [`ux-accessibility-review`](../ux-accessibility-review/SKILL.md) for rendered
  viewer/tree review, and [`playwright-e2e`](../playwright-e2e/SKILL.md) for
  browser-visible workflows.
- Use [`performance-review`](../performance-review/SKILL.md) for catalog-scale
  browsing, rendering, caching, and background-workload evidence.
- Use [`security-review`](../security-review/SKILL.md) and
  [`threat-modeling`](../threat-modeling/SKILL.md) for parsing, uploads, sharing,
  metadata exposure, derivatives, URLs, caches, and retention. GPS, face/person
  tags, camera identifiers, timestamps, captions, and audio may be sensitive.
- Use [`test-driven-development`](../test-driven-development/SKILL.md) and
  [`testing-strategy`](../testing-strategy/SKILL.md) for test design and levels.
- Use [`photo-supreme-scripting`](../photo-supreme-scripting/SKILL.md) for Photo
  Supreme's embedded Object Pascal scripting environment and its catalog API.

## Completion Checklist

- Original, asset, rendition, recipe, and asset-version semantics are distinct.
- Ingest, duplicate, metadata-conflict, deletion, and restore behavior is stated.
- Hierarchy cycles and smart-collection query semantics are prevented or defined.
- Previews, proxies, originals, and exports apply current authorization and
  privacy rules independently.
- Tests cover orientation, metadata precedence, hierarchy invariants, idempotent
  ingest, edit/version distinction, and rendition invalidation where relevant.
- Performance evidence uses representative catalog sizes, media fixtures, and
  bounded decode/render workloads.

## Non-Goals

Do not prescribe a codec, image-processing library, cloud provider, ORM, schema,
or UI framework. Do not use this skill as a replacement for generic SQL, API,
language, security, or styling guidance, and do not apply it to ordinary document
management without photo/video asset lifecycle requirements.
