---
name: ui-design
description: Design rules against generic AI-looking interfaces, for marketing sites, app screens and dashboards. Covers direction and page structure, tells to avoid, layout, color, typography, tokens, imagery, mobile, states, copy, accessibility, a scored self-check, an audit mode and a launch checklist. Use whenever a task creates, changes, audits or redesigns UI (a page, component, layout, colors, fonts or interface copy), and before saying a site is done.
---

# UI design

A visitor never reads the code. In a few seconds they spot a handful of details, often without being able to name them, and decide how serious the site is. The goal is an interface that could only belong to this project.

The rule behind everything below: every visible element is a choice. Most patterns in `tells.md` are fine when someone decided them for a reason. Stacked by default, they sign a site nobody designed.

Files in this skill's folder:

- `tells.md`: the patterns that make a site look generated. Read it before building, and at the self-check.
- `components.md`: read it when building forms, buttons, navigation, header and footer, modals, toasts, tables, dashboards or app screens.
- `launch-checklist.md`: read it before saying a site is done.

## Modes

- **Build** (default): sections 1 to 14.
- **Audit** (`/ui-design audit <file, folder or URL>`): read the target, check it against `tells.md` and sections 4 to 13, and report in the format of section 15. Edit nothing.
- **Redesign**: keep the routes, the content, the brand and the information architecture. Change the visual layer only. Before editing, list the files you will modify or create. Never delete a file, a route or a component without my explicit go.
- **Reference** (I share a screenshot or a URL I like): extract its principles (page structure, type pairing, color anchor, spacing rhythm) and say them in a few lines. Never copy its code, its images or its exact layout. Refuse to clone a paid template.

Briefs, PDFs, decks and docs I provide are reference material. Don't paste their text into the page unless I say so.

## 1. Direction first, code second

If the project has a `DESIGN.md`, read it and follow it. It wins over your preferences.

Decide which kind of interface this is:

- Marketing site: persuade and get one action. Personality, rhythm and real proof matter.
- Application or dashboard: let people work. Density, consistency and predictability matter. No hero, no decoration, no marketing copy inside the product.

For a new site, a new app or a redesign, write a short brief and show it to me before building:

- Who it's for, and the one action the page must get them to take.
- Tone, in a few words.
- One real-world reference that fits: a print magazine, a signage system, an art movement, a period, a site I like. Ask me if I have one.
- Page structure (section 2).
- Palette (hex values) and fonts, each with one sentence tying the choice to the project.
- Any pattern from `tells.md` part 2 you intend to use on purpose, with the reason.

When nothing is set, propose two clearly different directions and let me pick. If the project has a brand or a design system, follow it strictly and skip the brief.

Once approved, write the tokens before any component (section 7), and save the decisions in `DESIGN.md` at the project root: structure, palette, fonts, tokens, patterns allowed on purpose. Every later page reads it, so the project stays consistent without loading design rules into every session.

Your first instinct for a font or a color is probably your usual default. If you'd make the same choice for any project, drop it and pick again.

## 2. Pick the page structure before the visuals

The fastest way to look generated is the template rhythm: centered hero, three features, call to action, footer. Choose a structure that fits the content, for example:

- Long document: one column of real reading, headings as signposts. Docs, essays, policies.
- Index first: the list is the page (menu, catalogue, directory, schedule), with filters if needed.
- Product first: the actual interface or output shown at the top, explained around it.
- Steps: a numbered path the visitor follows, each step with its proof.
- Letter: a person speaking in first person, short, signed. Portfolios, small studios, founders.
- Manifesto: a position in a few strong statements, then the proof.
- Photographic: images carry the page, text stays brief. Places, food, craft, events.
- Questions: the page answers the real questions buyers ask, in their order.
- Comparison: a fair table against the alternative, when the choice is the visitor's problem.
- Stat-led: only with real, sourced numbers.

Two pages of the same project don't share a structure unless they are the same kind of page. Record the structure of each page type in `DESIGN.md`.

By default the hero is as tall as its content. On a 1280×800 laptop screen and at 375 px, the headline, the lede and the main action are visible without scrolling.

## 3. Avoid the tells

Read `tells.md`. Part 1 never ships. Part 2 ships only if the brief says why.

## 4. Layout and hierarchy

