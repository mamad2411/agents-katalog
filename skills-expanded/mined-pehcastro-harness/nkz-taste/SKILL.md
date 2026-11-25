---
name: nkz-taste
description: Design and build product UI with taste, for native mobile (iOS-first, Expo / React Native) and web (products, landing pages). Supports named styles with exact visual contracts and reusable layouts. Covers the product decision (what the screen is for, what the one action is, what to cut), the craft floor (four states, forms, accessibility, microcopy), and the feel (design, interaction, animation). Use when building, refactoring, polishing, or reviewing any screen, component, flow, or page, and when a request sounds like "make this feel designed", "elevate the design", "apply polish", "review this for craft", or "remove the ux noise".
license: MIT
metadata:
  version: "2.2"
  requires: nothing. Uses project tokens or installs the explicitly selected style into them.
---

# Taste

Taste is the art of the invisible. You look at it and you know it is good, and you cannot point at the one thing that made it so.

Four layers, in this order. Each one is a different question, and a good answer to a later question cannot rescue a bad answer to an earlier one.

| Layer | Question | Where |
|---|---|---|
| **Product** | Should this exist, and what is its one job? | [product.md](./references/product.md) |
| **Craft** | Does it work for everyone, in every state? | [craft.md](./references/craft.md) |
| **Direction** | What should it look like, and why this and not the default? | [direction.md](./references/direction.md) |
| **Feel** | Does it look, behave, and move well? | design / interaction / animation files |

Most UI work fails at Product and gets polished at Feel. A beautiful screen that does the wrong job is a more expensive mistake than an ugly screen that does the right one. Do not start at Feel.

Within Feel:

```
Design      → how it looks
Interaction → how it behaves
Animation   → how it feels
```

Two rules hold across all of it:

- **Nobody should notice an animation.** If a user notices motion, it was too much. Motion is for continuity and feedback, never for attention.
- **Interaction without feedback is not interaction.** Every action confirms itself inside 100ms, before the work is done.

## The loop

Run this in order. Do not skip step 1 because the request sounds small: a request for one button still sits inside a screen that has a job.

1. **Frame the product.** Name the surface, the user's job, the one primary action, and what happens before and after. Identify unnecessary additions, if any. Read [product.md](./references/product.md). Ten minutes here changes what you build; ten minutes at step 6 changes a shadow.
2. **Survey what is in place.** Find the token source, the component library, the animation library, the existing conventions. See *In place vs out of place* below.
3. **Resolve the style.** If a style was selected, load its contract and recipes using the router below; those decisions are already made. Otherwise **set the direction**, when the work is new or brand-facing. State the read, set the intensity dials, write the four-part plan, then critique it against the answer you would give any similar brief. Read [direction.md](./references/direction.md). Skip this only when you are working inside an established system that already made these decisions.
4. **Pick the platform and load the files.** Native mobile and web share philosophy and share almost no mechanics. See the router below.
5. **Propose before you build**, when the change is more than a component. State the frame, the direction, the layout, and the trade-off you are making. One paragraph, not a document.
6. **Build**, installing the selected style centrally when applicable, then taking every visual value from the project's token source. Never invent a hex, a font, or an arbitrary px inline. See *Tokens* below.
7. **Pass the pre-flight.** Blocking. See below.
8. **Report the trade-offs.** Name what you knowingly skipped and why, and name every new token the project needs.

## Named styles

A style is a portable visual contract, not a color preset or a sample app. It fixes palette, type, geometry, surface construction, controls, and motion. Recipes map that contract to different product content.

| Style | Platform / intent | Read when selected |
|---|---|---|
| **recess** | Web dashboards and tools; recessed frames, raised neutral faces, compact typography, restrained pixel texture | [style.md](./styles/recess/style.md), then [recipes.md](./styles/recess/recipes.md) |

`Use nkz-taste, style recess` is enough to select it. Read both files before building; a name or summary is not the specification. Load only the selected folder. Recess is not the skill's automatic default. If no style is selected, preserve an established system or follow direction.md for new work. If a named style is missing or unsupported on the target platform, state that instead of silently substituting one.

**Precedence:** explicit user constraints first; product correctness, accessibility, and interaction requirements remain mandatory. Within those bounds, the selected style controls aesthetic decisions over generic reference examples and existing library defaults. Preserve working component behavior while replacing visual defaults. Do not blend styles or invent a fresh direction on top. A user request to preserve a font or palette is an intentional adaptation: apply it and report the difference from the contract.

