---
name: sync-businessflow-feature
description: Keeps the canonical Synamcps business repository and landing aligned with user-visible product features. Use when adding, changing, releasing, previewing, or deprecating a feature, API capability, MCP tool, integration, security control, or user workflow.
---

# Sync product work to businessflow

The canonical workflow is `../businessflow/.cursor/skills/sync-synamcps-feature/SKILL.md`, resolved from the parent `Projects` directory.

After implementing and verifying a user-visible product change:

1. Read and apply the canonical skill.
2. Use this product repository’s code, tests, API schema, and docs as primary technical evidence.
3. Create or update the feature record in `../businessflow/features/`.
4. Update affected business artifacts there and the landing implementation in `../synamcps-landing`.
5. Run the canonical validation steps and report all artifact dispositions.

If `businessflow` or `synamcps-landing` is unavailable, do not invent a substitute path. Report the unresolved synchronization as incomplete.

Internal refactors, tests, and fixes with no user-visible or commercial impact may be marked `not-applicable`; explain the reason in the implementation summary.
