---
name: report-press
description: Research a subject and publish it as a one-page, newspaper-style HTML report with an animated Markdy diagram per section (state diagrams for things that change state, C4 container views for structure), every claim labelled with its source. The model writes a Markdown story; the report-press binary owns layout, branding, diagram sizing and the lint. Use when asked for "a report", "a one-pager for the team", "a recommendation we can share", "an HTML report with diagrams", "a newspaper-style write-up", "report-press", or to turn research into something peers can read. Not for PR evidence reports (use pr-proof) or plain Markdown docs.
---

# report-press

A report is a **story** (Markdown, reviewable in a PR) that the `report-press`
binary prints as one self-contained HTML page. You own the judgement: what the
report claims, what evidence backs each claim, which diagram shows it. The
binary owns everything mechanical: layout, typography, brand, inlining Markdy,
sizing figures so labels stay legible, and the checks.

Never hand-write the HTML. Every defect the binary fixes was hit by hand first.

## Install

```bash
cargo install --locked --path ~/.claude/skills/report-press/scripts    # or skills/report-press/scripts in this repo
report-press --version
```

The page prints in the Wolven Tech brand: a howling-wolf mark beside a text
wordmark (frontmatter `publisher:`, else "Wolven Tech") on newsprint, with a
monochrome night-forest palette (ink `#16191d`, accent `#5f6b76`, accent on dark
`#b8c0c8`, moon-gold highlight `#c9a95c`). For a house style, edit
`scripts/src/brand.rs` (logo SVG and colours) and reinstall.

## Workflow

### 1. Pin the question

One sentence: what the reader should know or decide after reading. Pick the
shape:

| Shape | Lead says | Back page |
|---|---|---|
| Recommendation | what to do, why these pieces | questions for the room, not checked |
| Explainer | how the thing works, in one sentence | open questions, not checked |
| Findings | what is wrong / what changed, with numbers | follow-ups, not checked |

### 2. Research, with sources

Fan out when the subject spans repos or the web: one subagent per independent
source (local code, web, a tracker). Ask each for facts **with paths, line
numbers and URLs**, and for what it could not confirm. A subagent's report is
testimony: re-read the claims your headline rests on yourself.

Every factual sentence gets a label, written `{{…}}`:

- `{{observed: \`path:line\`}}`: you read or ran it this session
- `{{subagent read}}` / `{{subagent: \`file:line\`}}`: a subagent read it, you did not
- `{{inferred from X}}`: your conclusion
- `{{not checked}}`: say so rather than state it

### 3. Shape the edition

- **Lead** (`#`): the finding or recommendation, the evidence, then a
  `> [!NOTE]` with the limit. One pull quote (`> …`) at most.
- **4–8 story sections** (`##`): one finding each. The headline **states the
  finding** ("A bead is agent work, blocked only by another bead"), never a
  label ("Beads").
- **Every lead and story section carries one figure.** Choose by what the
  section is about:
  - something **moves through states** (a request, a ticket, a review, a
    proposal) → `scene type=state`
  - **what talks to what** (repos, services, tools, people) → `scene
    type=architecture` with `group` boundaries: a C4 container view
- **Back page**: `{.back}` sections (questions, follow-ups) and **last** the
  `{.notchecked}` section. Always present.

Format: [references/format.md](references/format.md). Diagram grammar and the
limits measured against the vendored Markdy: [references/diagrams.md](references/diagrams.md).

### 4. Write the story

Path: `docs/reports/YYYY-MM-DD-<slug>.md`, or the repo's existing `docs/`
section if it has a better home. Start from [examples/explainer.md](examples/explainer.md).

Prose rules (the lint checks the mechanical ones):

- Lead with the finding, then evidence, then the limit. Numbers over adjectives.
- No escalation openers, no "X, not Y" foils, no "worth noting".
- At most 2 em dashes per 100 words.
- Never estimate in time. Use `[[rock]]` / `[[sand]]` / `[[water]]` plus what would move it up.

### 5. Check, then build

```bash
report-press check docs/reports/2026-10-28-subject.md
report-press build docs/reports/2026-10-28-subject.md      # writes the .html beside it
```

`check` exits 1 on errors and `build` refuses to write. Fix every error. For
each warning, fix it or decide to keep it. A "ranks" warning means the figure
will scroll sideways: merge states, split the figure, or keep it as a strip
because the sequence is the point.

### 6. Look at it

A build that exits 0 has not shown that a single figure draws. Open the page
and read the renderer's own counters:

```bash
agent-browser open file://$PWD/docs/reports/2026-10-28-subject.html
agent-browser wait 6000
agent-browser eval "JSON.stringify({warn:window.__markdyWarnings,fallbacks:document.querySelectorAll('.fallback').length,figs:document.querySelectorAll('figure[data-markdy]').length,drawn:[...document.querySelectorAll('.stage')].filter(s=>s.querySelector('svg')).length,overflow:document.documentElement.scrollWidth>innerWidth})"
```

Pass: `warn` is `[]`, `fallbacks` is 0, `drawn` equals `figs`, `overflow` is
false. Then repeat at phone width (`agent-browser set viewport 390 844`) and in
the other colour scheme (`agent-browser set media dark`), and screenshot and
read at least the lead and one wide figure. Close the browser when done.

### 7. Land it

Commit the `.md` and the `.html` together and add a row to the docs index
(`docs/README.md`) in the same commit. The `.md` is the source; rebuild the
`.html` whenever it changes.

## What the binary guarantees

- One file, no network: CSS, the renderer and Markdy 1.5.7 are inlined (about
  350 KB), so it opens from `file://` and in a mail attachment.
- Figures are sized from their own extent and never drawn below 0.75 scale;
  wider ones scroll inside their frame with a caption hint.
- Light and dark schemes; `prefers-reduced-motion` gets static SVG; skip link,
  visible focus, phone width.
- The brand (Wolven Tech mark and its palette) is compiled in. A story cannot
  change it; `brand_tests.rs` fails a build whose brand colours drop below
  WCAG AA where they carry text.
