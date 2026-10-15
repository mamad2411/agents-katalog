---
name: ui-imagegen-director
description: Direct high-quality frontend UI work by using Codex Image Gen for visual mockups, then implementing the selected direction in code with browser-based visual QA. Use when the user asks for a better-looking web UI, UI mockup, app screen, dashboard, landing page, visual redesign, or wants Image Gen/GPT Image 2 to guide frontend implementation. Avoid for backend-only work or tiny style tweaks that do not need visual direction.
---

# UI ImageGen Director

Use this workflow when visual direction is the weak link: the user wants a polished frontend, Codex is producing generic UI, or a generated mockup would give the implementation a stronger target.

This skill composes three activities:

1. Create or refine a UI direction with Image Gen.
2. Translate the selected direction into real frontend code.
3. Verify the rendered result in a browser and iterate visually.

## Workflow

1. Inspect the product context before designing:
   - audience and job-to-be-done
   - screen type: dashboard, settings, editor, commerce, landing page, game, etc.
   - existing framework, design system, component library, and constraints
   - whether the page is an operational tool, expressive site, or immersive/game UI

2. Pick one clear visual direction before calling Image Gen.
   - Prefer a concrete direction such as refined B2B operations, editorial analytics, luxury fintech, industrial console, playful maker tool, scientific workspace, or focused commerce catalog.
   - Treat boldness as intentionality, not visual noise. Dense operational tools can be excellent without becoming decorative.
   - Decide the memorable design move: typography, information density, layout rhythm, product imagery, surface treatment, motion, or interaction model.

3. Write an Image Gen prompt that is implementation-oriented.
   - Ask for a UI screenshot or screen mockup, not a marketing poster, unless the user explicitly wants marketing.
   - Include layout regions, expected content density, states, and constraints.
   - Prohibit generic AI UI patterns: default SaaS cards everywhere, purple-blue gradient dominance, meaningless decorative blobs, fake glass panels, ungrounded icons, oversized hero sections for tools, and placeholder text that hides hierarchy.
   - Ask for visual clarity that can be translated into components: spacing, type hierarchy, navigation, controls, table/list structure, empty/error/loading states, and responsive intent.

4. Use Image Gen when a new visual target or raster asset is needed.
   - Invoke the built-in image generation path, or explicitly use `$imagegen` when asking another agent or writing a reusable prompt.
   - For project-bound assets, keep generated images in the project and wire references to project-local files.
   - Do not use a generated screenshot as the final UI. It is a reference unless the user asked for a bitmap asset.

5. Critique the generated direction before coding.
   - Check whether it fits the product, audience, and workflow.
   - Check implementation feasibility: component structure, responsive behavior, text density, asset needs, animation cost, and accessibility.
   - If it misses the intent, do one targeted Image Gen revision instead of drifting through many unrelated variants.

6. Implement the chosen direction in code.
   - Reuse existing components, tokens, routing, state, and data patterns.
   - Encode the visual direction with real layout, typography, CSS variables/design tokens, states, and responsive constraints.
   - Use generated bitmap assets only where they are the intended asset: hero imagery, backgrounds, illustrations, product imagery, textures, or sprites.
   - Keep operational tools efficient and scannable. Avoid landing-page composition for dashboards, CRMs, editors, and admin tools.

7. Verify visually in a browser after frontend changes.
   - Start or reuse the dev server.
   - Open the relevant route with the Browser plugin or Playwright when available.
   - Check desktop and mobile widths when layout is responsive.
   - Look for text overflow, overlapping UI, unstable dimensions, broken assets, inaccessible contrast, blank canvases, and mismatch with the selected direction.
   - Iterate in code until the rendered UI is coherent, not merely until tests pass.

8. Prepare the final report.

## Final Report

Include:

- chosen visual direction
- generated asset or mockup paths, if any
- implementation files changed
- browser/device checks performed
- remaining visual risks or follow-up work

## Prompt Template

Use this shape when asking Image Gen for the visual target:

```text
$imagegen
Create an implementation-oriented UI mockup for <product/screen>.

Audience and job: <who uses it and what they need to accomplish>
Screen type: <dashboard/settings/editor/landing page/etc.>
Visual direction: <one concrete aesthetic direction>
Memorable design move: <typography/layout/density/media/motion/etc.>
Required regions: <navigation/header/main content/actions/states>
Content density: <sparse/balanced/dense> with realistic labels and data hierarchy
Implementation constraints: design must translate into web components and responsive CSS
Avoid: generic SaaS card walls, purple-blue gradient dominance, decorative blobs, fake glass, unreadable tiny text, marketing hero layout unless requested
Output: high-quality UI screenshot-style mockup, clear hierarchy, realistic spacing, no watermark
```

Then implement from the selected mockup:

```text
Use the selected UI mockup as visual reference. Do not paste it as the UI.
Recreate the direction with real components, CSS, responsive layout, accessible states, and project-local assets where needed.
After implementation, use the browser to compare the rendered route against the direction and fix visible issues.
```

## When to Skip Image Gen

Skip generation and implement directly when:

- the user requests a small deterministic CSS fix
- the project already has a strict design system and the task is just applying it
- the UI is primarily data correctness, form behavior, or accessibility remediation
- the requested asset is an existing SVG/vector/icon-system edit that should stay code-native
