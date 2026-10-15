---
name: infographic-design
description: >-
  Design polished, professional explanatory graphics as SVG or single-file
  HTML. Use when the user asks for an infographic, 資訊圖表,
  懶人包, 圖解, a one-pager, a visual summary, or a
  timeline/comparison/process ("how it works") graphic — even without the
  word "infographic" — and to review an existing one ("幫我看這張圖表哪裡
  可以改"). Use for a learning recap when a teaching dialogue ends
  ("學習總結成一張圖", "visual recap of what you taught me"); that route
  needs no further prompting. Also use when another skill needs a figure
  designed for a document it is producing. Do NOT invoke for a single
  standalone chart embedded in analysis output, for dashboards / BI tooling,
  for slide decks (use a pptx workflow), for explaining a term in plain
  language (use plain-speak), or for data-dense charts where the numbers are
  themselves the subject or precise scales matter (annual-results decks,
  survey findings, statistical graphics) — hand those to a
  data-visualization workflow. An explicit ask for an infographic /
  資訊圖表 / 懶人包 / one-pager always qualifies even when the underlying
  data is precise; the data-density exclusion applies only when the user
  names a chart, plot, or dashboard instead. Quantities that serve as
  evidence inside an explanation (a funnel's drop-off, a cache hit-rate)
  stay in scope.
version: 0.11.1
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: design infographic data-visualization svg visual-communication
  agentskills_spec: "1.0"
  openclaw:
    emoji: "📊"
---

# Infographic Design — 資訊圖表設計

Approach this as the design lead at a small studio known for infographics
that are unmistakably its own — the ByteByteGo-grade diagrams
people save and repost because they made a mechanism *click*. This client has
already rejected proposals that felt templated, and is paying for a
distinctive point of view: make deliberate, opinionated choices about
palette, layout, and visual metaphor that are specific to this brief, and
take one real aesthetic risk you can justify.

**Ground it in the subject.** If the brief leaves the subject open, pin
it yourself before designing: name one concrete subject, its audience, and
the graphic's single job, and state your choice. The subject's own world —
its materials, instruments, artifacts, and vernacular — is where distinctive
choices come from: a TLS diagram borrows from locks and sealed envelopes, a
CDN diagram from geography, a queue from physical lines. Build with the
brief's real content throughout.

**Structure is information.** Structural devices — numbering, lanes,
dividers, badges — should each encode something true about the content; a
device earns its place by carrying a fact. Numbered markers (① ② ③) are
appropriate only when the content actually is a sequence; lanes only when parties genuinely act separately.
Question each device before incorporating it.

Derive the arrangement from how the parts actually relate — what feeds
what, what contains what, what loops back. Three topics rendered as three
equal blocks encodes the order you listed things in, which is a fact about
your notes rather than the subject. The test: a layout that would survive
with the content swapped for something else entirely came from the outline —
rebuild it from the relations.

For calibration: AI-generated infographics have a recognizable default look,
and two of its tells are worth naming because they slip past every rule
elsewhere — prose bullets dumped into boxes instead of being turned into
visual relations, and the warm-cream-plus-terracotta palette (near #D97757 —
Anthropic's own Claude accent, so it reads as a tell). These are defaults
rather than choices. Where the brief pins a direction, follow it exactly;
where it leaves an axis free, spend that freedom on a real choice.

## Process: plan, critique the plan, then build

Work in two passes. First, brainstorm a compact plan from the brief: the one
message, the dial position, a palette named as hex roles, the layout concept
(one-sentence prose or an ASCII wireframe), and the **signature** — the
single element this graphic will be remembered by (a derivation drawn as
converging flows, a worked example threading every step, an unexpected but
apt visual metaphor).

Then review that plan against the brief before building: if any part reads
like the generic default you would produce for any similar graphic — work
through a similar prompt in your head to see if you arrive somewhere
similar — revise that part. Only after confirming the plan is specific to
this brief should you write SVG, following the plan exactly. Do this
planning and iteration in your thinking; show the user the version you
already believe in.

**Spend your boldness in one place.** Let the signature element be the one
memorable thing, keep everything around it quiet and disciplined, and cut
any decoration whose job for this brief you cannot name. Before delivering,
take one look and remove one accessory.

## Procedure

### 1. Set the dials, then distill one message

Think in the six tensions of Cairo's visualization wheel (*The Functional
Art*): abstraction–figuration, functionality–decoration, density–lightness,
multidimensionality–unidimensionality, originality–familiarity,
novelty–redundancy. The dials' **home position is fixed** at the end Cairo
maps to scientists and engineers: abstract, functional, dense,
multidimensional. Precision is the default on every request, and density
scales with how much the subject holds (a multi-party
mechanism ⇒ real lanes, cross-party arrows, payloads on the arrows,
derivations drawn as data-flow — `references/bytebytego-style.md`).

What you decide per request is whether to *pull a dial* away from home, and
every pull needs a purpose and a source:

- **Retention pull** (toward redundancy + familiarity) — when the graphic
  exists so someone *remembers*: teaching recaps, onboarding. This is the
  Holmes move: dual naming and an analogy vocabulary are licensed here and
  only here, and the second name must come from somewhere real that
  predates the drawing — the dialogue that taught it, the audience's own
  vernacular. Canonical case: `references/learn-loop-viz.md`.
- **Simplification pull** (toward lightness + figuration) — only on an
  explicit signal ("for laypeople", "one glance", a poster or social
  brief). It trades density away, so the signal has to come from the brief
  itself.

Absent that signal, stay at home. Either way, **declare the position** in one line —
*home*, or the pull with its purpose and source — because step 9 checks the
build against what you declared here.

Then write the one message: "After seeing this, the viewer should understand
___." One sentence, before any drawing. Multiple stories → pick the strongest
or propose a series.

**Done when** both lines exist: the declared position and the one message.

### 2. Pick the output format

Recommend one, let the user choose: **SVG** (default; source of truth for
PNG/PDF), **HTML** (single self-contained file when motion or interactivity
earns its place — directional flow lines get `class="flow"`, structural lines
stay still; baseline CSS in `references/svg-construction.md`), **PNG** social,
**PDF** print, **PPTX** via the pptx skill.

One route skips this step: a learning recap (`references/learn-loop-viz.md`)
is always a single self-contained animated HTML file. The route settles
both the format choice and the motion question — build it and say what you
built.

**Done when** exactly one format is settled and stated — recommended and
chosen, the recap's forced HTML, or (embedded) the host's.

**Embedded mode.** When the graphic is a figure inside a document another
skill is producing, that skill owns the surface and this one owns the
content. Every content rule still binds — archetype, density, payload on the
arrow, one name per thing, honest quantities, the words. What yields, and
only this:

- **The headline.** A standalone canvas carries its own takeaway at 2–3×
  body size because it travels alone; a figure travels under the host's own
  heading, where a second headline would make the same point twice on one
  page. Keep the figure's largest text at the host's figure-title scale and
  let the surrounding prose carry the takeaway.
- **Colour and type** — the host's tokens and type scale replace step 7 and
  `references/color-typography.md`.
- **The wrapper** — the host owns the page frame, the column, and the page
  background (`references/svg-construction.md` describes a sheet delivered
  on its own). Emit the bare figure element and let the host place it.
- **Format, and the final check** — the host decides both; the step 9
  delivery gate is written for a standalone canvas, and the host's own
  checks govern a figure sitting in its page.

Say which host you are building into and take its tokens.

### 3. Choose the layout archetype

Match the data's shape, then let the dial position set the density (see
`references/layouts.md`): process/flow, comparison, hierarchy, timeline,
part-whole, geo, hero-stat. For technical explainers read
`references/bytebytego-style.md` — numbered walkthrough welded to the
diagram, worked example, making abstract concepts visual. For a visual recap
of a completed teaching dialogue also read `references/learn-loop-viz.md`.

**Done when** one archetype is named and it survives the outline test: if the
arrangement would sit unchanged on a different subject, it came from your
notes — rebuild it from how the parts actually relate.

### 4. Build the three-level hierarchy

- **L1 — takeaway**: the headline, embedded *inside* the image (a reposted
  image must still explain itself), phrased as the point — a question or a
  finding. Biggest, boldest, 2–3× body size.
- **L2 — sections**: subheads, key figures. L1+L2 alone tell the skeleton.
- **L3 — support**: labels, captions, source. Quiet and small.

One font family; vary size/weight/colour across levels. Most of the surface
is text, and labels template as easily as layouts do — `references/words.md`.

**Done when** every text element sits at exactly one level, and L1+L2 read on
their own still tell the skeleton.

### 5. Compose on a grid, spend whitespace

8-pt grid, consistent gaps, ~40% air. Density is earned with a bigger
canvas and more *relations* — as content grows, grow the sheet and hold the
gaps.

Density that is earned still has to be navigable. Past roughly one screen,
a reader stops reading and starts *scanning back* — looking for the place
they saw a thing before. Give them landmarks: an icon on every recurring
node type (`references/icons.md`), and a surface treatment that means one
thing consistently (`references/color-typography.md`) — landmarks are what
turn each re-find into a jump rather than a linear search through
same-shaped cards.

**Done when** every box lands on the 8-pt grid with consistent gaps and ~40%
air, and every recurring node type carries a landmark — an icon plus a
surface that means one thing.

### 6. Visualize quantities honestly

Quantities appear here as *evidence inside an explanation* — a funnel's
drop-off, a hit-rate, a before/after; graphics where the numbers are the
subject were handed off at the door. The honesty rules bind regardless of
size:

Zero-baseline bars, no 3-D, no dual axes, area scales by value not diameter.
Round numbers unless precision is the point. Cite the source (small, L3).
Embedded forms and hero numbers: `references/charts.md`.

**Done when** every quantity — the hero number and each inline stat alike —
has cleared the rules above.

### 7. Colour and type

One neutral + one theme + one accent, ~60/30/10; the accent marks the single
most important thing. Derive the palette from the subject's world (verified
starting points, application principles, and type scales:
`references/color-typography.md`) and contrast-check it before layout. Icons: inline vector from
`references/icons.md`, one style throughout.

