---
name: brand-guidelines
description: >
  Universal brand guideline engine for producing, reviewing, and suggesting brand-compliant
  marketing materials for ANY company. Use this skill whenever a task involves brand identity,
  visual consistency, marketing collateral, or corporate design standards. Triggers include:
  brand guidelines, brand book, visual identity, corporate identity, brand compliance,
  brand review, brand audit, marketing materials, social media copy, poster design,
  banner design, PPT template, presentation template, company brochure, brand colors,
  typography guidelines, tone of voice, brand voice, logo usage, brand assets,
  style guide, design system, marketing collateral, campaign materials, brand consistency check.
  Also trigger when a user mentions producing materials like posters, banners, social posts,
  company introductions, pitch decks, brochures, flyers, email templates, or video storyboards
  and wants them to follow a specific brand look-and-feel. Even if the user doesn't say
  "brand guideline" explicitly, use this skill when any visual or verbal consistency with
  a company identity is implied.
---

# Brand Guidelines Engine

A universal skill for producing, reviewing, and advising on brand-compliant materials across
any company. This skill turns a brand configuration file into an active quality gate — every
deliverable you produce or review passes through brand rules automatically.

## How This Skill Works

The skill operates in three modes depending on what the user needs:

| Mode | Trigger | What Happens |
|------|---------|--------------|
| **Configure** | User provides brand info or uploads a brand guide | Parse → generate `brand-config.json` |
| **Produce** | User asks to create a deliverable (poster, PPT, copy…) | Load config → apply brand rules → create output |
| **Review** | User asks to check/audit existing material | Load config → run compliance checklist → report issues |

## Quick Start

### Step 0 — Load or Create Brand Configuration

Every task begins here. Check if a `brand-config.json` exists in the working directory or
in the user's uploaded files.

**If config exists**: Read it and confirm the brand name with the user.

**If config does NOT exist**: Ask the user for brand information. They may:
- Upload an existing brand guideline document (PDF, DOCX, PPT, image)
- Describe their brand verbally
- Point to a company website

Then generate the config by running:
```bash
python3 <skill-path>/scripts/init_brand_config.py --output brand-config.json
```
Edit the output JSON to fill in the user's brand details. The config structure covers every
aspect of brand identity — see `references/brand-config-template.md` for the full schema
and field-by-field guidance.

**Minimum viable config** (enough to start producing materials):
```json
{
  "brand_name": "Company Name",
  "colors": {
    "primary": [{"name": "Main", "hex": "#000000"}],
    "accent": [{"name": "Accent", "hex": "#FF6600"}]
  },
  "typography": {
    "heading_font": "Poppins",
    "body_font": "Inter"
  }
}
```

Even a partial config is useful — the skill will work with whatever is provided and flag
gaps when they matter for the specific deliverable.

---

## Mode 1: Configure — Building the Brand Config

When the user provides brand source material (a PDF brand book, a website, verbal descriptions),
your job is to extract structured brand data into `brand-config.json`.

### Extraction Workflow

1. **Read the source material** carefully. For PDFs, extract text; for images, describe visual
   elements; for websites, note colors, fonts, and layout patterns.

2. **Map to the config schema**. Walk through each section of `references/brand-config-template.md`
   and fill what you can find.

3. **Infer what's missing**. If a brand guide shows a blue header but doesn't list the hex code,
   eyeball it or ask the user. If tone-of-voice examples exist but no explicit personality traits
   are listed, derive them from the examples.

4. **Ask to fill gaps**. Present the user with a summary of what you found vs. what's still
   missing. Prioritize gaps that affect near-term deliverables.

5. **Validate colors**. Run `scripts/validate_brand.py --config brand-config.json --check colors`
   to ensure contrast ratios meet WCAG AA for all foreground/background combinations.

6. **Save and confirm**. Write the final `brand-config.json` and give the user a visual summary:
   color swatches (as an HTML or SVG artifact), font hierarchy, and key verbal guidelines.

---

## Mode 2: Produce — Creating Brand-Compliant Deliverables

When a user asks you to create any marketing material, follow this workflow:

### Step 1 — Identify the Deliverable Type

Read `references/deliverable-specs.md` to find the matching deliverable type and its specs.
Common types:

| Category | Deliverables |
|----------|-------------|
| **Social Media** | Instagram post/story/reel, Facebook post/cover, LinkedIn post/banner, Twitter/X post, TikTok, WeChat Moments, Xiaohongshu |
| **Digital Ads** | Web banner (IAB sizes), display ads, email header |
| **Presentations** | Pitch deck, company intro, sales deck, keynote template |
| **Print** | Poster (A3/A2/A1), flyer (A5/A4), brochure, business card, letterhead |
| **Long-form** | Company brochure/lookbook, annual report, brand book itself |
| **Video** | Storyboard, title card, end card, lower-third template |
| **Copy** | Taglines, social captions, website copy, email campaigns, press releases |

### Step 2 — Apply Brand Rules

For every deliverable, apply these rules from the brand config:

**Visual rules** (read `references/visual-identity.md` for details):
- Colors: Use ONLY colors from the brand palette. Primary color dominates (60-30-10 rule:
  60% primary/neutral, 30% secondary, 10% accent).
- Typography: Use only approved fonts at approved sizes. Headings in heading font,
  body in body font. Never mix unapproved fonts.
- Logo: Follow clear-space rules, minimum size, and approved placement positions.
  Never stretch, rotate, recolor, or add effects to the logo.
- Imagery: Follow the brand's photography/illustration style. Consistent filters,
  cropping ratios, and subject matter.
- Layout: Respect the brand's grid system and spacing conventions. Consistent margins
  and padding across materials.

