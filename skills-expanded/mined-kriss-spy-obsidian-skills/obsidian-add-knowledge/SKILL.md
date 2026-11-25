---
name: obsidian-add-knowledge
description: "Add knowledge to an Obsidian vault: reconcile duplicates, capture a source, or save supplied text, a URL, or a topic into the owning note."
---

# Obsidian Add Knowledge

**Reconcile before writing.** Identify each subject and its intended sense, read supplied sources, and search names, aliases, and contents for the owning note. Extend that note rather than creating a near-duplicate; a passing mention in an index or application note does not establish ownership.

## Outcomes

- **Update** — an existing note owns the concept; add only the missing knowledge.
- **Create** — an independently useful concept has no owning note.
- **Already covered** — the owning note contains the requested knowledge.
- **Ask** — the subject or scope remains too ambiguous to choose safely; explain the ambiguity in message text and request the missing distinction.

For **Already covered**, report the owning note and stop without an edit.

## Two modes

**Small capture:** append to an obvious existing owner. Read that note, check the incoming facts against it, and propose the addition in one turn. Skip folder comparisons and peer sampling; after confirmation, write the approved addition. Switch to Placement if ownership is uncertain.

**Placement:** create a note/category or resolve competing owners. Inspect the strongest matching notes, compare competing neighborhoods and their contents, and verify the actual parent path. Load the placement reference below. A new category needs concrete sibling candidates. A user-specified target needs a preview, but only needs competing-location research if it conflicts with the vault.

## Proposal shape

In normal message text, give each exact vault-relative target path, **Update** or **Create**, a compact outline or patch preview, why it owns the concept over the closest alternative (if any), source URLs, and useful WikiLinks resolved against the real tree. Keep the note proportional to the payload. Put paths, URLs, evidence, and previews in message text, never in the `question` tool.

## Hard gate

**Stop after the proposal until the user confirms the exact target and substance.** A named target alone is not approval of unseen content. After confirmation, apply only the approved change, preserve surrounding content, and read back the saved note against the preview. If the user changes subject, target, or scope, revisit the affected evidence and proposal.

## Load only what this capture needs

- When choosing a folder or comparing neighborhoods, read [references/placement.md](references/placement.md).
- When creating a note or local metadata/headings are unclear, read [references/note-shape.md](references/note-shape.md); sample peers only for a missing or contradicted convention.
- After writing, run `node scripts/check-note.mjs <path>…` from this skill directory with every target in the run, using absolute note paths or `OBSIDIAN_VAULT_PATH` plus vault-relative paths. Report its output verbatim and the created/updated paths. A failure remains a failure; distinguish pre-existing defects from the approved edit before fixing anything outside its scope. The checker validates file targets, not heading/block existence or semantic duplication.

The checker requires Node 20+ and the pinned `yaml` dependency. If missing, run `npm ci --prefix <skill-directory>` once; scripts and references are relative to this skill, not the vault's working directory.

## Tool order

Use the vault's Obsidian CLI first for reads, searches, and edits. Use MCP only for gaps such as Dataview, UI automation, or bulk operations the CLI cannot handle. In cloudnotes, the Obsidian MCP server is disabled in `opencode.json` (verified October 2026); check current availability rather than changing configuration. If the CLI is unavailable, report that limitation and use permitted filesystem operations for the same approved scope.
