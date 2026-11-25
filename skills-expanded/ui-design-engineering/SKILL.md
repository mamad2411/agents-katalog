---
name: ui-design-engineering
description: Design, implement, harden, and review production-grade user interfaces for web apps, dashboards, SaaS products, admin tools, forms, and responsive frontend components. Use when building or improving UI/UX, translating Figma or requirements into code, styling React/Vue/Svelte/HTML views, reviewing frontend quality, fixing accessibility or motion, refining interaction states, improving performance, or validating responsive layout and visual polish. Integrates with Skill-Agents frontend workflows and browser, Playwright, Figma, package, test, and validation MCP tools.
---

# UI Design Engineering

Build interfaces that emerge from the product, user, and workflow rather than from a generic template.

## Choose The Mode

- **Build mode:** inspect the product context, implement the interface, and validate it in a browser.
- **Review mode:** report concrete violations first, explain impact briefly, and propose the smallest useful fix.

For a detailed review checklist, read [references/ui-audit.md](references/ui-audit.md).

For attribution and the external ideas that informed this skill, read [references/credits.md](references/credits.md).

## Skill-Agents Integration

When this skill is loaded through `mcp-tools`:

1. Use `route_request` to select the workflow and related skills.
2. Prefer the `frontend-ui` toolset for implementation and browser QA.
3. Prefer the `design-frontend` toolset when Figma or design mapping is involved.
4. Use `build_agent_context` to load only the selected workflow and skills.
5. Use MCP tools in this order when available:
   - `project`, `repo-index`, `package`, and `docs` for discovery.
   - `figma` and `browser-page-map` for design and page context.
   - `code-editing` for implementation.
   - `browser`, `playwright`, and `playwright-actions` for visual and interaction QA.
   - `test-inspection`, `ci`, and `validation` for verification.
6. Follow MCP safety policy and the project's allowed roots. Do not request broader tools than the task needs.

With Local LLM Orchestrator, use `main-llm-tools` while developing or auditing UI so the model receives this skill and the required MCP tools. A direct model such as `main-llm` or `coding` does not load skills automatically.

## Workflow

1. Inspect before designing
   - Read the existing frontend structure, design tokens, component library, routes, and nearby screens.
   - Reuse established primitives and patterns unless they are the source of the problem.
   - Identify the actual user, their immediate goal, the environment, and the frequency of the workflow.

2. State the design intent
   - Name the product domain, desired density, visual tone, and interaction character.
   - Identify one signature element that belongs specifically to this product.
   - Name the obvious generic defaults to avoid.
   - For operational tools, prioritize scanning, comparison, repeated action, and predictable navigation.

3. Design the information architecture
   - Lead with the user's primary task, not decorative content.
   - Establish navigation, hierarchy, grouping, and action priority before visual styling.
   - Keep page sections unframed; use cards only for repeated items, modals, or genuinely bounded tools.
   - Do not place cards inside cards.

4. Implement complete behavior
   - Build real controls and wire their expected interactions.
   - Include loading, empty, error, disabled, selected, hover, focus, and success states when applicable.
   - Use icons for familiar tool actions and labels or tooltips for unfamiliar icons.
   - Preserve the project's framework, state-management, styling, and component conventions.

5. Enforce accessibility
   - Prefer native semantic elements and established accessible primitives.
   - Give every interactive control an accessible name.
   - Make keyboard focus visible and preserve logical tab order.
   - Manage dialog focus, Escape behavior, and focus restoration.
   - Associate form labels, help text, errors, required state, and invalid state correctly.
   - Respect reduced motion and never rely on color, hover, or toast messages alone.

6. Refine visual craft
   - Use typography, spacing, density, color, and elevation as one coherent system.
   - Match type scale to context; compact tools need compact headings.
   - Use tabular numerals for changing data and stable dimensions for controls and grids.
   - Avoid default-looking palettes, gratuitous gradients, glow effects, decorative blobs, and generic hero layouts.
   - Keep accent color deliberate and ensure the interface is not dominated by one hue family.

7. Keep motion purposeful
   - Add animation only when it clarifies change, hierarchy, causality, or spatial continuity.
   - Prefer transform and opacity; avoid animating layout and large blur surfaces.
   - Keep interaction feedback fast and stop looping animation when it is not visible.
   - Do not let motion delay primary actions.

