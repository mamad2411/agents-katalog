---
name: openclaw-logo-maker
description: openclaw-logo-maker lets the user design and generate logos and brand identity visuals for OpenClaw sub-agents, helping them create consistent, recognizable branding across an AI agent team without needing a graphic designer.
---
**Version:** 1.0.0
**Author:** James (AI Assistant) for Charles (The Mad Scientist)
**Date Created:** April 2026

---

## What This Skill Does

This skill openclaw-logo-maker lets the user design and generate logos and brand identity visuals for OpenClaw sub-agents, helping them create consistent, recognizable branding across an AI agent team without needing a graphic designer.

## Description

Automates the creation of 10 professional logo variations across diverse design styles (3D, dynamic, geometric, luxury, modern, minimalist, etc.) for any brand using the Google Gemini 3.1 Flash Preview API.

Use this skill whenever a user requests:
- Logo design or brand identity creation
- Logo variations or redesigns
- Brand mark exploration
- Tagline-integrated logo concepts

---

## Workflow Overview

```
Intake → Script Creation → Generation → Background Removal → ZIP Delivery → Guide
```

1. **Intake:** Gather brand details using the Brand Intake Format
2. **Create Script:** Build `generate_logos.py` with brand-specific prompt templates
3. **Generate:** Run the script — produces 10 logo variations
4. **Post-Process:** Auto-generates white background versions + transparent PNGs (20 files total)
5. **Package:** ZIP archive delivered to user with a variation guide

---

## Brand Intake Format

Collect these details before generating:

| Field | Example |
|-------|---------|
| Brand / Company Name | "REI Transaction Mastery" |
| Industry / Niche | "Real Estate Investment Training" |
| Primary Color(s) | "Deep Purple and Gold" |
| Brand Personality | "Authoritative, Premium, Trustworthy" |
| Optional: Tagline | "Close Deals Smarter with AI" |
| Optional: Abbreviation | "RTM" |
| Optional: Preferred Styles | "3D, Geometric, Modern" |
| Optional: Styles to Avoid | "Cartoon, Retro" |
| Optional: Existing Logo | (attach reference image) |
| Optional: Competitor Logos to Avoid | "Anything too similar to Apple or Amazon" |

---

## Required Setup

### API Key
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Default Model:** `gemini-3.1-flash-image-preview` (confirmed working for logo generation)

**Alternative models:**
- `gemini-3-pro-image-preview` — higher quality, slower
- `gemini-2.5-flash-image` — alternative flash-based image gen

### Dependencies
```bash
pip install google-genai pillow
```

### Execution
```bash
cd ~/.openclaw/workspace/skills/openclaw-logo-maker
python scripts/generate_logos.py \
  --brand "Brand Name" \
  --industry "Industry/Niche" \
  --colors "Primary Colors" \
  --personality "Brand Personality" \
  --tagline "Optional Tagline" \
  --output outputs/brand-name-v1
```

---

## Logo Styles Generated

Each run produces exactly **10 distinct variations**:

| # | Style | Description |
|---|-------|-------------|
| 1 | **3D Premium** | Dimensional, polished, modern tech aesthetic |
| 2 | **Dynamic Gradient** | Bold color transitions, forward-motion feel |
| 3 | **Geometric Abstract** | Clean shapes, mathematical precision |
| 4 | **Luxury Minimal** | Understated elegance, thin lines, premium feel |
| 5 | **Modern Flat** | Clean 2D, scalable, versatile |
| 6 | **Futuristic Tech** | Sharp angles, circuit-inspired elements |
| 7 | **Iconic Monogram** | Letter-based mark, elegant typography |
| 8 | **Nature-Inspired** | Organic shapes, subtle environmental feel |
| 9 | **Heritage/Classic** | Traditional, trustworthy, established feel |
| 10 | **Abstract Dynamic** | Custom blend of modern trends, high energy |

---

## Output Files

For each style, the following are generated:

- `style-NAME-transparent.png` — transparent background, white/dark logo
- `style-NAME-white-bg.png` — solid white background version

**Total Output:** 20 PNG files + 1 ZIP archive

---

## Post-Processing Pipeline

The script uses Pillow (PIL) for:
1. Transparent background creation (white/dark elements on transparency)
2. White background version generation
3. PNG optimization and quality control

---

## Prompt Template Strategy

Each logo style uses a highly detailed prompt template that includes:
- Brand name and industry context
- Specific color palette (hex codes included)
- Style description with technical parameters
- Technical specs (transparent background, centered composition, etc.)
- Explicit negative guidance (no cartoon, no clipart, no stock feel)

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| API key invalid | Verify GEMINI_API_KEY in .secrets/gemini.env |
| Quota exceeded | Check Google AI Studio quota, use fallback model |
| Image generation fails | Retry with reduced prompt complexity |
| Background removal fails | Use original images as fallback, note in guide |

---

## Files in This Skill

```
openclaw-logo-maker/
├── SKILL.md                          ← This file
├── scripts/
│   └── generate_logos.py             ← Main generation script
├── references/
│   └── prompt_templates.md           ← Full prompt reference
└── outputs/
    └── [brand-name-v1.zip]           ← Generated output (created at runtime)
```

---

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/openclaw-logo-maker

# Install dependencies
pip install google-genai pillow

# Run logo generation
python scripts/generate_logos.py \
  --brand "Chucky Buys Lucky Houses" \
  --industry "Real Estate Investment" \
  --colors "Gold and Navy Blue" \
  --personality "Bold, Confident, Trusted" \
  --tagline "We Buy Houses Fast" \
  --output outputs/chucky-buys-lucky-v1
```

---

*Skill created by James for Charles — The Mad Scientist*
*OpenCLAW Ecosystem • April 2026*
