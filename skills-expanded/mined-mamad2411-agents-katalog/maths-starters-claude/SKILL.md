# CLAUDE.md — Maths Starters

Read this before writing any code in this repo.

## What this is

A single-purpose React app: it generates a four-box maths starter for a UK
secondary classroom, displayed on an interactive whiteboard. Nothing else.

Each box holds a **topic** (e.g. "Pythagoras", "Volume"), drawn at random from
a pool the teacher has selected in the topic panel. The teacher's unit of
choice is the topic, not the individual skill — there are roughly 30 topics
against 150-odd skills, and a teacher thinks "we did Pythagoras this week".

Every box has three buttons:

| Button | Action |
|--------|--------|
| new | Same skill, fresh numbers |
| ↻ | Next skill within the same topic, cycling in catalogue order |
| ⇄ | Swap this box to a different topic from the pool |

Difficulty is a single board-wide band — Foundation, Core or Stretch — set by
the header stepper. It applies to all four boxes at once.

### Superseded: the recency model

Earlier drafts resolved each box from the class's position in an ordered
scheme of work, with the four boxes labelled Last lesson / Last week / Last
topic / Last year. **That model is gone.** `SPEC.md` §4 (`resolveSlots` and
its fallback chain), §5 (shuffle and label switching) and §7.2 (the scheme
screen) describe it and are marked superseded there; they are kept as a
possible future direction, not as a description of the app. There is no
`resolveSlots`, no class record, no tick list, and no calendar arithmetic
anywhere in the code.

The reason for the change: every class has a different scheme and year group,
and a single ordered scheme cannot represent that. A teacher going room to
room needs to load four questions in seconds without first telling the app
where their class is.

## What this is not

This is a deliberate reduction of a larger five-section teaching app. Do not
add Diagnostic, Learn, Examples or Challenge sections. Do not add PDF
worksheet generation, JSXGraph, user accounts, or a backend. If a feature
request would pull any of those back in, say so rather than building it.

## Commands

```bash
npm install      # Node 20+
npm run dev      # Vite dev server
npm run build    # production build
npm run preview  # preview the production build
npm run lint     # oxlint (react/rules-of-hooks, react/only-export-components)
```

Check `package.json` before assuming a test runner is or isn't wired up.

## Current state

The app is built and running. Roughly:

```
src/
  components/    Board.jsx  Header.jsx  Slot.jsx  TopicPanel.jsx  Figure.jsx
  curriculum/    skills.js  topicPool.js  schemes/haese-igcse.json
  generators/    algebra/  geometry/  puzzles/
  lib/           archivoMath.jsx
```

- `Board.jsx` orchestrates: draws four topics from the pool, holds the
  difficulty band, the timer, the reveal state, and the three per-box actions.
- `Slot.jsx` renders one box; `Figure.jsx` maps a `visualization.type` to an
  SVG branch; `archivoMath.jsx` is the maths renderer.
- `topicPool.js` owns the localStorage-backed topic selection.
- `skills.js` is the catalogue and the board's single entry point
  (`generateForSkill`).

`haese-igcse.json` is **not imported by the running app**. It is the build
backlog: an ordered list of textbook sections with the skill ids each needs
and a `status` of `ready` / `todo` / `skip`. It has drifted from `skills.js`
in places (ids that no longer exist, entries still marked `todo` whose
generators are written). Treat a mismatch as drift to be reported, not as a
signal that a generator is missing.

## Key documents

Read the relevant one before structural changes. They are written not to
disagree, so treat a conflict as a bug to flag rather than a choice to make
silently — with the one exception of the superseded sections above, where
this file wins.

| File | Covers |
|------|--------|
| `SPEC.md` | Question shape (§3), the maths renderer's parser/fallback split (§6), persistence. §4, §5 and §7.2 are superseded — see above |
| `DESIGN.md` | Visual system, tokens, layout rules, figure sizing |
| `MIGRATION.md` | What ported from `maths-teaching-app`, what was left behind, defects in the source to fix rather than reproduce |
| `README.md` | User-facing overview and repository layout |
| `reference/starter-board.html` | Design export. Read-only — nothing builds from it |

## Non-negotiable conventions

### 1. Generators are pure functions returning data

A generator takes an options object and returns a plain data object. It must
never return JSX, never import React, and never read from React state.

```js
export const generateVolumeCuboid = (options = {}) => {
  const { difficulty = 'core' } = options;
  // ...
  return {
    instruction: 'Find the volume of the cuboid',
    answer: '120',
    answerUnits: '\\text{cm}^3',
    workingOut: `V = l \\times w \\times h${NL}V = 8 \\times 5 \\times 3${NL}V = 120`,
    visualization: { type: 'cuboid', l: '8 cm', d: '3 cm', h: '5 cm' },
    metadata: { topic: 'volume-cuboid', difficulty },
  };
};
```

`visualization` is a **config object**. `Figure.jsx` maps `type` to an SVG
branch. No JSX above the renderer, ever.

`NL` is a real newline (`'\n'`), never the two characters `\n`.

### 2. One question shape

Every generator returns the shape in `SPEC.md` §3. There is no legacy format
in this repo.

A **forward** question carries everything on the figure and returns no
`questionMath` — `instruction` names the task and the labelled edges supply
the numbers. A **reverse** question (given a volume, find a length) returns
`questionMath`, because the given quantity is not a length and cannot sit on
the figure as a dimension label. Follow that split.

