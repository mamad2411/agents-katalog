---
name: BalajiSlides
description: Balaji Srinivasan slide design system. USE WHEN balaji slides, balaji style, evidence slides, balaji presentation, split layout slides, create balaji deck, artifact-driven slides.
---

# BalajiSlides

Slide design system based on Balaji Srinivasan's presentation style. Evidence over decoration. Every slide makes one argument backed by a real artifact — screenshot, map, chart, code snippet, or quote. No corporate templates, no stock imagery, no bullet-point walls.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/BalajiSlides/`

If this directory exists, load and apply any PREFERENCES.md or configurations found there.

## MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the WORKFLOWNAME workflow in BalajiSlides skill to ACTION"}' \
  > /dev/null 2>&1 &
```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CreateBalajiSlides** | "create slides", "balaji deck", "make presentation", "build slides" | `Workflows/CreateBalajiSlides.md` |

## Quick Reference

- **Layout:** Left-headline / right-visual split (35/65)
- **Headlines:** Bold, 1-6 words, opinionated thesis statements
- **On-slide text:** Headline only. Optional 1-line caption. No paragraphs on slides.
- **Speaker notes:** All explanatory text, context, and talking points go here — the speaker SAYS it, the audience SEES the visual
- **Visuals:** Real artifacts only — screenshots, maps, charts, code, photos
- **Background:** White or light gray (dark for code slides only)
- **Typography:** Sans-serif, high contrast, left-aligned

**Full Design Guide:** Read `DesignGuide.md` in this skill's root for complete style rules.

## Examples

**Example 1: Create a talk on network sovereignty**
```
User: "create balaji-style slides on why decentralized identity matters"
-> Invokes CreateBalajiSlides workflow
-> Loads DesignGuide.md for style rules
-> Structures numbered sequence (Section 1, 2, 3...)
-> Each slide: opinionated headline + 2-4 sentence body + real artifact
-> Outputs markdown slide content ready for Google Slides
```

**Example 2: Convert existing bullet-point deck to Balaji style**
```
User: "reformat these slides in balaji style"
-> Invokes CreateBalajiSlides workflow
-> Reads existing slide content
-> Converts bullet lists to short paragraphs
-> Replaces decorative visuals with real evidence artifacts
-> Adds opinionated headlines to each slide
```

**Example 3: Create a single evidence slide**
```
User: "make a balaji-style slide showing app store rankings"
-> Invokes CreateBalajiSlides workflow
-> Uses Pattern 2: Full-Screen Evidence
-> Screenshot dominates slide, small title overlay top-left
-> Minimal text — the visual IS the argument
```