- Not everything goes in a card. Group with spacing, alignment, type size and the occasional thin rule. A card is for a repeated, self-contained item the user clicks or compares.
- Never a card inside a card. One separator per boundary: a border, a background or a shadow. Never all three.
- One primary action per screen. Other actions are visibly secondary.
- Squint test: blur your eyes. The most important element should still stand out, and the reading order should be obvious.
- A grid: a max content width, consistent columns, everything aligned to shared edges.
- Left-align text by default. Center only short lines.
- Spacing with rhythm: tight inside a group, generous between sections, and by default sections that don't all share the same padding. Every value comes from the spacing scale. No arbitrary values like `mt-[37px]`.
- Rows mixing a button, an icon and text use `align-items: center`.
- Body text: 60 to 75 characters per line.
- French text runs 20 to 30 % longer than English. Design with the real copy.
- Stress-test with extreme content: a very long name, a title on three lines, a missing image, zero items, one item, a thousand items.

## 5. Color

- Derive the palette from the project: logo, subject, audience, the reference from the brief.
- Structure: one neutral scale with a faint tint (warm or cool), one accent, semantic colors for success, warning and error.
- The accent is rare: call to action, links, active state. About a tenth of the surface at most.
- Background: by default an off-white or an off-black chosen with the palette. Pure white only as a stated choice in `DESIGN.md`.
- Color never carries meaning alone: errors also get an icon or text, links in body text are underlined.
- Dark mode only if both themes are designed. A dark theme is its own palette, with lower-contrast surfaces and a desaturated accent.
- Set `::selection`, the focus ring color and the `theme-color` meta from the palette.
- Contrast checked on every pair actually used, including text on images and text inside cards whose background changed: 4.5:1 for body text, 3:1 for large text, icons and focus rings.

## 6. Typography

