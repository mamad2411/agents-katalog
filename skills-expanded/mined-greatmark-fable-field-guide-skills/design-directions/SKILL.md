---
name: design-directions
description: >-
  Generate several deliberately divergent single-file HTML prototypes with
  fake data so the user can react before real implementation — iterable
  HTML, not one generated image or a Cursor canvas. Use when the user wants
  design options or a UI mockup to react to ("mock up a page"), says
  "design directions", "出几个设计方向", "出几版 UI", "哪种页面风格好",
  "我说不好想要什么样", or can only judge a design by seeing it; also
  consider offering directions first when the user asks to build a UI whose
  look was never discussed. Not for
  technical feasibility spikes or functional MVPs ("做个原型验证跑不跑得通"),
  and not for copying one concrete reference as the end state (use
  reference-hunt); a reference named only as inspiration stays here.
---

# Design Directions

The user has "unknown knowns": criteria they can only articulate when they see
something. Give them things to react to, cheaply, before touching real code.

## Workflow

1. Confirm scope from context: what surface is being designed (page, panel,
   component, report) and what data it shows. Do not ask more than one
   clarifying question; guessing reasonably is part of the point. If it
   turns out the user wants a technical feasibility spike, say this skill
   does not apply and build the spike instead.
2. Build **4 deliberately different directions** by default (fewer only if
   the user asks; at one direction this skill's divergence machinery is
   moot — say so, and either just build it or propose a second contrasting
   take). Different means different layout philosophy, density, hierarchy,
   or interaction model — not one design with four color schemes. Before
   building, put all directions on one shared set of axes (layout
   philosophy, density, hierarchy, interaction model) and state each
   direction's position on them; every pair of directions must sit at
   opposite ends of at least one axis.
3. Deliver as self-contained HTML: inline CSS/JS, realistic fake data
   hardcoded inline (in the language of the conversation), no build step,
   no network calls. Aim for high-fidelity visuals — the user should react
   to the design, not the sketchiness; static is fine, and add only the
   minimum JS that makes the core loop legible (e.g. a ticking timer for a
   timer app). When interaction itself is the core loop (charts, drag,
   filtering), prefer rendering one frozen mid-interaction moment (tooltip
   already open, panel mid-drag) over scripting it; script only what a
   static frame cannot convey. Include a viewport meta; default to desktop
   web unless the surface is obviously mobile — then wrap in a phone-width
   (390px) frame. For non-web surfaces (CLI/TUI, email, native), still
   deliver HTML but simulate the medium honestly — monospace grid and
   16-color palette for a terminal — and never show an effect the real
   medium cannot render. Default to one file per direction (a single file
   with a direction switcher only if the user asks). Write files to a
   scratch directory under the project root (`./design-directions/`; in a
   non-project directory, confirm where to put them first), never into the
   real app; do not commit them. In a git repo, exclude the directory:
   `n=design-directions/; p="$(git rev-parse --git-path info/exclude 2>/dev/null)" && { mkdir -p "$(dirname "$p")" && { grep -qxF "$n" "$p" || echo "$n" >> "$p"; }; } 2>/dev/null || echo "note: could not exclude — leaving it untracked, never staging it"`
4. Name each direction with a short memorable label and one sentence on the
   idea behind it, so the user can say "the second one, but denser".
5. Self-check before showing: render each file (headless browser or
   screenshot tool if available) and verify it holds up at the target
   viewport — no layout breakage, all fake data visible, no console errors.
   Then the divergence gate: if the screenshots shown side by side would
   read as tweaks of one design, rebuild the weakest until they don't. If
   no renderer is available, downgrade explicitly: run static checks (tags
   balanced, inline JS parses, no external URLs, viewport meta present) and
   tell the user the files are unrendered — ask them to report any breakage
   on first open. Fix what you find before presenting; a broken first
   render defeats the purpose.
6. Present for reaction: screenshot each direction and embed the images in
   your reply (fall back to `open design-directions/*.html` if you cannot
   render), and ask what to keep and what to kill. Then iterate on the
   chosen direction, or combine elements on request.

## Rules

- Do not modify application code, add dependencies, or wire up backends at
  this stage.
- Use realistic fake data (plausible names, numbers, edge-case lengths) —
  lorem ipsum hides layout problems.
- If the project has an established design system, keep its tokens and
  branding; diverge on layout, density, and information architecture instead.
- Do not build these prototypes as Cursor canvases: canvas locks a single
  flat visual style and only works in Cursor.
- Push at least one direction beyond the user's stated taste; the point is
  to discover what they didn't know they wanted. Under an established
  design system this rule stays inside the tokens: push on structure and
  information architecture, not on brand.

## Examples

Four directions for a pomodoro timer:

- **Monolith** — one giant timer, fullscreen, nothing else on screen.
- **Workbench** — three-pane workspace: task list, timer, session stats.
- **Garden** — playful narrative: each finished session grows a plant.
- **Ticker** — data-dense terminal: streaks, logs, and stats in a grid.