Selecting a style authorizes creating or mapping its tokens and shared component styles within the requested scope. It does not authorize changing product behavior or restyling unrelated surfaces. For a single-page application of a style, scope its theme and its portals; for an app-wide request, apply it centrally. Do not ask again simply because the current tokens differ.

For future styles, add `styles/<name>/style.md` and `recipes.md`, then one catalog row above. The contract states platform, fixed values, allowed adaptations, and checks. Recipes state dimensions, composition, responsive behavior, and when each pattern applies. Keep both independent of a source repository, screenshots, brand names, and example business data. Do not copy shared accessibility rules into every style.

## Router

Pick the platform first. The philosophy is universal, the mechanics are not.

- **Native mobile** (iOS-first, Expo / React Native): touch, gesture, haptics, springs, sheets, safe areas. No hover, no CSS, no tables, no sidebars.
- **Web** (product or landing page): mouse and keyboard, hover and focus, CSS / Motion, denser layouts allowed.

| Concern | Native mobile | Web |
|---|---|---|
| Product frame | [product.md](./references/product.md) | [product.md](./references/product.md) |
| Craft floor | [craft.md](./references/craft.md) | [craft.md](./references/craft.md) |
| Aesthetic direction | [direction.md](./references/direction.md) | [direction.md](./references/direction.md) |
| What not to reach for | [ai-tells.md](./references/ai-tells.md) | [ai-tells.md](./references/ai-tells.md) |
| Design | [mobile-design.md](./references/mobile-design.md) | [web-design.md](./references/web-design.md) |
| Interaction | [interactions.md](./references/interactions.md) → *Mobile Interaction* | [interactions.md](./references/interactions.md) |
| Animation | [animations.md](./references/animations.md) → *Native motion* | [animations.md](./references/animations.md) → CSS / Motion |
| Why a rule exists | [laws.md](./references/laws.md) | [laws.md](./references/laws.md) |

Load what the task needs, not everything.

- **A signup form:** product, craft, one design file.
- **A landing page or anything brand-facing:** product, direction, ai-tells, one design file, animations.
- **A component inside an existing system:** craft, interactions, animations.
- **A review of existing code:** craft and laws, because craft is where things break and laws is how you explain it. Add ai-tells if the complaint is that it looks generic.
- **A redesign:** product (*Redesigns*), direction unless a style already fixes it, then the rest.
- **A selected style:** product, craft, the platform design file, and that style's two files. Shared references supply behavior; the style supplies the visual contract.

Every task loads at least one design file. Craft is never optional: it is the floor, not a specialization.

## The always-rules

These seventeen apply to every surface on every platform. If you remember nothing else, apply these. Everything in the reference files elaborates them.

**Product**

1. One screen, one job. If you cannot say the job in a sentence, the screen is two screens.
2. Establish one dominant task or fact. When a primary action exists, make it clear; do not invent a button for a read-only surface.
3. Cut before you add. The best version of a feature is the one with fewer elements that still does the job.
4. Push complexity into the system, never onto the user. Detect the timezone, pre-select the safe option, parse the messy input.

**Craft**

5. Four states, every data view: empty, loading, error, success. All four designed, all four coded.
6. Errors say what happened, why, and how to fix it, and offer a way back. Never "Something went wrong."
7. Offer undo for reversible destructive actions and confirmation for irreversible ones. Confirmation does not make an action reversible.
8. Body text contrast at least 4.5:1. Interactive targets at least 44×44 on touch, 24×24 minimum anywhere.
9. Color is never the only signal. Pair it with an icon, a label, or a shape.
10. Everything reachable and operable by keyboard on web, with a visible focus ring. Never `outline: none` without a `:focus-visible` replacement.

**Feel**

11. Space is the primary hierarchy tool. Space between groups is always larger than space within a group.
12. Every value comes from the token scale. Use the selected scale, including its specified optical offsets and frame thicknesses.
13. Feedback inside 100ms, always. Optimistic where the action is low risk.
14. Ask whether it should animate at all before asking how. High-frequency and keyboard-initiated actions do not get entrance choreography. Immediate visual feedback remains; a selected style may specify brief hover/press transitions.
15. Entry/exit motion is transform and opacity only, under 300ms for UI, ease-out entering, exits faster than entrances, and it honors reduced motion. Never `ease-in`, never from `scale(0)`.
16. Emphasis is rare. If everything is emphasized, nothing is.
17. For every distinctive choice, ask: did I choose this, or reach for it? If you cannot say why it suits this subject, it is a default in costume. See [ai-tells.md](./references/ai-tells.md).

