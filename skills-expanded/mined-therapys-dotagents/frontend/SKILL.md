---
name: frontend
description: "Build and polish production-ready frontend interfaces using Emil Kowalski's design-engineering approach. Use when creating or restyling web pages, components, or apps; reviewing UI polish; adding or fixing animations and transitions; choosing UI primitives; improving mobile touch behavior; or stress-testing layouts with real-world data. Covers HTML/CSS/JS, React, Vue, and other web frameworks."
---

# Frontend Design Engineering

Build interfaces that feel right: purposeful motion, responsive controls, good defaults, and invisible correctness. This replaces the previous aesthetic-first frontend guidance with Emil Kowalski's approach. The code is the deliverable, not a mood board.

## Load the right guidance

Paths are relative to this skill's directory, not the project's working directory.

1. **Always read [Design Engineering](references/emil-design-eng/SKILL.md)** before building, polishing, or reviewing UI. It defines the philosophy, motion decisions, component details, and Before/After/Why review table.
2. Load additional guides when relevant:

| Task | Read |
| --- | --- |
| Build an animation, transition, or gesture | [Animate](references/animate/SKILL.md); its [RECIPES.md](references/animate/RECIPES.md) for matching components |
| Choose accessible primitives or a frontend dependency | [Pick UI Library](references/pick-ui-library/SKILL.md) |
| Mobile layouts, touch, safe areas, viewport, keyboard, PWA | [Mobile Native](references/mobile-native/SKILL.md) |
| Stress-test realistic edge cases | [Break UI](references/break-ui/SKILL.md) and its [CATALOG.md](references/break-ui/CATALOG.md) |
| Animation performance triage | [Performance Cheatsheet](references/performance-cheatsheet.md) |

These are bundled reference guides, not independently installed slash commands. References to `emil-design-eng`, `animate`, `mobile-native`, `pick-ui-library`, or `break-ui` mean the local guides above. Other upstream skills mentioned in those guides are not bundled: do not claim to invoke them. For a motion review or audit, use the Design Engineering checklist and Animate's rules; for other missing workflows, say what's unavailable if it matters.

The upstream "Initial Response" blocks and invocation metadata are for standalone skills. Here, follow the user's concrete request immediately; do not insert a canned introduction or wait for another question. The library guide may be read as a reference without a separate explicit invocation.

## Workflow

1. Inspect the existing UI, framework, dependencies, tokens, and project conventions. Identify audience, task, content, states, and constraints. Ask one focused question at a time only where a missing decision materially changes the implementation.
2. Preserve established visual identity and use existing tokens. Do not replace fonts, palettes, layout, or dependencies merely to look different. If a project has additional local design-system guidance, read it and treat its brand-specific layout, typography, surface, and motion rules as authoritative.
3. Choose accessible primitives before hand-rolling dialogs, menus, toasts, or focus management. Reuse installed equivalents; do not churn libraries without a request. Apply React-specific recommendations only in React projects.
4. Gate every animation by frequency and purpose before choosing tool, properties, easing, duration, interruption, and exit. No motion is a valid result. Use the cheapest tool that fits; ship reduced-motion behavior and touch-safe hover gating with it.
5. Implement working, semantic, responsive code. Cover loading, empty, error, disabled, and populated states as applicable. Preserve labels, contrast, visible keyboard focus, focus restoration, and keyboard operation.
6. Verify with available checks and browser tooling. Check narrow and wide layouts, supported themes, realistic content, rapid interruption, keyboard input, and reduced motion. Mobile emulation is not hardware verification. Say plainly which checks you could not run.

## Application guardrails

- Use pointer-down for immediate visual feedback, not for committing actions. Keep semantic button/link activation so keyboard users work and pointer users can cancel a press.
- Reduced motion must actually disable existing movement and transform transitions, not merely add a fade beside them. Preserve essential state changes and feedback.
- Prefer transform/opacity for motion, but do not assume every CSS/WAAPI animation or clip-path is compositor-accelerated. Verify in the target browser; treat blur and layout animation as measured exceptions, not defaults.
- Stress-test with plausible or schema-backed values. A dev-only fixture toggle must never ship to production. In a requested audit, report design tradeoffs before fixing; in a requested implementation, address unambiguous bugs within scope.

## Output

Ship code in the project's files and summarize changes, checks, and any unverified behavior briefly. For UI reviews, use an actual **Before / After / Why** markdown table. For a dedicated worst-case audit, use Break UI's findings format. Do not claim visual or device verification you did not perform.

Source and adaptation notes: [UPSTREAM.md](UPSTREAM.md).
