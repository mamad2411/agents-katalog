---
name: nimbuu-ui-ux
description: "Nimbuu UI/UX Skill. Logic-driven interface design distilled from Refactoring UI, Practical UI, and Fundamentals of Creating a Great UI/UX. Three uses. (1) ALWAYS when starting a new project, greenfield app, landing page, or prototype with no design system, no tokens, no brand kit, so spacing, type, colour, hierarchy, and components come from a system instead of guesswork. (2) AUDITING an existing or large product: does the UX hold up, is the visual hierarchy right, are contrast and accessibility met, are forms, buttons, and copy sound, is the design system obeyed. (3) Any UI/UX question that should cite a rule and its rationale. Triggers: 'Nimbuu UI UX Skill', 'nimbuu ui', 'design system do zero', 'projeto novo sem design system', 'auditar UI', 'auditar UX', 'revisar a interface', 'a hierarquia ta certa', 'review this UI', 'audit this interface', 'is this UX sound', 'no design system', 'make this UI look designed', 'why does this UI look off'."
---

<!--
Cross-agent notes (informational; ignored by host agents):
  - Canonical path: ~/.agents/skills/nimbuu-ui-ux  (read by Codex, Copilot CLI, Amp)
  - Symlinked to ~/.claude/skills/nimbuu-ui-ux     (read by Claude Code)
  - Update in one place, both hosts see it.
  - `allowed-tools` intentionally omitted to stay host-neutral.
  - Published at github.com/Haamiahphp/nimbuu-ui-ux under MIT.
  - This is a synthesis, not an excerpt. Every rule carries a source tag. See README
    for attribution and links to buy the source books.
-->

# Nimbuu UI/UX

Interface design as a system of logical rules, not taste. Every detail has a rationale
you can state out loud. If you cannot say why a value is what it is, it is not designed
yet, it is guessed.

## Source keys

Every rule in this skill is tagged with where it comes from. Use these when citing:

| Key | Book | Weight |
|-----|------|--------|
| **RUI** | *Refactoring UI*, Adam Wathan & Steve Schoger (2018) | Highest for craft: hierarchy, colour construction, depth, polish |
| **PUI** | *Practical UI*, Adham Dannaway (2022) | Highest for usability + accessibility: forms, buttons, contrast, copy |
| **CT** | *Fundamentals of Creating a Great UI/UX*, Elisa Paduraru / Creative Tim (2022) | Component catalogue and page anatomy. Weakest on rigour; treat its 2021 trend advice as dated |

When two sources conflict, see **Where the sources disagree** below. Never silently pick
one, say which you followed and why.

## The five mental models

Everything else is downstream of these.

1. **Usability risk** (PUI). Judge every decision by the risk that someone struggles.
   Thin light-grey text, unlabelled icons, coloured headings that look like links: each
   is a risk you took for aesthetics. Take it knowingly or not at all.
2. **Interaction cost** (PUI). The sum of physical and mental effort to finish a task:
   looking, scrolling, reading, clicking, waiting, typing, thinking, remembering. It is
   measurable, so it is reducible. Keep actions near what they act on (Fitts), cut
   distractions, cut choices (Hick).
3. **Cognitive load** (PUI). Brain power spent operating the interface instead of doing
   the task. Reduce by removing styles and information, grouping, using familiar
   patterns, staying consistent, and giving the screen a clear hierarchy.
4. **Hierarchy is everything** (RUI). Most of what makes something "look designed" is
   not styling. It is that important things look important and everything else gets out
   of the way. When something will not stand out, de-emphasise its competitors instead
   of shouting louder.
5. **Systems over instances** (RUI + PUI). Never pick a value from an unlimited pool.
   Define a small set in advance for size, weight, line-height, colour, margin, padding,
   width, height, shadow, radius, border width, opacity. You do the hard thinking once
   instead of every time.

## Non-negotiables

These are the rules to apply without asking. They are cheap, and breaking them creates
real harm.

