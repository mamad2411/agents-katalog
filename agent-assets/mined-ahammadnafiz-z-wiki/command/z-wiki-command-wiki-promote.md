---
description: Promote stubs that crossed promotion thresholds into full concept/entity pages.
argument-hint: "[slug | --all | --list]"
when_to_use: Use to graduate stubs whose source_count or inbound_refs_primary has met the threshold. INGEST no longer auto-promotes — it only flags candidates. This command is the explicit promotion gate so the (expensive) full-page generation step is user-controlled. Triggered by phrases like "promote stubs", "graduate pending concepts".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Wiki Promote

Promote stubs that crossed a page-creation threshold into full pages.
Deliberate, user-triggered — INGEST never does this on your behalf.

## Why this is a separate command

Stub promotion is the single most expensive step in INGEST: each
promotion is a ~300–1200 word full-page generation. Auto-promoting
inside INGEST burned Claude tokens on pages the user hadn't yet
decided were load-bearing. This command makes the cost visible and
scoped.

## Dispatch

### Mode 1: `$ARGUMENTS` empty or `--list`

List candidates without writing anything:

1. Ensure `wiki/.meta/backlinks.json` is fresh — if older than the
   newest file in `wiki/sources/` or `wiki/concepts/` or
   `wiki/entities/`, run `python3 scripts/build_meta.py --embed-if-enabled` first.
2. For every page whose `type: stub` frontmatter matches:
   - `source_count >= 2` (source axis), **or**
   - `inbound_refs_primary >= 5` (reference axis — counts inbound
     wikilinks only from `sources/`, `concepts/`, `entities/`; never
     from `outputs/` or `syntheses/`)
   print one line: `slug · source_count=N · inbound_refs_primary=M · title`.
3. Print totals. Exit. No writes.

### Mode 2: `$ARGUMENTS` is a slug

Promote that one stub:

1. Read the stub. Extract its existing summary, tags, source
   backlinks, any hand-written notes.
2. Pick the right template (`templates/concept.md` for concept
   stubs, `templates/entity.md` for entity stubs).
3. Write a full page preserving:
   - `title`, `tags`, `date_created`, existing `summary` (as
     starting point).
   - All existing inbound-source references as "Appears in:"
     citations.
4. Set frontmatter `type: concept` or `type: entity`,
   `status: draft`, `date_modified: today`.
5. **Before writing, show me a draft.** Do not commit until I
   confirm. This is the control point.

### Mode 3: `$ARGUMENTS` is `--all`

Promote every candidate. Implement as a loop over Mode 2, with one
confirmation at the start ("Promote N candidates? y/n") rather than
per-page. Useful after a big ingest batch.

## Quality bar for promoted pages

The promoted page must earn the graduation:
- 300–1200 words of synthesis, not transcription.
- At least 2 distinct inbound source citations worked into prose.
- "Related concepts" section with at least 2 `[[wikilinks]]`.
- Plain-language first paragraph that could stand alone as a
  definition.

If the source material doesn't support that bar, push back: tell me
the stub should stay a stub until more sources come in. Do **not**
pad a promoted page to hit word counts.

## After promoting

- Run `python3 scripts/build_meta.py --embed-if-enabled` to refresh the sidecar.
- Run `python3 scripts/shard_index.py` to update catalogs.
- Append one entry per promoted page to `wiki/log.md`:
  `## [YYYY-MM-DD HH:MM] promote | <slug>`.

## Reporting

- Candidates listed (with thresholds crossed)
- Pages promoted (with before/after word counts)
- Pages skipped and why
