---
name: shakespeare-writing-studio
description: Produce publish-ready Chinese and English writing packages across WeChat articles, Medium/Substack essays, research notes, founder memos, op-eds, speeches, data storytelling, statistical graphics, and platform-ready HTML. Use this unified workflow for writing, rewriting, sourcing, lowering AI feel, creating visuals, and packaging final articles for Claude Code, Claude CLI, Codex CLI, and local agents.
---

# Shakespeare Writing Studio

This workflow turns a rough idea, draft, notes, transcript, outline, or research question into a publish-ready writing package.

Treat Chinese and English work as modules inside one editorial system. Select modules by platform, language, article type, and visual need.

## Main Deliverables

- `final.md`: publish-ready article, essay, memo, speech, or research note.
- platform HTML: `wechat-ready.html`, `medium-ready.html`, or clean web preview.
- visuals: `assets/*.svg`, `charts/*.svg`, cover, mechanism diagram, source-backed chart, statistical atlas, timeline, map, or data card.
- `publishing-note.md`: title options, subtitle/deck, social copy, source cautions, visual notes, AI-feel cleanup notes.

## 0. Select Modules

Always read the relevant modules before writing.

For every task:

- `references/source-quality.md` before any background search.
- `references/human-voice.md` before rewriting.
- `references/editorial-lessons.md` before drafting, titling, or designing visuals.
- `references/visual-production.md` before any cover, chart, diagram, or image.
- `references/editorial-qa.md` before delivery.

For Chinese WeChat:

- `references/wechat/chinese-finance-tech-writing.md`
- `references/wechat/wechat-layout-patterns.md`
- `references/wechat/layout-wechat.md`

For English long-form:

- `references/medium-writing-patterns.md`
- `references/platform-formats.md`

For research and data:

- `references/research-data.md`
- `references/data-visuals.md`

For final release:

- `references/release-gate.md`

## 1. Build The Spine

Extract:

- target language and platform
- intended reader
- core claim
- arguable stance
- title direction and search terms
- facts, dates, names, numbers
- source needs
- examples and scenes
- visual opportunities
- phrases that sound AI-generated

Before drafting, write the stance in one sentence. If it reads like "this trend is important," "值得关注," or "there are opportunities and challenges," rebuild the argument before polishing.

If the user gives a sharper title direction, preserve its tension and keywords. Do not smooth it into a safer generic title.

## 2. Choose The Format

Pick one primary format:

- Chinese WeChat finance / technology article
- English Medium / Substack essay
- research-backed article
- data-led report
- founder/operator note
- executive memo
- op-ed
- speech or keynote draft
- product / technology essay
- narrative argument

The format controls the opening, section rhythm, evidence density, visual density, and ending.

## 3. Research With Source Discipline

Use research only when it materially improves the piece.

Allowed:

- primary sources
- official announcements
- public filings
- reputable named reporting
- official datasets
- research institutions

Rejected:

- generic SEO pages
- unsourced blogs
- random statistics
- repost farms
- AI summaries

Every number used in the article or visual must have a source and date.

## 4. Write And Rewrite

Rules:

- Open with something concrete.
- Keep one central spine.
- Let paragraphs vary in length.
- Prefer concrete verbs over abstract nouns.
- Use examples before broad claims.
- Keep the writer's point of view visible.
- Remove generic AI scaffolding.
- Do not overbalance the argument into bland neutrality.
- Do not invent strategic frames that the sources and article do not support.

## 5. Visuals And Charts

Visuals are shared across Chinese and English work. Statistical graphics, covers, timelines, mechanism diagrams, and source-backed charts are available to both.

Before making a visual:

1. Write the visual job in one sentence.
2. Choose a direction from article content.
3. Pick the visual type.
4. Sketch 3–5 nodes, numbers, or cards.
5. Build the SVG/HTML.
6. Check readability at mobile width.

Hard rule: do not default to dark background. Dark visuals are allowed only when the article's subject, tone, and metaphor justify them.

For research-led articles, consider one hero statistical graphic when the reader needs to see a system rather than one metric.

Cover rule: the cover must be understood in 3 seconds on a phone. Avoid literal mountain / flag / summit graphics, generic route maps, cheap arrows, and abstract node diagrams unless the article itself demands that metaphor.

## 6. Platform Packaging

Produce:

- primary title
- alternate titles
- subtitle/deck
- platform-specific preview description
- social teaser
- suggested tags or WeChat summary
- source table if research was used
- visual list and source notes

## 7. QA

The piece is not done until:

- the stance is clear
- the opening earns attention
- each section advances the argument
- no unsupported claims remain
- no paragraph feels like generic AI filler
- data sources are listed when used
- visuals match the article direction
- charts clarify the argument
- cover does not lower the article's perceived quality
- platform preview reads well on mobile
- the ending lands with a thought, not a summary

## Hard Rules

1. Do not invent facts, quotes, numbers, sources, or personal experiences.
2. Mark missing specifics as `[TK]` or `◻◻`.
3. Background search must use top-tier sources only.
4. Remove obvious AI sentence scaffolds.
5. Never use visuals as decoration.
6. Never default to one visual style across projects.
7. Never use unsupported architecture/product language to make the article sound deeper.
8. If AI assistance materially shaped the article and the target platform requires disclosure, note it in `publishing-note.md`.
