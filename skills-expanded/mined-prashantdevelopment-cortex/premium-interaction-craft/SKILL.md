---
name: premium-interaction-craft
description: Micro-interaction and interaction-state quality bar for UI components — hover, press, focus, loading, success/error feedback, transitions, easing and timing. Use when building or polishing buttons, cards, menus, forms, toggles, modals, toasts, or when the user says the UI feels "cheap", "static", "not snappy", or wants it to feel premium.
---

# Premium Interaction Craft

Written for this agent-kit. The goal is interfaces that feel responsive and intentional — not more animation. Pair with `motion-framer` (React), `gsap-core` (timelines), `high-end-visual-design` (visual polish).

## 1. Every interactive element has all its states

| State | Requirement |
|---|---|
| Default | Clear affordance: it looks clickable/typeable. |
| Hover (pointer devices only) | Subtle change within 100–150ms. Wrap in `@media (hover: hover)` so touch devices don't get sticky hover. |
| Active / pressed | Immediate feedback (<50ms): e.g. `scale(0.97)` or darker fill. |
| Focus-visible | Visible ring using `:focus-visible`, ≥ 3:1 contrast, never `outline: none` without a replacement. |
| Disabled | Lower contrast + `cursor: not-allowed` + real `disabled`/`aria-disabled`. Explain why if not obvious. |
| Loading | Keep width stable (no layout jump), show spinner/progress, block double-submit. |
| Success / error | Inline, specific, reversible where possible. Errors say what to do next. |
| Empty | Every list/table/search has a designed empty state with a next action. |

## 2. Timing and easing

- Micro feedback (hover, press, toggle): 100–200ms.
- Small UI transitions (dropdown, tooltip, accordion): 150–250ms.
- Larger movement (modal, drawer, page section): 250–400ms. Anything above 500ms must be decorative and skippable.
- Enter with ease-out (fast start, soft landing); exit faster than enter (~70% of enter duration) with ease-in.
- Springs for things the user drags or throws; tweens for things the system moves.
- Never use `linear` for UI movement (only for spinners/progress).
- Stagger lists by 30–60ms, cap the total stagger so the last item is in by ~400ms.

## 3. Performance rules

- Animate `transform` and `opacity` only. Avoid animating `width/height/top/left/box-shadow/filter: blur()` on large areas.
- Use `will-change` only during the animation, never globally.
- No animation should block input. Buttons must work while a hover animation is still running.

## 4. Feedback patterns worth using

- Optimistic UI for fast, reversible actions (like, toggle, reorder) with rollback on failure.
- Toasts for background results; inline messages for form errors. Toasts that contain actions do not auto-dismiss too fast (≥ 5s, pause on hover/focus).
- Skeletons that match the final layout for loads > 300ms; nothing for loads < 300ms (avoid flash).
- Copy-to-clipboard shows a check state for ~1.5s.
- Magnetic buttons, cursor followers, tilt cards: only on hero/marketing surfaces, disabled on touch and reduced motion.

## 5. Accessibility is part of craft

- Respect `prefers-reduced-motion`: replace movement with opacity or instant state changes.
- Touch targets ≥ 44×44px (WCAG 2.2 minimum is 24×24; aim for 44).
- Keyboard: every pointer interaction has a keyboard path (Enter/Space on custom controls, Esc closes overlays, focus is trapped in modals and returned on close).
- Announce async results with `aria-live="polite"` where a sighted user would see a change.

## 6. Done checklist

- [ ] All states in section 1 exist for every interactive component touched.
- [ ] Durations/easing follow section 2; one consistent set of tokens (e.g. `--dur-fast`, `--dur-base`, `--ease-out`).
- [ ] Tested with mouse, keyboard only, touch (or device emulation), and reduced motion on.
- [ ] No layout shift during loading/success/error transitions.
