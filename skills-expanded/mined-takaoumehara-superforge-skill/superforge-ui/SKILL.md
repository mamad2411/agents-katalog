---
name: superforge-ui
description: >
  Design and build interfaces across Web, iOS (SwiftUI), and Android (Jetpack
  Compose), covering layout, visual hierarchy, typography, responsive
  behaviour, state specification, and micro-interactions. Opens by sourcing the
  visual direction from references or a design made in another tool, and
  extracting the system behind it — structure, space, type, colour role, motion
  character, imagery — because a model designing from its own priors returns
  the average of everything it has seen. Follows a five-phase design process,
  Apple HIG, and Material 3. Use when the user says "design", "UI", "UX",
  "layout", "screen", "component", "make it look better", "animation",
  "typography", "onboarding", "first launch", "permission prompt", "デザイン",
  "画面", "見た目", "レイアウト", "アニメーション", "余白", "使いにくい",
  "オンボーディング", "初回起動", "権限の許可", "AIっぽいデザイン", "参考サイト",
  "インスピレーション", "デザインシステムに落とす", "moodboard", "reference
  site", "遅い", "パフォーマンス", "多言語", "3D", "shader", "sound", "音",
  "方向性を見せて", or runs /superforge-ui.
license: MIT
metadata:
  author: Takao Umehara
  version: "10.3"
compatibility: >
  Standalone.
  Reads docs/brand.md and docs/product-idea.md when present, writes docs/design.md and docs/design.html.
  Falls back to the codebase's existing conventions when no design system exists.
---

# Superforge UI — Interface Design, Motion & Native Engineering Engine

Use this skill when designing or implementing user interfaces across Web, iOS (SwiftUI), and Android (Jetpack Compose). This engine guarantees high aesthetic value, typography perfection, state specification, and micro-interaction polish.

---

## 0a. Name the job before sourcing anything

Two questions decide whether the rest of this process solves the right problem,
and both get answered implicitly if they are not answered out loud.

**What does success look like on *this surface*?** Persuade (they decide and
act) · Operate (they finish a task) · Read (they understand) · Experience (they
are inside the work). **Pick it from the surface, not from the company** — a
developer tool's landing page is Persuade, a fashion house's documentation is
Read. Each mode also names what it may legitimately sacrifice, and a mode that
gives up nothing is a wish rather than a mode.

**Preserving or replacing?** Refinement keeps the identity, the behaviour, and
everything outside the stated scope. Redesign keeps product truth and function
but treats the old look as *evidence*, not as something to improve.
**Never split the difference** — polish spent on a look already decided against
is the most wasted work in this process.

Both, plus the rule that a pinned brief outranks every default in this suite →
**`references/surface-and-scope.md`**.

---

## 0. Source the direction before designing anything

A model asked to "make it look good" returns **the average of everything it has
seen**, and averages look like averages — that is the entire explanation for the
recognisable "AI interface" look. A stronger model produces a better-executed
average, not a different one.

So before any token is chosen, settle where the direction comes from: references
the user admires, an existing design arriving from another tool (Claude Design,
Google Stitch, Figma, v0), or — declared honestly — nothing. Then extract the
**system** behind it in six layers (structure, space, type, colour, motion,
imagery), never the content, and record the sources and the deliberate
divergences → **`references/design-sourcing.md`**.

**When there is genuinely nothing to work from**, do not fall back to a
restrained default — that is what a model produces with no direction at all, so
choosing it lands on the same page as choosing nothing. Commit to a named
direction, push exactly one axis, keep the rest quiet, and label the source
honestly → **`references/aesthetic-direction.md`**.

Three references beat one: one produces imitation, three force you to find the
principle they share.

### The outcome is enough; tool discovery is agent work

