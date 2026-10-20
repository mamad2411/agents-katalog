# Brand Brain

Build a complete brand system using Claude and Claude Design. Workflow by @theromanknox.

## Overview

Give Claude your brand-brain folder → it produces a full design system: logo lockups, type scale, color tokens, and UI components — ready to hand to any designer or AI tool.

## Folder Structure

Create a `brand-brain/` folder containing:

```
brand-brain/
├── brief.md          # Brand story, values, target audience, tone
├── colors.md         # Primary, secondary, accent hex values + usage rules
├── typography.md     # Font choices, weights, size scale
├── logos/            # Existing logo files (SVG, PNG)
├── inspiration/      # Reference screenshots or URLs
└── examples/         # Existing designs you want to match
```

## Step 01 — Create Your Design System

Give Claude Design the `brand-brain/` folder and say:

```
Using everything in my brand-brain folder, build a complete design system. Produce:
1. Logo lockups (horizontal, stacked, icon-only)
2. Type scale (display / heading / body / caption with px/rem values)
3. Color tokens (CSS variables for primary, secondary, accent, neutrals, semantic colors)
4. Core components (button, card, input, badge) styled to the brand

Output as HTML + CSS design token file I can paste into any project.
```

## Step 02 — Generate Marketing Assets

```
Using my brand design system, create:
- Instagram post template (1080×1080)
- LinkedIn banner (1584×396)
- Email header (600px wide)
- Presentation title slide

Match the brand colors, fonts, and visual language exactly.
```

## Step 03 — Build a Brand Guide

```
Using my brand-brain folder and the design system we built, write a brand guide covering:
1. Brand story (2 paragraphs)
2. Voice and tone (3 adjectives + do/don't examples)
3. Color palette with hex values and usage rules
4. Typography rules (font pairing, weights, hierarchy)
5. Logo usage rules (clear space, wrong uses)
6. Photography style (mood, subjects, lighting)

Format as a shareable PDF-ready markdown document.
```

## Brief Template

```markdown
# Brand Brief

## Name
[Brand name]

## Tagline
[One sentence]

## Story
[Why does this brand exist? What problem does it solve?]

## Target Audience
[Who are they? Age, lifestyle, goals, pain points]

## Values
[3–5 core values]

## Tone
[e.g. confident, warm, minimal, bold]

## Visual Mood
[e.g. dark luxury / clean minimal / editorial / playful]

## Competitors
[Who are they? What do you want to look different from?]

## Colors I Like
[Hex values or descriptions]

## Fonts I Like
[Font names or vibes]
```