**Verbal rules** (read `references/tone-of-voice.md` for details):
- Tone: Match the brand personality. If the brand is "professional yet approachable",
  every piece of copy should reflect that balance.
- Terminology: Use preferred terms, avoid deprecated ones. Honor the brand's glossary.
- Messaging hierarchy: Lead with the primary message, support with secondary points.
  Calls-to-action should use approved language.
- Platform adaptation: The same message gets reshaped for each platform's conventions
  (LinkedIn is professional; Instagram is visual-first; Twitter is concise).

### Step 3 — Size and Format the Output

Consult the size table in `references/deliverable-specs.md` for exact dimensions, DPI,
file format, and bleed requirements. Key principles:

- **Digital**: RGB color mode, 72-150 DPI, pixel dimensions matter
- **Print**: CMYK color mode, 300 DPI minimum, add bleed (typically 3mm)
- **Social**: Each platform has its own image sizes — ALWAYS check the latest specs
- **Presentations**: 16:9 widescreen (33.87cm x 19.05cm) is default; confirm with user

### Step 4 — Quality Gate

Before delivering ANY material, run the brand compliance review:

```bash
python3 <skill-path>/scripts/validate_brand.py --config brand-config.json --material <output-file>
```

Also mentally walk through the checklist in `references/review-checklist.md`:
- Are all colors from the approved palette?
- Are fonts correct (family, weight, size)?
- Is the logo used correctly (size, spacing, variant)?
- Does the copy match the brand voice?
- Are dimensions correct for the intended platform?
- Is there sufficient contrast for readability?
- Are mandatory legal elements present (copyright, disclaimers)?

---

## Mode 3: Review — Auditing Existing Materials

When a user asks you to review or audit materials for brand compliance:

### Review Workflow

1. **Load the brand config** and understand the full brand system.

2. **Examine the material**. For images, describe what you see (colors, fonts, layout, logo usage).
   For documents, read the content. For presentations, check each slide.

3. **Score against the checklist**. Use `references/review-checklist.md` and score each
   category (Visual Identity, Typography, Color, Logo, Imagery, Copy, Format).

4. **Generate a compliance report** with this structure:
   ```
   # Brand Compliance Report — [Material Name]

   ## Overall Score: X/100

   ## Summary
   One-paragraph overview of compliance level.

   ## Findings

   ### Passes (what's correct)
   - ...

   ### Issues (what needs fixing)
   For each issue:
   - **What**: Description of the violation
   - **Where**: Location in the material
   - **Rule**: Which brand guideline it violates
   - **Fix**: Specific recommended correction

   ## Recommendations
   Prioritized list of improvements.
   ```

5. **Offer to fix**. For each issue found, offer to produce a corrected version.

---

## Working With Other Skills

This skill often works alongside other creation skills. The brand config acts as a
constraint layer on top of their output:

| Partner Skill | How Brand Guidelines Applies |
|---------------|------------------------------|
| **pptx** | Apply brand colors, fonts, and logo to presentation templates. Use brand imagery style. |
| **docx** | Apply brand fonts, heading styles, and color accents to documents. Enforce tone of voice. |
| **xlsx** | Apply brand colors to chart formatting and header styling. |
| **pdf** | Ensure generated PDFs follow brand typography and color rules. |

When invoking a partner skill, pass the relevant brand parameters explicitly:
- Color hex codes for fills and text
- Font family names and sizes
- Logo file path and placement rules

---

## Platform-Specific Copy Guidelines

When writing copy for social media or marketing channels, adapt the brand voice to each
platform's conventions. Read `references/tone-of-voice.md` for the full framework, but
here's the quick reference:

| Platform | Max Length | Tone Shift | Format Notes |
|----------|-----------|------------|-------------|
| LinkedIn | 3000 chars | More professional, thought-leadership | Paragraphs, minimal emoji |
| Instagram | 2200 chars | Visual-first, lifestyle-oriented | Short paragraphs, strategic emoji, 3-5 hashtags |
| Twitter/X | 280 chars | Punchy, conversational | One core message, 1-2 hashtags max |
| Facebook | 500 chars optimal | Community-oriented, storytelling | Questions work well, link-friendly |
| WeChat | 2000 chars | Relationship-focused, informative | Longer form OK, image-text mix |
| Xiaohongshu | 1000 chars | Authentic, personal, lifestyle | Emoji-rich, tip-style formatting, 10+ hashtags |
| Email Subject | 50 chars | Direct, benefit-focused | Front-load the value proposition |
| Email Body | Varies | Warm but professional | Clear CTA, scannable sections |

---

## Brand Config Quick Reference

The `brand-config.json` is structured into these top-level sections:

| Section | Purpose | Reference |
|---------|---------|-----------|
| `brand_name` | Company name | — |
| `brand_identity` | Mission, values, positioning, personality | `references/brand-config-template.md` |
| `colors` | Full color palette with codes | `references/visual-identity.md` |
| `typography` | Font families, sizes, hierarchy | `references/visual-identity.md` |
| `logo` | Usage rules, variants, clear space | `references/visual-identity.md` |
| `imagery` | Photography/illustration style | `references/visual-identity.md` |
| `verbal_identity` | Tone, terminology, key messages | `references/tone-of-voice.md` |
| `deliverable_defaults` | Per-type default settings | `references/deliverable-specs.md` |

---

## Dependencies

- Python 3.8+ (for scripts)
- Pillow (for color palette visualization)
- python-pptx (when working with presentations)
- python-docx (when working with documents)
- openpyxl (when working with spreadsheets)

These are typically pre-installed. If not, install with:
```bash
pip install Pillow python-pptx python-docx openpyxl --break-system-packages
```
