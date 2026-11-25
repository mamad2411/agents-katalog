---
tags: [backend, yorkie, crdt, sync, pattern]
name: yorkie-crdt-sync-pattern
description: Apply a single doc.update callback for local mutations and pullRemoteChangesIntoLocal(WithNodeIds) for remote→local sync in Yorkie-backed apps
source_project: lucida-builder-r3
version: 1.0.0
category: backend
---

# Yorkie CRDT sync pattern

## Trigger
- Editing canvas/document state in a Yorkie-backed React app.
- Reviewing code that mutates a Yorkie document via side-channel helpers.

## Steps
1. Apply local changes inside a single `doc.update(root => { ... })` call. Never build a parallel "push" pipeline — removing such pipelines was validated in this project (see `content.md`).
2. For remote→local sync, call `pullRemoteChangesIntoLocal()` for full syncs, or `pullRemoteChangesIntoLocalWithNodeIds(nodeIds)` when only specific nodes need to refresh.
3. Keep metadata (lists, menus, finders) on the team server. Keep live document state in Yorkie. Do not mix.
4. When deleting a legacy push helper, update every caller to call the underlying handler directly (the project's `#41` refactor did exactly this).

## See also
- See `content.md` for the concrete call shapes and anti-patterns.