8. Validate before handoff
   - Run the narrowest available lint, typecheck, and component tests.
   - Open the real page in a browser and inspect desktop and mobile viewports.
   - Check overflow, text wrapping, occlusion, focus order, keyboard use, state changes, and console errors.
   - For canvas, 3D, charts, and media, verify rendered pixels rather than trusting DOM presence.
   - Iterate on visible defects before reporting completion.

## Enhancement Modes

Choose the smallest mode that satisfies the request. Combine modes only when the task genuinely spans them.

- **Shape:** clarify the user, task, information architecture, and design direction before coding.
- **Build:** create a new component, screen, flow, or application experience.
- **Adapt:** make an existing interface work across breakpoints, devices, input methods, and content lengths.
- **Audit:** inspect accessibility, responsiveness, interaction, performance, architecture, and visual consistency.
- **Harden:** add robust loading, empty, error, edge-case, localization, and recovery behavior.
- **Polish:** refine typography, spacing, alignment, color, elevation, microcopy, and interaction feedback.
- **Optimize:** reduce rendering cost, asset weight, layout work, animation jank, and unnecessary client state.
- **Distill:** simplify noisy hierarchy, controls, labels, and repeated decoration without removing needed capability.

## Framework Awareness

- Detect the framework and version from the project before choosing patterns.
- Follow existing routing, rendering, data-fetching, state, styling, testing, and component conventions.
- Use framework-specific best practices already present in the repository.
- For React, inspect rendering boundaries, effect usage, keys, memoization pressure, and bundle cost.
- For Vue, preserve Composition or Options API conventions, reactivity boundaries, and router/store patterns.
- For Svelte, preserve component composition and current reactivity conventions.
- For Three.js or canvas work, verify visual output, resize behavior, asset loading, controls, and animation loops.
- Do not migrate frameworks, routers, state libraries, CSS systems, or primitive libraries unless requested.

## Hardening Requirements

- Test realistic long text, empty data, failed requests, slow requests, and partial permissions.
- Consider localization expansion, pluralization, dates, numbers, and right-to-left layout when relevant.
- Preserve user input during recoverable errors.
- Avoid layout shifts when asynchronous content arrives.
- Ensure touch targets and hover behavior also work for keyboard and touch users.
- Confirm destructive actions, prevent accidental double submission, and communicate background progress.

## Build Rules

- Use the project's existing component primitives first.
- Do not mix primitive libraries within one interaction surface.
- Do not hand-roll keyboard or focus behavior when a proven primitive exists.
- Do not block paste in text inputs.
- Use dynamic viewport units for full-height layouts and account for mobile safe areas.
- Keep z-index values on a small documented scale.
- Avoid arbitrary styling values when project tokens already express the intent.
- Do not introduce a landing page when the requested product should open directly into the working experience.
- Do not add explanatory UI copy about implementation, styling, or keyboard shortcuts unless the product requires it.

## Review Output

Report findings by severity:

```text
Findings
- [P1] Short title - file:line
  User impact and concrete fix.

Validation
- Viewports and interactions checked.
- Tests or browser checks run.

Residual Risk
- Anything not verified.
```

Priority guidance:

- `P0`: unusable core flow, severe accessibility barrier, or destructive behavior.
- `P1`: broken interaction, keyboard/focus failure, major responsive overlap, or inaccessible form/dialog.
- `P2`: incomplete state, confusing hierarchy, performance issue, or significant inconsistency.
- `P3`: localized polish issue with low user impact.

## Final Quality Checks

- Can the intended user complete the primary workflow efficiently?
- Does the interface still identify its product domain if the logo and product name are hidden?
- Is hierarchy visible when squinting or viewing at a distance?
- Would replacing the layout, type, or tokens with common defaults materially change the design?
- Are all interactive states accessible by keyboard and understandable without color alone?
- Is the mobile composition deliberate rather than merely compressed?
- Did browser verification confirm the implementation rather than only the source code?

## Source And Attribution

This skill is an original Skill-Agents synthesis. It was informed by patterns cataloged in the [UI Skills directory](https://www.ui-skills.com/skills/) and by the credited skill authors listed in [references/credits.md](references/credits.md). Do not present this skill as an official UI Skills or upstream-author skill.
