---
name: design-core
description: Shared design principles that the other design skills build on. Covers visual composition (alignment, contrast, hierarchy, proximity, white space, repetition, unity), interface writing (voice, tone, labels, errors, empty states, field hints), and an interface quality baseline (states, accessibility, focus, motion, copy, AI tells). Use when designing or reviewing a screen, page, component, flow, or UI copy, when another design skill (design-flow, figma-generate-design, a frontend build) is about to place or write something, or when the user asks "review this design", "is this layout right", "check the UI copy", "design principles", "หลักการออกแบบ", "ตรวจงานดีไซน์", "เขียนข้อความบนหน้าจอ", or says a screen or page "looks generic", "looks AI-made" or "needs more taste", or an open creative choice (a name, headline, palette, poster, cover, game idea) is left to the agent or called "too generic", "boring", "typical AI", "too safe", "cliché" or "seen it before", or wants to design from reference images, Inspo or Awwwards references, three variants, or a long "cook" iteration loop scored against references, or hands over one picture of a robotic animal, machine or device to rebuild in three.js as an object that takes itself apart (a "cutaway", "exploded view", "make this image a 3D model that comes apart", a 60 fps teardown film with a synced score). Not a style of its own: it never overrides the file's or product's existing design system.
---

# Design Core

The principles every design skill in this repo applies, in one place, so each skill doesn't
restate them. Other skills load this one; this one doesn't do Figma calls, captures or code.

## Order of authority

1. **The user's explicit request.**
2. **The product's own system**: its components, variables, text styles, term list and
   capitalization. A file that uses Title Case on buttons keeps Title Case.
3. **Platform rules** for where the design ships (Apple HIG, Material, WCAG).
4. **This skill's defaults.** They fill gaps; they never replace something that already exists.

When two rules here disagree with the product, report the gap. Don't silently restyle.

## The rules in short

**Composition** (detail and checks: [references/visual-principles.md](references/visual-principles.md))

- One focal point per screen. Hierarchy decides what is seen first, second, third.
- Every element sits on a grid line, a shared edge, or a baseline. Use auto layout, not nudging.
- Related things sit close; unrelated groups get more space between them than within them.
- Spacing, color, type and radius come from tokens. Repetition of the same values is what makes
  a screen feel designed.
- Contrast is for meaning: the primary action, the error, the current item. Not decoration.

**Writing** (detail and checks: [references/writing.md](references/writing.md))

- Most important information first. One idea per screen when you can.
- Buttons and links start with a verb and say what happens: "Send", "Save draft", not "OK",
  "Let's go", or "Click here".
- Errors sit next to the problem, don't blame, and say how to fix it.
- Empty states say what to do next and offer the button to do it.
- Keep one term per concept, one capitalization style per element type, no "we".

**Interface baseline** (detail and checks: [references/interface-quality.md](references/interface-quality.md))

- Every screen has its default, empty, loading and error state, and long content doesn't break it.
- Every control is reachable and named: label, focus ring, contrast, target size.
- Motion only where it gives feedback, and it respects reduced motion.
- No AI tells: decorative gradients, a generic three-card row, rounded cards everywhere,
  filler adjectives.

**Reference first** (detail: [references/reference-first.md](references/reference-first.md),
[references/cook-loop.md](references/cook-loop.md))

- References carry the look, the prompt stays short. The product's screens come first; outside
  references (Inspo MCP, Awwwards MCP, the browser) fill only what it leaves open.
- New page: three static variants side by side before app code. Layout before motion.
- A bar per dimension, scored by a fresh-context critic on side-by-side images. The author's own
  score never decides; a user's correction becomes a calibration offset.
- Feedback is marked-up screenshots and the build's own terms (grid, padding, hex), not "cleaner".

**Off-default** (detail: [references/off-default.md](references/off-default.md))

- Before an open creative choice, write "the default here is X", then leave X unless the case asks
  for it. Its well-known opposite is the second default.
- Start from the case's own facts; when the request is thin, from
  [`scripts/seed.py`](scripts/seed.py) (`visual`, `text`, `idea`), never from "what would be most
  interesting".
- Every choice gets a one-sentence reason from a fact about this project.
- Posters and covers: the AI look is the finish, so pick a making method and let its marks replace
  it. Interfaces keep their grid; the working parts (what must be read or pressed) stay whole.
- An escape that worked last time is the next default.

**Cutaway** (detail: [references/cutaway.md](references/cutaway.md))

- One picture in, a three.js object built from code out, opened part by part. The build runs in
  the cutaway skill; this is the method.
- **The output is an interactive page the viewer drives by hand**, never a film-only page: the
  film plays until they click; then each part's pill (or number key) opens or closes that part and
  parts combine, drag orbits, scroll zooms, double-click resets, "Play film" hands back. Build it
  with [`cutaway/manual.js`](cutaway/manual.js) and [`cutaway/interactive.js`](cutaway/interactive.js).
