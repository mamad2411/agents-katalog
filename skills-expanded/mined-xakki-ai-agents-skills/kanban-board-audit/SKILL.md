---
name: kanban-board-audit
description: 'Audit Kanban cards for duplicate, completed, blocked and epic-ready work, and repair or reorganize a board while preserving scope and stages. Use before prioritizing, grouping into epics or fixing board relationships. RU: аудит доски, дубли карточек.'
license: MIT
disable-model-invocation: true
---

# Kanban board audit and maintenance

Use before prioritizing cards, grouping them into epics, or reorganizing and repairing board relationships.

## Board audit

Use before prioritizing cards or grouping them into epics. Inspect the authoritative board through the project or runtime interface and retain its scope, lifecycle, and authorization boundaries.

1. Capture the initial board state, allocation mechanism, relevant stages, existing epics, and repository status when applicable.
2. Read each source card's title, criticality, tags, scope, acceptance criteria, decisions, dependencies, and status. Search the relevant active and historical stages by ID, title, and subject before declaring a card unique or incomplete.
3. Classify each card as unfinished implementation, historical/discovery record, blocked or controlled operation, or duplicate. Cite the completed work or decision supporting each exclusion. A card's stage alone does not establish whether its work remains.
4. Group implementation cards by actual execution boundary and dependency order, honoring any priority explicitly set by the user. Keep historical ledgers as context and isolate controlled live-data or destructive actions with their required authorization and evidence; do not silently add those actions to an epic. Similarly named credentials or identities are not interchangeable without evidence of the same authority. Do not promote a grooming card while its open questions remain unresolved.
5. When creation is requested and authorized, use the project's allocator and record concrete child IDs, ordering, integration criteria, and decisions. Resolve draft mistakes only within the owner's authorized scope and reconcile any counter against the authoritative board; do not assume rollback is safe.
6. Check the exact changed cards with the project linter when available. Separate targeted results from whole-board results, report unavailable or failing checks honestly, and check the intended Git diff when applicable.

Report the proposed or created epics, excluded records and their supporting evidence, controlled operations, and outstanding decisions. Do not commit without an explicit user request.

## Board maintenance

Use for reorganizing an existing board, creating missing organizational parents, or repairing card relationships. Do not implement work merely because a card describes it.

1. Resolve the authoritative board and its supported operations through the project or runtime. Inventory relevant stages, existing parents, links, dependencies, and pending work; preserve unrelated uncommitted edits when the board is repository-backed.
2. Keep children in their actual stages and completed work as historical references. An organizational parent does not itself advance, reopen, or complete a child. Do not edit a child merely to restate a relationship, or create multiple parents for the same child.
3. When authorized to create parent epics, use the board's actual template and include purpose, ordered child IDs and paths, current stages, blockers, non-goals, and integration criteria. An existing parent is not a reason to omit other requested parent cards. Mark overlapping implementation as a decision to resolve rather than silently duplicating it.
4. Archive a superseded executable card only when the owner explicitly authorizes that disposition. Record its replacement and unique acceptance evidence in both records, update affected parent references, and use the supported archive operation. Preserve historical context; label resolved or deferred questions so they are not mistaken for active gates. Archival is not completion.
5. Validate the exact changed cards and the board using its available linter. Distinguish newly introduced failures, unrelated pre-existing failures, excluded stages, and unrun checks. Verify the requested number and names of cards and required sections. If an explicitly requested naming convention causes a warning, report the warning rather than silently changing the allocation state. For repository-backed boards, verify whitespace for both tracked and new files, and confirm only authorized cards and paths changed. Do not stage unless authorized or commit without an explicit user request.

Report the created or modified records, verified checks, existing blockers, and unresolved decisions. Never alter a completed card or product code unless the task explicitly includes that action.
