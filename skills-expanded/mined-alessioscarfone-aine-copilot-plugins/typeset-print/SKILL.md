---
name: typeset-print
description: Typeset professional print documents by overlaying a DESIGN.md design system onto bundled print templates. Reads any DESIGN.md (auto-discovered in project root, provided by path, or pasted inline), maps its tokens to template CSS variables, then fills the chosen template with the user's content. Best for structured print documents (resume, one-pager, letter, long-doc, slides, equity report, changelog) where predictable layout matters more than pixel-perfect design-system fidelity. Supports Latin-script languages only (English, Italian, Spanish, French, German, Portuguese, Dutch, etc.). Does not support Chinese, Japanese, or Korean. Triggers on "typeset this document", "use a print template", "apply my DESIGN.md to a document template", "generate a styled document". Do not use for CJK output or dark/screen-only design systems (use typeset-free instead).
---

# typeset-print

Apply a DESIGN.md design system onto structured print templates. The templates handle print-safe layout; the DESIGN.md provides the visual identity.

Print templates are bundled with this skill at `assets/templates/*-en.html` (relative to this SKILL.md). Read the needed template file directly — do not modify it.

---

## Step 0 · Load the design system

Resolve the DESIGN.md using this priority chain — first match wins:

1. **Workspace auto-discovery** — silently check if a file named `DESIGN.md` (case-insensitive) exists in the root of the current project. If found, read it and continue. Emit one line: *"Using DESIGN.md found in project root."*
2. **User-provided path** — if the user attached a file with `@file` or typed a path, read that file.
3. **Inline paste** — if the user pasted DESIGN.md content directly in the message, use it as-is.
4. **Ask once** — if none of the above apply: *"No DESIGN.md found in the project root. Please attach the file or paste its content."* Do not proceed until one is provided.

After loading, extract the following mappings to override template CSS variables:

| DESIGN.md token | CSS variable | Fallback if absent |
|---|---|---|
| Page / background color | `--parchment` | `#f5f4ed` |
| Card / surface color | `--ivory` | `#faf9f5` |
| Primary accent / brand color | `--brand` | `#1B365D` |
| Primary text / foreground | `--near-black` | `#141413` |
| Secondary text / muted | `--dark-warm` | `#3d3d3a` |
| Tertiary / caption text | `--stone` | `#6b6a64` |
| Border / divider color | `--border` | `#e8e6dc` |
| Display / heading font stack | `--serif` | `Charter, Georgia, Palatino, serif` |
| Tag / badge background | `--tag-bg` | `#E4ECF5` |

### Compatibility check

Before proceeding, evaluate DESIGN.md Section 1 (Visual Theme & Atmosphere):

- If the design system describes a **dark background** (e.g. `#000`, `#111`, `#0d0d0d` as the page color), warn: *"This design system uses a dark background. The bundled templates are optimised for light print output. Consider using typeset-free for better fidelity."* Then ask the user whether to continue or switch.
- If the design system is explicitly **screen-only** (glassmorphism, neon, neumorphism, etc.), issue the same warning.
- If the user confirms to continue, apply the tokens as-is and note that print results may vary.

---

## Step 1 · Language gate

Detect the language of the user's content and request.

Accept: Latin-script languages — English, Italian, Spanish, French, German, Portuguese, Dutch, Polish, Romanian, and others using the Latin alphabet.

Reject: Chinese, Japanese, Korean, Arabic, Hebrew, Thai, and any script that requires non-Latin glyph rendering. If detected, reply:

> "This skill supports Latin-script languages only. For Chinese or Japanese documents, use a CJK-capable typesetting tool."

Then stop.

---

## Step 2 · Intent extraction (silent)

Verify these four dimensions before choosing a template. Do not ask unless two or more are genuinely unclear.

| Dimension | Extract | Example |
|---|---|---|
| Purpose | Why this document exists | Pitch / align team / apply for a role |
| Audience | Who reads it and what they know | Technical CTO vs. non-technical board |
| Constraint | Hard limits on length, format, delivery | "One page max", "print A4" |
| Success | What counts as done | They schedule a call / approve budget |

If two or more are unclear, ask in a single compact message. Never ask all four as a form.

---

## Step 3 · Document type

Route to a bundled print template:

| User says | Type | Template |
|---|---|---|
| "one-pager / exec summary / product brief / pitch" | One-Pager | `one-pager-en.html` |
| "white paper / report / technical doc / annual summary" | Long-Doc | `long-doc-en.html` |
| "letter / cover letter / memo / recommendation" | Letter | `letter-en.html` |
| "resume / CV / curriculum vitae" | Resume | `resume-en.html` |
| "slides / deck / presentation / pitch deck" | Slides | `slides-weasy-en.html` |
| "equity report / investment memo / valuation" | Equity Report | `equity-report-en.html` |
| "changelog / release notes / version log" | Changelog | `changelog-en.html` |

Read the chosen template from `assets/templates/<template-name>` (bundled alongside this SKILL.md).

### Diagrams (embed inside long-doc or slides)

When the document needs a chart or diagram, extract the `<svg>` block from the matching file in `assets/diagrams/` and embed it inside a `<figure>` in the document body.

