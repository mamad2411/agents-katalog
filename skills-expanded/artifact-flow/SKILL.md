---
name: artifact-flow
description: OUTPUT IS ALWAYS A SINGLE `.html` FILE (never `.md`, never separate per-screen files) containing multiple screens navigated by clickable hotspots and/or a hash router. Use this skill whenever the user asks for a clickable prototype, clickable mockup, multi-screen flow, user-flow walkthrough, "click-through demo", "tap-through prototype", interactive wireframe, or any artifact whose primary shape is "a sequence of screens linked by hotspots". Pair with `artifact-css` for the underlying design system. Do NOT use for slide decks (use `artifact-deck`) or for fully-functional editors (use `artifact-editor`).
---

# artifact-flow

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file.** A clickable flow has many screens. ALL of them live in the same file, switched by JavaScript (clicks on hotspots, hash routing). NEVER one HTML per screen.
>
> File extension is `.html`. File name typically `<flow>-prototype.html`.

---

A clickable, hotspot-driven prototype. The reader experiences a multi-screen user flow by clicking marked targets on each screen. Useful for walking stakeholders through a feature before it's built, or for capturing a UX path in a single shareable file.

Read `artifact-css/SKILL.md` first for the OUTPUT CONTRACT, the design tokens, and the class vocabulary. This skill uses **vanilla JS only** — no jQuery required.

## When to reach for this skill

- User says "make me a clickable mockup of X", "wireframe the signup flow", "show me what the multi-step migration UI would look like".
- User wants a stakeholder to *feel* the flow without engineering it.
- User wants a single-file deliverable that captures an end-to-end UX path.

If they want one screen per slide for a presentation, use `artifact-deck`. If they want a fully working editor with state, use `artifact-editor`.

## Anatomy of a flow

Four element types.

1. **Flow chrome** — fixed top bar with: flow title, current screen N / total, breadcrumb of screen names. Optional "Reset to start" button.
2. **Screen** — a `<section class="screen" id="scr-<key>">`. Only the active screen is visible. Each screen is a mocked-up page (header, body, ghost CTAs, fake data — whatever the real UI would show).
3. **Hotspots** — clickable regions overlaid on screen elements. Each carries a `data-go="<screen-key>"` attribute pointing to the next screen. Hotspots can be visible (subtle pulsing ring) or invisible (full-bleed transparent layer over a button).
4. **Annotations** — optional small numbered callouts on the side of the canvas explaining what's happening on this screen. Toggleable via "Notes on / off".

Five to ten screens is the right zone. More = wireframe inflation. Fewer = doesn't justify the format.

## Hotspot styles

Three patterns. Pick per screen.

| Pattern | When |
|---|---|
| **Full-bleed** — invisible div covering an entire CTA / button | Most natural — user clicks where they'd click in the real UI |
| **Ringed** — a subtle dashed outline over the active region, pulsing | First-time flows where the user needs to be told where to click |
| **Visible button** — labelled `.button` that says "Continue" / "Next" | When mocking happy-path narration over a complex screen |

Avoid mixing patterns within one screen. Pick one per screen.

## Navigation contract

- **Click on a hotspot** — go to the screen it points to.
- **Back button in chrome** — return to previous screen in history.
- **Hash routing** — `#scr-<key>` jumps to a named screen. Shareable.
- **Reset** — return to first screen, clear history stack.
- **N or →** — advance to "primary next" hotspot (the one marked `data-primary`).
- **B or ←** — go back.

## Fallback contract

With JS disabled:
- All screens render stacked top-to-bottom.
- Each screen is labelled with an `h2` header so the reader can tell what's what.
- Hotspots render as visible `<a>` anchors linking to `#scr-<key>` — still navigable via in-page anchors.

## Voice and density rules

1. **Real-looking data.** Fake screens with `Lorem ipsum` look like a wireframe. Fake screens with plausible names, plausible numbers, plausible copy look like a real preview. Use the second.
2. **One primary action per screen.** Even if the real UI has six buttons, the flow walks a happy-path. Other buttons render as `.muted` ghosts that don't react.
3. **Don't fake what the next screen looks like.** If clicking "Save" in the real UI would show a toast and stay on the page, then in the flow clicking "Save" should also stay (with a faked toast), not navigate to a new screen.
4. **Annotate sparingly.** Annotations are for capturing the *why* of a screen, not the *what*.
5. **The closing screen exists.** Every flow ends. The last screen has a "Flow complete" callout + a "Restart" button.

## Common mistakes

- **Hotspots that go nowhere.** If `data-go` references a screen ID that doesn't exist, clicking the hotspot is silently broken. Always lint the IDs.
- **Sequential numbering only.** Real UX is a tree, not a chain. Use named screen keys (`scr-cart`, `scr-checkout`, `scr-confirm`) — not `scr-1`, `scr-2`, `scr-3`.
- **Wireframe greyboxes.** A flow is supposed to *feel* real. Use the actual artifact.css palette and components. Don't go grey-on-grey unless that's literally the brand.
- **No back button.** A flow without back is a presentation. The whole point is interactivity.

## After the artifact

Offer two derivatives:
1. A flat screen map (text outline) listing all screens and their primary outgoing hotspots. Useful for a PR description.
2. A list of suggested next steps if this prototype were greenlit (what to build first, what's risky, what's unknown).
