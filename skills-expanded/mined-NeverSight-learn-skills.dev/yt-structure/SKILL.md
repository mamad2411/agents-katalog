---
name: yt-structure
description: Use when turning a YouTube video, talk, podcast, or web article into a clean, citable Markdown document for an LLM knowledge library or RAG/OKF bundle — triggers like "transcribe and structure this video", "structure this transcript", "add this talk/article to the library". Covers pulling captions, faithful structuring, and editor's-note / [?] flagging.
---

# yt-structure

## Overview

Turn a spoken or web source into a faithful, scannable, citable Markdown file for LLM ingestion.

**Core principle: structure and clean phrasing only — never paraphrase substance, never invent content, and flag what you can't verify instead of guessing.**

## When to use

- A YouTube video, conference talk, podcast, or lecture → a cleaned `.md`.
- A blog post / web article you want as faithful text (not a summary).
- Adding a source to your knowledge library (a target library folder, an OKF/RAG bundle — at Pesty this is usually the internal Agents library).

**When NOT to use:**
- A messy *meeting* transcript with crosstalk (Gemini/Fathom) → that's a separate internal cleanup process (de-fragment turns), not covered by this skill.
- You just want a quick summary — this produces a faithful structured document, not a digest.

## Step 1 — Ingest the raw source

**Video / talk / podcast:**

Use the bundled script at `scripts/yt-transcript` (relative to this skill folder):
```
scripts/yt-transcript <youtube-url> [output-dir]
```
Writes a clean `<slug>.txt` (strips YouTube's rolling-window caption duplication) and prints the path. Run it with no args for usage. Prerequisite: `yt-dlp` (`brew install yt-dlp` or `pipx install yt-dlp`). Do NOT use Tactiq, web tools, or `youtube-transcript-api` — they waste tokens and break sentences.

If the script isn't available in this environment, fall back to the raw command it wraps:
```
yt-dlp --skip-download --write-auto-sub --sub-lang 'en.*,en' --sub-format vtt -o '%(id)s.%(ext)s' <url>
```
then strip the timestamp/tag markup and deduplicate repeated caption lines yourself.

**Web article:**
```
curl -sL "<url>" | pandoc -f html -t markdown_strict
```
Use this for blog posts — agent web-fetch tools *summarize* prose and lose faithful text. (Official docs pages usually come through a web-fetch tool fine.) Prerequisite: `pandoc` (install via brew/apt) — or any equivalent HTML→Markdown converter works.

## Step 2 — Structure into a sibling `.md`

Write `<slug>.md` next to the raw source, same slug. Follow these conventions exactly:

- **Header block:** `# Title`, then `**Speaker:**` / `**Author:**` line, then `**Source:**` <url>.
- **`##` headers** at topic transitions; `###` for sub-beats.
- **Strip filler** (um, uh, "kind of", "you know", redundant so/well/right, doubled phrases). Phrasing cleanup only.
- **`> [Visual: …]`** blockquotes for on-screen references (clips, slides, diffs, B-roll, demos).
- **Verbatim quotes / cited passages → blockquotes**; **bold** the takeaways.
- **End with `## Recap`.**
- **`### Editor's note`** at the end: list proper-noun corrections you made + any unresolved `[?]` flags.
- **Multi-speaker:** preserve who-said-what; never invert authorship (don't credit a listener/agreer with the speaker's point).
- **Flag, don't guess:** garbled names/tools/companies get a `[?]`. Verify the big factual flags (names, tools, claims) with a web search before de-flagging.

**Example output** (illustrating the conventions above):

```markdown
# Why Most SaaS Onboarding Fails
**Speaker:** Jane Rivera
**Source:** https://youtube.com/watch?v=abc123

## The core problem

### Users never reach the "aha moment"
**Most churn happens before value is ever felt.** Rivera argues teams over-invest
in visual polish and under-invest in the first five minutes of use.

> [Visual: funnel chart showing 80% drop-off before day two]

> "We rebuilt onboarding around one metric: time to first real result."

She attributes the framework to Kathy Sierra [?] — spelling unconfirmed.

## Recap
Ship a narrow, guided first-run path; measure time-to-value, not signups.

### Editor's note
Corrected "Rivera" (garbled as "Rivero" in captions). Unresolved: `[?]` on
"Kathy Sierra" — not yet verified via web search.
```

## Step 3 — Add to the library (if building one)

Append the new file to the library's `INDEX.md` / `index.md`. If the library is an **LLM-wiki / OKF bundle**, also update the concept pages the source touches (don't just add a file) — follow that library's `CLAUDE.md` maintenance loop.

## Common mistakes

| Mistake | Fix |
|---|---|
| Tactiq / `youtube-transcript-api` for captions | Use `scripts/yt-transcript` (dedups, LLM-ready) |
| A web-fetch tool for a blog article | It summarizes — use `curl … \| pandoc` for faithful text |
| Paraphrasing or compressing substance | Clean phrasing only; keep the content |
| Guessing a garbled proper noun | `[?]` flag + a web search to confirm |
| Inverting authorship in multi-speaker talks | Preserve attribution; agreement ≠ authorship |
| Skipping the Recap / Editor's note | Both are required closers |
</content>

---

> Maintained by [Pesty Marketing](https://pestymarketing.com) · Browse the [full skill catalog](https://pestymarketing.com/agent-skills/).
