---
name: visual-explainer
description: >
  Visual explainer: self-contained HTML for architectures, diffs, plans, slides,
  tables, and recaps. Default home .scratch/visuals/; tracked docs/visuals/ when
  the ask is for team/group/commit/docs. Use when the user asks for a diagram,
  architecture overview, visual plan, slide deck, diff review, plan review,
  project recap, fact-check, comparison table, help choosing a visual, or any
  visual explanation; or when about to dump a complex ASCII table (4+ rows or
  3+ columns).
---

# visual-explainer

Turn visual or tabular intent into one **self-contained HTML** file and open it.
Prefer HTML over ASCII murals when this skill is loaded.

## Workflow

### 1. Resolve mode

Pick **one** mode (or explicit manual name).

| Mode | Manual name | Clear signals (run — do not ask) |
|------|-------------|----------------------------------|
| Diagram | `generate-web-diagram` | diagram, architecture, arch diag, flowchart, explain visually |
| Visual plan | `generate-visual-plan` | implementation plan as visuals, “I need a plan…”, feature plan HTML |
| Slides | `generate-slides` | slide deck, presentation, magazine-quality slides |
| Diff review | `diff-review` | review this diff, “see the diff”, visual diff, architecture before/after |
| Plan review | `plan-review` | compare plan to codebase, plan risk |
| Project recap | `project-recap` | mental model, catch me up, context switch back |
| Fact-check | `fact-check` | verify doc against code, fact-check this HTML/MD |
| Complex table | *(diagram/table)* | about to print 4+ row or 3+ col ASCII table → HTML instead |

**Visual plan** ≠ **plan review**: new/feature plan → visual plan; plan vs code or plan risk → plan review.

Several modes fit → prefer the **narrower** review/plan/slides mode over a generic diagram. `--slides` on a scrollable topic → slides mode for that topic.

Unclear mode, or user asks for help before creating → suggest **once** (recommended + 1–2 alternates) and wait. Do **not** ask when a clear signal or manual name is present.

**Done when:** mode is named (or one suggest-and-wait is in flight).

### 2. Resolve home

| Home | When |
|------|------|
| `.scratch/visuals/` | Default — private, draft, or no durable cue |
| `docs/visuals/` | Durable/public cues — [references/homes.md](references/homes.md) |

Soft uncertainty (“maybe later”) → `.scratch/visuals/` without asking. Ask placement **only** when the user wants help choosing a home. Companion `.md` (if any) uses the **same** home.

**Done when:** write root is named.

### 3. Load mode refs

Read only what this mode needs:

| Mode | Read |
|------|------|
| Diagram / complex table | [references/generate-web-diagram.md](references/generate-web-diagram.md) + template below |
| Visual plan | [references/generate-visual-plan.md](references/generate-visual-plan.md) |
| Slides | [references/generate-slides.md](references/generate-slides.md) (pulls authoring, visual patterns, deck shell) |
| Diff review | [references/diff-review.md](references/diff-review.md) |
| Plan review | [references/plan-review.md](references/plan-review.md) |
| Project recap | [references/project-recap.md](references/project-recap.md) |
| Fact-check | [references/fact-check.md](references/fact-check.md) |

**Templates** (non-slides, pick by content):

- Text-heavy architecture → [references/architecture.html](references/architecture.html)
- Mermaid flows / sequence / ER / state → [references/mermaid-flowchart.html](references/mermaid-flowchart.html) + [references/libraries.md](references/libraries.md)
- Tables / matrices → [references/data-table.html](references/data-table.html)
- CSS / overflow / connectors → [references/css-patterns.md](references/css-patterns.md)
- 4+ major sections → [references/responsive-nav.md](references/responsive-nav.md)
- Named palette or theme picker → [references/themes.md](references/themes.md)

**Defaults:** Mermaid for topology/flows; CSS Grid for text-heavy architecture; `<table>` for data; Chart.js for dashboards. Slides follow generate-slides (frozen shell + action-title outline).

**Done when:** required refs for this mode are loaded.

### 4. Design, then write HTML

Commit audience, diagram type, and aesthetic before coding (vary; no Inter / purple-on-white cliché). Follow mode-required sections. One complete self-contained HTML document (inline CSS; CDN ok for Mermaid / Chart.js / fonts).

**Done when:** HTML content is ready to write.

### 5. Deliver under the resolved home

1. Ensure the home exists.
2. Write `*.html` with a descriptive kebab-case name.
3. Companion `<same-basename>.md` **only** when the user asks for an AI-readable equivalent; HTML is visual SoT; ask before replacing an existing companion.
4. Open in the browser when allowed; otherwise report the `file://` path.
5. Chat: short summary + path(s). Do not paste the full HTML.
6. **Slides:** `python3 skills/visual-explainer/scripts/check_slides.py <deck.html>` exits 0 before claiming done.

**Done when:** HTML is on disk under the home, browser opened or path reported, companion rules honored, and slides checker green when mode is slides.

## Boundaries

- Do not write ASCII/box-drawing as the primary artifact when this skill is loaded.
- Do not write under `/pm/` or agent install dirs; homes are `.scratch/visuals/` or `docs/visuals/` only.
- Do not treat a companion `.md` as the HTML source.
- Do not ask mode when the ask already names slides / diff / plan-review / etc.
- Do not rewrite the slides **deck shell** engine; do not ship a slides deck with a failing `check_slides.py`.
- Do not invent PPTX export.
