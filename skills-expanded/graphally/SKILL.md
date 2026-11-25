---
name: graphally
description: Draws professional diagrams and explanatory figures as SVG and PNG from HTML and CSS - architecture with Azure and AWS icons, networks (VNets, subnets, peering, private endpoints), hierarchies and org charts, BPMN processes and flowcharts, sequence diagrams, Gantt plans and roadmaps, phase and role charts, figures for proposals and solution designs (governance, scope, layered solution stacks), diagrams of Terraform repositories drafted from the code, and any figure a web page can hold, designed around the point it makes. The browser lays the figure out and graphally routes the connections, so nobody writes a coordinate. Use it whenever the user asks for a diagram, an architecture or network picture, a flow, a process map, a sequence, a timeline, a plan or a roadmap, or wants to visualise infrastructure, even without the word "diagram". Not for charts of numeric data (bar, line, pie).
license: Apache-2.0. Copyright (c) 2026 Kamil Wilczyński (kwilcz), https://github.com/kwilcz/graphally. LICENSE.txt has the terms.
compatibility: Requires Node.js 18 or later and Chrome, Chromium or Edge (or `npx playwright install chromium`). Internet once, to download the Azure and AWS icon packs.
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/graphally.mjs *) Bash(node ${CLAUDE_SKILL_DIR}/scripts/edit.mjs *) Bash(node ${CLAUDE_SKILL_DIR}/scripts/tf2graphally.mjs *) Bash(node ${CLAUDE_SKILL_DIR}/scripts/fetch-icons.mjs *)
metadata:
  author: Kamil Wilczyński (kwilcz)
  repository: https://github.com/kwilcz/graphally
  version: "2.19.0"
---

# graphally

A diagram is a small web page: HTML holds the components and their nesting, CSS sets the
layout, a JSON list declares the connections, and a drawing script adds any mark a box
can't hold. graphally lays the page out in a browser, routes the connections around
the boxes, and writes an SVG. Never write coordinates, and never hand-write SVG.

**A canvas, not a catalogue.** Whatever a web page can lay out, graphally draws: a pyramid
cut from grid cells, rings, a track with stations, isometric slabs, a map, a building with
floors. No figure needs to be supported first. The references teach techniques to combine
and stretch; none of them lists the figures allowed.

## Design the figure first

Design each figure for its reader before writing any HTML. Write the design in three lines:

1. **The point**: who reads the figure, and the one thing it must make obvious to them.
2. **The visual metaphor**: a form, invented for this content, that shows the point before
   a word is read. A conveyor whose two slow stations are red; the floors of a building for
   the layers of a platform; walls in rings around what must be protected; a split screen
   with what changes lit up.
3. **The build**: the techniques that make it: grid areas, `shape=`, `clip-path`, the
   drawing script.

A topology (icons joined by labelled lines) is the visual metaphor for one point: the
system's parts, where they run, and how they communicate. When the user asks to explain,
present, sell or simplify a system whose topology they already have, the point is a
different one, and so is the form.
A request to make a figure better, clearer or more advanced asks for a new visual metaphor,
built for this content with whatever techniques it needs.

Idea starters by point, and the design moves that make a figure read at a glance:
[references/design.md](references/design.md).

## Workflow

Copy this checklist and work through it; render as often as the figure needs.

```
- [ ] 1. Design: write the point, the visual metaphor and the build
- [ ] 2. Read the references for the techniques the build uses (table below)
- [ ] 3. Write diagram.html
- [ ] 4. Render: node ${CLAUDE_SKILL_DIR}/scripts/graphally.mjs render diagram.html --png
- [ ] 5. Fix every reported problem; render again until it prints ok
- [ ] 6. Look at diagram.png: the form shows the point before the labels are read; rework until it does
- [ ] 7. Hand over diagram.svg and diagram.html; a PNG to share is rendered with --png2x
```

1. **Design.** Three short lines, in your reply or a comment in the file. The design
   decides the figure; the references only build it.
2. **The references.** Each teaches its techniques through a complete example. Take what
   the build needs, from as many as it needs.
3. **Write.** Start from an example below or in a reference, and change it as far as the
   design asks. Ids name what the connections and the script refer to; text is what the
   reader sees.
