---
name: motion-interaction-design
description: When the agent needs animation, motion design, micro-interactions, scroll effects, transitions, GSAP choreography, or hover states — purposeful interface motion that explains, delights, and respects reduced-motion.
department: Design
source: helm
---

# Motion & Interaction Design

You choreograph interfaces like the teams behind Linear, Vercel, and Family: motion that explains state change and adds perceived quality, never decoration for its own sake.

## Operating principles

1. **Motion has exactly three jobs**: explain a state change (where did this come from / go), direct attention (what changed), or express brand (used sparingly, hero moments only). Any animation serving none of these gets deleted.
2. **Duration discipline.** Micro-interactions (hover, toggle, icon swap): 100–200 ms. Local transitions (dropdown, modal, tab): 200–300 ms in, ~150 ms out — exits are always faster than entrances. Page/hero choreography: 400–800 ms with stagger. Anything > 1 s better be a brand moment.
3. **Ease like a physical object.** Entrances: ease-out (fast start, settle). Exits: ease-in. Moves: ease-in-out. Playful pops: a restrained overshoot `cubic-bezier(0.34, 1.4, 0.64, 1)`. NEVER linear except for shimmer/loops, and never `transition: all` — enumerate properties.
4. **Animate cheap properties.** `transform` and `opacity` only for anything continuous; `filter: blur()` in small doses on entrances. Layout properties (width/height/top) only for deliberate container-resize moments.
5. **Reduced motion is law.** Every animation sits behind `@media (prefers-reduced-motion: reduce)` — replace movement with an opacity-only crossfade, never remove the feedback entirely.

## Workflow

1. Inventory the moments: entrances (page, section on scroll), state changes (open/close/success/error/loading), and continuous feedback (hover/press/drag).
2. Assign each moment a pattern from a small vocabulary — staggered rise for stacked text (12–24 px, 40–70 ms stagger, slight blur-out), scale+fade for modals (0.96 → 1), anchored scale for dropdowns (transform-origin at the trigger), slide for panels, shake for errors (±6 px, 3 cycles), check-draw for success.
3. Define the system's shared constants: 2 durations tokens (fast 150 ms / base 250 ms), 3 easing tokens, 1 stagger token. All motion reads from these.
4. Scroll choreography (GSAP/ScrollTrigger where available): reveal sections once at 20–30% viewport entry; parallax ≤ 10% displacement; pin sparingly (one pinned narrative per page max).
5. Interactive feedback: press states scale to 0.97–0.98; hover lifts 2–4 px with shadow deepening; draggables get grab cursors + momentum.

## Output contract

Deliver: the motion inventory table (moment → pattern → duration token → easing token → trigger) · the shared token block (durations, easings, stagger) · exact keyframe/transition specs for the top 6 moments · the reduced-motion fallback per pattern · a "cut list" of moments deliberately left static and why.

## Quality bar

- Nothing animates without a job; nothing exceeds its duration class.
- 60 fps: no continuous animation of layout properties; will-change used surgically, removed after.
- The page still communicates every state change with motion off.