- **WCAG 2.1 AA is the floor.** 4.5:1 for text ≤18px, 3:1 for large text (≥24px regular
  or ≥18px bold) and for any non-decorative UI element: form borders, checkboxes, radio
  buttons, button shapes, icons that carry meaning. (PUI)
- **Never use colour alone** to convey state, meaning, or interactivity. Always pair with
  an icon, underline, border weight, shape, or text. (RUI + PUI)
- **No pure black, no pure-black-on-white, no pure-white-on-pure-black.** Use a very dark
  grey. The 0%/100% brightness gap causes eye strain and halation. (PUI + CT; RUI agrees
  greys should start from a very dark grey, not `#000`)
- **Labels above inputs, always.** Never placeholder-as-label. Single column form. (PUI)
- **Minimum target 48pt × 48pt**, minimum 8pt between adjacent targets, 16pt between
  buttons. (PUI)
- **Body copy ≥18px, line-height ≥1.5, line length 45 to 75 characters.** (PUI + RUI)
- **Two font weights.** Regular (400/500) and bold (600/700). Nothing under 400 for UI
  text. (RUI + PUI)
- **One typeface**, a neutral sans, until you have a reason. A second one is for headings
  only. (PUI)
- **Left-align text.** Centre only for headings and blocks of 2 to 3 lines or fewer.
  Right-align numbers in tables. (RUI + PUI)
- **Sentence case**, not Title Case. (PUI)
- **Spacing inside a group is always smaller than spacing around it.** Ambiguous spacing
  is a bug, not a style. (RUI + PUI)

## Starting a new project with no design system

This is the primary trigger for this skill. Full procedure with worked numbers is in
**`greenfield.md`**. The short form:

1. **Design a feature, not a shell.** Not the navbar. A real piece of functionality with
   real content. (RUI)
2. **Grayscale first, mobile width first.** ~400px canvas, no colour. Forces spacing,
   size, and contrast to carry the hierarchy. (RUI + PUI)
3. **Lock the spacing scale** before anything else: 8 / 16 / 24 / 32 / 48 / 80 pt.
   Never two adjacent values closer than ~25%. (PUI + RUI)
4. **Lock the type scale**: base 16 or 18px, ratio 1.200 to 1.250 for apps and
   dashboards, 1.333 to 1.500 for marketing. Round to whole px. Then hand-tune.
   Never `em` for the scale itself. (PUI + RUI)
5. **Lock the colour palette.** Two valid constructions, pick by product complexity:
   PUI's 5 variations of one hue (simple product, fastest, accessibility rules baked in),
   or RUI's 9-step ramps 100 to 900 (complex product, many semantic states).
   Full recipes in `chapters/ch05-colour.md`.
6. **Lock elevation and radius**: 3 shadows (small / medium / large), 3 radii
   (8 / 16 / 32pt for small / medium / large elements). Shadow colour is the darkest
   palette variation, never black. (PUI + RUI)
7. **Build the smallest components first** (button, input, avatar), compose upward into
   cards, then templates. (PUI)
8. **Write the usage rules down.** A system without usage guidelines is a pile of tokens.
   Minimum: what the brand colour may touch, what marks interactivity, button weights,
   spacing rules per level, capitalisation, alignment. (PUI)

## Auditing an existing product

The second primary trigger: a project already exists and the question is whether the UX,
the UI, and the hierarchy actually hold up. **Full protocol in `audit.md`.** The shape:

**Four passes, in this order.** Each is cheap and catches a different class of problem.
Do not jump to pass 3 because visual problems are the ones you can see.

1. **System integrity.** Is there a system at all, and does the product obey it? Count the
   distinct font sizes, weights, greys, spacing values, radii, and shadows actually
   rendered. A long tail of one-off values is the finding, and it is the one that explains
   most of the others. Check whether usage guidelines exist at all.
2. **Accessibility.** Who is locked out? Contrast on text **and** on form borders, buttons,
   checkboxes, and meaningful icons. Colour used as the only signal. Target sizes. Headings
   and link text that must survive being read out of context.
