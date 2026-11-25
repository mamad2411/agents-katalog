---
name: music-library-safety
description: Guard consequential personal music-library work with explicit ownership, preview, recovery, and approval checks. Use before scanning, tagging, moving, deduplicating, importing, deleting, or synchronizing music files, metadata, playlists, samples, stems, or mixlists.
---

# Music Library Safety

Use this skill before any operation that can change personal music files, metadata, collections, or service-visible media.

## Purpose

Preserve the distinction between the server listening library and the workstation production hierarchy. Require a known owner, preview, recovery path, and exact approval before consequential writes. This skill is a safety gate; route actual beets, tag, import, or player operations to their specialized companion skill.

## Boundary Check

1. Identify the target path, data type, canonical owner, and intended outcome.
2. Classify the target as one of: server listening library, workstation samples/stems/projects/mixlists, approved disposable fixture, metadata index, or unknown.
3. Stop if the target is unknown, crosses the server/workstation boundary, contains personal production material, or would distribute copyrighted media.
4. Treat production media, personal samples, stems, projects, mixlists, and original downloads as irreplaceable unless an approved recovery source is demonstrated.

## Safe Workflow

1. **Inspect first.** Collect a read-only inventory, identify duplicates or malformed metadata, and record what would change.
2. **Confirm recovery.** Verify the relevant backup, fixture, or original source before a move, overwrite, deduplication, or bulk metadata change.
3. **Preview.** Produce a dry run, manifest, or explicit before/after list. Never infer that a preview implies permission to execute.
4. **Request exact approval.** Name the target paths, operation, maximum scope, handling of conflicts, and rollback method for consequential writes.
5. **Execute only the approved subset.** Preserve originals until validation succeeds; do not expand a batch because similar files appear nearby.
6. **Validate and record.** Check expected files, metadata, and service-visible results. Record counts and decisions without storing private paths, raw media listings, credentials, or copyrighted media.

## Hard Stops

Stop and request clarification when an operation would delete or overwrite files, move data across the server/workstation boundary, modify a live listening library without demonstrated recovery, change a playlist or mixlist with no reversible export, or touch an unapproved network share or mount.

## Representative Scenario

**Request:** “Remove duplicate tracks from the library.”

**Route:** Produce a read-only duplicate report; identify the canonical location and recovery source; present the exact candidate set and keep rule; obtain approval; then remove only the approved copies. Do not delete files merely because hashes or tags look similar.

## Companion Skills

- Use `music-library-organizer` for approved ingest, tagging, and organization.
- Use `dj-library-curator` for curation decisions after the safety gate.
- Use `homelab-change-control` when an operation touches a server mount, service, or storage boundary.
- Use the approved music ownership and recovery contracts when available; treat absent contracts as a blocker rather than an invitation to infer policy.
