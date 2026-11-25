---
name: frontend-design
description: "Distinctive, intentional visual design for new or reshaped UI (pages, sites, apps, components). Use for aesthetic direction that avoids templated AI defaults. Not for quick polish passes."
license: Complete terms in LICENSE.txt
---

# Frontend Design

Approach this as the design lead at a studio known for giving every client a distinct visual identity. This client has already rejected proposals that felt cliché or templated and is paying for a point of view: make deliberate choices about palette, typography, and layout that are specific to this brief, and take aesthetic risk when it's justified.

## Ground the design in the subject

If the brief doesn't say what the product or subject is, propose one concrete subject, audience, and primary job, and confirm it. Use anything in memory about the client's preferences or project as a hint. The subject's industry, materials, and vernacular are where distinctive choices come from: a toy for girls aged 8 to 11 looks nothing like a dashboard for financial analysts. Use the brief's real content throughout.

## Design principles

The hero is seen first. Open with the most characteristic thing in the subject's world, in whatever form fits: headline, image, animation, live demo, interactive moment. A big number with a small label, supporting stats, and a gradient accent is the default treatment; use it only if it's truly the best option.

Typography carries the personality. Use one family or two, and if two, make them clearly distinct. Choose faces deliberately rather than the ones you'd reach for on any project, and set a clear scale following The Elements of Typographic Style, with intentional weights, widths, and spacing. When type is a headline or visual element, make the treatment an active part of the design. Keep lines under 80 characters; serif body can run slightly longer and wants slightly more line-height than sans.

Avoid these default typographic treatments, the commonest tells of a generated page:
- Accenting a single word or phrase in a headline (italic, bold, or a different color).
- All caps for labels.
- Unnecessary labels above content.

Visual structure is information. Borders, numbering, eyebrows, dividers, and labels should encode something about the content, not decorate it. Numbered markers (01 / 02 / 03) only fit content that really is a sequence, like steps or a timeline.

Use non-user-triggered motion sparingly, only to draw attention. One orchestrated moment (a page-load sequence or one reveal) lands better than scattered effects; fade-and-slide-up on every section and hover transitions on every card read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed.

## Process: plan, review against the brief, build, critique

For calibration, AI-generated design currently clusters around these traits:
1. a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta or warm-clay accent (often near #D97757, Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell);
2. a near-black background with a single bright acid-green or vermilion accent;
3. a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns;
4. the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration;
5. template chrome that appears whatever the subject: a tracked-out ALL-CAPS eyebrow above every heading; meta strings joined with middle dots ('A · B · C'); labels built as 'WORD — fragment' with a spaced em dash; tinted near-black (#0B0B0B, #111) standing in for black; a monospace face for small data labels; a '→' appended to link and button text.

All are legitimate for some briefs, but they are defaults rather than choices. Where the brief pins down a visual direction, follow it exactly, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults. Balance doing what you're good at with treating each project as a chance to experiment.

Work in two passes. First, write a short design plan as a compact token system:
- Color: the base palette as 4 to 6 named hex values.
- Type: the typefaces and their roles.
- Layout: a concept in one-sentence descriptions and ASCII wireframes to compare options, including alignment (left, center, justified).
- Principles: what makes this page unique.

Then review the plan against the brief before building. If any part reads like the default you'd produce for any similar page (run a similar prompt in your head and see if you land in the same place), revise it and say what changed and why. Only then write the code.

In CSS, watch selector specificity: classes easily cancel each other out (a type-based `.section` against an element-based `.cta`), especially with padding and margin between sections.

## Restraint and self-critique

Spend your boldness in one place. Let one element be memorable, keep everything around it quiet, and cut decoration that doesn't serve the brief. Build to a quality floor without announcing it: responsive to mobile, visible keyboard focus, reduced motion respected, accessible contrast, a harmonious palette. Critique as you build, with screenshots if the environment supports it. Before leaving the house, look in the mirror and remove one accessory. If you have somewhere to jot notes about what you've tried, use it so future passes try something new.

## Writing in design

Words are design content: they exist to make the interface easier to understand and use. Before writing, ask what the design needs to say.

- Write from the user's side, in plain language. A user manages notifications, not webhook config. Describe what something does rather than selling it; specific beats clever.
- Active voice. A CTA says exactly what happens ("Save changes", not "Submit"), and an action keeps its name through the flow: "Publish" leads to "Published".
- Errors say what went wrong and how to fix it, without apologizing or being vague. An empty screen is an invitation to act.
- Conversational tone: plain verbs, sentence case, no filler, matched to brand and audience. Each element does one job.