| User says | Diagram file |
|---|---|
| architecture / system diagram / components | `assets/diagrams/architecture.html` |
| flowchart / decision flow / branching logic | `assets/diagrams/flowchart.html` |
| quadrant / 2×2 matrix / priority matrix | `assets/diagrams/quadrant.html` |
| bar chart / category comparison | `assets/diagrams/bar-chart.html` |
| line chart / trend / time series | `assets/diagrams/line-chart.html` |
| donut / pie / distribution | `assets/diagrams/donut-chart.html` |
| state machine / lifecycle / state diagram | `assets/diagrams/state-machine.html` |
| timeline / milestones / roadmap | `assets/diagrams/timeline.html` |
| swimlane / cross-team flow / cross-role process | `assets/diagrams/swimlane.html` |
| tree / hierarchy / org chart | `assets/diagrams/tree.html` |
| layer stack / OSI / layered architecture | `assets/diagrams/layer-stack.html` |
| venn / set overlap / intersection | `assets/diagrams/venn.html` |
| candlestick / OHLC / price history | `assets/diagrams/candlestick.html` |
| waterfall / revenue bridge / P&L bridge | `assets/diagrams/waterfall.html` |

Auto-select from data when content contains numerical data (first match wins): OHLC fields → candlestick; +/- contributions summing to total → waterfall; one series summing to ~100% ≤ 6 items → donut; two+ series across time → line; one series across time → bar; 2×2 positioning → quadrant; hierarchy depth ≥ 2 → tree; process with decision branches → flowchart.

Always wrap the extracted SVG in `<figure><figcaption>…</figcaption></figure>` with a caption that states the insight, not just the data range.

---

## Step 4 · Build the token override block

Produce a CSS block to prepend inside the template's existing `:root {}` declaration. Override only tokens extracted in Step 0 — leave everything else intact.

```css
/* DESIGN.md token overrides — injected by typeset-print */
:root {
  --parchment: /* from DESIGN.md */;
  --ivory: /* derived or fallback */;
  --brand: /* from DESIGN.md accent */;
  --near-black: /* from DESIGN.md foreground */;
  --dark-warm: /* from DESIGN.md secondary text */;
  --stone: /* from DESIGN.md muted */;
  --border: /* from DESIGN.md border */;
  --serif: /* from DESIGN.md display font stack */;
  --tag-bg: /* from DESIGN.md badge/tag bg, or derived */;
}
```

### rgba conversion

WeasyPrint does not render `rgba()` backgrounds correctly on tags and badges (double-rectangle rendering bug). If any DESIGN.md color value uses `rgba()`, convert it to an equivalent solid hex by blending on the page background before inserting into the override block. Document the conversion as a comment:

```css
--tag-bg: #E0F0FF; /* converted from rgba(0,120,255,0.12) on #ffffff */
```

### Typography mismatch handling

If the DESIGN.md font stack uses web fonts not available as system fonts, add a note to the layout intent (Step 4.5) and fall back to the nearest system serif. Do not add `@font-face` declarations unless the user provides font files.

---

## Step 4.5 · Layout intent note

Before filling the template, write a short note (under 60 words, prose) stating: template chosen, token overrides applied, any fallbacks or warnings, output format. Continue immediately — do not wait for approval.

Example:
> Layout intent: Resume (EN), bundled print template with Stripe design tokens — navy `#061b31` as brand, white surface, sohne-var mapped to Charter fallback (web font unavailable). One rgba conversion: tag-bg `rgba(83,58,253,0.1)` → `#EAE9FE`. Output: HTML + PDF.

---

## Step 5 · Content distillation

Auto-detect whether the input needs distilling. Do not ask.

| Skip distill | Run distill |
|---|---|
| Content already has section labels matching the template | Raw prose or brain dump |
| Metrics are quantified with units | Numbers scattered or implied |
| User wrote "use as-is" | Multi-source dump (email thread, chat, notes) |

When distilling, extract facts, map to template sections, gap-check, and ask once with a gap table.

---

## Step 6 · Fill the template

Apply changes to the template in this order:
1. Prepend the token override block from Step 4 immediately before the closing `}` of the existing `:root {}` block
2. Fill all `{{PLACEHOLDER}}` fields:

| Placeholder | Rule |
|---|---|
| `{{AUTHOR}}` | Resume/letter: person's name from content. All others: leave blank (build script infers) |
| `{{DOC_TITLE}}` / `{{LETTER_SUBJECT}}` | Infer from H1 or main title |
| `{{DESCRIPTION}}` | One sentence ≤ 150 chars from the first paragraph |
| `{{KEYWORDS}}` | 3–5 keywords from title + section headings, comma-separated |

3. Fill body content — data over adjectives, no padding, no invented metrics
4. Verify no `{{...}}` remain — if any do, replace with `[DATA NEEDED: field name]`

---

## Step 7 · Build and verify

Run the build script from `src/design/scripts/build.mjs` (relative to this skill's plugin root):

```bash
node scripts/build.mjs --html output.html          # placeholder + structure check
node scripts/build.mjs --pdf output.html           # WeasyPrint → output.pdf
node scripts/build.mjs --check output.html         # palette anti-pattern scan
```

If WeasyPrint is not installed, provide the browser-print fallback instruction (Chrome → File → Print → Save as PDF, background graphics on, margins None).

Report the result. If any check fails, self-correct and re-run before handing off.
