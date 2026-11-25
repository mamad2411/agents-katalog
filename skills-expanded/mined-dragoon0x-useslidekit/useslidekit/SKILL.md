---
name: useslidekit
description: "Comprehensive presentation design skill for Claude Code. Projection-aware design, audience-adaptive layouts, narrative architecture, perceptual data visualization, anti-AI-slop detection, rehearsal intelligence, and multi-format export. Complements Anthropic's built-in PPTX skill."
version: 1.0.0
---

# useSlideKit

## When to Use

Activate when the user asks to create, improve, redesign, or review a presentation,
deck, slides, pitch, or keynote. This skill handles content strategy, design precision,
and quality assurance. It complements (never conflicts with) Anthropic's built-in PPTX
skill which handles file generation.

## Quick Start

1. **Identify audience** → Load references/AUDIENCE.md, select profile
2. **Structure narrative** → Load references/NARRATIVE.md, choose framework
3. **Design slides** → Load references/DESIGN-SYSTEM.md for visual rules
4. **Add data** → Load references/DATA-VIZ.md for chart precision
5. **Add motion** → Load references/MOTION.md for animation rules
6. **Write speaker notes** → Load references/SPEAKER.md for rehearsal prep
7. **Quality check** → Load references/RUBRIC.md, score, refine if < 80
8. **Anti-slop scan** → Load references/ANTI-SLOP.md, fix detections
9. **Glance test** → Load references/GLANCE-TEST.md on every slide
10. **Export** → Load references/EXPORT.md for format-specific rules

## Core Principles

### The Glance Test (applies to every slide)

A person should understand the slide's point in 3 seconds. Not read every word.
Understand the point. If they can't, the slide has too much content, unclear hierarchy,
or a topic-label heading instead of an assertion heading. See references/GLANCE-TEST.md.

### Audience-First Design

Every design decision — density, typography, color, animation, speaker notes — changes
based on who is watching. An investor deck is not a conference talk is not a team update
is not a workshop handout. Load references/AUDIENCE.md FIRST. Everything else follows.

### Projection-Aware Color

Screens emit light. Projectors reflect it. This means: lower contrast in bright rooms,
color temperature shifts, washed-out pastels. Every color choice must account for the
viewing environment. See references/DESIGN-SYSTEM.md §2.

### Assertion Headlines

Every slide title is a complete sentence stating the takeaway. Not "Revenue" but
"Revenue grew 34% year-over-year driven by enterprise expansion." The headline IS
the message. The body is evidence. If you read only the headlines in sequence, you
should understand the entire presentation. This is the Ghost Deck Test.

## Intake Questions (ask before building)

| # | Question | Default if unanswered |
|---|----------|----------------------|
| 1 | Who is the audience? | General professional |
| 2 | What is the one thing you want them to DO after? | Understand and agree |
| 3 | Presentation or async reading? | Presented live |
| 4 | Projector, screen, or both? | Screen (laptop/monitor) |
| 5 | Duration? | 15 minutes |
| 6 | How many slides max? | 12-15 |
| 7 | Brand colors/fonts? | Neutral dark theme |
| 8 | Data available? | No — use narrative evidence |
| 9 | Tone? | Confident, clear, direct |
| 10 | Export format? | PPTX |

## Workflow

```
INTAKE → AUDIENCE PROFILE → NARRATIVE FRAMEWORK → OUTLINE
→ SLIDE DESIGN → DATA VIZ → SPEAKER NOTES → MOTION
→ GLANCE TEST → ANTI-SLOP SCAN → RUBRIC SCORE → EXPORT
```

### Stage 1: Intake & Audience Profile
Gather answers to 10 questions. Load references/AUDIENCE.md. Select the matching
profile (investor, conference, internal, workshop, async). The profile sets defaults
for density, typography scale, animation level, and speaker note depth.

### Stage 2: Narrative Architecture
Load references/NARRATIVE.md. Choose the right framework based on purpose:
- Persuade → Problem-Agitation-Solution (PAS)
- Inform → Situation-Complication-Resolution (SCR)
- Teach → What-So What-Now What
- Sell → Before-After-Bridge
Select framework, write the 1-sentence thesis, build the 3-5 point structure.

### Stage 3: Outline & Slide Titles
Write assertion-headline for every slide. Run the Ghost Deck Test: read only
the headlines in order. Do they tell the complete story? If not, restructure.
Reference: SLIDE-PATTERNS.md for per-slide-type specs.

### Stage 4: Slide Design
Load references/DESIGN-SYSTEM.md. Apply typography scale, color system,
spacing grid, and layout rules from the audience profile.

### Stage 5: Data Visualization
Load references/DATA-VIZ.md. For every data point: select chart type from the
decision matrix, apply perceptual encoding rules, add annotations.

