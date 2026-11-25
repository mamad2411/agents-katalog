---
name: slp-summarize
description: Summarizes study material (pasted, attached, or from a topic's resources/ or sources) into a note in topics/*/notes/, in the topic's notes language unless the user asks for another, and files the source into the topic's wiki. Use when the user says "summarize this", "/slp-summarize", "add this summary to the note", or pastes or attaches a fragment of a book or article to condense.
---

# Summarize

Condenses material into the topic's notes, in the format those notes use, and
records the source in the topic's wiki.

## Required data (ask together if missing)

1. **Source**:
   - **pasted**: in the message.
   - **attached**: a PDF or image; read it with `Read`.
   - **`resources/`**: a file in `topics/<topic>/resources/` (uploads from the
     app land there); ask which if they don't say.
   - **local path**: a `path` entry of `topic.json` `links`. Missing file: say
     so in one line and ask for another source.
2. **Destination**: topic and note (e.g.
   `topics/example/notes/01-methods-and-status-codes.md`). The note being
   worked on in this conversation, if any. **No note fits**: create
   `notes/NN-<slug of its h1>.md` (next free `NN`) with a single `# ` title.
3. **Level** (default `medium`):
   - **compact**: bullets with the key idea of each concept; examples only if
     essential.
   - **medium**: shorter than the original but understandable without it;
     the most important examples.
   - **extensive**: close to full study notes; keeps nuances, most examples
     and distinctions. Still a summary, not a translation.
4. **Language**: an explicit request wins; else `language.notes`; no
   `language` set: ask once.

Data already given in the conversation: don't ask, summarize.

Log a `summary` activity ([slp-session §Activity](../slp-session/SKILL.md#activity)).

## Note format

[formats.md § Notes](../../reference/formats.md#notes): one `# ` per file
(don't add a second), `##` topics, `###` subtopics, `- ` lists, one idea per
item, no nested lists (the app flattens them), prose paragraphs, GFM tables
allowed. Leave existing raw HTML and HTML entities (`&#42;`, `&lt;`) as they
are and add no new markup. A mermaid or math fence only when the text describes a structure or
formula better understood drawn.

## Summary rules

- Write naturally in the output language, study-notes style, not a literal
  translation.
- Keep important technical terms in their original language when it differs
  (*trade-off*, *coupling*), explained if needed.
- Nothing that isn't in the source. No conclusion, no repetition.
- Keep the most important examples (more at `extensive`, fewer at `compact`).
- Already covered in the note: merge it and say so, don't duplicate.

## How to add it

Append at the **end** of the note as new `##`/`###` sections (a source with
its own subheadings gets them translated). Use Edit to append; don't rewrite
existing parts unless asked.

## After writing

1. **Wiki ingest** ([formats.md § Wiki](../../reference/formats.md#wiki)):
   write or update `wiki/sources/<kebab>.md` (`type: Source`: what the source
   covers and the concepts it touches), upsert the `wiki/concepts/` pages it
   touches with footnote citations, add the open session's `id` to each
   Concept's `studied`, and update `wiki/index.md`.
2. `progress/status.md` → **Summary written:** yes (for the current unit).
3. Report in 1-2 lines which headings were added to which note. Don't repeat
   the summary in the chat.
4. Ask whether this finished the unit; if yes, run
   [slp-session §Unit done](../slp-session/SKILL.md#unit-done).