Do not require the user to know a library name or add a phrase such as “research
the latest options.” When a new Medium or Large UI phase leaves the technique
open, inspect the existing stack, then read **`references/library-discovery.md`**
and perform one bounded fresh scan before naming or installing anything. Compare
a native or already-installed approach with current maintained options, state
the selection reason and cost, and—when the request is to build or change the
product—continue through implementation and evidence. Do not stop at a
recommendation list. A bounded follow-up does not reopen discovery unless its
requirements invalidate the choice.

---

## 1. Five-Phase Design Process

1. **UNDERSTAND**: Surface target user context, map assumptions, and reframe requirements.
2. **IDEATE**: Explore layout structures, navigation patterns, and component hierarchies — **from the extracted direction in §0**, not from scratch.
3. **DESIGN**: Construct complete screens, typography grids, color assignments, and content states.
4. **EVALUATE**: Run accessibility audits (WCAG 2.2 AA), contrast checks, and simulated persona testing. Hand the accessibility half to **`superforge-a11y`** — it owns the criterion ledger and writes `docs/accessibility.md`. Do not restate the criteria here.
5. **PREPARE**: Output clean production components, design tokens, and implementation specs.

Step-by-step detail for DESIGN and EVALUATE is in `references/design-process.md`.

---

## 2. UX Spec & State Completeness (`ux-spec`)

No UI component is complete until all 7 component states are explicitly engineered:
1. **Default**: Normal resting state.
2. **Hover**: Suble elevation/border highlight on cursor hover.
3. **Focus**: Distinct keyboard focus outline (`:focus-visible`).
4. **Active**: Touch/press tactile feedback (`scale(0.97)`).
5. **Disabled**: Reduced opacity (`0.4`), disabled pointer events.
6. **Loading**: Skeleton placeholder or inline spinner.
7. **Error**: Inline error messaging with clear recovery CTA.

---

## 3. Typography & Spacing Rhythm (`typeset`)

- **Strict Type Scale**: Use a mathematical modular type scale (1.250 Major Third or 1.333 Perfect Fourth).
- **Line Length & Height**: Restrict body text width to 45–75 characters per line. Line height `1.5` for body, `1.1`–`1.2` for headlines.
- **Spacing Grid**: Align all margins, paddings, and component gap sizes strictly to an 8px grid (4px for micro-gaps).

---

## 4. Web Motion & Micro-Interactions

- **Motion communicates or it is cut.** Every animation serves feedback, status,
  feedforward, or transition. If it serves none, delete it — decoration is a cost
  every user pays on every visit.
- **GPU Acceleration**: Animate ONLY `transform` and `opacity`. Where layout
  genuinely must change, use **FLIP** rather than animating width/height/top/left.
- **Easing follows the property, not taste**: `ease-out` entering, `ease-in`
  exiting, **`linear` for opacity, colour, and rotation**, no easing at all
  during an active drag.
- **View Transitions**: Use native `@view-transition` or morphing animations between page views.
- **Reduced motion is a runtime check**, not only a media query — stop JS loops,
  scroll engines, and autoplaying media, and confirm the page still tells its story.

Durations, the easing token set, the compositor pipeline, scroll-engine
synchronisation, native-platform equivalents, and the eight-question interaction
score → **`references/motion-system.md`**.

---

## 4b. Performance and language are layout decisions, not later problems

Both of these are treated as engineering problems discovered at the end, and
both are decided here, in this file, at the moment a layout is agreed.

**Performance.** The hero video, four webfont weights, the icon library
imported whole, an animation on a layout-triggering property — by the time
anyone profiles, components are built on top of those and the fix is a redesign.
Set three numbers into `docs/design.md` alongside the tokens: time to something
useful, time to visible response, and weight of the first screen — each with a
consequence for exceeding it. Sources of weight in order, perceived speed
(which is free and entirely design), and native budgets →
**`references/performance-budget.md`**.

