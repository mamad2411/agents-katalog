---
name: link-hygiene
description: Find and fix broken wikilinks, orphaned notes, and missing backlinks across the vault. Use when the user asks to "clean up links", "find broken links", "fix dead references", or do periodic vault maintenance.
---

# link-hygiene

Periodic vault cleanup: broken links, orphans, and missed cross-references. Always preview before writing.

**Read `../reviewed-edit/references/vault-safety.md` before your first write.** It carries the shared rules: the three write modes, per-file delete confirmation, plan-before-applying, one unit at a time.

## When to use

- "Clean up my vault."
- "Find broken links."
- "What notes aren't connected to anything?"
- "Suggest links for my recent notes."

## Constraints

- Writes outside `$OAS_VAULT_WRITE_DIR` need the `reviewed` or `full` write mode. Under `scoped` they fail, so suggest changes instead of applying them.
- Print the full plan and get approval before the first write.
- Never mass-delete. Orphan status is a hint, not a verdict. Every delete needs explicit per-file confirmation.
- Show the user a summary (counts + sample) before applying any batch change.

## Tool chain

### Phase 1: Inventory (read-only)

1. **`vault_unresolved`**: list every broken wikilink and its source file.
2. **`vault_orphans`**: notes with no links in or out.
3. **`vault_recent`** with `limit: 20`: recently-modified notes are the likeliest candidates for missed links.

Summarise counts and show the user before acting.

### Phase 2: Fix broken links

For each unresolved link, decide:
- **Typo?** Use `vault_search_replace` on the source file with the corrected wikilink.
- **Missing note the user wants?** Create it via `vault_create` (inside `$OAS_VAULT_WRITE_DIR`) with a stub (`# Title\n\n(placeholder)`), then the wikilink resolves.
- **Stale reference?** Use `vault_search_replace` to remove the wikilink.

Never decide without asking: present the user with `{source, broken_link, proposed_action}` and wait for confirmation on ambiguous cases.

### Phase 3: Suggest new links

For each recent note (from step 3):
1. **`vault_suggest_links`** with `limit: 5`.
2. Filter suggestions: drop low-score hits; drop anything that would create a circular reference that isn't meaningful.
3. Present the list; on approval, insert `[[target]]` wikilinks via `vault_search_replace` (find the anchor phrase, add the link) or `vault_patch` (insert after a specific heading).

### Phase 4: Surface orphans (no action)

List orphans grouped by folder. Ask the user whether any should be linked from an index note, archived, or deleted. Never delete without explicit per-file confirmation, even after the user approves the batch (`../reviewed-edit/references/vault-safety.md` has the batching rules).

## Example output to user

```
Link hygiene report for the vault:
- 12 broken wikilinks across 7 files
- 23 orphan notes
- 4 recent notes have 2+ high-confidence link suggestions

Proceeding with broken links first. Fix plan for notes/foo.md:
  [[consensus-algo]] → typo? did you mean [[consensus-algorithm]]? (file exists)

Apply this fix? (y/n)
```
