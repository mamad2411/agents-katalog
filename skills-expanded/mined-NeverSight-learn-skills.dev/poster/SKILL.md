---
name: poster
description: Use when the user needs an academic poster, conference poster, poster-style visual summary, section planning, figure-text balance, or poster packaging workflow.
---
# Academic Poster Workflow

Create a poster-ready content package without duplicating the full workflows of the other writing skills.

## Purpose

This skill is for **poster-specific organization**:
- define the poster's audience and message
- decide what belongs on the poster and what must be omitted
- convert literature or manuscript content into poster sections
- route figure/layout work to `/draw` and `/document`

Do not treat a poster like a shortened paper. A poster is a **visual argument** with a small number of high-priority claims.

## When To Use

Use this skill when the user wants:
- a conference poster
- a poster-style literature summary
- a visual one-page research overview
- help deciding poster sections, text density, and figure priorities

If the user mainly wants:
- a slide deck: route to `/document`
- a long written report: route to `/technical-report`
- a paper section: route to `/paper-writing`

## Workflow

### 1. Clarify Poster Context

Identify:
- target venue or audience
- poster goal: present a study, summarize a topic, or pitch a direction
- expected size or format if the user knows it
- available materials: workspace papers, manuscript draft, figures, data

### 2. Choose The Content Source

Use one main upstream workflow:

| Situation | Route |
|-----------|-------|
| Poster summarizes a research field | `/literature-review` |
| Poster presents a user's own paper or method | `/paper-writing` |
| Poster motivates a new topic or open problem | `/research-gap` |

### 3. Build A Poster Skeleton

Default sections:
1. Title + one-sentence claim
2. Background / problem
3. Method or comparison frame
4. Key evidence or findings
5. Main takeaway
6. References / contact / QR block if needed

Keep these rules:
- one central claim, not many equal claims
- prefer figures, tables, and short bullets over dense prose
- each section should answer one question only
- remove any paragraph that needs sustained close reading

### 4. Route Assets And Packaging

- Use `/draw` when the poster needs diagrams, cleaned figures, timelines, or concept maps.
- Use `/document` when the result should be packaged into a practical file such as `PPTX` or another layout-friendly deliverable.
- If the user explicitly needs a print-ready poster size, keep the poster structure here, then use `/document` to implement the layout.

## Output Pattern

Recommended outputs inside `workspace/<name>/`:
- `poster-outline.md`
- `poster-copy.md`
- `poster-assets/`
- packaged deliverable from `/document`

## Principles

- **Poster first**: optimize for scanability, not completeness.
- **Visual priority**: text exists to support figures and claims.
- **Claim discipline**: every block must support the poster's main message.
- **Honest scope**: current first-class packaging is via `/document`; do not imply a dedicated poster renderer if none exists.

## Example

用户说："帮我把这个工作区做成一个 conference poster"
→ 用本 skill确定 poster 骨架和主张，再转 `/paper-writing` 或 `/literature-review` 生成文案，必要时接 `/draw` 和 `/document`