- **Not done until** [`cutaway/check_page.mjs`](cutaway/check_page.mjs) passes on the built page
  and the page is open in the browser. A 60 fps film with a synced score only when asked.
- A 10–12 line checklist per picture, measured: dark share ≥ 0.8 of the picture's, proportions
  within a few hundredths. A still first; stop after round 2 and wait for a yes before filming.
- Port the closest approved film 1:1 and change the body only; every beat its own camera.

## How to use it

**Follow the working order** in [references/workflow.md](references/workflow.md): understand →
inventory → intent → build → review → hand off, with a check at the end of each stage.
Its short form:

1. Write the screen's job in one sentence. Take behavior from the source, never guess it.
2. Inventory the product's components, tokens, text styles and words before drawing; collect
   references for what it leaves open.
3. Show the plan as text (content order, focal point, states, copy) before building; for a new
   page, three static variants.
4. Build the default state first from instances and tokens, then the other states.
5. Screenshot, score (a fresh-context critic when there are references), fix the top findings,
   at most three rounds. Report the scores. A long showcase build runs the cook loop instead.
6. Hand off states, behavior, tokens and gaps per screen.

**When building**, read the reference that matches the work before placing or writing anything:
visual principles for layout, writing for any visible text, interface quality for states and
controls, and [references/taste.md](references/taste.md) when the work is a page or a screen with open
style choices (classify the kind, copy before layout, decide on purpose, check like a gate).
Then build with the product's own tokens and components.

**Worked example:** [examples/github-profile](examples/github-profile/README.md) is an animated
GitHub profile (SVG hero and skills panel) that runs the whole workflow end to end: brief and
kind, a v1 rejected for copying its reference, the open choices behind v2, and the render
checks that found and fixed real overflow bugs. Its `src/build.py` can be reused for other
self-contained animated SVGs.

**On Roblox**, game-dev's [`design-ui`](../../game-dev/design-ui/SKILL.md) applies these rules to a game's
HUD and menus: the brief gate, Roblox's safe insets and conventions, three more review rows.

**When reviewing**, score each dimension 0–10 and say what a 10 would look like for this screen:

| Dimension | Source |
|---|---|
| Hierarchy and emphasis | visual-principles.md |
| Alignment, proximity, white space | visual-principles.md |
| Consistency (repetition, unity, tokens) | visual-principles.md |
| Copy (labels, errors, empty states) | writing.md |
| States and edge cases | interface-quality.md |
| Accessibility | interface-quality.md |
| Fit to kind, no generic look | taste.md, off-default.md |
| Closeness to the references (when there are any) | reference-first.md, cook-loop.md |

Report findings as `screen or file:location — issue → fix`, most severe first. A finding needs
a location and a concrete fix; "feels off" isn't one. Pass is 8 or higher on every row.

**When the request is vague** ("make it clean", "more professional"), pin down these before
designing, and ask about the ones the product doesn't already answer: palette, accent, body
type, display type, layout model, mood, density, and what to exclude.

## Sources

- Apple Human Interface Guidelines, [Writing](https://developer.apple.com/design/human-interface-guidelines/writing)
- Figma Resource Library, [Graphic design principles](https://www.figma.com/resource-library/graphic-design-principles/)
- [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills) (Apache-2.0):
  `web-design-guidelines` (Vercel Web Interface Guidelines), `impeccable-design-polish`,
  `plan-design-review`, `design-brief`
- [Leonxlnx/cook](https://github.com/Leonxlnx/cook) (MIT): intake, target, bar and calibration,
  fresh-context critics, round ledger, pacing; scaled down from its long showcase runs
- Reference tools: [Nutlope/inspo](https://github.com/Nutlope/inspo) (MIT),
  [INSANE0777/Awwwards-mcp](https://github.com/INSANE0777/Awwwards-mcp) (MIT)
- [Nyxera0x/cutaway](https://github.com/Nyxera0x/cutaway) (MIT), on
  [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) (MIT): the picture-to-3D
  teardown method (checklist, measured density and proportions, still gate, per-beat cameras,
  timeline-synced score); the runtime stays in that skill
- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT): the method only (kind
  first, copy first, deliberate choices, checks with ids, waivers), not its kit or scripts
- [mankidev/antialgorithm](https://github.com/mankidev/antialgorithm/tree/8706a2d49511954d0d092f732eb5853497ad25fc)
  (MIT): name the default and leave it, the seed (`scripts/seed.py`, vendored unchanged), making
  methods over the AI finish, the escape becoming a default; its `rough.py` and `check.py` stay
  in that repo

The references paraphrase these sources. Re-check them when a rule seems out of date.
