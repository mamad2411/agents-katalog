---
name: pptx
description: Use this skill for any work on .pptx files — create, read, edit, extract speaker notes/comments, manipulate layouts and master slides, combine or split decks, work with templates. Trigger when the user mentions a .pptx filename, "PowerPoint", "Keynote-compatible deck", or asks for a slide deliverable that must open in PowerPoint / Keynote / Google Slides. Use for board decks, investor decks for security companies, customer presentations, technical architecture decks, and bilingual (ES/EN) content. Defer to ckmslides when the user wants an HTML web presentation; defer to create-deck / sales:create-an-asset when the user wants a deal-context-driven sales deck (those skills coordinate with this one when .pptx output is required).
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Scope and Sibling Boundaries

Use this skill for the **mechanics of .pptx files**. Defer or coordinate when the deliverable or context shifts:

| If the user wants... | Use |
|---|---|
| .pptx file (open in PowerPoint/Keynote/Google Slides) | **this skill** |
| HTML web presentation, scrollytelling, web-embedded slides | `anthropic-skills:ckmslides` |
| Sales/investor deck driven by deal context, prospect research, CRM signals | `sales:create-an-asset` (which calls this skill if .pptx is the chosen output) |
| Strategic deck with brand/design system | `anthropic-skills:ckmdesign` / `anthropic-skills:ckmslides` for HTML; **this skill** if the deliverable must be .pptx |
| Word doc | `docx` |
| PDF | `pdf` (this skill exports .pptx → PDF on request) |
| Convert .pptx → PDF | **this skill** (use `soffice --headless --convert-to pdf`) |

When a request is ambiguous between .pptx and HTML ("make me a deck about X"), default to **this skill** if the user mentions PowerPoint, Keynote, Google Slides, "I'll edit it later", "send to the board", or attaches a .pptx template; default to `anthropic-skills:ckmslides` if they say "web", "shareable link", "embed", or "scroll".

When `sales:create-an-asset` or `create-deck` decides .pptx is the right format, this skill handles the file production.

---

## Quick Reference

| Task | Approach |
|---|---|
| Read / extract text | `python -m markitdown deck.pptx` |
| Extract speaker notes | `python-pptx` `slide.notes_slide.notes_text_frame.text` |
| Extract comments | unpack OOXML → `ppt/comments/comment*.xml` |
| Visual overview | `python scripts/thumbnail.py deck.pptx` |
| Edit existing deck (preserve formatting) | `python-pptx` against the file directly — see **Editing** |
| Create from template | unpack → manipulate slides → repack — see [editing.md](editing.md) |
| Create from scratch | `pptxgenjs` (Node) — see [pptxgenjs.md](pptxgenjs.md) |
| Bulk find/replace across slides | `python-pptx` iterate `text_frame.runs` |
| Add/edit speaker notes | `python-pptx` `notes_slide.notes_text_frame.text = "..."` |
| Combine decks | unpack both → copy slide XML + rels → repack |
| Split deck | `python-pptx` copy selected slides into new pres |
| Convert to PDF | `soffice --headless --convert-to pdf deck.pptx` |
| Convert to images for QA | `pdftoppm -jpeg -r 150 deck.pdf slide` |

---

## Reading

```bash
# Text-only extraction
python -m markitdown presentation.pptx

# Visual grid of all slides
python scripts/thumbnail.py presentation.pptx

# Raw XML (when you need full fidelity — animations, masters, theme)
python scripts/office/unpack.py presentation.pptx unpacked/
```

### Speaker notes (often where the real content lives)

```python
from pptx import Presentation
prs = Presentation("deck.pptx")
for i, slide in enumerate(prs.slides, 1):
    if slide.has_notes_slide:
        notes = slide.notes_slide.notes_text_frame.text
        if notes.strip():
            print(f"--- Slide {i} ---\n{notes}\n")
```

### Comments

Comments live in `ppt/comments/comment*.xml` after unpack. For programmatic access:
```bash
python scripts/office/unpack.py deck.pptx tmp/
ls tmp/ppt/comments/
```

---

## Editing (preserve source formatting)

**Default: edit the file in place with `python-pptx`.** This preserves themes, masters, fonts, and layouts. Only fall back to unpack/repack when you need to change master slides, themes, or animations that python-pptx does not expose.

