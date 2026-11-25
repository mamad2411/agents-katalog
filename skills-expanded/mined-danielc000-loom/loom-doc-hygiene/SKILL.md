---
name: loom-doc-hygiene
description: Apply whenever writing or editing documentation, notes, or knowledge files (vault notes, READMEs, design/architecture docs, changelogs). Enforces rewrite-in-place over append, no contradictions, bounded docs, and no hard-wrapped prose. Shipped and kept current by Loom.
---

# doc-hygiene

Rules to apply on **every** documentation edit. Docs are a living source of truth, not an append-only log. A reader should be able to trust that what a doc says now is what is true now.

## Rules

1. **No contradictions.** A document must not assert two things that cannot both be true. Before adding a statement, scan the surrounding doc for anything it conflicts with and reconcile them in the same edit.

2. **Rewrite in place — never append "UPDATE:" notes.** When information becomes outdated, debunked, or false, **edit the original sentence/section to be correct**. Do not leave the stale text and bolt on "UPDATE:", "EDIT:", "Note (2026):", "~~struck-through~~ now actually…", or a trailing correction. Replace the wrong content with the right content as if it had always been right. (Git history preserves what changed — the doc itself should read clean.)
   **Exception — immutable decision records (`docs/adr/**`):** an Architecture Decision Record's entire value is the decision history, so this rule inverts for it. Never rewrite an existing ADR's decision to reflect new information. If a decision changes, **amend** the ADR by adding new information (e.g. a status update) or **supersede** it by writing a new ADR that records the new decision and marks the old one superseded. This exception is deliberately narrow: it applies only to files under `docs/adr/**`. A mutable decision register elsewhere (e.g. `docs/decisions/`) and every other design/architecture doc still follow this rule as written — rewrite them in place.

3. **Tidy loose ends.** Resolve dangling references, half-finished sentences, TODOs that are now done, and links to things that moved or were deleted. If a section is now empty or redundant, remove it.

4. **Keep docs bounded.** Don't let a doc grow without limit. Prefer revising existing sections to adding new ones. Consolidate duplicated explanations into one canonical place and link to it. Length should track the size of the subject, not the number of times it was touched.

5. **Shallow, stable structure for a notes collection.** In a multi-note vault/docs tree, keep a **one-level** folder taxonomy — don't pile notes flat, and don't nest deeply. **Fixed-path / canonical docs** (ones referenced by exact path — a resume log, a note a `CLAUDE.md` pins by path) stay at the collection root; every other note lives in a taxonomy folder. Maintain an **`_Index.md`** map-of-content at the root: read it to locate a note instead of Globbing, and update it when you add or move one.

6. **One line per paragraph — never hard-wrap prose.** Write each paragraph, list item, or table row as a single physical line and let the editor soft-wrap it. Do **not** insert manual line-breaks to hold prose to a column width (~80/100 chars). Hard-wrapping fights the one-line-per-block model editors like Obsidian assume, produces noisy reflow diffs when a sentence is later edited, and re-wraps unpredictably across viewers. Deliberate markdown breaks are still fine — a blank line between blocks, or a trailing `\` / two trailing spaces for an intentional hard break — but column-width wrapping is not.

## How to apply

- **Editing an existing doc:** read the whole relevant section first, fold new information into it, and delete what the new information supersedes. The diff should show the doc moving from one correct state to another — not accreting.
- **Editing an ADR (`docs/adr/**`):** never edit the recorded decision in place. Add an amendment, or write a new ADR that supersedes it and update the old record's status to point at the new one.
- **Line breaks:** one physical line per paragraph or bullet; never wrap prose to a fixed column. Break lines only at real block boundaries (a blank line, a new heading, a new list item).
- **Status/decision claims:** only state something is "done", "fixed", "verified", or "decided" if it is actually true right now; if you're changing a prior claim, overwrite it, don't annotate it.
- **When unsure whether old content is still true:** verify before deleting; if it contradicts current reality, surface that rather than silently keeping both versions.
- **Writing a decision record (extracted from a code comment, `docs/adr/**`/`docs/decisions/**`):** the `/worker` and `/orchestrate` doctrine own when a comment counts as one and the `@decision <id>` anchor grammar — this skill governs the record FILE once you're writing it: one file per id always (a second decision under the same id is a new section, never a second file), `docs/adr/**` stays immutable (rule 2's exception above), `docs/decisions/**` is ordinary mutable doc hygiene.