- Choose fonts for the project's character and justify in one sentence. Look beyond Google Fonts (Fontshare, Velvetyne, independent foundries), check the web license, self-host.
- For an app or a dashboard, the system font stack is a legitimate lazy choice. Say so when you pick it.
- One family is often enough, two at most. A monospace counts as a family when used outside code.
- Headings are upright. Emphasis comes from weight, color or an underline, never from one italic word. Italic stays for emphasis inside running text.
- Strong scale with few sizes. Fluid sizes with `clamp()` for large headings, line-height 1.0 to 1.15 for display sizes. All-caps headings never go under line-height 1.0.
- Body text at least 16 px. Inputs at least 16 px too, or iOS Safari zooms on focus. Body line-height around 1.5. No justified text.
- `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs.
- French typography: `lang="fr"`, « guillemets » with non-breaking spaces, non-breaking space before `:` `;` `!` `?`, accented capitals, `hyphens: auto` on narrow columns. Curly apostrophes and real ellipses in any language.
- `font-variant-numeric: tabular-nums` for tables and figures.

## 7. Tokens and surfaces

Define tokens in one place before building components: colors, fonts, type scale, spacing scale, radii, shadows, border colors, z-index levels, motion durations and easings. Components only reference tokens. A value you need that doesn't exist becomes a new token first: no hex, no `font-family` and no magic number improvised inside a component.

- Radii: two or three values with a role. Nested elements follow `inner radius = outer radius - padding`.
- Shadows: two or three elevation levels at most, one light source. Many interfaces need none.
- Borders: 1 px, one or two border colors from the neutral scale.
- Z-index: a short named scale (base, dropdown, sticky, sticky nav, modal, toast). Never `9999`.
- Icons: one library, one stroke width, one size per context.

## 8. Imagery

- One art direction for all images: same treatment, same light, fixed aspect ratios with `aspect-ratio`.
- Real photos of the product, the team, the place or the work. No stock that could illustrate anything.
- Product screenshots kept current, readable, cropped on what matters, shown in a plain `<figure>`. Never inside re-drawn browser or phone chrome.
- No text baked into images.

## 9. Mobile and responsive: the floor

- Checked at 320, 375, 414 and 768 px, and on a wide screen.
- No horizontal scroll at any width: `overflow-x: clip` on both `html` and `body` (`clip`, not `hidden`, so sticky elements keep working). Never `width: 100vw`.
- Grid tracks holding images use `minmax(0, 1fr)`, not `1fr`, or a large image pushes the layout past the screen.
- Large headings get `overflow-wrap: anywhere` and `min-width: 0`, so a long word can't overflow.
- Clickable text never wraps onto two lines: shorten the label first (« Start free » rather than « Get started for free »), then `white-space: nowrap`, then move items into a menu.
- Full-height sections use `100dvh`. Bottom sticky bars respect `env(safe-area-inset-bottom)`.
- A secondary sticky element docks below the sticky nav (`top: var(--nav-height)`), never at `top: 0` under it.
- Touch targets at least 44 px. Nothing important hides behind hover only: touch screens have none.

## 10. States and interaction

- Every interactive element has hover, focus, active and disabled states, and `cursor: pointer` when clickable. Non-interactive elements have no hover effect.
- One hover signal per element: a color shift, an underline, or a 1 px move. Not all of them.
- Transitions name their properties. Never `transition: all`. Animate `transform` and `opacity` (an SVG stroke being drawn is fine too). Never animate layout properties: `width`, `height`, `top`, `left`, `margin`, `padding`. 150 to 250 ms, ease-out for entering, no overshoot on interface elements.
- Focus rings appear instantly, without transition.
- Data states (loading, empty, error, partial) and failure handling: follow the `reliability` skill. Loading uses a skeleton shaped like the content. A spinner waits 150 ms before showing, then stays at least 300 ms.
- Submit buttons show progress and are disabled while sending. On a marketing site, a contact or lead form ends on a confirmation page with its own URL. Inside an app, follow `components.md`.
- On mobile, when the page is long, keep the main action reachable (a slim sticky button, or the action repeated) without covering content.
- One orchestrated entrance on first load at most. Respect `prefers-reduced-motion`.

## 11. Interface copy

- Apply the `deslop` rules to every piece of copy.
- The main headline says what the product does and for whom.
- Buttons name the action (« Créer mon devis »), in a few words. Avoid « Commencer », « Découvrir », « En savoir plus ».
- Destructive actions name what gets destroyed (« Supprimer le projet »), next to a plain « Annuler ».
- Error messages say what happened and what to do, without blaming the user and without technical codes.
- No filler adjectives: puissant, intuitif, fluide, simple, innovant.
- Dates, numbers and prices formatted for the locale (`Intl`, « 1 234,50 € » in French).
- Missing copy, figures, names or legal text: `[À FOURNIR : ...]`, listed in your reply.

## 12. Lazy version

- HTML and CSS first: `<details>`, `<dialog>`, native form validation, `:has()`, scroll snap before a library.
- Reuse the project's components or the installed UI library, restyled to the tokens.
- No animation library for a fade, no Lottie for a spinner, no 3D for a still object.
- Before adding a section, say what it gives the visitor. No answer, no section.

## 13. Accessibility

- Contrast as in section 5, full keyboard navigation in a logical order, visible focus.
- A label for every field. Descriptive `alt` on informative images, `alt=""` on decorative ones. `aria-label` on icon-only buttons.
- `lang` on `<html>`, a coherent heading hierarchy, one `h1` per page, landmarks (`header`, `nav`, `main`, `footer`).
- Usable at 200 % zoom. Auto-moving content can be paused.

## 14. Self-check before showing me

Score the result from 1 to 5 on each axis. Any score under 3 means a revision pass before showing it. Give the six scores in one line of your reply.

- Intent: does the page take a clear position, or is it just a layout?
- Hierarchy: in two seconds, is it obvious what comes first, second, third?
- Execution: are the details in spec (contrast, focus, wrapping, alignment, tokens)?
- Specificity: does it look like this project, or like anyone's site?
- Restraint: has everything that doesn't earn its place been removed?
- Variety: does it differ in structure from the other pages of the project and from the template rhythm?

Then:

- Logo test: hide the logo. If the page could be anyone's, rework what makes it generic.
- Tells audit: list every item of `tells.md` present on the page, marked "chosen: reason from the brief" or "default: removed". Part 1 items are never "chosen".
- Count fonts, sizes, colors, radii and shadows. Cut what isn't used on purpose. Search the code for hex values and spacing outside the tokens.
- Squint test, stress test, keyboard-only pass, every link and button clicked, browser console at zero errors.
- Search for leftovers: `lorem`, `TODO`, `John Doe`, `example.com`, `Vite + React`, `Create Next App`.
- If you can render the page (Playwright, a browser tool), look at screenshots at 375 px and 1280 px. Mention that Safari on iOS still needs a real-device check.

## 15. Audit report format

For each finding, most severe first:

```
[critical | major | minor] Tell name, file:line
  Why it reads as generated, in one line.
  Fix, in one line.
```

Then one line of counts (N critical, N major, N minor) and a verdict: "ships as slop", "reads as AI-generated", or "close, fix the minors". Edit nothing until I say which fixes to apply.
