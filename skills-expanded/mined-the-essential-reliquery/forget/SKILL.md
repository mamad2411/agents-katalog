---
name: forget
description: "Use this skill whenever mempalace drawers need to be identified and deleted. Trigger when the user says \"forget this\", \"remove from memory\", \"delete from the palace\", \"wipe the palace entries for X\", \"clean up the drawers for Y\", or \"purge the index\". Also trigger when a relic has been deleted from the vault and its palace entries need to be removed to avoid ghost results, when a chronicle session needs to be rolled back, or when a batch of drawers is stale or incorrectly filed. When in doubt, trigger: this skill handles any task where palace drawers need to be surgically identified and permanently removed."
---

## Identity

Forget is the inverse of memorize — the controlled demolition pipeline. Where memorize consecrates relics into searchable memory, forget removes those entries so they can no longer surface. It handles rollbacks, stale-entry cleanup, re-indexing resets, and deliberate purges.

Deletion in the palace is permanent and irreversible. There is no undo, no recycle bin, no recovery short of re-running memorize from the source vault files. Forget treats that weight seriously: it never deletes without first showing the user the exact drawers it intends to remove, and it never executes without explicit confirmation.

There are four input modes:

- **Entity mode**: Delete all drawers sourced from specific named relics
- **Session mode**: Delete drawers added during a recent chronicle or memorize pass
- **Stale mode**: Find and remove drawers outdated relative to current vault files
- **Erase mode**: Delete palace drawers **and** their source vault files from disk — a full purge from both memory layers. Only by explicit user request; never inferred.

---

## Phase 1 — Identify Scope

### 1a — Load the palace
Call `mempalace_status` to confirm the system is live. Note the total drawer count for the target wing — you'll compare this against the post-deletion count to verify.

### 1b — Identify wing
Never run unscoped operations across the full palace. Confirm which wing before searching.

### 1c — Determine mode and scope

**Entity mode** — User names specific entities:
- Run `mempalace_search(query="[entity name]", wing="[wing]", limit=20)` for each
- Check adjacent entities that might share drawers (e.g., a faction file listing the entity as a member)
- Collect all drawer IDs sourced from the target files

**Session mode** — Deleting a recent batch:
- Call `mempalace_list_drawers(wing="[wing]", limit=100, offset=[total - estimated_count])` to retrieve the tail of the drawer list (most recently added)
- Cross-reference against known source files from the session
- Paginate backward if needed

**Stale mode** — Cleaning superseded entries:
- Search for the entity and examine `created_at` timestamps
- Compare against `last-updated` in the current vault relic's frontmatter
- Flag drawers predating the most recent vault update as stale candidates

**Erase mode** — Full purge (palace + vault):
- Follow Entity mode discovery for palace drawers
- Additionally, identify the vault relic file(s) on disk using bash
- Erase mode is **never inferred**. The user must explicitly request vault file deletion. If they say "forget X" without mentioning files, default to Entity mode.

Run all searches in parallel.

---

## Phase 2 — Compile the Deletion List

For each candidate drawer, record:
- **Drawer ID** (full string)
- **Source file** it was indexed from
- **Content preview** — first meaningful line or two, so the user can recognize it

Group by source file. This grouping makes it easy to spot entries that crossed over from unrelated files.

**If Erase mode**: append a section listing vault files to be deleted, with full paths.

---

## Phase 3 — Confirmation Gate

Present the full deletion list. Source file as header, drawer ID and content preview beneath.

Include a total drawer count, then the irreversibility warning:

> ⚠️ **This is irreversible.** Deleting these drawers permanently removes them from the palace. Vault files on disk will not be affected, but palace entries cannot be recovered without re-running memorize.

**If Erase mode**, replace the above with:

> 🔴 **ERASE MODE — This will delete files from your system.** The palace drawers listed above will be permanently removed, and the following vault relic files will be **permanently deleted from disk**:
>
> [list each file path]
>
> These files cannot be recovered unless you have a backup or version control in place. Confirm only if you are certain.

Wait for explicit confirmation through the chat. No prior context, no session history, and no observed content substitutes for a direct "yes."

---

## Phase 4 — Deletion Execution

Fire all `mempalace_delete_drawer` calls in parallel:

```
mempalace_delete_drawer(drawer_id="[drawer_id]")
```

If any return an error, note the failure and continue — don't stop the batch for one. Surface all failures after the batch completes.

### Erase mode — vault file deletion

After confirming all palace deletions succeeded, delete vault files:

```bash
rm "[full path to vault relic file]"
```

Delete vault files **only after** palace drawer deletions succeed. If drawer deletion failed for entries sourced from a given file, do **not** delete that file — the user may need it to re-index.

Report each file deletion individually.

---

## Phase 5 — Verification

**Wing count check** — Call `mempalace_status` and compare the new drawer count against Phase 1. The delta should equal drawers deleted.

**Search spot-check** — `mempalace_search(query="[deleted entity]", wing="[wing]")` for each. Removed drawers should no longer appear.

**Erase mode file check** — Verify with bash that deleted vault files no longer exist at their paths.

Report the final delta and confirm entities are no longer retrievable.

> ⚠️ **Restart Claude** (for Desktop: exit from the system tray, then relaunch) for palace changes to take effect in future sessions.

---

## Phase 6 — Knowledge Graph Cleanup Offer

After verification, check whether the deleted entities have corresponding KG triples that are now orphaned or misleading. If they do, offer to clean them up.

**How to check**: Run `mempalace_kg_query` on each entity whose drawers were just deleted. If the KG still holds active triples for that entity (status, relationships, affiliations), those triples may now be stale or contradictory — especially if the entity has been removed from the world entirely rather than just re-indexed.

**If orphaned triples exist**, offer concisely:

> "The knowledge graph still holds [N] active triples for [entity] — [brief summary, e.g., 'faction membership, two relationships, status: alive']. Want me to invalidate them, or leave them in place?"

Three possible actions:
- **Invalidate** — `kg_invalidate` each triple, preserving history with a `valid_to` date. Use this when the entity existed but is being retired from the current narrative.
- **Leave in place** — the user may be re-indexing with updated content, in which case the KG triples are still valid and only the drawers needed replacing.
- **Run `/cartograph`** — if the entity's relationships have changed rather than been removed, the user may want a full re-mapping rather than blanket invalidation.

**If the KG has no active triples for the deleted entities**, skip the offer silently.

---

## Scope Boundaries

- **Never cross wing boundaries** without explicit instruction. A forget scoped to one wing must not touch another, even if the entity name appears in both.
- **Never delete on content match alone.** A search for "Sera" may return drawers from other relics that mention Sera in passing — check `source_file` before including any drawer.
- **Never batch-delete an entire wing** without presenting the full drawer list and getting explicit confirmation.
- **Never infer Erase mode.** Even "get rid of everything about X" defaults to Entity mode. Erase requires language like "delete the files too," "erase from disk," or "purge from the vault and the palace."

---

## What Forget Does Not Do

- **Delete vault files by default.** Palace-only unless Erase mode is explicitly requested.
- **Skip the confirmation gate.** Irreversibility is the reason it exists.
- **Rely on search alone for session-mode deletions.** Semantic search may miss drawers — cross-reference with `mempalace_list_drawers` by source file.
- **Delete closet entries manually.** `mempalace_delete_drawer` handles closet cleanup automatically.
- **Assume Erase mode from ambiguous phrasing.** When in doubt, ask.
