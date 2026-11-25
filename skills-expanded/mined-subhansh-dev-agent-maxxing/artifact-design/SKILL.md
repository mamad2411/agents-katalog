---
name: artifact-design
description: Design artifacts with deliberate palette, typography, and layout choices — avoid templated AI-generated designs.
---

# Artifact Design — Deliberate Design Choices

Extracted from Claude Code's bundled `artifact-design` skill.

## Core Principle

Approach as the design lead at a small studio known for versatility, giving every client a visual identity pitched at the treatment the task actually calls for. Make deliberate choices about palette, typography, and layout that are specific to this subject. Avoid templated designs.

## Read the Request First

Calibrate treatment, not whether to design. A doc deserves the same craft as a landing page — what changes is the treatment.

Many requests call for a utilitarian treatment: a plan, a memo, a demo. Make it polished with real typographic hierarchy, considered spacing, and a proper palette, but avoid over-designing. Most pages do not need a flashy hero.

Some requests call for an editorial treatment: a landing page, a game, an app or tool they'll keep or share.

When unsure: a well-composed page is never the wrong answer; an over-designed visual identity sometimes is.

## Fundamentals for Every Artifact

### Honor What's Already There
Look for an existing design system first. When one exists, apply it; everything below fills gaps and never overrides. Precedence: user's words → project's system → your choices.

### Ground It in the Subject
If the subject isn't already clear, pin it: one concrete subject, its audience, and the page's single job. The subject's own world — its materials, instruments, vernacular — is where distinctive choices come from. Build with real content throughout, never lorem.

### Pair Typefaces
Typography carries the page. Inline the face as a @font-face data URI. Keep running text near 65 characters wide; set a type scale and stay on it; give headings `text-wrap: balance`, body text room to breathe, and uppercase labels a touch of letter-spacing.

### Choose Neutrals, Don't Default to Them
A pure mid-grey reads as unconsidered; a grey with a slight hue bias toward the page's accent reads as chosen. Pure white and near-black are fine grounds when they suit the subject.

### Let Layout Do the Spacing
Lay out sibling groups with flex or grid and `gap`, not per-element margins. Wide content gets `overflow-x: auto`. Use `font-variant-numeric: tabular-nums` wherever digits line up.

### Avoid AI-Generated Design
AI-generated design clusters around:
- Warm cream (#F4F1EA) with serif display and terracotta accent
- Near-black with lone acid-green or vermilion pop
- Purple-to-blue gradient hero on white
- Inter or Space Grotesk as the "safe" face
- Emoji as section markers
- Everything centered
- `rounded-lg` everywhere
- Accent bar/rail on rounded cards

Where the user pins down a direction, follow it exactly. Where nothing is specified, don't spend that freedom on defaults.

### Build Cleanly
Close every non-void element, double-quote attributes, give keyboard focus a visible state, respect `prefers-reduced-motion`. For generative graphics, use Canvas or WebGL rather than hand-authoring SVG paths.

### CSS Rules
Watch selector specificities. Structure the cascade so it doesn't silently undo your spacing.

### Writing the Copy
Words are design material, not decoration. Write from the user's side of the screen — name things by what people recognize, not how the system is built. Active voice. Errors explain what went wrong and how to fix it.

### Structure is Information
Structural devices should encode something true about the content, not decorate it. Numbered markers only make sense if content is actually a sequence.

### When It's a UI, Not a Document
Surface the summary before the detail. Encode state in form as well as number. Semantic color is separate from accent. Give sparklines the same care as type.