**Done when** the palette is bound to its 60/30/10 roles with the accent on
exactly one thing, and every text and graphic pair has passed contrast —
before you lay out.

### 8. Accessibility

WCAG 4.5:1 for text (3:1 for large/graphic), and give every distinction
colour makes a second channel — label, position, or line-style. Respect
`prefers-reduced-motion` in HTML output.

**Done when** every distinction the colour makes is also carried by a label,
position, or line-style — drop the graphic to grayscale and it still reads.

### 9. Critique, then gate, then deliver

Critique the artifact as a reader before you check it against rules: could
someone meeting it cold state the message in 8 seconds, and *verify* the
mechanism's core relation from the drawing alone? Does the build match the declared dials — home
actually dense (lanes, payloads, derivations), a pulled dial
actually justified by its purpose and source? Is anything colour-only, source-less, or
fake-precise? When a real-world exemplar of this genre exists (a published
ByteByteGo diagram, a chart you admire), hold your artifact next to it —
external comparison catches what rule-checking can't. Fix what you find.

Then run the deterministic gate as the final seatbelt — it catches
reader-harming defects (parse errors, broken refs, clipped/overflowing text,
contrast, tiny fonts); design quality was the reader-critique's job:

```
python scripts/check.py out.svg --bg "<canvas>" --pad <card-padding>
```

Exit 0 required before delivering. If it flags something, fix the cause
(usually: cut words first, then shrink type, enlarge boxes only last —
growing the canvas, with the grid's gaps held). Advisory warnings (font
naming, emoji, var() renderer compat, restyle structure) are judgment calls,
yours to weigh.

**Done when** every reader-critique question answers yes and the gate returns
exit 0 — the green gate is the seatbelt, the reader-critique the driving.

## Building the output

Construction mechanics — text fitting (the #1 failure mode), CJK handling,
`:root` var restyle structure, HTML wrapping with the flow-animation
baseline, export recipes — live in `references/svg-construction.md`. Read it
before writing SVG. Keep the palette in `:root` variables and group elements
semantically (`<g id="step-1">`) so a restyle is a single variable swap.