### Stage 6: Speaker Notes
Load references/SPEAKER.md. Generate per-slide notes with timing, transition
cues, and key phrases. Add Q&A prep for predictable questions.

### Stage 7: Motion Design
Load references/MOTION.md. Add entrance animations for content reveals,
transitions between slides, and chart build sequences. Respect reduced-motion.

### Stage 8: Quality Assurance
1. Run the Glance Test on every slide (references/GLANCE-TEST.md)
2. Run the Anti-Slop scan (references/ANTI-SLOP.md)
3. Score with the 100-point rubric (references/RUBRIC.md)
4. If score < 80, identify 3 weakest areas, fix, re-score (max 2 iterations)

### Stage 9: Export
Load references/EXPORT.md. Generate in requested format.
Use Anthropic's built-in PPTX skill for .pptx file creation.

## Reference Files (loaded on demand)

| File | What It Contains | Load When |
|------|-----------------|-----------|
| references/AUDIENCE.md | 7 audience profiles with complete design presets | Always — load first |
| references/NARRATIVE.md | 4 storytelling frameworks with selection criteria | Stage 2 |
| references/DESIGN-SYSTEM.md | Typography, color, spacing, layout — projection-aware | Stage 4 |
| references/COLOR-PALETTES.md | 12 complete themed palettes with screen + stage variants | Stage 4 |
| references/TYPOGRAPHY-DEEP.md | Font pairing matrix, weight mapping, hierarchy system, number typography | Stage 4 |
| references/SLIDE-PATTERNS.md | 9 per-slide-type specs with exact measurements | Stage 3-4 |
| references/DATA-VIZ.md | Chart selection matrix, annotation rules, perceptual encoding | Stage 5 |
| references/TABLES.md | Table design, number formatting, comparison table patterns | Stage 5 |
| references/ICONOGRAPHY.md | Icon sizing, style rules, circle treatment, source libraries | Stage 4-5 |
| references/SPEAKER.md | Rehearsal intelligence, timing, transitions, Q&A prep | Stage 6 |
| references/MOTION.md | Animation timing, easing, transition rules | Stage 7 |
| references/TRANSITIONS.md | Pacing curve, slide pairs, transition phrases, flow anti-patterns | Stage 7 |
| references/GLANCE-TEST.md | 3-second comprehension test methodology | Stage 8 |
| references/ANTI-SLOP.md | 30 AI presentation slop patterns with detection/fixes | Stage 8 |
| references/RUBRIC.md | 100-point quality scoring with testable criteria | Stage 8 |
| references/CHECKLIST.md | 40-item pre-flight checklist (content, visual, structural, export) | Stage 8 |
| references/ACCESSIBILITY.md | WCAG contrast, color blindness, cognitive load, alt text | All stages |
| references/VIRTUAL.md | Zoom/Teams/Meet-specific design rules and sizing | Stage 4 (if virtual) |
| references/INDUSTRY.md | Industry-specific patterns for 7 sectors | Stage 2-4 |
| references/HANDOUT.md | Adapting a presentation into a self-contained leave-behind | Stage 9 |
| references/CONTENT-DENSITY.md | Exact word/bullet/element counts per audience × slide type | Stage 3-4 |
| references/WHITESPACE.md | 30% rule, spacing hierarchy, breathing slides, margin specs | Stage 4 |
| references/IMAGE-TREATMENT.md | Crop rules, overlay opacities, resolution requirements, screenshot treatment | Stage 4-5 |
| references/CODE-SLIDES.md | Code formatting, syntax highlighting palettes, terminal styling | Stage 4 (if code) |
| references/BRAND-ADAPTATION.md | Brand audit checklist, color/font/logo adaptation rules | Stage 1-4 |
| references/RESPONSIVE.md | Aspect ratio handling, safe zones for multi-ratio | Stage 4 |
| references/OPENING-SLIDES.md | First 3 slides methodology, hook types, problem framing | Stage 3 |
| references/CLOSING-SLIDES.md | Last 3 slides, CTA patterns, Q&A handling | Stage 3 |
| references/PACING-CALCULATOR.md | Duration planning, per-slide timing, pacing patterns | Stage 6 |
| references/NUMBER-FORMATTING.md | Display rules, alignment, change indicators, precision, context | Stage 4-5 |
| references/DIAGRAM-PATTERNS.md | Process, hierarchy, funnel, matrix, cycle, architecture diagram specs | Stage 4-5 |
| references/LANGUAGE-PRECISION.md | Headline formulas, bullet compression, words to delete | Stage 3-4 |
| references/EXPORT.md | Multi-format output rules (PPTX, HTML, PDF) | Stage 9 |

---
*useSlideKit by Dragoon0x. Educational and experimental. DYOR.*
