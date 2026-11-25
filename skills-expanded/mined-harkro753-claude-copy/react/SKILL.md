---
name: react
description: >
  Clone a captured website into verified shadcn/ui React components — a capture
  session becomes one component per route with its captured states as props,
  themed from the site's own tokens, every state gated against its own reference
  screenshot. Use when the deliverable is a real component tree rather than a
  static page: an app, a dashboard, a console, anything with behaviour (hover,
  focus, keyboard nav, a command palette, tabs, dialogs), or whenever the user
  says React, shadcn, components, or wants the clone to be maintainable rather
  than a flat file. Also use when several captures differ only by URL fragment —
  those are one component with states, not separate routes. Prefer the html
  skill for a landing or marketing page where a static file is the deliverable.
---

# clone:react — capture session → verified shadcn routes

**In:** a session folder — `pages.json` + one folder per page holding `ref.png`,
`source.html`, `computed.json`, `meta.json`.
**Out:** a vite + shadcn project at `apps/<site>/ui/`, one React component per
route in `ui/src/routes/`, themed from `ui/theme.json`, where every captured
state's `check` exits 0 against its own `ref.png`.

**Read [`references/pipeline.md`](../../references/pipeline.md) first** — the
CLI, the phases, the loop discipline and the four hard nevers are there and are
not repeated here. This file is only what differs for React.

```
clone prep <session> --target react
clone extract | resolve | cluster
clone init | map | check | build
```

## Why components, and where the project lives

**A screenshot is the resting frame of components that have behaviour.** A
command palette cloned as HTML is a `div` with a fake list; composed from
`Command` it filters, takes `⌘K`, traps focus and returns a value. Hover, focus
rings, disabled states and keyboard nav are all in the component and none of them
are in `ref.png`. Cloning frames throws that away every time.

**The project lives inside the capture folder it clones** — `apps/<site>/ui/`,
one per site, not one for the repo. It costs a `node_modules` per clone and buys
three things: a tree you can hand to someone whole, a `components/ui/` that is
unambiguously *this* site's to edit, and no path in the loop that leaves the app
folder — the fonts and baked glyphs the route asks for are project assets under
`ui/public/`, not a sibling directory two levels up.

## What prep does differently: states, not duplicate routes

**A URL that differs only in its fragment is folded into a state.**

```
new: 1 component, 3 states — base, settings-general, settings-customize-connectors
```

Under a static target those three captures are three routes, which means
hand-cloning the same shell into three files and fixing every bug three times.
Here they are one component and a `state` prop, each still gated against its own
`ref.png`. This is most of what the target buys.

## extract · resolve · cluster

Same phases, two outputs used differently:

- **`shared/glyphs.json` names become lucide-react imports.** `resolve` already
  matched every glyph to a `lucide:<name>`, so `<SearchIcon />` is a lookup, not
  a decision. Icon *colour* comes from `currentColor` and the component.
- **A glyph you set to `keep` is a file `resolve` bakes**, and it lands in the
  project at `ui/public/icons/`, so the route asks for
  `<img src="/icons/<file>.svg">` — one path, resolved the same by `vite dev` and
  `vite build`. `resolve` legitimately runs before the project exists; `init`
  moves them then.
- **`shared/tokens.css` feeds `init`, not your markup.** You never paste a hex
  into a route.

## init — the project, and the capture's values as tokens

First run tells you the one-time project command, to run **in the app folder**:

```
cd apps/<site> && pnpm dlx shadcn@latest init --name ui --template vite \
  --base radix --preset nova --no-monorepo --yes
```

Nothing else to install — no bundler plugin, because there is no bundle in the
loop. Drop the `.git` that `shadcn init` leaves behind, or the outer repo sees a
gitlink instead of your routes.

Then `init` writes `ui/theme.json` — the capture's values in shadcn's semantic
slots. It derives what a histogram can derive (`background`, `foreground` and the
base font from the capture's root; `sidebar` from the tall narrow box every route
shares; `border` from the most common non-zero border; `primary` as the
highest-chroma colour; `radius`, the text scale and its line-heights by
frequency) and **leaves the rest null**, because which of twelve greys is `muted`
and which is `accent` is a naming decision, and naming is the one thing a
histogram cannot do. Name them from `candidates` (frequency-ranked, what the site
actually uses — do not invent), then re-run `init` to generate `theme.css`.

Get this phase right and the loop gets short: **a wrong token fails two hundred
boxes across four routes and one edit fixes all of them.** That is the trade this
target makes for the Tailwind translation layer, and it only pays if the tokens
are real.

`init` also regenerates `vite.config.ts`, `index.html`, `src/main.tsx`,
`src/clone-env.d.ts`, `src/theme.css` and `src/fonts.css`, and copies the
capture's woff2 into `ui/public/fonts/`. Those are not yours to edit; two things
in them matter:

- **route and state come from the query string**, `?route=<entry>&state=<state>`,
  and `main.tsx` reaches every route through `import.meta.glob`. That is what
  lets one dev server answer every captured state.
- **`@font-face` with `url("/fonts/…")`**, served from `public/`. `init` reads
  each cut's weight, style and stretch out of its filename — declaring four
  static cuts at `1 1000` makes them all equal matches and Blink renders the whole
  page in whichever came last.

`init` writes one route stub per entry, listing the states it must serve. Stubs
are never overwritten.

## map — which component each node already IS

Writes `shared/shadcn.md`: every node the capture describes, its box, and the
component proposed from tag + geometry + style. Confirm or correct in
`shared/shadcn.json`, re-run, and it prints the `add` line.

