---
description: Ingest a vetted web resource (Wikipedia article, blog post, tutorial, or docs page) into a credibility-scored source file — curated registries first, then WebSearch/WebFetch
argument-hint: <url> | wiki "<topic>" | search "<query>" (e.g. wiki "diffusion model", https://lilianweng.github.io/...)
allowed-tools: Read, Write(sources/**), Write(course/**), Glob, WebSearch, WebFetch, Bash(date:*), Bash(sh .claude/src/pyrun:*)
---

Ingest a **factual, verifiable, widely-used** web resource into
`sources/web_<slug>.md`, recording a **credibility score** so every downstream
citation is auditable. Prefers **curated registries** (Wikipedia, official docs,
canonical blogs) and falls back to `WebSearch`/`WebFetch`, scoring each candidate
with `resources_cli.py` (a deterministic domain-tier prior) plus your own judgment
for borderline cases. Normally invoked by `/curriculum` as a pull step, but can be
run directly.

If **$ARGUMENTS** is empty, ask the user for a URL, a `wiki "<topic>"`, or a
`search "<query>"`, then continue.

## Layout

Output goes to the **personal** `sources/` by default; when invoked by `/curriculum`,
write to that course's **per-course library** `course/<slug>/library/` instead (the
caller passes the destination directory). Either way the filename is `web_<slug>.md`.
Template:
`.claude/Templates/web_source.md`. The engine is `.claude/src/resources_cli.py` (stdlib; needs
no API key). The credibility keep-threshold is **0.60** by default.

## Mode A — `wiki "<topic>"` (curated registry, preferred)

1. **Search** Wikipedia and review the scored hits:
   ```bash
   sh .claude/src/pyrun .claude/src/resources_cli.py --wikipedia "<topic>" -k 5
   ```
   Each JSONL line has `title, url, snippet, score, tier`. Pick the best-matching
   article (confirm with the user if ambiguous).

2. **Fetch** the full article content:
   ```bash
   sh .claude/src/pyrun .claude/src/resources_cli.py --wiki-page "<exact title>"
   ```
   Returns `title, url, summary, extract` (full plain text), `references`, `score`.

3. **Format & write** (Step "Write" below) using `extract` as `## Content`. Keep
   the substantive sections; you may drop "See also"/"External links" tails (note
   the omission). Wikipedia is `canonical` tier — it clears the threshold.

## Mode B — `<url>` (a specific page)

1. **Score the domain** first:
   ```bash
   sh .claude/src/pyrun .claude/src/resources_cli.py --score "<url>"
   ```
2. **Fetch** the page with `WebFetch` (returns clean Markdown). While reading,
   note the **signals** that refine credibility: a named author/byline, a
   references/citations section, and the publication year.
3. **Decide** (see *Credibility decision* below). If kept, **format & write**.
   If dropped, tell the user why (one line) and stop.

## Mode C — `search "<query>"` (discovery)

1. **Search** with `WebSearch` for the query (optionally seed from curated hubs:
   `sh .claude/src/pyrun .claude/src/resources_cli.py --hubs "<area>"`).
2. **Score** each candidate's domain with `--score <url> <url> ...`.
3. **Present** the top 3–5 as a list labelled `tier · score · why` (highest first),
   and ask which to ingest. For each chosen URL, continue as **Mode B** from step 2.

## Credibility decision

For each candidate combine the deterministic score with the signals you observed:

- **`tier == "blocked"`** → never ingest.
- **score ≥ 0.60** → keep.
- **score in [0.45, 0.60)** → *escalate*: judge from the fetched content whether
  it's authoritative, factually grounded, and widely-recommended (named expert
  author, cites primary sources, official/maintained). Keep only if yes; record
  your one-line reason.
- **score < 0.45** → drop unless the user explicitly insists.

Record the final `score`, `tier`, and a one-line `rationale` in frontmatter. Never
ingest content you can't attribute to a real, identifiable source.

## Write

1. Get today's date: `date +%Y-%m-%d`.
2. Slugify the title to snake_case → `<dest>/web_<slug>.md` (`<dest>` = `sources/` by
   default, or `course/<slug>/library/` when `/curriculum` invoked this skill). If it
   exists, ask before overwriting.
3. Write following `.claude/Templates/web_source.md`:
   - `type: web_source`, `title`, `url`, `retrieved: <today>`.
   - `credibility:` block with `score`, `tier`, `rationale`.
   - `concepts_mentioned:` the key concepts the page covers (for retrieval/links).
   - `source_links:` the canonical URL.
   - `## Content`: the cleaned objective text (headings, lists, code, LaTeX
     preserved; nav/ads/boilerplate stripped). Faithful — no personal input, no
     invented facts; note any large omissions.

## Wrap up

Report: the file written, its credibility `score`/`tier`, concepts extracted, and
any candidates dropped (one-line reason each). If invoked directly, offer to run
`/collate <topic>` to fold this source into a paper/concept page.