### Find and replace text (preserves formatting)

```python
from pptx import Presentation
prs = Presentation("deck.pptx")
REPL = {"{{COMPANY}}": "AcmeCorp", "{{DATE}}": "Q2 2026"}
for slide in prs.slides:
    for shape in slide.shapes:
        if not shape.has_text_frame: continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:                # iterate runs, not text_frame.text
                for k, v in REPL.items():
                    if k in run.text:
                        run.text = run.text.replace(k, v)
prs.save("deck.filled.pptx")
```

Editing `text_frame.text` directly destroys run-level formatting (font, size, bold, color). Always edit at the **run** level when preserving styling matters.

### Add / edit speaker notes

```python
slide.notes_slide.notes_text_frame.text = "Talk track in Spanish: ..."
```

### Bulk operations across all slides

```python
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    r.font.name = "Calibri"
```

### Template-based creation

For decks built from a `.pptx` template the user provides, see [editing.md](editing.md). Workflow: analyze template with `thumbnail.py` → unpack → duplicate slide layouts → fill content → clean leftover placeholders → pack.

---

## Creating from Scratch

When no template exists, use `pptxgenjs` (Node). See [pptxgenjs.md](pptxgenjs.md) for full API. For Python-only environments, `python-pptx` works but layout control is more manual.

---

## Bilingual (ES/EN) decks

Common for PR-based companies presenting to bilingual boards or US/PR audiences:

- Two-column layout with EN left / ES right per slide, OR
- Two slide masters (EN deck + ES deck) generated from a single content YAML
- Speaker notes in the speaker's preferred language; on-screen text in audience language

For accent characters (á é í ó ú ñ ¿ ¡), use a font that includes Latin-Extended glyphs — Calibri, Arial, Inter, Source Sans, Georgia all work. Avoid Impact and decorative fonts that drop accent marks.

---

## Design Standards (avoid generic-AI look)

**Don't ship boring slides.** Plain bullets on white = forgettable.

### Before starting

- **Pick a content-informed palette.** If your colors would work equally well on a completely unrelated topic, you didn't pick well. For a cybersecurity deck: deep navy + signal-red accent, or charcoal + lime, not generic Office blue.
- **Dominance over equality.** One color carries 60-70% visual weight, 1-2 supporting tones, one sharp accent. Never give all colors equal weight.
- **Sandwich structure.** Dark backgrounds for title and conclusion; light for content. Or commit to dark throughout for premium feel.
- **One repeating visual motif.** Pick ONE element — rounded image frames, icons in colored circles, thick single-side borders — and carry it across every slide.

### Color palettes

| Theme | Primary | Secondary | Accent |
|---|---|---|---|
| Midnight Executive | `1E2761` navy | `CADCFC` ice | `FFFFFF` white |
| Cybersec Signal | `0B132B` deep navy | `1C2541` slate | `FF3366` signal red |
| Forest & Moss | `2C5F2D` forest | `97BC62` moss | `F5F5F5` cream |
| Coral Energy | `F96167` coral | `F9E795` gold | `2F3C7E` navy |
| Warm Terracotta | `B85042` terracotta | `E7E8D1` sand | `A7BEAE` sage |
| Ocean Gradient | `065A82` deep blue | `1C7293` teal | `21295C` midnight |
| Charcoal Minimal | `36454F` charcoal | `F2F2F2` off-white | `212121` black |
| Teal Trust | `028090` teal | `00A896` seafoam | `02C39A` mint |
| Berry & Cream | `6D2E46` berry | `A26769` rose | `ECE2D0` cream |
| Sage Calm | `84B59F` sage | `69A297` eucalyptus | `50808E` slate |
| Cherry Bold | `990011` cherry | `FCF6F5` off-white | `2F3C7E` navy |

### Per-slide layout options

Every slide needs a visual element. Layouts:

