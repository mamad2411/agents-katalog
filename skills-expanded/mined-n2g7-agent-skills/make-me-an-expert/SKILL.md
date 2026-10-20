---
disable-model-invocation: true
name: make-me-an-expert
description: >
  This skill should be used when the user says "make me an expert in",
  "/make me an expert in", "continue expert pack", "teach me from .expert",
  or "make me an expert — continue". Also use it when the user is stuck on a
  chapter in an existing `.expert/<topic>/` pack. It builds a sourced
  `.expert/<topic>/` pack and one Markdown coursebook PDF. Then it teaches
  from that pack. After it writes files, it applies `ste-writing` and `unslop`.
  Not tutoring-only (learn), workspace lessons (teach), or lit-review reports
  (deep-research).
source: original
date_added: "2026-08-29"
---

# Make Me An Expert

Build a sourced path from novice to competent practitioner. Also give a map of the frontier.

Write a local expert pack and one coursebook PDF. Then teach from that pack.

This is not a certificate. This is not a slide deck. This is not a dump of copyrighted books.

All pack prose and teaching replies must pass `ste-writing` and `unslop` before you show them. See [references/ste-pass.md](references/ste-pass.md).

## When to Use

- The user says "make me an expert in …", "/make me an expert in …", "continue expert pack", "teach me from .expert", or "make me an expert — continue"
- The user wants a sourced `.expert/<topic>/` pack and one Markdown coursebook PDF. Then teaching from that pack
- The user is stuck on a chapter in an existing `.expert/<topic>/` pack and needs gap-fill

## When NOT to Use

- Tutoring only, drills, study guides, or "help me understand X" with no pack. Use `learn`
- A multi-file teaching workspace as the main artifact. Use `teach`
- A literature review or research report with no coursebook and no teaching loop. Use `deep-research`
- Slide decks. Do not compose `2slides-ppt-generator` or `frontend-slides`
- The user has started coding or other work. Pause teaching. Leave `STATE.md`. Do not take over Agent mode

## Constraints

- **Pack path:** always `<user-project>/.expert/<topic-slug>/`. Never write packs inside `~/.agents/skills/` or this skills repo. If the current workspace is the skills library, ask for a target project path first.
- **PDF:** a paginated coursebook from Markdown. Not 16:9 slides.
- **Compose cap:** at most 4 sibling skills this run. Search the catalog first. Load one `SKILL.md` at a time. Never bulk-read the library.
- **STE and unslop:** always on after you write pack Markdown and before you render the PDF. Also run them on each teaching reply. They do not count toward the cap of 4.
- **YouTube:** transcripts and `watchlist.md`. This agent cannot watch video.
- **Copyright:** Distill and cite. Never paste full books, papers, or transcripts into `kb/` or the PDF. Link out.
- **Safety:** educational material. Not professional advice. This includes medical, legal, and financial advice. Put this line in the PDF too.
- **Expertise ceiling:** fluency and a map of open debates. Not mastery.

## Resume

This skill does not auto-load (`disable-model-invocation: true`).

1. Write `.expert/<topic-slug>/STATE.md` in the user project. Copy [templates/STATE.md](templates/STATE.md).
2. During intake, offer an optional Cursor project rule in that repo. The rule should notice `.expert/` and resume in Ask mode. If the user accepts, add a short rule. When `.expert/` exists, load `STATE.md` and continue from the current chapter.
3. Tell the user the resume line: **make me an expert — continue**
4. Later chats: load `STATE.md` first. Reuse `composed_skills`. Do not redo the research pass unless sources are stale or the user asks.

## Pack layout

```
.expert/<topic-slug>/
  STATE.md
  MISSION.md
  SOURCES.md
  kb/
  course/book.md
  output/expert-course.pdf
  watchlist.md
  supplements/
```

`kb/` holds distilled, cited notes. `course/book.md` is the coursebook source and the PDF source. `supplements/` holds gap-fill addenda.

[templates/chapter.md](templates/chapter.md) is the section shape inside `course/book.md`. It is not a second file tree. Do not create `course/ch-*.md`. The PDF script reads one `course/book.md`.

## Phases

Run in order. Stop if the user switches to other work.

### 1. Intake

Ask once. Then proceed. Details: [references/intake.md](references/intake.md).

