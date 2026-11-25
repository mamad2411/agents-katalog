---
name: master-and-layout-mapper
description: Maps every slide onto the correct master layout with the right placeholders so the deck is structurally on-template before any styling.
---

# Master and Layout Mapper

## When to use

Use this skill when content has been dropped onto blank slides instead of the template's defined layouts. A common symptom is a deck where every slide is technically a "Blank" or "Title and Content" layout but the real content is a tangle of free-floating text boxes. Run this first, before any color, font, or logo work, because every later fix is easier once each slide sits on the right master layout.

## What it does

It produces a slide-by-slide mapping from each current slide to the correct layout in the brand template, then applies that layout so the right placeholders, background, and built-in styling appear. The output is a deck where each slide is on its intended layout (Title, Section Header, Title and Content, Two Content, Comparison, Divider, Closing, and so on) rather than on a blank canvas.

## Method

Work from the template's slide master and its child layouts, not from the individual slides.

1. **Read the master and its layouts.** List every layout the template defines and what it is for. A typical corporate template has: a Title slide, a Section Header or Divider, a one-content layout, a two-content layout, a Comparison layout, a content-with-caption layout, a full-bleed image layout, an agenda layout, and a Closing or Contact layout. Note the placeholders each layout carries (title, subtitle, body, content, picture, footer, date, slide number).

2. **Classify each existing slide by its real job.** Ignore how it was built and ask what the slide is doing: opening the deck, dividing a section, presenting a single idea, comparing two things, showing one chart, showing a full-bleed image, summarizing, or closing. Write the intended layout name next to each slide.

3. **Match job to layout.** Map each slide's job to the closest template layout. A single-chart slide maps to the one-content layout. A side-by-side maps to Two Content or Comparison. An image-only slide maps to the full-bleed image layout. A "thank you" slide maps to Closing.

4. **Apply the layout.** For each slide, change its layout to the mapped layout (in PowerPoint, Home then Layout, or right-click then Layout). This brings in the layout's placeholders and background. Do not yet move content into them; that is the Placeholder Discipline skill's job. Here you only set the correct layout.

5. **Flag mismatches.** When a slide does not fit any layout cleanly (for example a custom dashboard), note it as a candidate for the closest layout plus manual adjustment, rather than forcing it onto a wrong layout.

6. **Reset stray overrides.** If a slide has a manually painted background or a hidden background graphic that conflicts with the layout, flag it for reset so the layout's real background shows through.

Ground the mapping in the template's own naming. If the template names a layout "Section Divider," use that name in the output so the user can find it in the layout gallery.

## Inputs

- The deck to fix (or a description of its slides).
- The brand template (.potx or .thmx) or a list of its layout names and the placeholders each one carries. If the template is not provided, ask for the layout list before mapping.

## Output format

A numbered mapping table rendered as prose or a list, one row per slide:

- Slide number and a short label.
- Current layout (often "Blank" or wrong).
- Correct layout from the template.
- One-line reason.
- A flag if the slide needs manual attention.

End with a short "apply order" note: which slides are clean swaps and which need a human eye.

## Example

Input: a 14-slide deck where slides 1, 5, and 9 are section openers built as blank slides with a big text box, and slides 2 to 4 are single charts on blank canvases.

Output (excerpt):

- Slide 1. "Title." Current: Blank. Correct: Title slide. Reason: opens the deck, needs the title and subtitle placeholders. Clean swap.
- Slide 2. "Revenue by region." Current: Blank. Correct: Title and Content. Reason: one chart under one action title. Clean swap.
- Slide 5. "Part 1. Market." Current: Blank. Correct: Section Header. Reason: divides a section. Clean swap.
- Slide 9. "Part 2. Operations." Current: Blank. Correct: Section Header. Clean swap.

Apply order: swap slides 1, 2 to 4, 5, and 9 directly. Slide 11 (custom dashboard) maps to Title and Content but keep the custom grid and adjust by hand.
