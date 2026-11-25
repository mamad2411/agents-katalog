---
name: html-report
description: Use whenever the result of a task is a research, analysis, comparison, plan, roadmap, audit, strategy, recommendation or any multi-section deliverable meant to be read, in an agent that has no Claude Artifacts (Codex, Cursor, Gemini CLI, Copilot, Windsurf, Cline, OpenCode, Aider, local models). Writes one polished, self-contained HTML file (tables, charts, timelines, navigation, both themes) into the project and, on revisions of the same topic, edits that same file. In Claude with Artifacts, use rich-report instead.
---

# HTML report: deliverables as one self-contained page

The same house style and structure as `rich-report`, delivered as a local `.html` file that opens in any browser and can be sent as an attachment. No hosting, no account, no build step.

## When to apply

Research results, comparisons, plans and roadmaps, audits, strategies, recommendations, any report with 3+ sections or a data table. Short answers, explanations, code changes and command output stay in chat.

If the agent cannot write files (a chat app), give the same structure as clean Markdown in the reply instead.

## One file per topic

1. Save to `reports/<topic-slug>.html` in the current project (create `reports/`). Name the file after the topic and keep the name.
2. A follow-up on the same topic ("add", "recalculate", "shorter", changed inputs) edits that file; it never creates a second one. Refresh every place the change affects and keep a short "What changed" block near the top (date plus 2-4 bullets, latest few only).
3. A genuinely different topic gets a new file. If unsure, ask in one line.

## Build

1. Start from `skeleton.html` in this folder. Keep its tokens, fonts, radii, spacing and component CSS; replace the sample content; delete components the content does not need. Keep the two `impeccable-disable` comments at the top of `<style>` (they silence false contrast and padding findings from the Impeccable hook), and give any new bordered component at least 12px of padding.
2. Unlike an Artifact, the file is a whole document: wrap the skeleton in `<!doctype html><html lang="…"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">…</head><body>…</body></html>`, with `<title>` and `<style>` in the head.
3. Everything inline: CSS, JS, SVG icons, data. Google Fonts is the only external request; the font stacks fall back to system fonts offline. If a chart library is truly needed, load one pinned version from a CDN and say the chart needs internet.
4. Both themes through `prefers-color-scheme`; works at 400px wide with no horizontal page scroll; tables scroll inside their own container.
5. Open it once if the agent can (`start`, `open` or `xdg-open` with the file path), fix what is visibly broken, then stop.
6. In chat: the file path plus 2-3 lines (main conclusion, where to look first). Do not paste the report into chat.

## House style, anatomy and content rules

Identical to `rich-report`: Linear-inspired neutral surfaces with one lavender-blue accent (`#5e6ad2`, `#828fff` as text on dark), Onest at 400/500/600, JetBrains Mono for IDs and dates, hairline borders, no shadows, gradients or emoji markers; header, 3-4 takeaway cards, contents rail, sections that open with their conclusion; real tables, charts drawn to scale, timelines, risks with severity pills, `<details>` for long reasoning. If `rich-report` is installed next to this skill, read its SKILL.md for the full component table; otherwise the skeleton shows every component.

## Truthfulness

Numbers, quotes and sources come from the actual work. Never invent data to fill a chart. Mark estimates and low-confidence items visibly.

## Checklist

- [ ] Same-topic revision edited the same file
- [ ] Answer visible without scrolling; takeaways match the body
- [ ] Opens offline with no console errors; both themes readable; fine at phone width