1. **Scope:** this repo, the named topic, or both
2. **Prior knowledge:** none / some / practitioner, plus 3 to 5 probe questions. Do not assume they know what they claimed.
3. **Goal:** ship in this repo, interview, academic, or operational fluency
4. **Limits:** time, languages, topics to skip, depth ceiling
5. **Teaching style:** default explainer. Offer `learn` or `explain-like-socrates` if they ask. Do not copy those skills.
6. Offer the optional project rule. Give the resume line.

If the codebase is in scope: catalog and structure first. Then targeted reads. Do not bulk-read this skills library.

### 2. Catalog route

Follow [references/compose.md](references/compose.md). Run the skill-recommender protocol in this process. Search `_catalog/` only. Pick 1 primary skill ID and up to 3 supporting skill IDs. Write them to `STATE.md` under `composed_skills:`. Load each matching `SKILL.md` one at a time, only if it matches this run. Cap 4 siblings.

Do not compose `2slides-ppt-generator`, `frontend-slides`, or `pdf-official`. Skip API-key search tools (`tavily-web`, `exa-search`, `firecrawl-scraper`) unless the user already has keys.

### 3. Research

Follow [references/research.md](references/research.md). Rank: official docs and primary papers, then textbooks and surveys, then high-signal talk transcripts, then reputable blogs. Skip SEO junk.

Cap ingest per run: about 8 to 15 core text sources, and about 3 to 5 transcripts. Default fetch: composed `efficient-web-research` and `defuddle`. Academic topics: `papers-skill`. YouTube: `youtube-full` transcripts. Put the rest on `watchlist.md`.

### 4. Knowledge base

Write distilled notes into `kb/` with citations. Record ingest status in `SOURCES.md`. If `wiki-builder` is composed, borrow provenance habits. Do not replace the `.expert/` layout.

### 5. Coursebook Markdown

Follow [references/curriculum.md](references/curriculum.md). Write one linear `course/book.md`. Do not create `course/ch-*.md`. Use [templates/chapter.md](templates/chapter.md) as the section shape inside that file.

- Map of the territory
- Diagnostic: "you said you know X" as a 1-page check
- Foundations, then core, then advanced, then frontier
- Worked examples tied to this repo when scope includes it
- Active-recall questions and practice tasks per chapter
- Annotated bibliography
- What experts still argue about

### 6. STE and unslop

Follow [references/ste-pass.md](references/ste-pass.md). Load `ste-writing`. Rewrite pack Markdown. Then run `unslop --stdin --deterministic` on those files. Check the result. Then continue.

### 7. Coursebook PDF

Render with this skill's `scripts/render_coursebook.py`. Markdown to HTML to PDF. WeasyPrint first. Pandoc as fallback. Packs live in the user project. The script lives in the skills repo. From the user-project cwd:

`python3 <skills-root>/make-me-an-expert/scripts/render_coursebook.py .expert/<topic-slug>/course/book.md -o .expert/<topic-slug>/output/expert-course.pdf`

Resolve `<skills-root>` as: project `.agents/skills`, else this repo root, else `~/.agents/skills/`. Write `output/expert-course.pdf`. Printable TOC and page numbers. Not slides.

### 8. Teach

Follow [references/teaching.md](references/teaching.md). Teach from `kb/` and the current chapter. One idea at a time. Check understanding. If `learn` is composed, use that skill's retrieval-check pattern. If the user asked for Socratic style, load `explain-like-socrates`. Write each reply in STE. Then run `unslop` on the reply before you send it.

### 9. Gap-fill

When the user is stuck or a diagnostic fails: research the missing prerequisite. Append `kb/` and `supplements/`. Run the STE and unslop pass again. Re-render the PDF or a short supplement PDF. Then explain again. Say this clearly: they claimed X. The gap is Y. You added Y. Update `STATE.md` (`known` / `unknown` / `open_gaps` / `last_chapter`).

## Mode

- **Ask mode:** teach from the pack.
- **Agent mode:** research, write files, render PDF. If the user starts other work, pause.

## References

- [references/intake.md](references/intake.md): scope and diagnostic questions
- [references/compose.md](references/compose.md): catalog routing, sibling list, do-not-compose
- [references/research.md](references/research.md): queries, source ranking, YouTube and transcript rules
- [references/curriculum.md](references/curriculum.md): coursebook outline, expertise ceiling
- [references/ste-pass.md](references/ste-pass.md): STE rewrite and `unslop` on pack files and replies
- [references/teaching.md](references/teaching.md): Ask-mode teaching, gap-fill, handoff to `learn` or Socratic