**A second language.** German runs 30–40% longer than English, and short strings
expand the most — so buttons break first. **Never size a container to its
current text**, never bake text into an image, never assemble a sentence from
fragments. Doing this now costs almost nothing; retrofitting it is a rebuild.
Text expansion, RTL, locale-aware formats, string extraction, and the honest
three-way decision about whether to be multilingual at all →
**`references/internationalization.md`**.

---

## 4c. The floor, checked on the built result

Before editing UI — after the direction is settled, not during planning — the
things that are true of good work in any direction: measured contrast, 65–75ch
measure, more space above a heading than below, elevation declared once, inner
radius = outer − padding, `tabular-nums` on changing numbers, every state
present with real copy at every breakpoint.

And the defaults that appear when a decision was skipped, grouped by **why**
they appeared: what the component library ships (cards as structure, eyebrows
everywhere, section numbers), shortcuts for a feeling not earned (gradient text,
glass as decoration, monospace as costume), and values nobody chose (solid hex
borders, opacity as a disabled state, pure grey, brand colour carried unchanged
into dark mode) → **`references/build-floor.md`**.

---

## 4c. Show three directions, and propose the one they did not ask for

Committing to one direction is right for **building** and wrong for
**deciding**. Put **three named positions** in front of the user first — three
*positions*, not three intensities of the same idea — each with its concept, the
axis it pushes, what it gives up, and its cost. **Always name a recommendation**;
three options with no recommendation hands the decision back to someone who
asked precisely because they did not want to make it alone. Then build the
chosen one completely and **never average them** (`references/aesthetic-direction.md` §1b).

And on Experience and Persuade surfaces, **propose something they did not ask
for.** People cannot request a fluid that reacts to the cursor if they do not
know it can exist. Propose it in the language of sensation — "the background
could be liquid that moves away from you" — never in the language of the
technology, and **carry the price in the same breath** (§4d). A proposal
without a cost is a sales pitch.

**Then say what to actually install.** A sensation with no route to a tool
leaves a designer exactly where they started. Names live in one dated file,
`references/toolchain.md`, mapped from each sensation — and it also reads the
other way, because some capabilities only became askable once the technology
existed.

When the user delegates the choice or asks for autonomous implementation, show
the three positions compactly, name the recommendation, adopt it, and continue
in the same run. Waiting for the user to repeat “use your recommendation” adds
no information. Pause only when the tradeoff changes the goal or crosses a stop
condition in the router.

**Propose from a menu, not from memory.** `references/effect-vocabulary.md`
holds what is actually possible — matter that flows, swarms that assemble,
things that grow differently on every load, space you move through, and sound
computed rather than played — each named by how it feels, tiered by cost, and
kept free of library names so it does not expire. Without it, "make it
impressive" returns a gradient.

---

## 4d. Shaders, 3D, and anything GPU-drawn

Reach for the **cheapest tier that achieves the effect** — CSS before SVG before
a minimal WebGL wrapper before a full 3D engine — because most effects people
reach for 3D to achieve sit two tiers below it. Then pay for it honestly: weight
and time-to-first-frame come out of §4b's budget, and **the frame rate has to be
measured on a mid-range phone**, which is the one number that cannot be reasoned
to.

Two costs decide whether it survives real use, and neither is bytes: **a running
GPU loop drains and heats a phone** (so stop it off-screen and on a hidden tab),
and **a canvas is a blank rectangle to a screen reader**. `prefers-reduced-motion`
does not reach a JavaScript render loop — the loop must check it itself.

Cost tiers, what to decide before opening a tool, the fallback rule, and why the
surface's mode usually settles it → **`references/heavy-visuals.md`**.

**This file names no libraries on purpose.** Which renderer leads changes yearly;
the decision does not.

---

## 4e. Sound

The least-used expressive axis, and therefore the one with the most
distinctiveness still available — and the one with the sharpest downside, since
a visual mistake is ignored and an audio mistake closes the tab.

