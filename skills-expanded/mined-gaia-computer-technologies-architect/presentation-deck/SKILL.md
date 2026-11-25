---
name: presentation-deck
description: Plans a slide deck or set of presentation boards for a specific audience — client meeting, planning committee, design review panel, competition jury, or pin-up — as a slide-by-slide storyline stating what each slide must prove, the image or drawing it needs, and speaker notes, plus a board layout when the output is printed boards. Use when the architect wants a "presentation", "deck", "boards", "pin-up", "structure my slides", "planning committee presentation", or "competition panels". Hands the written argument to concept-narrative, images to render-prompt, and the hard questions to design-critique; can build boards in Figma or Miro if their MCP is connected.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Presentation Deck

A presentation is an argument made with images. Each slide has one job: to prove one thing to this audience. Decks fail when they show everything that was drawn rather than what the room needs to decide. This skill plans the argument first, then the images, then the words.

## When to use

- Before a client presentation, design review, planning committee, pre-app, or competition submission.
- When the architect has a pile of drawings and renders and needs an order.
- Laying out A1 / A0 boards or digital panels for a jury or exhibition.

## Input

- **Audience and decision.** Who is in the room and what they must decide or feel at the end (approve Stage 2, grant permission, shortlist, choose option B).
- **Format and limits.** Slide count, time slot, board count and size, submission rules (competitions often fix panel count, size, fonts, and anonymity).
- **Material available.** Drawings, diagrams, renders, models, photos, precedents. List what exists; the plan should use it.
- **The argument.** The concept narrative or the one-sentence idea. If none exists, hand to `concept-narrative` first or infer it and say so.
- **Known concerns.** Objections, client worries, officer comments, jury criteria.

## Process

1. **Write the one sentence.** What should the audience believe when you finish? Everything serves that.
2. **Build the storyline before the slides.** A reliable spine for design presentations: context → problem / brief → idea → how the idea works (plan, section, sequence) → what it is like (experience, materials) → how it answers their concerns → what we need from you. Adjust per audience:
   - **Client** — lead with their brief and decisions needed; options side by side; cost and programme implications flagged.
   - **Planning committee / officers** — site and policy context first, then design response, then impacts (neighbours, heritage, townscape). Use verified, accurate views; avoid flattering renders that misrepresent scale.
   - **Design review panel** — the idea and its rigour; show the working, not just the result.
   - **Competition jury** — read in seconds; the idea must land from one image and one sentence.
3. **One slide, one claim.** For each slide write: the claim (a full sentence, not a topic), the evidence (which drawing or image proves it), and speaker notes. If a slide has no claim, cut it.
4. **Image list.** For each slide, name the existing asset or the gap ("need: sectional perspective through courtyard, dusk"). Hand gaps to `render-prompt` or the drawing team.
5. **Rehearse the hard question.** Add a backup slide for the objection most likely to come up; use `design-critique` to find it.
6. **Boards.** For printed panels, lay out the reading order (top-left to bottom-right), the hero image, the one-line idea at large size, and a consistent grid and scale bar for drawings.
7. **Build, if tools are connected.** If a Figma or Miro MCP is connected, offer to create frames for each slide or board with titles, claims, and image placeholders. Otherwise output the plan for the architect's own tool (InDesign, Keynote, PowerPoint, Google Slides).

## Domain knowledge

- **Time.** Roughly one to two minutes per content slide is a common working pace; for a 10-minute slot, plan eight to twelve slides. Say this is a rule of thumb.
- **Drawings over renders for credibility.** Plans and sections convince technical audiences; renders persuade lay audiences but invite suspicion if they flatter.
- **Accurate visual representation.** Planning and heritage contexts may expect verified views or a stated methodology for visualisations. Never present an AI image as a verified view.
- **Titles are claims.** "The courtyard brings south light to every flat" beats "Courtyard".
- **Consistency.** One typeface family, one north arrow, one scale-bar style, consistent drawing scales across options.

## Output format

```
DECK PLAN — [Project] — [Audience] — [Date]
Decision sought: [ ]
The one sentence: [ ]
Format: [n slides / n boards at size], [time slot]

| # | Claim (slide title) | Evidence / asset | Status | Speaker notes |
| 1 | [ ] | [drawing/render ref or NEED: ...] | have / need | [2–3 lines] |

BACKUP SLIDES
- [anticipated question] → [slide content]

IMAGE GAPS
- [description of image needed] → [render-prompt / drawing team]

BOARD LAYOUT (if boards)
[reading order, hero image position, grid, text hierarchy]
```

## What you don't do

- Don't invent project facts, areas, costs, or consultation outcomes for slides. Placeholders and a list of what to confirm.
- Don't present AI renders as verified views or as representing approved designs.
- Don't fill slides to fill time. Cut anything that doesn't prove the claim.
- Don't write the full narrative here — hand to `concept-narrative`.
- Don't make claims of policy compliance on a slide. "Responds to [policy]" with the officer's assessment to follow.
