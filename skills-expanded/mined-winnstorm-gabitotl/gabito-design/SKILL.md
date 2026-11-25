---
name: gabito-design
description: Design judgment for any visual, layout or design task: UI, web pages and components, Word/docx, PowerPoint/pptx slides, PDF, spreadsheets/xlsx, charts and dashboards, diagrams, images, logos and posters. Use it for design, redesign, style, restyle, critique, audit, polish, layout, typography, color, "make it look better" or "make it less generic". Apply it alongside the format-specific skill (docx, pptx, pdf, xlsx) that produces the file; this one decides how it should look.
license: Apache-2.0
metadata:
  author: gabitotl
  version: "1.0"
  optional: "true"
---

# GabitoDesign: make visual work look intended

You decide how something should look and why. A format skill (docx, pptx, pdf,
xlsx, a web framework) only produces the file; use both when both apply.

## How to work

1. **Know the surface.** What is it, who reads or uses it, what must they do or
   understand, in which medium and size? If you cannot say it in one sentence, ask
   one question before designing.
2. **Pick the mode** (below) and the module for the medium.
3. **Reuse the project's design decisions.** If `DESIGN.md` exists at the project
   root, read it and follow it. If not and the work is more than a one-off, run
   the `context` command and record the decisions there (template in
   `references/design-md.md`).
4. **Decide, then build.** Choose type scale, color roles, spacing, and the one
   focal point before writing markup, slides or cells. Use real content, never
   lorem ipsum.
5. **Review before handing over.** Walk the quality floor and the anti-patterns
   of the module. Fix, then say what you chose and why in two or three lines.

## Modes: pick by the surface

| Mode | Surface | Optimize for |
|---|---|---|
| Persuade | marketing page, landing page, pitch deck, poster, ad | one message, emotion, a clear next step |
| Experience | immersive product, onboarding, portfolio, editorial site, game UI | flow, pacing, memorable moments |
| Operate | dashboard, tool, admin, form, data table, spreadsheet | speed, density, error-free repetition |
| Read | long document, report, article, docs, ebook, README | comfort over time, scanability, trust |

A surface can mix two (a landing page with a pricing table); the dominant job
sets the mode and the other adjusts details. Read `references/modes.md` when
unsure or when the user asks for a different feel.

## Modules: load the one that matches the medium

| Medium | File |
|---|---|
| Web pages, apps, components, CSS | `references/web-ui.md` |
| Word, PDF, reports, letters, one-pagers | `references/documents.md` |
| PowerPoint, Keynote, slides, decks | `references/presentations.md` |
| Spreadsheets, charts, dashboards, tables | `references/data-charts.md` |
| Diagrams, flows, architecture, maps | `references/diagrams.md` |
| Images, logos, icons, posters, covers | `references/images.md` |

Every module has principles, a quality floor and its own anti-patterns. The
cross-medium list of generic-output tells is in `references/anti-patterns.md`.

## Commands: invoked by naming them

Say "gabito-design critique", "gabito-design polish the pricing page" or just
"critique this". The steps, when to use each and the done-criteria are in
`references/commands.md`; open it when a command is named.

| Command | Use it to |
|---|---|
| context | record or refresh the project's design decisions in `DESIGN.md` |
| document | write the decisions of an existing design into `DESIGN.md` |
| extract | pull repeated values and patterns into tokens or components |
| shape | plan structure and content before any visuals |
| craft | build a new piece end to end |
| critique | judge a design against its goal and propose fixes |
| audit | check accessibility, consistency, responsiveness, performance |
| polish | final pass on spacing, alignment, states, details |
| distill | remove everything that does not serve the goal |
| harden | make it survive real content, errors, edge cases |
| onboard | design first-run, empty states and guidance |
| bolder | raise energy and contrast when it is timid |
| quieter | reduce noise and intensity when it shouts |
| animate | add purposeful motion |
| colorize | add or fix color with roles and contrast |
| typeset | choose and tune type |
| layout | fix structure, grid, rhythm and hierarchy |
| delight | add small, earned moments of personality |
| overdrive | push one piece to an ambitious technical or visual level |
| clarify | fix confusing copy, labels and instructions |
| adapt | adjust to another size, medium, context or audience |
| optimize | cut weight, load time, file size or cognitive load |
| variants | produce distinct alternatives to compare |

Without a command, run `shape` mentally for new work and `critique` for existing work.

## Universal quality floor

Every output, in every medium, clears these before it ships.

- **One focal point.** Squint: the eye lands on the most important thing first,
  then the second. Size, weight, color and space create rank; do not give three
  elements the same loudness.
- **Hierarchy in few steps.** Three to five text levels. Each step is clearly
  different (a ratio of about 1.2 to 1.5), never nearly equal.
- **A spacing scale.** Pick a base unit (4 or 8) and use multiples. Related items
  sit closer than unrelated ones; the gap tells the grouping.
- **A grid and alignment.** Shared edges, consistent margins. Center only short,
  single-focus content; left-align running text.
- **A type scale and measure.** Two families at most; body 45 to 75 characters
  per line, line height 1.4 to 1.6 for body; real minimum sizes (screen body
  16 px, print body 10 to 12 pt, slide body 24 pt).
- **Color with roles.** Neutral base, one primary, one or two semantic colors
  (success, warning, danger). Color is never the only carrier of meaning.
- **Contrast.** WCAG 2.2 AA: 4.5:1 for body text, 3:1 for large text, icons and
  component boundaries; focus is visible. Check both light and dark when both exist.
- **Restraint.** Fewer colors, fonts, effects and borders than you think. Every
  decoration must earn its place; remove the last one you added.
- **Real content and states.** Use true text, numbers, names and lengths. Design
  empty, loading, error, long and short cases, not only the happy one.
- **Accessibility by default.** Semantic structure, alt text or captions, reading
  order, keyboard use, touch targets of at least 24 px (44 px preferred), reduced motion.
- **Consistency.** The same thing looks the same everywhere. Reuse tokens.

## Rules of engagement

- Defaults are not decisions. When you pick a font, color or layout, know why.
- Ask when the goal or audience is unclear; otherwise choose and explain.
- Respect an existing brand, template or design system over your taste; extend it.
- Match effort to the request: a quick fix gets a quick fix, not a redesign.
- Load `references/<x>.md` only when needed; do not read them all.
- Never claim a visual result you did not verify: render, screenshot or open the
  file when you can, and say so when you could not.

## Credit

GabitoDesign is an original work inspired by Impeccable by Paul Bakaus (Apache-2.0, https://impeccable.style). No Impeccable text or code is included.