### 3. The scheme is data, the catalogue is code

- `src/curriculum/skills.js` — holds generator function references. Code.
- `src/curriculum/schemes/*.json` — ordered lists of skill ids. Pure JSON.
  No functions, ever. Must survive `JSON.parse(JSON.stringify(scheme))`.

Every catalogue entry carries a `topic`. The topic is what the teacher picks
and what ↻ cycles within, so entries sharing a topic must be genuinely
interchangeable within a lesson — and must sit in a sensible order, since
that order is the cycle order.

`difficulties` lists only the bands a generator genuinely varies across.
Declaring a band the generator ignores is a lie the board cannot detect.

### 4. Difficulty bands change the shape of a question, not its numbers

Foundation, Core and Stretch must differ structurally. "The same question with
bigger numbers" is not a band. Worked examples of the principle:

- Surface area of a cylinder: curved surface only → both ends → one end with
  the diameter given rather than the radius.
- Surface area of a cone: slant height given → slant height given, total →
  slant height **withheld**, so Pythagoras comes first.
- Volume of a cuboid: three lengths → cross-sectional area × length → volume
  given, find the missing length.

Where π appears, Foundation and Core leave the answer exact (`45\pi`) so they
stay calculator-free. This is the textbook's own convention, not a house
invention.

### 5. Styling is plain CSS with custom properties

No Tailwind, no CSS-in-JS, no utility framework. Slot colours are passed as a
`--c` custom property and referenced as `var(--c)`; that is how one stylesheet
serves four differently-coloured slots. Tokens live in `:root`. Never hardcode
a hex value in a component — inside `Figure.jsx` that means the `color` prop
and `var(--ink)` only.

### 6. Maths rendering is hybrid, and figures are not part of it

Question, answer and working text go through the renderer: a custom Archivo
parser first, with KaTeX as a fallback for what it cannot take. See
`SPEC.md` §6 for the exact split. Anything falling back should do so
deliberately — a console warning from a generator that only uses `\times`,
`\frac` at one level, `\text{}` and `^` is a parser bug worth reporting.

**Figure labels are different.** They are plain SVG `<text>`, drawn by
`figLabel`, and never touch the renderer. So a figure label uses the literal
character: `°` not `^\circ` (there is a `plainAngleLabel` helper for this),
and `cm²` not `cm^2`. Passing LaTeX to a figure prints the backslashes.

`answerUnits` does go through the renderer. It accepts either a plain string
(`'cm'`, wrapped automatically) or LaTeX (`'\\text{cm}^3'`, passed through).
Units never belong in the `answer` string.

### 7. Figures are schematic

A figure's geometry is fixed and does not reflect its label values — the same
convention `parallel-transversal` established. A 20 × 3 × 2 cuboid drawn to
scale is an unreadable sliver; drawn fixed it stays legible and the labels
still tell the truth. Labels change; shapes do not.

Established conventions:

- **3D solids with flat faces** (cuboid, prism, pyramid) use **cabinet
  oblique**: front face true, depth receding up-right at 45° at half scale.
  Not isometric — `figLabel` only draws horizontal text, and isometric puts
  every edge on a slant with nothing to align against. Occluded edges dashed.
- **Curved solids** (cylinder, cone, sphere) draw each circular face as an
  ellipse with the far half dashed. For an arc from the left point to the
  right point, `sweep = 1` passes over the top and `sweep = 0` under the
  bottom, so the near half is `sweep = 0`.
- An `unknown` field names which label takes the slot colour; everything else
  is `var(--ink)`. Default to `null` where the unknown is usually not a
  labelled edge (an area or a volume).

### 8. Generators are verified by substituting the answer back

Before a generator is done, run it several thousand times per band and
recompute the answer **from the figure config and question text**, never from
the generator's own variables. That catches the failure a spot-check misses:
a figure and a generator that quietly disagree about which edge is which.

Also count distinct questions per band. A band that produces a few dozen
distinct questions has a real ceiling — document it honestly rather than
inflating the range to hide it. A cube has one parameter; no amount of
widening changes that, and a cube of side 60 cm is not a better question.

No hardcoded question banks. Pythagorean triples are generated with Euclid's
formula over a range and filtered, not listed.

## UK conventions

Maths (not math), brackets, indices, standard form, factorise, centre.
Metric units. IGCSE/GCSE grade descriptors.

## Interactive whiteboard constraints

- Everything fits one screen at 1920×1080. No vertical scrolling on the
  starter view, ever.
- Minimum touch target 44px. Assume a finger, not a mouse.
- Minimum body text 18px; question text larger.
- High contrast — these screens are viewed in daylight with the blinds open.

## Stack

React 18 + Vite, plain CSS with custom properties, KaTeX (dynamically
imported, fallback only), lodash. **No Tailwind.** No other dependencies
without asking.

## Working style

- Ask before inventing a convention. Consistency across generators matters
  more than any individual generator being clever.
- One thing at a time, verified on a board before the next thing starts. New
  figure types land as their own commit, before any generator depends on them.
- The textbook is inspiration for question shape and scaffolding only. Never
  copy a value out of it.
- Prefer deleting code from the old app over porting it "just in case".