**Nothing may make a sound the visitor did not cause. No audio on page load,
ever.** Anything a sound conveys must also be visible. The mute control lives on
the surface, is keyboard-reachable, and is remembered. Interface sounds stay
short, quiet, and pitch-varied on repeat — the same sample twenty times becomes
a mosquito. Nothing attaches to scroll or hover.

The highest-value use is the cheapest: a short confirmation of an action the
user took, so someone looking at their keyboard still knows it worked. The most
striking is generated tone rather than played file — a formula ships instead of
a recording, and it never repeats identically → **`references/sound.md`**.

---

## 5. Platform Native Specifications

### iOS Native (SwiftUI / UIKit):
- **Apple HIG Compliance**: Dynamic Type font scaling, SF Symbols with animated variable color, Native Sheets (`.presentationDetents`).
- **Tactile Haptics**: `UIImpactFeedbackGenerator` / `UINotificationFeedbackGenerator` integration.

### Android Native (Jetpack Compose / Kotlin):
- **Material Design 3 (Material You)**: Dynamic Color extraction (`dynamicDarkColorScheme`), Predictive Back gestures, surface tonal elevation, 48dp minimum touch targets.

Bottom navigation, search, live order status, empty states, and choosing a
slider versus a stepper are specified per platform in
**`references/component-patterns.md`**.

---

## Deeper references

- **`references/design-sourcing.md`** — where the visual direction comes from:
  the six extraction layers, the line between reference and imitation, turning a
  design made in another tool into a system, and what to do when there is no
  source at all. Read it **first**, before the process below.
- **`references/design-process.md`** — the six design steps in order, the four
  mandatory data states, reach and target sizing, form-validation timing, the
  interruption hierarchy, and the full quality checklist. Read it before
  designing screens.
- **`references/motion-system.md`** — durations by interaction class, easing
  chosen by the property being animated, the render pipeline and FLIP,
  scroll-driven motion, runtime reduced-motion handling, and the eight-question
  score for any interaction.
- **`references/design-system-output.md`** — the `docs/design.md` +
  `docs/design.html` two-artifact spec. Read it before touching tokens.
- **`references/landing-page.md`** — the conversion-specific layer for sales
  and marketing pages: section order as an argument, the hero specifically,
  and why mobile and desktop are different pages rather than one page scaled.
  Read it before designing anything meant to sell rather than to be used.
- **`references/slide-page.md`** — the other kind of long page: one that must
  survive being skimmed (case study, portfolio, project detail). Two layers per
  screen, one idea per screen, shape chosen by what the content is doing, and
  the render-with-reveal-disabled check that catches the "it looks blank"
  failure. Carries **no visual language** on purpose — the look comes from
  `design-sourcing.md`.
- **`references/surface-and-scope.md`** — the four modes and what each is
  allowed to sacrifice, refinement versus redesign and the never-split-the-
  difference rule, why a missing design file is not a greenfield, and why a
  pinned brief outranks your taste.

- **`references/build-floor.md`** — the checks on the built result and the
  refuse-list grouped by cause, plus the honest reconciliation of the expressive
  animation palette against the performance budget.

- **`references/aesthetic-direction.md`** — the Route C answer: ten named
  directions, the one-axis rule, the specific defaults that read as machine-made
  (Inter as a display face, purple-on-white, three equal cards, evenly
  distributed palettes, scattered scroll fades), atmosphere as a layer, and why
  minimal is not less work.

- **`references/toolchain.md`** — the bridge from a sensation to something you
  can install, dated and reviewed as one file so the rest of this skill stays
  durable. Also the reverse direction: reading what recently became possible and
  asking what it makes askable, with two guards against solutions looking for
  problems. Stops at the browser and the app bundle — installations and sensors
  belong to an interactive-experience skill.

- **`references/library-discovery.md`** — the default outcome-to-tool loop:
  inspect the repository, compare native and current maintained choices using
  official evidence, explain the decision, implement it, and verify its real cost.

