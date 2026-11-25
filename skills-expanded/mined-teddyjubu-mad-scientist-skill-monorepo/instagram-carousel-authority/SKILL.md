---

name: instagram-carousel-authority
description: instagram-carousel-authority lets the user turn a topic, offer, or business message into a strategic Instagram carousel built for reach, saves, shares, and authority-building, including the hook, slide structure, teaching angle, design direction, and caption strategy needed to make the post feel like a serious piece of content instead of random social filler.

---
Complete workflow for creating viral, authority-building Instagram carousels from research through publishing.

## What This Skill Does

This skill instagram-carousel-authority lets the user turn a topic, offer, or business message into a strategic Instagram carousel built for reach, saves, shares, and authority-building, including the hook, slide structure, teaching angle, design direction, and caption strategy needed to make the post feel like a serious piece of content instead of random social filler.

## Overview

This skill executes a full multi-phase pipeline:
1. **Intelligence gathering** — business research, competitor audit, trend analysis
2. **Strategic brief** — angle selection, hook formulas, slide structure, visual direction
3. **Carousel creation** — design system, slide production, quality checks, export
4. **Instagram publishing** — caption writing, hashtag strategy, optimal timing, direct publishing via Manus

## Execution Rules

- **Complete all phases sequentially** without stopping for approval between phases unless you encounter a blocker
- Use your judgment on all tool selections, methods, and approaches
- Do not ask questions unless absolutely necessary
- Do whatever it takes to complete the task

## Required Input

User must provide one of:
- Business URL
- Business name
- Social media account handle(s)

## Success Criteria

- Carousel positions the business as a credible authority in its niche
- Visual design is professional, scroll-stopping, and on-brand
- Caption and hashtags maximize organic reach and saves
- Post is published directly to the business's Instagram account via Manus Instagram integration
- All research, strategy, and design files are saved and provided as attachments

## Workflow

### Phase 1: Intelligence Gathering

Read [references/phase1-intelligence.md](references/phase1-intelligence.md) for detailed instructions on:
- Business deep-dive (core offer, positioning, target audience, brand identity, Instagram presence)
- Competitor content audit (top 5 competitors, carousel analysis, hook styles, visual patterns)
- Trend intelligence (trending hashtags, viral formats, optimal posting times)

**Output:** `intelligence_report.md`

### Phase 2: Strategic Brief

Read [references/phase2-strategy.md](references/phase2-strategy.md) for detailed instructions on:
- Viral angle selection (audience demand × competitor gaps × current traction)
- Hook formula (3 alternatives: contrarian claim, outcome promise, pattern interrupt)
- Slide-by-slide content structure (8–10 slides optimized for saves/shares)
- Visual direction (color palette, fonts, layout, mood)

**Output:** `carousel_brief.md`

### Phase 3: Carousel Creation

Read [references/phase3-design.md](references/phase3-design.md) for detailed instructions on:
- Design system (1080x1080px, consistent grid, typography, branding)
- Slide-by-slide production (cover hook, value slides, takeaway, CTA, brand)
- Quality checks (thumbnail legibility, word count, color contrast, alignment)
- Export formats (individual PNGs, combined PDF, preview strip)

**Outputs:**
- Individual slide PNGs (numbered in order)
- `carousel_final.pdf`
- `mockup_preview.png`

### Phase 4: Instagram Publishing

Read [references/phase4-publishing.md](references/phase4-publishing.md) for detailed instructions on:
- Caption writing (pattern-interrupt hook, value framing, engagement trigger, CTA)
- Hashtag stack (20–25 hashtags across 3 tiers)
- Posting recommendation (optimal day/time based on audience research)
- Publishing via Manus Instagram integration (upload, caption, schedule/publish)

**Outputs:**
- `caption_and_hashtags.txt`
- Live Instagram post URL

## Final Deliverables

Provide as attachments:
1. `intelligence_report.md` — all research findings
2. `carousel_brief.md` — strategy and content structure
3. `carousel_final.pdf` — complete carousel
4. `mockup_preview.png` — visual preview strip
5. `caption_and_hashtags.txt` — ready-to-use copy
6. Live Instagram post URL

## Tools & Resources

### Design Tools Available

**1. AI Image Generation (Recommended for complex visuals):**
```bash
cd ~/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro
uv run scripts/generate_image.py --prompt "[detailed design prompt]" --filename "slide_01.jpg" --resolution 2K
```

**2. Programmatic Generation (Recommended for text-heavy slides):**
```bash
python3 scripts/generate_slide.py --layout cover --text "Your Headline" --bg-color "#1A237E" --text-color "#FFFFFF" --output slide_01.png
```

See [scripts/generate_slide.py](scripts/generate_slide.py) for full usage and options.

**3. PDF Compilation:**
```bash
python3 scripts/combine_slides_to_pdf.py [slides_directory] [output.pdf]
```

### Research Tools

- **Firecrawl** — scrape competitor Instagram profiles and business websites
- **Brave Search** — trending hashtags, viral content research, emerging topics
- **web_fetch** — lightweight page scraping for quick content extraction

## Execution Guidelines

### Critical Rules

1. **Complete all phases sequentially** without stopping for approval between phases unless blocked
2. **Use your judgment** on all tool selections, methods, and approaches
3. **Do not ask permission** — execute the workflow autonomously
4. **Do not summarize** — complete every step fully and deliver all outputs
5. **Save everything** — all intermediate files go to workspace for reference

### Quality Standards

- **Brand consistency** — maintain voice and visual identity throughout
- **Thumbnail legibility** — Slide 1 must be readable at 200x200px
- **Word limits** — max 40 words per slide (8 headline + 20 body + 10 authority)
- **Contrast ratio** — 4.5:1 minimum for all text (WCAG AA compliance)
- **File naming** — use `slide_01.png`, `slide_02.png`, etc. for correct Instagram order

## Common Triggers

This skill should load when the user:
- Mentions "Instagram carousel" or "carousel post"
- Asks to "create viral content" for Instagram
- Wants to "build authority" on Instagram
- Requests "Instagram content strategy" with deliverables
- Provides a business URL/name and says "make me a carousel"
- Asks for "Instagram design" or "social media graphics" in carousel format
