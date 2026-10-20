---
name: learning-dashboard
description: Create polished, self-contained, ADHD-friendly HTML learning dashboards for dense technical content, codebases, AWS/DevOps topics, architecture, articles, reports, research, and long notes. Trigger when the user asks for a learning dashboard, midnight dashboard, ADHD visual explainer, deep visual HTML, multi-tab explainer, concept map, workflow/process flow, decision guide, recap quiz, or wants the same information explained through multiple visual formats. Prefer low-context offline HTML: dark theme, sticky navigation, tabs, cards, timelines, collapsible deep dives, quizzes, and minimal prose.
---

# Learning Dashboard

## Core behavior
Create a reusable visual learning surface, not a plain article. Convert dense information into a self-contained HTML dashboard that works offline and is easy to scan.

Default style: **Midnight Learning Dashboard**.

Default output: one `.html` file unless the user asks for a folder or course.

## First decide the output mode
- **Single dashboard**: default for articles, concepts, code, announcements, and medium topics.
- **Multi-page dashboard**: only for large codebases, courses, multi-module learning, or user request.
- **Compact dashboard**: use when the user asks for quick/short output.

## Required learning loop
Every full dashboard should show the same knowledge in several formats:
1. **Scan**: hero, 30-second view, chips, scorecards.
2. **Orient**: concept map, mental model, components, relationships.
3. **Move**: workflow, process flow, state flow, sequence, or timeline.
4. **Compare**: narrow table, cards, decision matrix, before/after.
5. **Apply**: practical examples, code path, AWS/DevOps use, checklist.
6. **Warn**: risks, traps, unknowns, failure modes.
7. **Remember**: recap quiz, memory hooks, flashcards.

## Dashboard sections
Use these sections when content permits:
- Sticky top navigation with short jump links.
- Hero with thesis, topic chips, and start buttons.
- 30-second view with 4-6 tiny cards.
- Tabs such as Overview, Engineer View, Deep Dive, Examples, Quiz.
- Snapshot cards for the most important points.
- Concept map or model map.
- Workflow/process flow.
- Decision guide using green/yellow/red framing.
- Comparison block; keep tables narrow.
- Timeline if dates/phases/releases exist.
- Collapsible `<details>` blocks for dense text.
- Recap quiz with reveal answers.
- Sources and assumptions when research/current facts are used.

## Use references only when needed
- For visual rules, read `references/design.md`.
- For component choices, read `references/component-library.md`.
- For output size and mode, read `references/output-modes.md`.
- For AWS/DevOps/codebase dashboards, read `references/devops-aws.md`.
- For quality checks, read `references/quality-gate.md`.
- For a ready skeleton, use `assets/midnight-dashboard-template.html`.

## Implementation rules
- Produce valid `<!doctype html>` HTML.
- Keep CSS and minimal JavaScript inline.
- Do not depend on external fonts, CDNs, remote images, Mermaid runtime, or Chart.js by default.
- Use responsive CSS. Desktop grids must collapse to one column on mobile.
- Include print CSS.
- Use semantic section IDs matching nav links.
- Use vanilla JS only for tabs and reveal quiz.
- Prefer styled HTML/SVG blocks over heavy libraries.
- If Mermaid is useful, include Mermaid source in a collapsible block and provide an HTML fallback diagram.

## ADHD rules
- Put the key answer above the fold.
- Use short paragraphs, strong headings, and visual anchors.
- Hide deep details until clicked.
- Repeat important concepts through map, flow, example, risk, and quiz.
- Avoid long tables. Put prose in cards.
- Add a "what to remember" section.

## File naming
Use lowercase, descriptive names:
- `learning_dashboard_<topic>.html`
- `midnight_learning_dashboard_<topic>.html`
- `index.html` for folders

## Quality gate
Before final response, verify:
- The user can understand the topic by scanning nav, headings, cards, and diagrams.
- The key decision is visible in under 30 seconds.
- Dense text is hidden behind tabs/details.
- The dashboard shows the topic in at least 3 visual forms.
- The HTML works offline and on mobile.
- The final chat reply is short and points to the output file.

## Final response
Return only:
- Output path/link.
- Best section to start with.
- Any major limitation or assumption.
