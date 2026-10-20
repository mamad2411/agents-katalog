---
name: ui-motion-design
description: Add tasteful, purposeful motion to UI components — easing curves, spring physics, timing, and micro-interactions — instead of generic linear CSS transitions or no motion at all. Use whenever a design/frontend task asks for animation, "make it feel alive," hover/tap/focus feedback, page or state transitions, or explicitly mentions motion design.
---

## When to add motion (and when not to)

Motion should communicate something — state change, causality, spatial relationship, or feedback that an action registered. It's not decoration.

**Add it for:** button/control feedback (press, hover, focus), items entering/leaving a list, expanding/collapsing sections, page or modal transitions, loading states, drag interactions.

**Skip or minimize it for:** dense data tables, dashboards refreshing frequently, anything a power user will interact with dozens of times a minute (repeated motion becomes friction, not delight), and always respect `prefers-reduced-motion`.

## Core principles

1. **Ease out for entrances, ease in for exits.** Things that appear should decelerate into place (`cubic-bezier(0.16, 1, 0.3, 1)` or similar "ease-out-expo" curves); things that disappear should accelerate away. A linear or symmetric ease reads as mechanical, not natural.
2. **Prefer spring physics over fixed-duration eases for interactive elements** (drags, toggles, anything the user's input directly drives) — a spring responds to interruption naturally; a fixed-duration tween looks broken if re-triggered mid-animation.
3. **Duration matches distance and importance.** Micro-interactions (hover, toggle, small icon state): 100–200ms. Larger transitions (modal open, page section reveal): 200–400ms. Never exceed ~600ms for something blocking user flow — beyond that it reads as slow, not premium.
4. **Stagger, don't synchronize, groups of elements.** A list of 5 items appearing at once looks like a glitch; a 20–40ms stagger between them reads as intentional and guides the eye.
5. **Never block input.** An animation should not prevent the user from immediately triggering the next action (e.g. clicking through mid-transition) unless there's a real reason to (irreversible action confirmation).

## Implementation patterns

**Pure CSS** (no animation library available/needed):
```css
.button {
  transition: transform 150ms cubic-bezier(0.16, 1, 0.3, 1),
              background-color 150ms ease-out;
}
.button:active { transform: scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  * { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}
```

**Framer Motion / React** (when the stack already includes it):
```jsx
<motion.div
  initial={{ opacity: 0, y: 8 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ type: "spring", stiffness: 400, damping: 30 }}
/>
```
Use `type: "spring"` with `stiffness`/`damping` (not `duration`) for anything the user can interrupt by re-triggering it (toggles, drags, hover-driven state).

## Anti-patterns

- Animating *everything* on a page — motion loses meaning when nothing is still.
- Bouncy/overshoot easing on serious, data-dense, or enterprise UI — reserve spring overshoot for playful/consumer contexts.
- A different easing curve or duration for every element — pick 2–3 motion "tokens" (a fast one, a standard one, a spring) and reuse them, the same way a type scale reuses a small set of sizes.
- Motion that can't be skipped/reduced for users with `prefers-reduced-motion` set.

## Related skills in this repo

- **frontend-design**: This skill's motion guidance is the animation-specific layer on top of that skill's general aesthetic principles — use both together when a build needs to feel alive, not just look right statically.
- **web-artifacts-builder**: Apply spring-based motion patterns to interactive artifact components.
- **design-templates**: The device-frame and product-3d-tilt templates can take subtle entrance/hover motion from this skill instead of being fully static.
- **premium-html-presentation**: Slide-transition timing/easing should follow the duration guidance here rather than defaulting to whatever the framework ships with.
- **design-dev-resources**: Its Motion.ed entry is a visual, interactive reference for the same easing/delay/masking/parallax techniques this skill describes in writing — use it to see a technique before applying it.
- **gsap-core** and its 7 siblings (`gsap-timeline`, `gsap-scrolltrigger`, `gsap-react`, `gsap-frameworks`, `gsap-utils`, `gsap-performance`, `gsap-plugins`): The official GreenSock implementation skills — use this skill to decide *what* motion should communicate, those for the actual GSAP code.

## Notes

Source: a "Claude Replaces Designers" screenshot-carousel video (@vibes.codes), which referenced a motion-focused skill in the style of well-known UI-motion practitioners (e.g. Emil Kowalski, known for motion-heavy open-source UI work). This skill captures the general, well-established motion-design principles that style is known for — it doesn't quote or attribute specific claims to any individual, since no verifiable source material was available to ground those.
