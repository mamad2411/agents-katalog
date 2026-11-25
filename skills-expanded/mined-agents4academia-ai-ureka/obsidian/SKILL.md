---
description: Ingest an Obsidian/markdown note into a structured notes file in notes/
argument-hint: <path to .md file> (e.g. "/Users/name/obsidian-vault/my_note.md")
allowed-tools: Read, Write(notes/**), Glob, Bash(date:*), Bash(python3:*)
---

Ingest an Obsidian note at **$ARGUMENTS** and produce a structured
`notes/obsidian_<slug>.md` file following the project template.

If **$ARGUMENTS** is empty, ask the user for a file path, then continue.

## Layout

All output is under `notes/` (personal notes, as opposed to
objective sources under `sources/`). Template lives at
`.claude/Templates/note.md`. Existing files in `notes/` are
style references — read one before writing your first output.

## Steps

1. **Extract.** Read the note at **$ARGUMENTS** with the `Read` tool. Identify:
   - The H1 (`# ...`) line as the `title`. If absent, fall back to the filename
     stem with underscores/dashes converted to spaces, in Title Case.
   - `[[wikilinks]]` and `#tags` — leave them in place inside the body. The
     navigator uses `[[wikilinks]]` as graph edges, so they must be preserved
     verbatim.
   - Concepts list: collect the target of each `[[wikilink]]` (the part
     before `|` if aliased, trimmed) plus each `#tag` name (strip the
     leading `#`). Dedup at exact-string level, preserve first-occurrence
     order. This becomes the `concepts_mentioned` field.

2. **Format.** Fill in the obsidian schema below. This skill extends the
   shared `.claude/Templates/note.md` with `source_links` (a list) and
   `concepts_mentioned`; the schema here is authoritative for obsidian notes.
   - `type: obsidian_note`
   - `title`: from Step 1
   - `source_links`: a YAML block list containing **$ARGUMENTS** verbatim as
     its single entry:

         source_links:
           - $ARGUMENTS

   - `concepts_mentioned`: an inline YAML list of the concepts collected in
     Step 1 (e.g. `[chain-of-thought, tool-use, transformers]`). Use `[]` if
     the note has no `[[wikilinks]]` or `#tags`.
   - `## Content`: the full note text. Preserve the author's wording, headings,
     lists, code blocks, emphasis, `[[wikilinks]]`, and `#tags` as faithfully as
     possible. Do not summarise unless the note is very long.

   Before writing, verify the envelope:
   - Starts with `---` on line 1; has a closing `---` delimiter.
   - Contains exactly these four frontmatter keys: `type`, `title`,
     `source_links`, `concepts_mentioned`.
   - `type` is the literal string `obsidian_note`.
   - `source_links` is a YAML list whose only entry equals **$ARGUMENTS** verbatim.
   - `concepts_mentioned` is a YAML list (possibly empty).
   - Body contains a non-empty `## Content` section.

   If any check fails, fix the envelope before writing.

3. **Write.** Slugify the title to snake_case (lowercase, spaces/dashes →
   underscores, drop non-alphanumeric characters). Write to
   `notes/obsidian_<slug>.md` with the `Write` tool. If the file
   already exists, ask the user before overwriting.

4. **Propose.** After writing, suggest the user:
   - Run `/retrieve <topic>` to find related sources and existing pages.
   - Run `/collate <topic>` to synthesise a paper or concept page from this
     note together with other sources on the same topic.

## Wrap up

Report: output file path, the title and wikilinks/tags preserved, and anything
skipped (one-line reason each).