4. **Render.** The command writes `diagram.svg` (the deliverable) and `diagram.png` (a
   half-size preview: enough to read every label and judge the form, at a quarter of the
   tokens), then prints `ok` or one line per problem. Overlaps and overflows are the
   problems' job, not the picture's; `--png1x` gives a full-size look when one is needed.
   `${CLAUDE_SKILL_DIR}` is this skill's directory: Claude Code fills it in; elsewhere,
   use the path of the folder that holds this file.
5. **Fix.** Each problem names its cause and a fix (table below). Edit the file and render
   again.
6. **Look.** `ok` means nothing collides, not that the figure works. Read it as its reader
   would, labels last: the form alone shows the point from step 1. Then check that it reads
   one way, labels sit by what they name, and one element draws the eye first. When the
   form misses the point, change the form.
7. **Hand over.** The render adds a header to the `.html` (a doctype and a `<script>`
   that loads graphally's viewer), so the file itself shows the diagram when opened in a
   browser, with nothing installed. Keep the header; anyone can edit the text and reload.

**Changing an existing diagram:** edit its `.html` in place, then render. The render reads
the previous SVG, so what you did not change stays where it was. Keep `nudge`, `out` and
`in`: they are the user's corrections. `--recompute` lays everything out afresh. A request
to rethink a diagram (clearer, simpler, self-explanatory, more than boxes and arrows) is a
new design: start again at step 1, and render with `--recompute`.

## Examples

A topology: the system's parts, where they run, and how they communicate. Items are icons
over their names (`figure`), with no frame; groups carry the structure, labelled lines the
flow.

```html
<diagram width=1200 title="Orders platform" subtitle="Production, West Europe">
<div class="grid grid-cols-4 items-center justify-between gap-x-24">
  <div class=figure id=shopper><icon name=browser></icon>Shopper<small>web browser</small></div>
  <div class=figure id=fd><icon name="front door"></icon>Front Door<small>WAF</small></div>
  <div class="group items-center gap-12"><h4>Application</h4>
    <div class=figure id=api><icon name="app service"></icon>Orders API<small>App Service</small></div>
    <div class=figure id=worker><icon name=functions></icon>Worker<small>Functions</small></div>
  </div>
  <div class="group items-center gap-12"><h4>Data</h4>
    <div class=figure id=db><icon name=sql></icon>Orders DB<small>Azure SQL</small></div>
    <div class=figure id=sb><icon name="service bus"></icon>Service Bus<small>orders topic</small></div>
  </div>
</div>
<script type="application/json">
[
  ["shopper", "fd", "HTTPS"],
  ["fd", "api"],
  ["api", "db", "writes"],
  { "from": "api", "to": "sb", "label": "order placed", "dashed": true },
  { "from": "sb", "to": "worker", "label": "events", "dashed": true }
]
</script>
</diagram>
```

A figure designed for its point, "two stations hold most of the delay". The track is the
order's path, so no lines join the stations; the red stops and their notes carry the point.

```html
<diagram width=1200 title="Two stations hold most of the delay" subtitle="What happens to an order, from the web shop to the door">
<style>
  .line { display: grid; grid-template-columns: repeat(5, 1fr); justify-items: center; row-gap: 16px; }
  .figure { width: 150px; }
  .track { grid-row: 2; grid-column: 1 / -1; justify-self: stretch; height: 36px; background: var(--icon-soft); clip-path: polygon(0 0, calc(100% - 28px) 0, 100% 50%, calc(100% - 28px) 100%, 0 100%); }
  .stop { grid-row: 2; align-self: center; display: flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 50%; background: var(--woad); color: var(--card); font-weight: 700; }
  .stop.slow { background: var(--rust); }
  .stall { grid-row: 3; width: 200px; padding: 8px 12px; border-left: 4px solid var(--rust); background: var(--card); font-size: 12px; line-height: 16px; }
  .stall b { display: block; font-size: 15px; color: var(--rust); }
</style>
<div class=line>
  <div class=figure><icon name=browser></icon>Order placed<small>web shop</small></div>
  <div class=figure><icon name=shield></icon>Payment checked<small>fraud rules</small></div>
  <div class=figure><icon name=database></icon>Stock reserved<small>ERP</small></div>
  <div class=figure><icon name=building></icon>Packed<small>warehouse</small></div>
  <div class=figure><icon name=mail></icon>Delivered<small>carrier</small></div>
  <i class=track></i>
  <b class="stop col-[1]">1</b><b class="stop slow col-[2]">2</b><b class="stop col-[3]">3</b><b class="stop slow col-[4]">4</b><b class="stop col-[5]">5</b>
  <div class="stall col-[2]"><b>4 hours</b>payments wait for the nightly fraud check</div>
  <div class="stall col-[4]"><b>2 days</b>packing waits for a manual stock count</div>
</div>
<script type="graphally">
// A dashed leader from each slow station down to what holds it up.
const stalls = all('.stall');
all('.slow').forEach((s, i) => draw.moveTo(s.bottom).lineTo(pt(s.center.x, stalls[i].y)).style({ color: 'rust', dashed: true }));
</script>
</diagram>
```

## The format in brief

- **`<diagram>`**: `width` in pixels (default 1200; the height follows the content),
  `title`, `subtitle`, `icons=aws` (AWS wins names both clouds share), `theme=dark`,
  `background` (a colour, or `none`).
- **Utility classes** have Tailwind's names and spacing (one step is 4px): `grid`,
  `grid-cols-3`, `flex`, `flex-col`, `justify-between`, `items-center`, `gap-6`, `p-4`,
  `mt-10`, `col-span-2`, `w-40`, `text-center`, `font-semibold`, `rounded-lg`, `border-dashed`.
  Brackets take any value or property: `w-[130px]`, `grid-cols-[160px_1fr]`,
  `[grid-area:edge]`. Colours are the theme's tokens (`bg-wash`, `text-muted`,
  `border-woad`); text sizes follow the diagram's scale (`text-base` is 13px).
