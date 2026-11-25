---
description: Collate personal notes and sources into a paper or concept page, or update an existing page with a new source
argument-hint: <topic or paper name> (e.g. "ReAct", "attention", "RLHF")
allowed-tools: Read, Write(papers/**), Write(concepts/**), Glob, Bash(date:*), Bash(sh .claude/src/pyrun:*)
---

Collate all personal notes and source material for **$ARGUMENTS** into a single
paper or concept page, distinguishing personal annotations from objective content.
Also handles updating existing pages when a new source is added.

If **$ARGUMENTS** is empty, ask the user for a topic or paper name, then continue.

## Step 0 — Check ingestion

Glob `sources/` and `notes/` for any files matching **$ARGUMENTS** (by slug or
title). If nothing is found, tell the user and prompt them to run the appropriate
ingestion skill first:

- PDF → `/zotero <path>`
- Notion export → `/notion <path>`
- Obsidian note → `/obsidian <path>`
- arXiv paper → `/alphaxiv <id or title>`

Then stop. If files are found, continue to Step 1.

## Step 1 — Retrieve

Run the BM25 retriever to get seed notes, then expand by following relevant
wikilinks — exactly as the `/retrieve` skill does:

1. ```bash
   sh .claude/src/pyrun .claude/src/retrieve_cli.py --retrieve "$ARGUMENTS"
   ```
   Each output line is `<file path>\t<title>`. These are your seed notes.

2. For each seed, `Read` it and follow any `[[wikilinks]]` you judge relevant
   to **$ARGUMENTS**, resolving them with:
   ```bash
   sh .claude/src/pyrun .claude/src/retrieve_cli.py --resolve "<link>"
   ```
   Output is `<link>\t<path|NONE>`; skip `NONE`. Stop after ~1–2 hops.

The relevant set covers all four dirs: `sources/`, `notes/`, `papers/`, `concepts/`.

If retrieve returns nothing relevant, name the closest topics already covered in
the base and stop without writing. Do not attempt to write a page with no source
material.

## Step 2 — Detect type

Decide: is **$ARGUMENTS** a **paper** (specific published work) or a **concept**
(topic, idea, technique)?

- If a paper → output to `papers/<slug>.md`, use paper template
- If a concept → output to `concepts/<slug>.md`, use concept template

If unsure, ask the user.

## Step 3 — Check for existing page

Slugify **$ARGUMENTS** to kebab-case and check whether `papers/<slug>.md` or
`concepts/<slug>.md` already exists.

- **Existing page found** → read it and **ask the user**: "I found an existing
  page for *<title>* — is this the one you want to update, or are you working on
  a different sense of the term?" If it's the same, switch to **Update Mode**
  (see below). If different, ask for a clarifying name to disambiguate the slug,
  then continue to Step 4.
- **No existing page** → continue to Step 4 (create from scratch).

---

## Update Mode — adding a new source to an existing page

Use this when a page already exists and a new source has been ingested that is
relevant to it.

### U1 — Identify new sources
Read the existing page's `sources:` frontmatter list. Compare against all
retrieved files from Step 1. Any file not already listed is a new source.

If there are no new sources, tell the user the page is already up to date and stop.

### U2 — Merge personal notes and annotations
For each new source:
- If from `notes/notion_*.md` or `notes/obsidian_*.md`: append to `## My Notes`
  as a new paragraph, clearly separated from existing content.
- If from `notes/zotero_*/annotations.md`: weave new annotations into the
  relevant objective content sections as callouts, following the annotation
  rendering rules in Step 5. Never duplicate an annotation already present.

### U3 — Merge objective content
Read the new source's `## Content`. Identify any claims, findings, or details
not already covered in the existing page's `## Summary` sections.
Add only genuinely new information — do not rewrite existing content.
Append to the relevant section or add a new section if needed.
Cite inline with a relative link to the new source file.

### U4 — Update frontmatter
Add the new source path to `sources:` in frontmatter. Update `created` → keep
original; do not change it.

### U5 — Write
Overwrite the existing file with the merged content. Report what was added.

---

## Step 4 — My Notes section (new page)

Read the relevant template (`.claude/Templates/paper.md` or `.claude/Templates/concept.md`).

Gather Notion/Obsidian material (files matching `notes/notion_*.md` or
`notes/obsidian_*.md`) into a `## My Notes` section at the top of the page:

- Include the full note content as plain paragraphs, preserving the author's words.
- Preserve all `[[wikilinks]]` and `#tags` exactly as written — do not convert or strip them.
- If there are no Notion/Obsidian notes, omit the section entirely.

## Step 5 — Objective Summary with Annotations (new page)

Write the objective summary from `sources/` material (Zotero source files,
AlphaXiv sources). Follow the appropriate template structure:

**Paper:** Summary, Key Contributions, Methodology, Important Concepts,
Connections to Related Work, Limitations & Open Questions.

**Concept:** Overview, thematic sections, Related Concepts.

Follow the **Page conventions** in `.claude/AGENTS.md` — grounding & citations,
mathematics in LaTeX (be mathematical where the material is; include critical
equations and derivations), and cross-linking. `Read` `.claude/AGENTS.md` if
those conventions aren't already in context.

**While writing each section**, check the Zotero annotation file(s) (files under
`notes/zotero_*/annotations.md`) for annotations that touch the content of that
section. Use the annotation's position description and annotated text to determine
where it belongs. Weave the annotation in immediately after the relevant
paragraph using the following rules:

### Annotation rendering rules

**Ink underline — no question or comment alongside:**
Bold the underlined phrase/sentence inline within the objective prose. The bold
signals the reader found this important without adding visual clutter.
Example: the sentence containing `"the Transformer is the first transduction model relying entirely on self-attention"` becomes `**the Transformer is the first transduction model relying entirely on self-attention**`.

**Ink underline — with a question or comment written alongside:**
Bold the underlined text in the prose, then immediately after the paragraph add
a `[!question]` callout quoting the question:
```
> [!question]
> "question text as written"
```

**Handwritten question (standalone, not tied to an underline):**
Add a `[!question]` callout immediately after the paragraph most relevant to
that question:
```
> [!question]
> "question text as written"
```

**Handwritten comment or expansion (not a question):**
Add a `[!note]` callout immediately after the relevant paragraph:
```
> [!note]
> "comment text as written"
```

**Ink circles, strokes, or marks on figures/diagrams:**
Add a `[!note]` callout near the prose describing that figure or diagram, briefly
noting what was circled or marked and what it likely indicates:
```
> [!note]
> Circled [element] in Figure N — marks [what the reader was tracking].
```

Skip any annotation that is too vague to place (e.g. a single mark with no
discernible text or figure reference), and note it in the wrap-up.

## Step 6 — Fill frontmatter (new page)

**Paper frontmatter:**
```yaml
title, type: paper, created, authors, year, related_papers, related_concepts, sources
```

**Concept frontmatter:**
```yaml
title, type: concept, created, related_concepts, related_papers, sources
```

`authors` and `year` are paper-only. Extract from the source material if available.

## Step 7 — Write (new page)

Write to `papers/<slug>.md` or `concepts/<slug>.md` (slug from Step 3).

## Wrap up

Report: file written or updated, which `sources/` and `notes/` files were used,
anything skipped (one-line reason each). Then ask the user if they're happy or
want to refine — loop via `/edit <page path>` until they are. Do not reindex
manually — the background poller rebuilds the index automatically after edits settle.