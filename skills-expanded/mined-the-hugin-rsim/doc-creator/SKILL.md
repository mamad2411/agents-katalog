# Skill: doc-creator

**Purpose:** Universal onboarding for creating any structured documents — portfolio guides, comparison tables, training materials, catalogs, reports, presentations. Output: HTML→PDF, DOCX, Slides.
**When:** User wants to create a document, guide, or presentation from sources (docx, PDF, website, data). Any type.
**Output:** Agreed document structure + chosen design + ready generator or file.

---

## PROCESS

### Step 1 — 4 universal questions (ask all, don't guess)

Ask user these 4 questions before any work:

1. **Document type:** what is it essentially?
   (guide / catalog / comparison / report / training / other — let them describe)

2. **Audience:** who reads it and what's their background?
   (role, expertise level, what they know, what they don't)

3. **Reader goal:** what should they be able to do / know / decide after reading?
   (one concrete action or state)

4. **Output format:** HTML→PDF / DOCX / Slides (Google, PowerPoint) / Web page?

> Don't proceed to Step 2 until all 4 answers received.
> If user answers partially — clarify the missing piece.

---

### Step 2 — Design choice (show options, wait for answer)

Show options explicitly — don't choose by default:

```
Выбери стиль документа:

A) Compact   — dense layout, lots of content per page,
               minimal decoration. Good for reference docs,
               technical comparisons, internal materials.

B) Rich      — large blocks, visual accents, icons,
               color highlights. Good for product guides,
               client materials, onboarding.

C) Sectioned — color section covers between chapters,
               each section starts on a new page.
               Good for multi-topic guides, catalogs,
               training courses.

D) Custom    — describe style in words or attach reference.
```

**Rule:** for options B, C, D — invoke `frontend-design` skill
to develop the design system (colors, typography, components)
**before** writing code. Don't improvise design during generation.

> Wait for explicit answer (A / B / C / D + description for D).

---

### Step 3 — Propose document structure

Based on Step 1 answers — propose structure:
- List of sections with names
- Block type per section: card / table / list / narrative / mixed
- Depth per section (number of fields / detail level)

**Rules:**
- Don't use fixed template — structure is determined by document type
- Catalog/guide type → card structure with audience-targeted fields
- Comparison type → matrix or parallel columns
- Training type → modular structure (topic → theory → example → question)
- Report type → executive summary + sections + appendix

> Show structure as a list. Wait for "ok" or edits.
> Don't start generating content until structure is confirmed.

---

### Step 4 — Sources and data

Find out what's available:

```
□ What sources are provided?
  - DOCX / text files
  - PDF (important: image-based or text? check get_text())
  - Website (URL for scraping)
  - Structured data (CSV, JSON, tables)
  - Only verbal instructions / session memory

□ Is there branding?
  - Logo / brand guide → apply
  - PDF with examples → run extract-brand-palette
  - Nothing → ask user for colors or use neutral palette
```

**For image-based PDF:**
- `fitz.get_text()` returns empty string → signal
- Content: ask user for text or via OCR
- Palette: pixel sampling via PyMuPDF (see `extract-brand-palette` skill)

---

### Step 5 — Generator architecture (if format is HTML→PDF)

Required principles:

```python
# 1. Data-template separation
#    All data — Python dicts/lists.
#    HTML — only in render functions. Never mix.

DATA = [{ "name": "...", "fields": {...} }]

def render_card(item): ...
def render_section(items): ...

# 2. Print CSS
@media print {
    .card { page-break-inside: avoid; }
    .section-cover { page-break-before: always; }
    body { font-size: 10pt; }
}

# 3. Encoding (Windows)
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 4. Output
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done. Open in Chrome → Ctrl+P → Save as PDF (A4)")
```

**User instructions after generation:**
Chrome/Edge → open output.html → Ctrl+P → Destination: Save as PDF →
Paper: A4 → Margins: None or Minimum → Background graphics: ✓ → Save.

---

## PRE-GENERATION CHECKLIST

- [ ] Step 1: all 4 questions asked and answered
- [ ] Step 2: design style chosen explicitly (A/B/C/D); for B/C/D — frontend-design invoked
- [ ] Step 3: structure proposed and confirmed by user
- [ ] Step 4: sources identified, branding clarified
- [ ] Step 5: if HTML→PDF — architecture matches principles above

> If any item incomplete — return to that step.
> Don't generate in "guess what's needed" mode.
