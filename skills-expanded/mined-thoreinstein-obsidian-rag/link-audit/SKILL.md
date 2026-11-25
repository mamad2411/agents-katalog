---
name: link-audit
description: >-
  Use when the user wants to audit vault link health, find broken wikilinks,
  orphaned notes, or semantic clusters. Triggers on "link audit", "broken links",
  "orphaned notes", "link health", "graph cleanup", or "find orphans".
---

# Vault Link Audit

Comprehensive audit of link health: broken wikilinks, orphaned notes, and semantic suggestions.

## Phase 1 — Broken Links

1. Call `obsidian_get_broken_links` (optionally with `subfolder` argument).
2. Present broken links grouped by originating file.
3. For each, suggest: delete the link, create a stub note, or correct the target name.
4. Offer to fix each with `obsidian_replace_in_note` (wrong name → correct name).

## Phase 2 — Orphaned Notes

1. Call `obsidian_list_notes` to enumerate all notes in scope.
2. For each candidate orphan, call `obsidian_get_backlinks`.
3. Notes with zero backlinks AND not in `Daily Notes/` are orphan candidates.
4. Present orphan list with options: link from a relevant note, move to archive, or delete.

## Phase 3 — Semantic Suggestions (Optional)

If the user asks for deeper suggestions:

1. For each orphan, call `obsidian_rag_query` with the orphan title as query, `limit: 5`.
2. If strong matches exist (low distance score), suggest `[[wikilink]]` connections.

## Arguments

Optional subfolder: `/link-audit Engineering/`

## Tips

- For large vaults, always scope to a subfolder first (Phase 2 on full vault is slow)
- Broken links in `Daily Notes/` are usually harmless — offer to skip them
- Never make edits without per-change user confirmation
- Run `/index` first if `obsidian_get_broken_links` seems incomplete
