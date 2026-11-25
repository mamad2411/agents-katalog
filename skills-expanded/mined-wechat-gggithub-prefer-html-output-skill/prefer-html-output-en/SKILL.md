---
name: prefer-html-output-en
description: When the agent is about to output long markdown (weekly reports, PR reviews, design comparisons, concept explainers, flowcharts, design systems and other deliverables meant for human reading), proactively evaluate whether to render it as HTML instead. Based on the 20 examples from ThariqS/html-effectiveness. Only proposes when a clear high-value scenario is detected; with user consent, generates the HTML file and opens it in the browser.
---

# prefer-html-output (English)

Help the agent render "long markdown intended for human reading" as HTML when the scenario benefits from it. Based on Anthropic Claude Code engineering lead Thariq Shihipar's [html-effectiveness](https://github.com/ThariqS/html-effectiveness) project — 20 real examples.

## When to trigger this skill (hybrid mode)

The agent runs the three layers in order before each reply. The user is only prompted when Layer 2 matches.

### Layer 1 · Hard exclusion (any match → silently use markdown)
- Output will be consumed by an automated pipeline (writing `.md` files, filling PR/issue descriptions, generating commit messages, writing logs, etc.)
- The user explicitly asked for markdown or plain text
- Short replies (~ < 20 lines) or conversational Q&A
- Main output is source code edits, command execution, or debug output

### Layer 2 · High-value scenario detection (only matches enter the proposal step)

Consult `references/scenario-map.md` to see whether the output intent matches one of these categories. The numbers in parentheses correspond to example files in `references/examples/`:

| Category | When it matches | Example IDs |
|---|---|---|
| Solution / design comparison | "compare 3 approaches", "several design directions", "A/B/C paths" | 01, 02 |
| Implementation plan | "implementation roadmap", "milestones + timeline", "risk table" | 16 |
| Code review output | "PR review report", "diff annotations", "per-file comments" | 03, 17 |
| Code understanding / architecture | "module dependencies", "unfamiliar package walkthrough" | 04 |
| Design system / component showcase | "color palette", "component states overview" | 05, 06 |
| Prototype / animation / interaction | "animation effect", "click flow", "interaction draft" | 07, 08 |
| Diagrams / flowcharts | "SVG diagram", "deployment flow", "decision tree" | 10, 13 |
| Presentation / report / explainer | "slide deck", "weekly report", "incident postmortem", "concept explainer", "feature explainer" | 09, 11, 12, 14, 15 |
| Ad-hoc editors (rare) | "triage board", "feature flag editor", "prompt tuner" | 18, 19, 20 |

### Layer 3 · Proposal phrasing

When Layer 2 matches, propose with this format:

> This content might work better as HTML (scenario: **{category}**, reference example **#{ID} {slug}**). Want me to generate the HTML and open it in your browser? (Reply "keep md" to stay on the original markdown plan.)

- User agrees → enter the generation flow
- User declines ("keep md" / "no" / negative) → use markdown as originally planned. Lower the proposal frequency for the same category in this session.

## Generation flow

1. **Learn the style first**: use the Read tool to open the matching example file `references/examples/NN-*.html`. Understand its layout, styling, and visualization logic.
2. **Generate the HTML**: use the Write tool to write the complete HTML (with `<!DOCTYPE html>`, inline CSS, inline JS where needed) to `/tmp/<slug>.html`.
   - Do not link external CSS/JS libraries (unless the source example itself uses a CDN).
   - Prefer semantic tags (section/article/figure).
   - Use a sensible font stack appropriate to the content language.
3. **Call render.sh**:
   ```bash
   bash ~/.claude/skills/prefer-html-output-en/scripts/render.sh /tmp/<slug>.html --scenario <key>
   ```
   `<key>` comes from the "Scenario keyword → ID quick lookup" table at the bottom of `references/scenario-map.md`.
4. **Reply to the user**: a one-sentence confirmation that includes the final path (read from the script's stdout) and that the browser has been opened.

## scenario key quick reference

See the table at the bottom of `references/scenario-map.md` for the full list. Commonly used:

- Weekly report → `weekly-report` (lands in `articles/YYYY-MM-DD/`)
- Incident postmortem → `incident-report` (lands in `articles/`)
- Concept explainer → `concept-explainer` (lands in `articles/`)
- Feature explainer → `feature-explainer` (lands in `articles/`)
- Slide deck → `slide-deck` (lands in `articles/`)
- Design comparison → `comparison` (lands in `temp/html-output/`)
- Implementation plan → `implementation-plan` (lands in `temp/`)
- PR review → `pr-review` (lands in `temp/`)
- Design system → `design-system` (lands in `temp/`)
- Flowchart → `flowchart` (lands in `temp/`)

If unsure, omit `--scenario` (defaults to `temp/html-output/`).

## render.sh parameters

```
bash scripts/render.sh <html_file> [--scenario <key>] [--no-open] [--long-term]
```

- `<html_file>`: required. Agent writes to `/tmp/` first.
- `--scenario <key>`: optional. Decides the destination folder.
- `--no-open`: optional, debug-only — skip launching the browser.
- `--long-term`: optional — force the file into `permanent/html/` (long-term storage).

Output: the final absolute path on stdout (single line).

All destination folders are created under the current working directory by default. The skill does not assume any project-specific layout.

## Cautions

- **Never generate HTML without explicit user consent.** This skill is propose → wait → execute by default.
- **Always read the matching example before generating.** This prevents stylistic drift and "HTML rendering" with poor results.
- **If the user declines, drop it.** Lower the proposal frequency for similar scenarios for the rest of the session.
- **Path decisions go through render.sh only.** Don't hand-roll `open` or `mv` — that bypasses the folder convention.