- **`references/effect-vocabulary.md`** — the menu the proposal step needs:
  around thirty effects across graphics, sound and native surfaces, each named
  by sensation rather than by library, with its rough cost and the surfaces it
  suits. Includes the instruction to propose nothing when nothing fits.

- **`references/sound.md`** — the three uses in order of how often they are
  right, the six non-negotiable rules, why timing rather than file size is the
  real constraint, and constraining generated tones to a scale so "something is
  off" becomes "this feels considered".

- **`references/heavy-visuals.md`** — shaders, 3D and GPU-drawn animation: the
  cost tiers, battery and heat, the first frame, the floor device, the screen
  reader and reduced-motion obligations, and the frequency rule that rules this
  out of any surface used many times a day.

- **`references/performance-budget.md`** — three numbers set with the design and
  measured by `superforge-verify`, where the weight actually comes from,
  perceived speed as a design problem, animation cost, and native budgets.

- **`references/internationalization.md`** — text expansion and the layouts it
  breaks, RTL and logical properties, why a sentence must never be assembled
  from fragments, locale-aware formats, keyed string extraction, and deciding
  whether to be multilingual at all.

- **`references/first-run.md`** — the gap between those two: the first thirty
  seconds after someone commits. Getting to a first real outcome instead of
  explaining the product, why first run means something different on web than
  on a phone, requesting permissions at the point of use rather than in a queue
  (a denial there is often permanent), and marking completion in a way you can
  still test afterwards. Read it before building any welcome screen, intro
  carousel, or setup wizard.

- **`references/component-patterns.md`** — the components almost every app
  rebuilds the same weak way: bottom navigation (count, destinations not
  actions, safe area, two-signal active state, badges), search that answers on
  focus, live status of an order or booking, the four-part empty state, input
  controls chosen by how often a value is entered, metric-card hierarchy, and
  exposing content instead of framing it.

- **`references/rive.md`** — stateful vector animation: when Rive earns its
  runtime and when CSS, video or a shader is the better answer, the different
  rules for a web app and a portfolio (one Rive moment, everything else HTML),
  the split between what Claude builds through the Rive MCP and what a person
  draws, and the state-machine spec and accessibility checklist for
  integration.

- **`references/interactive-components.md`** — Growth-Engineered Conversational
  & Interactive Components (GEC Framework): design standards for ROI calculators,
  assessment quizzes, multi-step wizards, and comparison grids that drive conversion.

## Artifact

Write **both** `docs/design.md` (YAML tokens & VVA Matrix alignment the agent parses) and
`docs/design.html` (a self-contained style guide and component preview a human can open and review).
They must never drift: editing one regenerates the other in the same turn.

The token file also declares the visual layer agents otherwise default on:
**tinted, layered elevation** (no neutral grey shadow), **density** per surface
mode, and **figure type tokens** for metrics — spec in
`references/design-system-output.md`.

Never inline a raw colour, size, or radius. If a needed token does not exist,
add it to `docs/design.md` and record it under `New patterns needed`.

## Delegate when a sharper skill is installed

`impeccable`, `frontend-design`, `taste-skill` (craft) ·
`design-system-builder`, `design-system` (system generation) · `typeset`,
`arrange`, `colorize`, `polish`, `normalize` (refinement) · `bolder`,
`quieter`, `delight`, `minimalist-skill` (tone) · `web-animation-design`,
`animation-patterns`, `gsap-*` (motion) · `clarify` (UI copy) · `ux-spec` ·
`superforge-a11y` (the a11y audit itself) · `accessibility-generator`, `audit`
(deeper a11y specialists) · `ios`, `swift`, `liquid-glass`,
`macos`, `watchos` (native) · `landing-page-creator`, `keynote-slide-page`
(sales pages — see `references/landing-page.md` first) · `dataviz` ·
`japanese-text` · `onboarding-generator` (native intro-screen scaffolding —
see `references/first-run.md` first, and decide whether intro screens are the
right answer before generating any).