- Two-column (text left, illustration/chart right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 content grid with image on the side
- Half-bleed image (full left or right) with content overlay
- Big-stat callout (60-72pt number, small label below)
- Comparison columns (before/after, pros/cons)
- Timeline / numbered process flow

### Typography

| Header font | Body font |
|---|---|
| Georgia | Calibri |
| Arial Black | Arial |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Inter Bold | Inter |
| Source Serif Pro | Source Sans Pro |
| Palatino | Garamond |

| Element | Size |
|---|---|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body | 14-16pt |
| Captions | 10-12pt muted |

### Accessibility (default ON)

- Body text contrast ratio ≥ 4.5:1 against background; titles ≥ 3:1
- Never rely on color alone (red/green) — pair with icon or label
- Min body size 14pt; 16pt preferred for projector decks
- Alt text on every meaningful image (`shape.alternative_text = "..."`)

### Spacing

- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room

### Don't

- Repeat the same layout slide after slide
- Center body text (left-align paragraphs/lists; center only titles)
- Skimp on size contrast (titles need 36pt+ vs 14-16pt body)
- Default to corporate blue
- Mix random spacing values
- Style one slide and leave the rest plain
- Make text-only slides
- Forget text-box padding when aligning to shapes (`margin: 0` or offset)
- Use low-contrast text or icons
- **Add an accent line under every title** — hallmark of AI-generated decks; use whitespace or background block instead

---

## Format Fidelity (cross-app: PowerPoint, Keynote, Google Slides)

Decks must open cleanly in all three. Common breakage points:

- **Fonts**: embed or use a cross-platform stack (Calibri, Arial, Georgia, Verdana). Keynote substitutes missing fonts silently and shifts layouts.
- **SmartArt** from python-pptx: avoid — Keynote often renders it as a flat image.
- **Custom XML / vendor extensions**: stripped by Google Slides import. Stick to standard `p:sp`, `p:pic`, `p:graphicFrame`.
- **Embedded videos**: link, don't embed, if the deck will be sent across platforms.
- **Charts**: pptxgenjs / python-pptx native charts are most portable. Avoid pasted Excel chart objects.
- **Animations**: minimal and standard (fade, appear, fly-in). Complex motion paths break in Keynote/Slides.

After build, verify cross-platform fidelity by exporting to PDF (`soffice --convert-to pdf`) and visually inspecting — if it looks right in PDF, it will render acceptably in Keynote/Slides.

---

## QA (required — assume there are problems)

Your first render is rarely correct. Approach QA as a bug hunt.

### Content QA

```bash
python -m markitdown output.pptx
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder|click to add|\{\{"
```

If grep returns hits, fix before declaring done.

### Visual QA — use a subagent even for 2-3 slides

You've been staring at the code. Subagent has fresh eyes.

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
ls slide-*.jpg
```

Subagent prompt:
```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words)
- Text overflow / cut-off at edges
- Decorative lines positioned for single-line title but title wrapped to two
- Footers / citations colliding with content above
- Elements too close (<0.3" gaps) or cards nearly touching
- Uneven gaps (cramped here, empty there)
- Insufficient slide-edge margins (<0.5")
- Misaligned columns
- Low-contrast text or icons
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content
- Accent lines under titles (the AI-deck giveaway)

For each slide, list issues even if minor.
```

### Verification loop

1. Generate → convert → inspect
2. List issues (if you found zero, look harder)
3. Fix → **re-verify only the fixed slides** (`pdftoppm -f N -l N`)
4. Repeat until a full pass reveals nothing new

Do not declare success until at least one fix-and-verify cycle has run.

---

## Workflow chains

- **Sales/investor deck**: `sales:create-an-asset` (or `create-deck`) drives the narrative; this skill produces the .pptx if that's the chosen format.
- **Brand-aligned deck**: `anthropic-skills:ckmdesign` / `anthropic-skills:ckmbrand` set tokens; this skill applies them to .pptx.
- **HTML version of an existing .pptx**: extract content here, hand to `anthropic-skills:ckmslides`.
- **PDF export**: this skill via `soffice --convert-to pdf`. For PDF post-processing (redact customer names, watermark, encrypt), hand to `pdf`.
- **Deck content from research**: `data:analyze` / `sales:account-research` produces the content; this skill produces the file.
- **Bilingual deck**: draft EN content, translate via `marketing:draft-content` for tone, build both decks here from a single content source.

---

## Dependencies

```
pip install python-pptx markitdown[pptx] Pillow
npm install -g pptxgenjs
# system: libreoffice (soffice), poppler (pdftoppm)
```
