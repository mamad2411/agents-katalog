---
name: canva-brand-kit
description: |
  Manage and apply brand kits in Canva. Use this skill when user wants to work with
  brand colors, fonts, logos, or maintain brand consistency across designs. Helps
  define brand guidelines and ensures designs follow brand standards.
  Requires Canva Pro/Enterprise for full brand kit features.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Canva Brand Kit Skill

> **QUICK REFERENCE**
> - **Scripts location**: `scripts/` (NOT `skills/canva-brand-kit/scripts/` - those don't exist)
> - **Brand voice files**: `references/brand-voice/`, `samples/brand-kits/`
> - **API client**: `scripts/canva_client.py` (import: `from canva_client import get_client`)
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
>
> **WARNING**: Commands below referencing `skills/canva-brand-kit/scripts/*.py` are WRONG paths.
> Write custom Python using `canva_client.py`. See `scripts/samples/sample_canva_operations.py`.

Manage brand identity elements and ensure brand consistency across Canva designs.

## Scope of This Skill

**This skill handles:**
- Define brand colors
- Set brand fonts
- Manage brand logos
- Apply brand kit to designs
- Check brand compliance
- Create brand guidelines documentation

**NOT handled by this skill:**
- Editing specific designs → Use `canva-image-editor`
- General content creation → Use `canva-content-generator`
- Exporting designs → Use `canva-export`

**Note:** Full Brand Kit features require Canva Pro or Enterprise.

## Brand Kit Components

### Colors
```json
{
  "primary": "#2E86AB",
  "secondary": "#F4D35E",
  "accent": "#EE6352",
  "neutral": {
    "dark": "#1A1A1A",
    "light": "#F5F5F5",
    "white": "#FFFFFF"
  },
  "text": {
    "primary": "#1A1A1A",
    "secondary": "#666666"
  }
}
```

### Fonts
```json
{
  "heading": {
    "family": "Montserrat",
    "weights": ["Bold", "SemiBold"]
  },
  "body": {
    "family": "Open Sans",
    "weights": ["Regular", "Medium"]
  },
  "accent": {
    "family": "Playfair Display",
    "weights": ["Italic"]
  }
}
```

### Logos
```
- Primary logo (full color)
- Secondary logo (monochrome)
- Icon/favicon
- Logo variations (horizontal, vertical, stacked)
```

## 3-Mode Workflow

### MODE 1: PLAN

1. **Assess Current Brand Kit**
   ```python
   # Check existing brand kit
   python skills/canva-brand-kit/scripts/get_brand_kit.py

   # Analyze brand usage across designs
   python skills/canva-brand-kit/scripts/analyze_brand_usage.py
   ```

2. **Document Brand Changes**
   ```
   ## Brand Kit Update Plan

   ### Current Brand Kit
   - Colors: 3 defined (#xxx, #yyy, #zzz)
   - Fonts: 2 (Roboto, Open Sans)
   - Logos: 1 (primary only)

   ### Proposed Changes
   1. ADD color: Accent color #EE6352
   2. UPDATE font: Replace Roboto with Montserrat
   3. ADD logo: Monochrome version

   ### Affected Designs
   - 15 designs use current brand kit
   - Changes may affect visual consistency
   ```

### MODE 2: CLARIFY

Brand-specific questions:

1. **Color Changes**
   - "New accent color #EE6352. Should I show a preview?"
   - "Replace existing color or add as new?"

2. **Font Changes**
   - "Switch from Roboto to Montserrat for headings?"
   - "Keep existing body font or change too?"

3. **Logo Updates**
   - "Add new logo variant or replace existing?"
   - "Which designs should use new logo?"

4. **Consistency**
   - "Apply changes to existing designs or new only?"
   - "Create before/after comparison?"

### MODE 3: IMPLEMENT

```python
# Update brand colors
python skills/canva-brand-kit/scripts/update_colors.py \
  --primary "#2E86AB" \
  --secondary "#F4D35E" \
  --accent "#EE6352"

# Update brand fonts
python skills/canva-brand-kit/scripts/update_fonts.py \
  --heading "Montserrat" \
  --body "Open Sans"

# Upload brand logo
python skills/canva-brand-kit/scripts/upload_logo.py \
  --file "input/logos/primary-logo.png" \
  --type "primary"

# Apply brand kit to design
python skills/canva-brand-kit/scripts/apply_brand.py \
  --design "DESIGN_ID" \
  --elements "colors,fonts"
```

## Available Scripts

### Brand Kit Management
- `get_brand_kit.py` - Get current brand kit
- `update_colors.py` - Update brand colors
- `update_fonts.py` - Update brand fonts
- `upload_logo.py` - Upload brand logo
- `export_brand_kit.py` - Export brand kit as JSON

### Brand Application
- `apply_brand.py` - Apply brand to design
- `batch_apply_brand.py` - Apply to multiple designs
- `check_brand_compliance.py` - Verify brand consistency

### Analysis
- `analyze_brand_usage.py` - See brand usage across designs
- `find_off_brand.py` - Find designs not using brand kit
- `generate_brand_report.py` - Create brand usage report

## Local Brand Definition

Define your brand in `samples/brand-kits/`:

```
samples/brand-kits/
├── brand-config.json       # Main brand configuration
├── colors.json             # Detailed color palette
├── typography.json         # Font specifications
├── logos/                  # Logo files
│   ├── primary.png
│   ├── secondary.png
│   ├── icon.png
│   └── variations/
├── guidelines.md           # Brand guidelines document
└── examples/               # Example brand applications
    ├── correct/
    └── incorrect/
```

### brand-config.json
```json
{
  "brand_name": "Your Brand",
  "tagline": "Your Tagline Here",
  "colors": {
    "primary": "#2E86AB",
    "secondary": "#F4D35E",
    "accent": "#EE6352",
    "background": "#FFFFFF",
    "text_primary": "#1A1A1A",
    "text_secondary": "#666666"
  },
  "fonts": {
    "heading": {
      "family": "Montserrat",
      "size_h1": 48,
      "size_h2": 36,
      "size_h3": 24,
      "weight": "Bold"
    },
    "body": {
      "family": "Open Sans",
      "size": 16,
      "line_height": 1.5,
      "weight": "Regular"
    }
  },
  "logos": {
    "primary": "logos/primary.png",
    "secondary": "logos/secondary.png",
    "icon": "logos/icon.png"
  },
  "spacing": {
    "minimum_logo_clearance": "20px",
    "section_padding": "40px"
  }
}
```

## Brand Compliance Check

Verify designs follow brand guidelines:

```python
python skills/canva-brand-kit/scripts/check_brand_compliance.py \
  --design "DESIGN_ID"

# Output:
# Brand Compliance Report for "Design Name"
#
# ✓ Colors: All colors match brand palette
# ✗ Fonts: Using Arial instead of brand font Montserrat
# ✓ Logo: Using correct primary logo
# ⚠ Spacing: Logo clearance is 15px (minimum: 20px)
#
# Compliance Score: 75%
#
# Recommendations:
# 1. Replace Arial with Montserrat for headings
# 2. Increase logo clearance to 20px
```

## Batch Brand Application

Apply brand to multiple designs:

```python
# Apply brand colors to all designs in folder
python skills/canva-brand-kit/scripts/batch_apply_brand.py \
  --folder "FOLDER_ID" \
  --elements "colors"

# Apply full brand kit to selected designs
python skills/canva-brand-kit/scripts/batch_apply_brand.py \
  --designs "ID1,ID2,ID3" \
  --elements "colors,fonts" \
  --preview true
```

## Color Accessibility

Check color combinations for accessibility:

```python
python skills/canva-brand-kit/scripts/check_accessibility.py \
  --foreground "#1A1A1A" \
  --background "#FFFFFF"

# Output:
# Contrast Ratio: 17.4:1
# WCAG AA (normal text): ✓ Pass
# WCAG AA (large text): ✓ Pass
# WCAG AAA (normal text): ✓ Pass
# WCAG AAA (large text): ✓ Pass
```

## Typography Guidelines

Font usage recommendations:

```
## Heading Hierarchy

H1: Montserrat Bold, 48px
   - Main titles
   - Hero sections

H2: Montserrat SemiBold, 36px
   - Section headers
   - Slide titles

H3: Montserrat SemiBold, 24px
   - Subsections
   - Card titles

## Body Text

Body: Open Sans Regular, 16px
   - Paragraphs
   - Descriptions

Caption: Open Sans Regular, 14px
   - Image captions
   - Small print

## Special Use

Accent: Playfair Display Italic
   - Quotes
   - Emphasis
```

## Safety Guidelines

1. **Backup before changes** - Export current brand kit first
2. **Preview changes** - Use `--preview` flag when available
3. **Test on one design** - Before batch application
4. **Document changes** - Keep brand kit version history
5. **Consider existing designs** - Changes may affect consistency

## Example Interactions

### "Set up my brand colors"
```
[PLAN]
- Define primary, secondary, and accent colors
- Set text colors
- Configure background colors

[CLARIFY]
- "What are your brand colors? (hex codes)"
- "Do you have a color palette document?"

[IMPLEMENT]
- Create brand-config.json
- Upload to Canva brand kit
- Verify colors applied correctly
```

### "Check if my design follows brand guidelines"
```
[PLAN]
- Load brand configuration
- Analyze design elements
- Compare against brand rules

[CLARIFY]
- "Which design should I check?"
- "Strict or flexible compliance?"

[IMPLEMENT]
- Run compliance check
- Generate report
- List recommendations
```

### "Apply my brand to all marketing materials"
```
[PLAN]
- Identify marketing folder
- List all designs (25 items)
- Determine elements to update

[CLARIFY]
- "Apply colors, fonts, or both?"
- "Preview changes before applying?"
- "Skip any specific designs?"

[IMPLEMENT]
- Apply brand in batches
- Report progress
- Summary of changes
```

## Output Files

Brand operations saved to:
- `output/brand/brand_kit.json` - Current brand configuration
- `output/brand/compliance_reports/` - Compliance check results
- `output/brand/change_history.json` - Brand update history
