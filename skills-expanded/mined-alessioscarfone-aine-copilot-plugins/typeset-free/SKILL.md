---
name: typeset-free
description: Generate a self-contained HTML document styled entirely from a DESIGN.md file — no pre-built templates. Reads any DESIGN.md (auto-discovered in project root, provided by path, or pasted inline) and produces a pixel-faithful one-pager, resume, letter, long-doc, or slide deck in HTML + PDF. Supports Latin-script languages only (English, Italian, Spanish, French, German, Portuguese, Dutch, Polish, etc.). Does not support Chinese, Japanese, Korean, or other CJK scripts — use Kami for those. Triggers on "typeset this", "design a document", "make a one-pager with my design system", "use my DESIGN.md", "generate a styled doc", "turn this into a PDF using my design". Do not use for coding tasks, CJK output, or when no design system is available.
---

# typeset-free

Generate a fully styled, self-contained HTML document from a DESIGN.md design system. All CSS is produced inline from the design tokens — no external stylesheets, no pre-built templates.

---

## Step 0 · Load the design system

Resolve the DESIGN.md using this priority chain — first match wins:

1. **Workspace auto-discovery** — silently check if a file named `DESIGN.md` (case-insensitive) exists in the root of the current project. If found, read it and continue. Emit one line: *"Using DESIGN.md found in project root."*
2. **User-provided path** — if the user attached a file with `@file` or typed a path, read that file.
3. **Inline paste** — if the user pasted DESIGN.md content directly in the message, use it as-is.
4. **Ask once** — if none of the above apply: *"No DESIGN.md found in the project root. Please attach the file or paste its content."* Do not proceed until one is provided.

After loading, parse these sections (all optional — use defaults when missing):

| Section | Key output |
|---|---|
| Visual Theme & Atmosphere | Design intent note (used to guide layout decisions) |
| Color Palette & Roles | `--bg`, `--fg`, `--accent`, `--muted`, `--surface`, `--border` |
| Typography Rules | `--font-display`, `--font-body`, `--font-mono`, type scale |
| Component Stylings | Button, card, badge, input, nav patterns |
| Layout Principles | Max-width, grid, spacing unit, section rhythm |
| Depth & Elevation | Shadow levels |
| Do's and Don'ts | Anti-pattern list (referenced during generation) |
| Responsive Behavior | Breakpoints and collapsing rules |
| Agent Prompt Guide | Compositional hints — read this section to drive layout decisions |

If a section is absent, fall back to safe defaults (white background, system-ui sans-serif, 8px base unit, no shadows).

---

## Step 1 · Language gate

Detect the language of the user's content and request.

Accept: Latin-script languages — English, Italian, Spanish, French, German, Portuguese, Dutch, Polish, Romanian, and others using the Latin alphabet.

Reject: Chinese, Japanese, Korean, Arabic, Hebrew, Thai, and any script that requires non-Latin glyph rendering. If detected, reply:

> "This skill supports Latin-script languages only. For Chinese or Japanese documents, use the Kami skill."

Then stop.

---

## Step 2 · Intent extraction (silent)

Before choosing a document type, verify these four dimensions. Do not ask unless two or more are genuinely unclear.

| Dimension | Extract | Example |
|---|---|---|
| Purpose | Why this document exists | Pitch to investor / align team / apply for a role |
| Audience | Who reads it and what they know | Technical CTO vs. non-technical board |
| Constraint | Hard limits on length, format, delivery | "One page max", "print A4", "web page" |
| Success | What outcome counts as done | They schedule a call / approve budget / understand the architecture |

If two or more are unclear, ask in a single compact message. Never ask all four as a form.

---

## Step 3 · Document type

Route to one of five document types:

| User says | Type | Page target |
|---|---|---|
| "one-pager / executive summary / product brief / pitch" | **One-pager** | 1 page |
| "white paper / report / technical doc / annual summary" | **Long-doc** | 4–8 pages |
| "letter / cover letter / memo / recommendation" | **Letter** | 1 page |
| "resume / CV / curriculum vitae" | **Resume** | 1–2 pages |
| "slides / deck / presentation / pitch deck" | **Slides** | 8–20 slides |

If unsure, ask one question: *"Is this a one-pager, resume, letter, report, or slide deck?"*

