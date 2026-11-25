---
name: NSSlides
description: Network State presentation template system. Balaji's official slide design with evidence-backed layouts, full-text support, and Network State branding. USE WHEN network state slides, ns-slides, create network state presentation, ns presentation, balaji network state talk.
---

# NSSlides

Presentation slide system based on Balaji Srinivasan's official Network State slide templates. Evidence-first design with split layouts, device mockups, data visualizations, and consistent Network State branding.

NSSlides differs from the general BalajiSlides skill in that it **includes full body text on slides** alongside headlines and visuals, following Balaji's actual template system for Network State presentations.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/NSSlides/`

If this directory exists, load and apply any PREFERENCES.md or configurations found there.

## MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Running the WORKFLOWNAME workflow in NSSlides skill to ACTION"}' \
  > /dev/null 2>&1 &
```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CreateNSSlides** | "create ns slides", "network state presentation", "ns talk", "create network state slides" | `Workflows/CreateNSSlides.md` |

## Quick Reference

- **Layout:** Primary: Split layout (left text / right visual, ~40/60). Secondary: Full-screen evidence (dark bg).
- **Headlines:** Bold, 2-4 words max. Opinionated thesis statements.
- **Body text:** Short paragraphs allowed (unlike BalajiSlides). 2-4 sentences per slide, gray text.
- **On-slide text:** Headline + optional body paragraph. Minimal, clean.
- **Speaker notes:** All deep context and talking points go here.
- **Visuals:** Real artifacts only — screenshots, maps, charts, device mockups, data visualizations.
- **Background:** White/light gray for content slides. Black/very dark for data visualizations.
- **Typography:** Modern sans-serif (Inter, or similar), high contrast.
- **Branding:** Every slide includes Network State logo (bottom-left) + "ns.com" (bottom-right).

**Full Design Guide:** Read `DesignGuide.md` in this skill's root for complete style rules and slide templates.

## Examples

**Example 1: Create a Network State pitch deck**
```
User: "create ns slides for a network state investor pitch"
-> Invokes CreateNSSlides workflow
-> Loads DesignGuide.md for style rules
-> Structures numbered sequence (Section 1: What is Network State, Section 2: Economic Model, etc.)
-> Each slide: bold headline + 1-2 sentence body text + real visual artifact
-> Outputs Google Slides markdown format with Network State branding
```

**Example 2: Data explainer slide with map**
```
User: "make an ns-slides showing network state distribution by country"
-> Invokes CreateNSSlides workflow
-> Uses Pattern 2: Full-Screen Dark Data Slide
-> Dark background with world map visual taking 100% space
-> Left-overlay text: headline + explanatory paragraph
-> Footer: Network State + ns.com
```

**Example 3: Device mockup slide**
```
User: "ns-slides showing network state app on iPhone"
-> Invokes CreateNSSlides workflow
-> Uses Pattern 3: Device Mockup
-> Centered iPhone mockup with app UI screenshot
-> Caption below device with headline + short description
-> White background, clean and minimal
```