## In place vs out of place

Before you build, find out what the codebase already has. This decides whether you build on top or open a conversation.

**In place** means at least one of the three layers has structure to build on:

- **Design:** a token source, a Tailwind or theme config, CSS custom properties, a component library (shadcn, HeroUI, a custom kit). This does not mean the design is good. It means styling will be consistent.
- **Animation:** an animation library in the dependencies (Motion, Reanimated, CSS keyframe utilities). One source of truth beats scattered inline CSS.
- **Interaction:** existing patterns for feedback, loading, and error, whether they are good or not.

**Out of place** means the layer is missing entirely. An explicitly selected style supplies the visual system: install its tokens and build on appropriate accessible primitives. Otherwise use the task scope and existing conventions to decide whether to establish a shared foundation; ask only when a missing decision materially changes the requested result. Do not invent an unrelated design system while implementing a button.

You will often be asked for something small inside a large codebase. The survey is still cheap, and it is what keeps your work from reading as a foreign object.

## Tokens

Every visual value references the project's token source by name. Never an inline hex, font name, or arbitrary px.

**With a selected style:** map its complete palette, fonts, geometry, and component recipes into the central token/component layer. Add missing tokens there using the specified values. Do not use the closest shadcn token when it changes the contract. Alias names where useful; preserve computed values and surface relationships. Include portal surfaces and both supported modes. Report intentional adaptations, not a request to approve tokens already authorized by the style choice.

**Without a selected style:** when a rule needs a value the project does not have, do not invent it inline. Instead:

- Use the closest existing token for now.
- Flag it in your report as a **new pattern**: which property, what value the rule implies, where it is needed, and why nothing existing fits.
- Let the developer decide whether it joins the system.

Without a selected style, when the project has no token source at all, follow whatever convention the codebase already uses, say that you did, and recommend establishing one. A skill that quietly adds a sixteenth shade of grey is doing damage.

## Pre-flight

**Blocking.** Do not report the work done until every line passes or you have written down which one you waived and why. A waived item is a stated trade-off, not a silent omission.

- [ ] The surface has a clear task or primary fact, with an appropriately emphasized action when one exists.
- [ ] Every async surface designs and codes empty, loading, error, and success.
- [ ] Every interactive element has default, hover or focus-visible, active, and disabled, plus loading where async.
- [ ] Every form input has an associated label, the right `type` and `inputmode`, an `autocomplete` value, and validation on blur.
- [ ] Every error states what, why, and how to fix, with a recovery path.
- [ ] Every destructive action has undo or confirmation.
- [ ] Body text at 4.5:1 or better, interactive components at 3:1, focus rings at least 2px and 3:1.
- [ ] Touch targets at least 44×44, pointer targets at least 24×24.
- [ ] Keyboard reaches and operates everything, focus is visible and never obscured by sticky chrome.
- [ ] The layout survives 320px width on web, and the keyboard, rotation, and safe areas on mobile.
- [ ] Every animation has a purpose in one sentence. Nothing keyboard-initiated or high-frequency gets an entrance animation.
- [ ] Entry/exit motion is transform and opacity only, under 300ms for UI, correctly eased, exits faster than entrances, reduced-motion handled. No `transition: all`, no `scale(0)`, no `ease-in`.
- [ ] Anchored elements scale from their trigger. Hover is gated behind `@media (hover: hover)`.
- [ ] Every visual value came from a token. Selected-style values are installed centrally; other new patterns are flagged.
- [ ] If a style is selected, its contract and recipe checks pass across content, loading, empty, error, overlays, and supported modes; deviations are stated.
- [ ] Nothing added that the stated job did not require.
- [ ] For brand-facing work: the [ai-tells.md](./references/ai-tells.md) mechanical count passes, and one accent, one radius system, one theme hold across the whole page.
- [ ] Every visible string re-read. Nothing grammatically broken, invented-precise, or trying to sound thoughtful.

## Reporting

Say which layer dominated, name the trade-offs you made, and list the new tokens the project needs. Then ask for feedback. Do not narrate the rules you followed.
