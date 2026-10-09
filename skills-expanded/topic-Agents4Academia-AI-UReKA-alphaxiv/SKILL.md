---
description: Ingest a paper from AlphaXiv/arXiv (by arXiv ID or title) into a structured source file — fetches metadata, abstract, and the AI overview via the AlphaXiv API
argument-hint: <arXiv ID or paper title> (e.g. "2006.11239", "denoising diffusion probabilistic models")
allowed-tools: Read, Write(sources/**), Write(course/**), Glob, Bash(date:*), Bash(sh .claude/src/pyrun:*)
---

Ingest a paper from [AlphaXiv](https://www.alphaxiv.org) (an arXiv front-end with
AI overviews and metadata) into `sources/alphaxiv_<slug>.md`. Unlike `/zotero`,
there's **no local PDF** — content is fetched from the AlphaXiv API: bibliographic
metadata, the abstract, and an AI-generated overview. This is normally invoked by
`/collate` as an ingestion step, but can be run directly.

If **$ARGUMENTS** is empty, ask the user for an arXiv ID or paper title, then continue.

## Layout

Output goes to the **personal** `sources/` by default. When invoked by `/curriculum`,
write instead to that course's **per-course library** `course/<slug>/library/` (the
caller passes the destination directory) — fetched course material stays out of the
personal base until the learner masters it and `/tutor` promotes it. Either way the
filename is `alphaxiv_<slug>.md`.
Template: `.claude/Templates/source.md`. The fetch tool is
`.claude/skills/alphaxiv/scripts/alphaxiv.py` (stdlib only; the ingestion commands
below need no API key).

## Steps

1. **Resolve the paper.**
   - If **$ARGUMENTS** is an arXiv ID (e.g. `2006.11239` or `2006.11239v2`), use it.
   - Otherwise treat it as a title/topic and search, then confirm the match with the
     user before ingesting:
     ```bash
     sh .claude/src/pyrun --need any .claude/skills/alphaxiv/scripts/alphaxiv.py search "$ARGUMENTS" --limit 5
     ```

2. **Extract.** Fetch the objective content for the resolved arXiv ID `<id>`:
   ```bash
   sh .claude/src/pyrun --need any .claude/skills/alphaxiv/scripts/alphaxiv.py paper <id>       # title, authors, date, abstract
   sh .claude/src/pyrun --need any .claude/skills/alphaxiv/scripts/alphaxiv.py metadata <id>    # authors, institutions, topics, GitHub
   sh .claude/src/pyrun --need any .claude/skills/alphaxiv/scripts/alphaxiv.py overview <id>    # AI-generated overview
   ```

3. **Format.** Write the file following `.claude/Templates/source.md` for the frontmatter
   contract, with exactly this structure (no need to consult other source files):

   ```markdown
   ---
   type: alphaxiv_source
   title: <paper title>
   concepts_mentioned: [<AlphaXiv topics + key concepts from the abstract>]
   source_links:
     - https://arxiv.org/abs/<id>
     - https://www.alphaxiv.org/abs/<id>
   ---

   ## Content

   ### Abstract

   <the paper abstract, verbatim>

   ### AI overview (AlphaXiv — AI-generated)

   <the AlphaXiv AI overview; this is AI-generated, not the authors' own text>

   ### Metadata

   - Authors: <...>
   - Institutions: <...>
   - Published: <date>
   - Topics: <...>
   - Code: <GitHub URL, if any>
   ```

   `source_links` holds URLs (a remote source has no local file). This is
   metadata + abstract + AI overview — **not** the full paper text; for full text,
   ingest the PDF via `/zotero`.

4. **Write.** Slugify the title to snake_case and write `<dest>/alphaxiv_<slug>.md`,
   where `<dest>` is `sources/` by default or `course/<slug>/library/` when `/curriculum` invoked
   this skill. If it exists, ask before overwriting.

5. **Propose.** After writing, ask the user:
   - Run `/collate <title>` to synthesise this source into a paper page?
   - Run `/collate <topic>` for any new concepts introduced?

## Notes

- Vendored, security-reviewed script from
  [danjuan-77/alphaxiv-skill](https://github.com/danjuan-77/alphaxiv-skill) (MIT, see
  `LICENSE` in this folder). It calls only `https://api.alphaxiv.org`.
- The ingestion commands (`search`, `paper`, `metadata`, `overview`) need no token.
  The script also has an `ask` command that needs `ALPHAXIV_TOKEN`; it's not used by
  this skill.

## Wrap up

Report: the file written, concepts extracted, anything skipped (one-line reason each).
