---
name: writing-issues-and-prs
description: Write, edit, review, or improve concise titles, bodies, and comments for issues, pull requests, and merge requests on GitHub and GitLab, and for work items (tickets, stories, tasks, epics) on Jira, Linear, and similar issue and project trackers.
license: MIT
---

# Writing Issues and PRs

Whatever the platform, the writing carries the weight. Stay platform-neutral unless the user or surrounding context calls for platform-specific terms.

For starting structures by scenario (bug report, feature request, PR/MR, work item, review comment), read `references/outlines.md`. Those outlines are examples, not fixed templates: treat them as a starting point and shape the writing to the actual situation — reorder, drop, add, merge, or invent sections as the case demands. Prefer a repo's or tracker's own template whenever one exists.

## Writing principles

- Be concise: omit needless words, cut redundancy and hedging, and prefer plain, direct prose. Make every word count. If it does not fit on one screen, it is too long.
- Be accurate, well-structured, and insightful, in a calm, natural, and human tone. Be skeptical and precise — double-check reasoning, sources, and assumptions.
- State the issue, request, or purpose clearly. Explain why it matters. Include concrete evidence.
- For English prose, follow these style guides, and apply their language-agnostic rules to prose in any language: _The Elements of Style_, _The Sense of Style_, and _Chicago Manual of Style_.

## Formatting rules

- Insert spaces between English words and CJK characters.
- Use `- ` (hyphen plus space) for unordered list items; never use `* ` or `+ `.
- Use `_italics_` for italics and `**bold**` for bold.
- For list items, omit the trailing period when all items are fragments; if any item is a complete sentence, end every item with a period.
- Never use horizontal dividers (`<hr>` or `---`).

### Titles

- Issue and work item titles use "Sentence case" (capitalize the first word only).
- Pull request and merge request titles use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format, following the `git-commit` skill: `<type>[optional scope]: <description>`.

### Body headings

- Do not force the text to begin with a heading. Use headings only when they add structural clarity; a short opening sentence or paragraph can come first.
- Use heading levels sequentially (`h2`, then `h3`, etc.); never skip levels.
- Never use `h1`, and never number headings (e.g., `## About me`, not `## 1. About me`).