3. **Hierarchy and layout.** Squint test every key screen. Ambiguous spacing. Competing
   primary buttons. Brand colour on non-interactive elements. Alignment. White space.
4. **Flow and interaction cost.** Walk the flows, do not just look at screens. Count clicks,
   scrolls, typed characters, and decisions. Wrong controls, unnecessary fields, inline
   validation, errors that do not say how to fix things, destructive actions without
   friction or undo.

**Rank findings by harm, do not list them flat.** P0 locks people out or loses data. P1 is a
real usability cost for many people. P2 is system decay that compounds. P3 is polish. Report
P0 and P1 exhaustively, group P2 by pattern, sample P3.

**Close with the systemic finding, not the list.** If forty problems all trace back to "there
is no spacing scale and no usage guidelines", that is the finding and the forty are evidence.
`audit.md` has the criteria for when to recommend rebuilding the token layer instead of
patching instances.

## Diagnosing an interface that "looks off"

Faster than a full audit, for a single screen. Run in this order. Stop when it is fixed.

1. **Squint test.** Blur or zoom out. Can you still tell what matters? If everything has
   the same weight, the problem is hierarchy, not styling. (PUI)
2. **Ambiguous spacing.** Is any gap inside a group equal to or larger than the gap
   around it? Fix that first, it costs nothing. (RUI)
3. **Too many values.** Count distinct font sizes, weights, greys, radii, shadows. More
   than the system allows means collapse them. (RUI + PUI)
4. **Contrast.** Run the ratios. Form borders and icons fail more often than text. (PUI)
5. **Competing emphasis.** More than one primary button? Coloured non-interactive
   elements? Badges that look like buttons? De-emphasise, do not amplify. (PUI + RUI)
6. **Not enough white space.** Add space before adding anything else. Start with too
   much and remove. (RUI + PUI)
7. **Only then** reach for polish: accent borders, decorated backgrounds, supercharged
   defaults. See `chapters/ch13-finishing-touches.md`. (RUI)

## Where the sources disagree

Read this before quoting any single book as settled.

| Topic | The disagreement | What to do |
|---|---|---|
| **Justified text** | RUI: fine if you also hyphenate, good for print-like layouts. CT: recommends it for articles. PUI: never for long body text, the word-spacing rivers hurt dyslexic and cognitively impaired readers. | Follow **PUI**. Accessibility beats aesthetics. Justify only in a deliberately print-mimicking layout, with hyphenation on. |
| **Grids** | RUI: "grids are overrated", percentage widths make sidebars and cards resize wrongly, use fixed width + `max-width`. PUI and CT: align the main layout to 12 columns. | Both. **12-column grid for the page-level layout**, gutters and margins from your spacing scale. **Fixed or `max-width` for individual components** that have an optimal size. Never shrink a component until the screen forces it. |
| **Type scale** | PUI: ratio scale (1.250). CT: golden ratio 1.618. RUI: hand-craft, ratios give fractional px and too few sizes for UI. | Generate with a ratio, **round to whole px, then hand-tune**. Ratio for a starting shape, eyes for the final set. Golden ratio is too coarse for UI. |
| **Palette size** | RUI: 8 to 10 greys, 5 to 10 shades per colour, up to ten colours for a complex UI. PUI: one brand colour and five variations is enough. | **PUI for a new or simple product** (fewer decisions, usage rules included). **RUI when you outgrow it**: data viz, many semantic states, dense dashboards. Do not start at RUI scale. |
| **Button alignment** | PUI: left-align everywhere including dialogs (F-pattern, screen magnifiers miss right-aligned buttons). CT: forward on the right, back on the left (OS convention). | **PUI by default** for consistency across forms and dialogs. PUI itself notes the impact is small if hierarchy is correct, so follow an existing product convention rather than breaking it. |
| **Trend styles** | CT actively promotes glassmorphism, neumorphism, and 3D as things to integrate. PUI names both as styles where clear hierarchy and sufficient contrast are very hard to achieve. | **PUI.** CT's trend list is a 2021 snapshot, not guidance. Trendy effects age badly and usually cost contrast. |
| **Icon de-emphasis** | CT: drop icon opacity to 50 to 60%. RUI and PUI: hand-pick a lower-contrast colour; transparency washes colour out and lets backgrounds bleed through. | **Hand-pick a colour** from your palette (the medium variation). Opacity is the lazy version and it looks disabled. |
| **Contrast standard** | PUI introduces APCA (WCAG 3 draft) and shows where WCAG 2 gives the wrong answer, especially on dark backgrounds. RUI and CT only know WCAG 2. | **WCAG 2.1 AA is the compliance floor** for anything commercial. Check APCA too and prefer designs that pass both. On dark UI, trust APCA when they disagree and still meet WCAG 2 numerically. |
| **Placeholder text** | CT: example text in the placeholder speeds users up. PUI: never use placeholder instead of a label; its contrast is almost always inaccessible. | **Label above the field, always.** A placeholder may exist *in addition*, and only if it clears 4.5:1. Search fields are the one reasonable exception. |
| **Disabled buttons** | CT lists "disabled" as a normal button state. PUI: avoid them; they strand users, fail contrast, and are not keyboard focusable. | **PUI.** Enable the button and validate on submit. If you must disable, put the reason next to it and keep it focusable. |