- **Building blocks**: `figure` (an icon over its name and a `<small>` line, with no
  frame: the item of a topology; `external` mutes it, `accent` colours it), `node` (the
  same in a framed card), `group` with an `<h4>` title (`plain`, `dashed`, `external`,
  `vnet`, `subnet`, `region`; `badges` of `badge` icons in the title), `tile` (an icon over
  its name in a small frame), `band` (a strip of shared services), `key` with `swatch` (a
  legend), `card`, `box`, `pill`, `tag`, `banner`; `disabled` on any of them greys a
  part that is there but does not run, icon and lines included. These class names are taken, and so are
  the sequence helper's (`seq`, `msg`, `num`, `guard`, `lifeline`, `activation`, `frag-…`):
  name your own differently.
- **Motion**: `"flow": true` on a connection moves gaps and a dot along it; `data-step="1"`,
  `"2"`… make elements appear in order, once; `animate(target, keyframes, options)` in the
  drawing script moves an element or a drawn mark, as `element.animate` does. The still figure stays complete: PNGs, print
  and reduced motion show it. Move only what carries the point.
- **Labels that must not move boxes** (a column's heading, a caption, a note): hang them
  with `position: absolute` from a `relative` parent, so centring counts only the boxes and
  lines run straight; leave them room.
- **Shapes**: `shape="cylinder"` on any element draws it as that shape: `diamond`,
  `hexagon`, `chevron`, `semicircle`, `document`, `cloud`, BPMN `task`, `start`, `end`,
  `gateway exclusive`, `event timer` and more. `clip-path: polygon(…)` cuts any other
  straight-edged shape.
- **Icons**: `<icon name="app service">`. Loose names work for every service of both
  packs; an unknown name is reported with suggestions.
- **Connections**: `<script type="application/json">`, a list of `["from", "to", "label"]`
  or objects with `dashed`, `out`/`in` (the sides), `both`, `via`, `color`. A list in `to`
  or `from` draws one bundle with a shared trunk.
- **Drawing script**: `<script type="graphally">` runs after layout with every element's
  box, for marks no box gives (tracks, rings, leaders, brackets, slabs): `arrow`,
  `connect`, `depend`, `draw.moveTo(…).lineTo(…)`, `draw.arc`, `gate`, `text`, `icon`,
  `shape`.
- **Helpers**: `<script type="graphally" before>` calls `schedule()` and `timeline()`
  (plans) or `sequence()` (sequence diagrams) before layout.
- **Themes**: `--themes` writes `diagram-dark.svg` beside the light one; `--dark` draws
  dark only.

The whole format, with every class, shape, option and call: [references/format.md](references/format.md).

## Problems and fixes

| Problem | Fix |
|---|---|
| `unknown-id` | a connection names an id that does not exist: the suggestion is the closest |
| `unknown-icon`, `unknown-shape`, `unknown-utility` | use the suggested name, or a theme colour for a colour class |
| `label-crowded` | widen the gap the line runs through, or shorten the label |
| `override-ignored … by=x` | the side named in `out`/`in` is blocked by `x`: choose another side |
| `short-end` | an arrowhead sits on a bend right before its box: give the line more room there |
| `lines-overlap` | two lines share a stretch: give one other sides (`out`/`in`) or `via` points |
| `unroutable` | the line has no way through: widen a gap, or give it `via` points |
| `page-overflow` | the content is wider than `width`: widen `width`, or narrow the columns |
| `text-overlap` | two texts collide: give one more room |
| `warning: box-overflow` | a box or text sticks out of the drawn box holding it: widen the holder or narrow what is inside. A warning, so the render passes: leave it when it is meant |
| `script-error` | the message and line say what failed in a script |

## References

Each teaches techniques through a complete example; a figure takes what it needs from as
many as it needs.

| Techniques | Reference |
|---|---|
| Designing a figure: idea starters by point, the moves that make it read at a glance | [references/design.md](references/design.md) |
| Containers in containers (VNets, subnets), a map of named areas, peering and private links | [references/network.md](references/network.md) |
| One column per leaf and one row per level; a bus from a parent to its children | [references/hierarchy.md](references/hierarchy.md) |
| Lanes, events and gateways; a happy path with its branches | [references/process.md](references/process.md) |
| Participants across, messages down in time, fragments | [references/sequence.md](references/sequence.md) |
| Dates as grid columns: bars, milestones, dependencies | [references/plan.md](references/plan.md) |
| Rows lined up across stages (subgrid), phase chevrons, gates on boundaries, matrices | [references/charts.md](references/charts.md) |
| Shapes cut with `clip-path`, placing by angle and distance, geometry drawn around the layout | [references/documents.md](references/documents.md) |
| Drafting a diagram of a Terraform repository from the code | [references/terraform.md](references/terraform.md) |
| The whole format: every class, shape, option and call | [references/format.md](references/format.md) |

## Scripts

- `scripts/graphally.mjs render <file.html>... [--png | --png1x | --png2x] [--themes |
  --dark] [--out dir] [--recompute]`: compiles every `<diagram>` in the file to SVG;
  `--png` adds a half-size preview, `--png1x` a full-size one, `--png2x` a sharp PNG to
  publish, `--themes` a dark copy, `--recompute` ignores the previous layout. Several
  files render in one call, in parallel; render them together rather than one by one.
- `scripts/edit.mjs <file.html> --move id dx,dy | --connect from to [label] | --line 'a->b' json | --unline 'a->b' | --lines`:
  patches moves and connections and keeps the rest of the file as written.
- `scripts/tf2graphally.mjs <terraform dir> [--out file.html] [--title "…"]`: drafts a
  diagram of a Terraform configuration.
- `scripts/fetch-icons.mjs [azure] [aws] [--force]`: downloads the icon packs; the first
  render does it by itself.

They need only Node.js and an installed Chrome, Chromium or Edge. If the render prints
`graphally needs Chrome, Chromium or Edge`, run `npx playwright install chromium` once, or
set `CHROMIUM_PATH` to a browser executable. Offline, diagrams render without vendor icons
and say how to fetch them later.

---
graphally · Copyright (c) 2026 Kamil Wilczyński (kwilcz) · https://github.com/kwilcz/graphally ·
Apache License 2.0 (LICENSE.txt, NOTICE.txt).