---

## Step 4 · Content distillation

Auto-detect whether the input needs distilling. Do not ask.

| Skip distill | Run distill |
|---|---|
| Content already has section labels matching the document type | Raw prose or brain dump without structure |
| Metrics are quantified with units | Numbers scattered or implied |
| User wrote "use as-is" | Multi-source dump (email thread, chat, notes) |
| Content count matches the document type slots | Too many or too few items for the chosen type |

When distilling:
1. Extract every fact, number, date, name, and action item
2. Map each to the target document's sections (see Step 5 layout rules)
3. Gap-check: list what the document needs but the content does not provide
4. Ask once with a gap table — do not guess to fill gaps

---

## Step 5 · Generate HTML

Produce a single `.html` file with all CSS inline in one `<style>` block. Never link external stylesheets or scripts.

### CSS custom properties block

Open the `<style>` block with a `:root {}` declaration. Map every parsed DESIGN.md token to a custom property. Minimum required set:

```css
:root {
  /* Colors — from DESIGN.md "Color Palette & Roles" */
  --bg: /* page background */;
  --fg: /* primary text */;
  --accent: /* primary CTA / link / highlight */;
  --muted: /* secondary text / captions */;
  --surface: /* card / container background */;
  --border: /* default border color */;

  /* Typography — from DESIGN.md "Typography Rules" */
  --font-display: /* display/heading font stack */;
  --font-body: /* body font stack */;
  --font-mono: /* monospace stack, or same as body if absent */;

  /* Spacing — from DESIGN.md "Layout Principles" */
  --unit: /* base unit, e.g. 8px */;

  /* Elevation — from DESIGN.md "Depth & Elevation" */
  --shadow-sm: /* subtle lift shadow */;
  --shadow-md: /* standard card shadow */;
}
```

Derive all spacing, font sizes, and component styles from these properties — never hard-code values that belong in the token set.

### Layout rules by document type

**One-pager**: Single `<main>` with a header block (title, eyebrow, meta), one metrics/highlights row, two to three content sections, and an optional footer. Max-width from DESIGN.md layout. `@page { size: A4; }` for print.

**Resume**: Header (name, contact), two columns (experience + skills/education sidebar) or single column if the design system has no two-column component pattern. Bullet items use `Action + Scope + Result` structure. `@page { size: A4; }`.

**Letter**: Date, sender block, recipient block, salutation, body paragraphs, closing, signature line. One column, generous line-height from DESIGN.md. `@page { size: A4; }`.

**Long-doc**: Cover or title block, table of contents (if > 3 sections), numbered sections with `<h2>` headers, supporting data (tables or inline charts described as SVG if needed), conclusion. `@page { size: A4; }`.

**Slides**: Each slide is a `<section class="slide">` inside a `<div class="deck">`. Page size from DESIGN.md or default `280mm 158mm` (landscape). Slide anatomy: eyebrow (section tag), headline assertion, evidence body (2–4 bullets or one visual), optional pinned conclusion. `@page { size: 280mm 158mm landscape; }`.

### Anti-patterns (from DESIGN.md "Do's and Don'ts")

Before emitting the file, check the parsed Don'ts list against the generated CSS. Flag and self-correct any violation. Common cross-design violations:

- Do not use font weights or colors not declared in the DESIGN.md palette
- Do not use `!important` unless overriding a browser UA reset
- Do not leave `{{placeholder}}` text in the final output
- Do not invent metrics or data — use `[DATA NEEDED: description]` if content is absent

### Section 9 guidance

Read the "Agent Prompt Guide" section of the DESIGN.md last, immediately before writing the HTML body. Use its component prompts verbatim as the compositional blueprint for the main content areas.

---

## Step 6 · Export

Emit the completed HTML file.

For PDF export, provide the WeasyPrint command:

```bash
weasyprint output.html output.pdf
```

Or, if WeasyPrint is not installed, instruct the user to open the HTML in Chrome and use **File → Print → Save as PDF** with margins set to None and background graphics enabled.

For PNG (sharing), provide:

```bash
weasyprint output.html output.pdf && pdftoppm -r 150 -png output.pdf output-page
```

Do not ask which format — emit HTML always. Offer PDF and PNG instructions as a follow-up note.
