---
name: claude-design-idea-to-ready
description: Take a UI from a one-line idea to on-brand, shippable design with Claude, in the correct order — brand foundation first, then components, screens, interactions, accessibility, and only then generation via /design. Use whenever someone wants to design, redesign, or generate a screen, page, component, or onboarding flow and wants the output to match an existing brand instead of looking like generic AI UI. Triggers on "design this screen", "build a UI for", "make this on-brand", "redesign", "generate a page/component", "use /design", or any task that will produce visual interface.
license: MIT
author: "@malik_chohra · Code Meet AI"
---

# claude-design-idea-to-ready

Drive a UI from idea to ready design in the order that actually produces on-brand output: the foundation before the screens, the generation last. This is the "brand first, generate second" pipeline. It composes with a memory bank-style memory bank (drop it in your skills folder) or runs standalone.

## The core rule

The model can only be as on-brand as the constraints it has before it generates. So the work is upstream. Never run `/design` (or generate any UI) until steps 1 to 5 exist. If they do not exist, scaffold them first.

## When this fires

Any task that will produce visual interface: a new screen, a redesign, a component, a page, an onboarding flow, a "make it on-brand" pass. If the user opens with `/design` directly, stop and check that the foundation (step 1) exists first.

## The pipeline (run in order)

1. **Foundation.** Locate or scaffold two files: `design/tokens.ts` (one source of truth: color, type, spacing, radius, as names not hex) and a `## Design rules` block in `CLAUDE.md` (one accent, monochrome base, 8pt spacing, one primary action per screen, no glassmorphism). Read `references/foundation-templates.md`. Nothing else proceeds until these exist.
2. **Components before screens.** List the components the brief needs. Define each against the tokens, with variants and states, before composing any screen. See `references/component-checklist.md`.
3. **Screens and hierarchy.** Compose screens from the defined components. Enforce one primary action; the eye finds it first. Everything else reads as secondary.
4. **Interactions and states.** Define loading, empty, error, and transitions. Motion 200 to 240ms. The happy path alone is half a design.
5. **Accessibility pass.** Contrast, touch targets, semantics. Run as a pre-generation checklist (`references/a11y-checklist.md`) so the model produces it by default.
6. **Generate with `/design`.** Now, and only now. Describe the screen in one line; the model generates against the foundation, syncs a live design, hands off code into the repo.
7. **Verify.** Read the output back against the `CLAUDE.md` design rules using `references/verify-rules.md`. Invented hex, second primary action, off-scale spacing → fix and re-run. This is the anti-hallucination check, pointed at UI.

## Files in this skill

- `references/foundation-templates.md` — paste-ready `tokens.ts` + `CLAUDE.md` design block.
- `references/component-checklist.md` — the component primitives + states to define before screens.
- `references/a11y-checklist.md` — the pre-generation accessibility gate.
- `references/verify-rules.md` — the step-7 checklist the agent runs against output.

Heavy detail lives in `references/`, loaded only when the relevant step runs, so the skill stays under 500 lines and does not burn context until a step needs it.

## Notes

- Platform-agnostic: the order is identical for web (Next.js) and mobile (React Native / Expo). Only the token values and component primitives change.
- Worked examples: getwireai.com (web, via AI Web Launcher) and Morrow Self onboarding (mobile, via AI Mobile Launcher).
- Companion playbook (PDF): "From Idea to Ready Design with Claude" on Code Meet AI.
