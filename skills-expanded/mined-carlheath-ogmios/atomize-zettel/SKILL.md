---
name: atomize-zettel
description: |
  After finished text work, identify concepts, people, places, and ideas
  worth atomic notes (Cards), link in existing cards, and suggest updates
  to cards where the new material casts new light on already-established ideas.

  [WHAT] Scan recently produced/edited text against `Cards/_index.md`. Return
  three lists: NEW CANDIDATES (concepts worth their own card), EXISTING TO LINK
  IN (cards that exist but aren't linked), EXISTING TO UPDATE (cards where the
  text adds something substantive). The user chooses per row. Closes "the loop"
  between writing and the knowledge graph.

  [WHEN] Use when: atomize, "suggest atomic notes", "link in cards", "update
  cards", after a finished chronicle/memo/report, after the ALGORITHM VERIFY
  phase on text-producing work. Use PROACTIVELY as a silent last step in the
  Algorithm's VERIFY phase when produced text is >800 words.

  [LANGUAGE] Configurable. Output: short, scannable list. No AI filler patterns.

  [EXPERTISE] Atomic notes, Zettelkasten weave, concept extraction, Cards
  index lookup, wiki-update convention.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# Atomize Zettel

**Role:** atomic-note curator. Helps the user identify what deserves a card, what should be linked in, and what needs updating after a piece of text work is done.

**Design principle:** don't automate creation. Automate the *question*. The user sees all suggestions and chooses. Silent when nothing is worth asking about.

## Live context

Configure per project. Common pattern:

- Cards folder: `{{VAULT_PATH}}/Cards/`
- Index: `{{VAULT_PATH}}/Cards/_index.md`
- Card template: `{{VAULT_PATH}}/Templates/Concept.md`

## Value threshold

The skill is invoked whenever conditions match (manually or from ALGORITHM VERIFY). **But only asks the user if there is substance.** If the candidate list is empty after filtering, return silently with `Atomize: no suggestions.` and finish. No false alarms.

A candidate passes the threshold if at least one applies:
- The concept appears 3+ times or is central to the text's argumentation
- It is a named entity (person, organisation, place, legislation, doctrine) not trivially recurring
- It is a technical term the user has defined or adopted
- It is a quote or reference to a thinker the user returns to

Filter out: common words, transition phrases, generic adjectives, items already in the Links field.

## Workflow

### 1. Identify target artefact
- Default: most recently edited file in writing folders (mtime, .md, >800 words)
- Or: explicit file specified by the user

### 2. Read the index
Read `Cards/_index.md`. Build a lookup: title + aliases → card.

### 3. Extract candidates
From the target artefact:
- Proper nouns (capital start, not sentence beginning)
- Recurring noun phrases (3+ occurrences)
- Terms in italics or quotation marks
- Wikilinks `[[X]]` that don't exist in Cards/

### 4. Classify

| Bucket | Rule |
|--------|------|
| **NEW CANDIDATES** | Term passes the value threshold, no match in index |
| **LINK IN** | Term passes the threshold, exact or alias match in the index, but no `[[X]]` in the text |
| **UPDATE** | The text contains substantive new material on a term that already has a card (new argument, new source, new observation) |

### 5. Present

Format:

```
Atomize — suggestions for "{filename}"

NEW CANDIDATES (N)
  • {term} — {one-line motivation: "central in §3, 4 occurrences"}
  • ...

LINK IN (N)
  • [[{card}]] — implicit in §X, not linked
  • ...

UPDATE (N)
  • [[{card}]] — {what the text adds, max 12 words}
  • ...

Walk through? (y/n/specific row)
```

If all three lists are empty: write `Atomize: no suggestions for "{filename}".` and finish.

### 6. Per user choice

**NEW CANDIDATE approved:**
- Create `Cards/{Term}.md` via the Concept template
- Pre-fill YAML, leave body for the user
- Update `Cards/_index.md` with a new row
- Backlink from the target artefact: add `[[Term]]` to `Links:` if the user wants

**LINK IN approved:**
- Edit target artefact: replace first bare occurrence with `[[Term]]` OR add `[[Term]]` to the `Links:` frontmatter (user chooses)

**UPDATE approved:**
- Show suggested addition as a diff
- User edits/approves
- Edit the card per the wiki-update convention below

## Card template (for new cards)

Use the user's concept template. Default:

```yaml
---
MOC: "[[Concepts MOC]]"
Created: {YYYY-MM-DD}
Modified: {YYYY-MM-DD}
Links:
  - "[[{target artefact}]]"
tags:
  - status-new
Type:
---

# [[{Term}]]

{Empty — user writes the substance}

## Sources
{If relevant: reference to the target artefact}

## Reflections

```

For people: change MOC to `People`, place in `Atlas/People/` instead of Cards/.
For places: separate MOC. For organisations: People MOC or own MOC per vault convention.

## Wiki-update convention

When an existing card is updated with new material from a text, **edit the card's body directly** but leave a clear revision trail at the end of the file.

Add (or update) a `## Revisions` section at the bottom:

```markdown
## Revisions

### 2026-05-02
Addition about [topic] based on [[target artefact]]. Paragraph 2 reformulated with [author]'s distinction between A and B.
```

Rules:
- Date as H3, chronological newest first
- 1-3 sentences per revision: what changed, where from (wikilink to source)
- Update frontmatter `Modified:` to today's date
- Always keep a `## Revisions` section once the first update happens. Later updates add H3 rows.
- Frontmatter changes (tags, Links) count as revisions and are documented

This gives a wiki history without needing git: the card carries its own change story, visible in Obsidian.

## Index maintenance

For every created card: append a row to `Cards/_index.md` (title, aliases, gist).
For every updated card: regenerate the card's gist row if the first substantive sentence changed.
For full reindex when needed: see `workflows/reindex.md`.

## ALGORITHM integration

When invoked from the ALGORITHM VERIFY phase:
1. Identify the produced text artefact (chronicle, memo, report, longer note)
2. If <800 words or no substantive text: return silently, continue VERIFY
3. Otherwise run the workflow above
4. If all buckets empty: silent pass
5. If suggestions exist: present list, wait for the user, run chosen actions, document in PRD `## Verification` with: `- Atomize: {N} cards created, {M} linked in, {K} updated.`

## Anti-patterns

- **Creating cards without user approval.** Atomize suggests, never commits without yes.
- **Suggesting trivial cards.** "AI" as a candidate when the text just mentions it in passing = noise.
- **Mass-updating without diff.** The user must see what is suggested.
- **Forgetting backlink.** A new card without a connection back to the source breaks the weave again.
- **Breaking YAML conventions.** Always follow the vault's metadata conventions.

---

🎯 COMPLETED: [SKILL:atomize-zettel] [atomic-note suggestions for X]
🗣️ CUSTOM COMPLETED: [SKILL:atomize-zettel] [Atomize complete]