What it **cannot** propose is the interesting half. Nothing in a capture says
"this is a Command palette" — those are *roles*, and the capture records tags and
geometry. Read `shared/components.md` for the repeated subtrees and name them:

| looks like | is | and brings |
| --- | --- | --- |
| a search field with a list under it | `Command` in `Dialog` | filtering, `⌘K`, keyboard nav |
| a segmented control | `Tabs` or `ToggleGroup` | roving tabindex, one active |
| a panel over a dimmed page | `Dialog` / `Sheet` | focus trap, its own overlay |
| a tall nav column | `Sidebar` | collapse, mobile sheet |
| a pill with a count | `Badge` | variants |

`npx shadcn@latest search @shadcn -q "<what it does>"` to find one;
`npx shadcn@latest docs <name>` **before** you author against it — read the real
API rather than guessing it.

## Authoring

One `.tsx` per entry in `ui/src/routes/`. Author entries in parallel with one
subagent each — separate files, so parallel writes are safe. `theme.json` and
`components/ui/` are not: edits there serialize.

- **Compose components.** A styled `<div>` is what you reach for when nothing
  fits, not what you start from. Follow the `shadcn` skill's rules.
- **`className` is for layout** — flex, gap, size, position.
- **Every state renders from the `state` prop.** No second copy of the shell:
  `state === 'settings-general' && <Dialog open>…`.
- **Author in CSS px**, flow layout not absolute coordinates, and nothing is a
  slice of `ref.png` — charts are `Chart`, gradients are CSS, a photograph you
  cannot rebuild is a neutral placeholder block.

### The fix ladder

`shadcn add` vendored the source into this project, so there is no "default" a
box can fail to reach. Every disagreement is reachable; the only question is
where the edit goes, and going a rung too low is what makes a clone
unmaintainable:

1. **A value → `theme.json`.** Colour, radius, type scale. One edit, every
   route. Re-run `init`.
2. **A repeated geometry → the variant, in the vendored component.** This site's
   buttons are 32px and `size="default"` is 36px? Change the variant in
   `src/components/ui/button.tsx` once and every Button on every route moves.
   **This is the normal path, not a last resort** — owning the source is the
   entire reason to use shadcn rather than a component library. Say in a comment
   what the capture measured, so the next reader sees a decision, not a nudge.
3. **A genuine one-off → `className="h-[34px]"` at the call site.** Fine, and
   only fine, when it really is one.

`check` tells you which rung you are on every cycle: it names classes that
restate a token (rung 1 — and they render identically, so `check` can never see
them) and values that repeat 3+ times (rung 2 — a variant nobody edited).

### Controls get a hover. Surfaces get one only if the capture declares it.

This is a hard rule, and it cost a shipped regression to learn:

- A **control** — a button, link, row, pill, field: anything up to about
  320×64 — has a hover that is *one property*. Copy it from `layout.md` when
  listed; where it is not, the component's own `hover:` is almost certainly
  right, because a control with no affordance is a bug in any design system.
  `check` reports a control that does nothing.
- A **surface** — a card, banner, tile, panel — has a hover that is a *composite
  treatment*: a scrim, a reveal, a lift. **If the capture's CSS does not declare
  it, do not build it.** A resting screenshot cannot show you which treatment it
  is or how strong, nothing in the loop can tell you the guess is wrong, and a
  half-right scrim looks materially worse than an inert card. `check`
  deliberately stays silent about these rather than prompting you to invent one —
  silence there is the rule, not a gap.

The one exception a reviewer will accept is a plain 1px hover border on a tile,
because it is a single property like a control's. Anything with an overlay or
more than one property: leave it out and say in `progress.md` that the capture
had no data for it. When `meta.json` reports `unreadableSheets > 0`, **every**
state on the route is in this position.

## check — and what it drives

`check` starts `vite dev` on a free port, points headless Chromium at
`?route=<entry>&state=<state>` for each captured state, and screenshots it. Then
the shared oracle, unchanged — same floors, same ranked digest, same `check.md`
with crops, same `sbs.png`. **Nothing was relaxed to make components pass.**

**And it drives the interaction states.** In the same session, after the resting
frame: mouse to each interactive box's centre, `elementFromPoint`, and compare the
computed style against the site's own harvested `:hover` declarations —
disagreements gate. It also diffs the hovered frame against the resting one, so a
state that changes nothing, or repaints half the page, is visible; and it leaves
`<slug>/hover/<id>.png` (resting | hovered) for every box it touched, which is the
only way to *see* a state.

This is not a pixel gate — there is no hover reference screenshot to be one
against. It proves values and blast radius, which catches a missing affordance
and a wrong hover colour, and does not certify a card's scrim.

One extra piece of loop discipline on top of the shared list: **check
`theme.json` first.** A systematic failure in a shadcn build is usually one
token, not thirty boxes. Grep the failing node id in `shared/shadcn.md` to see
which component it is.

**When a component cannot reach its box, say which and why.** "Radix `Select`
renders a trigger 4px taller than the capture at every size" is a finding worth
having. Overriding it silently is how the deliverable stops being shadcn.

## accept

Every state at `0 failing` — or only "Not asserted" boxes left, which is also
done, said with the reason. Then the link pass: for each `<a>`/`Link` whose
target matches another route's URL, point it at that route; uncaptured targets
get `href="#"`. Re-run `check` — hrefs paint no pixels, so it is a free
regression gate.

Report the per-route match, the crops that mattered, and **where the fixes
landed**: how many were tokens, how many were variants in vendored components,
how many stayed one-off classes. That last number is the one worth watching — it
is how much of this clone is not themeable.

`clone build` runs a real `vite build` to `ui/dist`. Deliberately not part of the
loop: `check` serves the source, so a cycle never waits on a bundle.