## Chapter index

Load on demand. Each chapter tags every rule with RUI / PUI / CT.

| File | Covers |
|---|---|
| `greenfield.md` | Step-by-step build of a design system from zero, with worked numbers |
| `audit.md` | Full review protocol for an existing product: four passes, severity ranking, report shape |
| `cheatsheet.md` | Every number in one place: scales, ratios, sizes, thresholds |
| `chapters/ch01-foundations.md` | Usability risk, interaction cost, cognitive load, the named laws, how to start a design |
| `chapters/ch02-design-system.md` | Predefined options, modular components, usage guidelines, consistency |
| `chapters/ch03-hierarchy.md` | Visual hierarchy, emphasis and de-emphasis, labels, semantics vs. styling, squint test |
| `chapters/ch04-layout-spacing.md` | Grouping (Gestalt), spacing scale and application, grids, alignment, white space, box model |
| `chapters/ch05-colour.md` | HSL/HSB, palette construction (both recipes), greys, contrast, dark mode, system colours |
| `chapters/ch06-typography.md` | Typeface choice, type scale, weights, line-height, line length, alignment, letter-spacing |
| `chapters/ch07-depth.md` | Light source, shadows, elevation, flat depth, overlap, gradients, radius |
| `chapters/ch08-forms.md` | Layout, labels, required/optional, field width, controls, validation, errors |
| `chapters/ch09-buttons.md` | Three weights, common mistakes, disabled buttons, alignment, target size, destructive friction |
| `chapters/ch10-copy.md` | Concision, sentence case, front-loading, inverted pyramid, link text, numerals |
| `chapters/ch11-images-icons.md` | Photos, text on images, intended size, user content, icon systems, illustrations |
| `chapters/ch12-components.md` | Navbar, header, cards, tables, charts, sidebar, footer, wizard, timeline, testimonials, empty states |
| `chapters/ch13-finishing-touches.md` | Supercharged defaults, accent borders, decorated backgrounds, fewer borders, breaking the mould |
| `glossary.md` | Every named term and law with its source |

## How to use this skill

- **Building UI**: read `greenfield.md` if there is no system yet, otherwise `cheatsheet.md`
  plus the one or two chapters the task touches. Do not load everything.
- **Auditing an existing product**: read `audit.md` and work its four passes. Keep
  `cheatsheet.md` open for the thresholds. Open a chapter only for findings you need to
  explain in depth.
- **Reviewing a single screen**: run the diagnosis order above, then open the chapter for
  whatever failed.
- **Answering a question**: cite the source key. If sources conflict, say so.
- **Applying a rule**: state the rationale. "16pt because it groups the label with its
  input and the next group is 32pt away" beats "16pt looks right".
