---
name: implement-from-design
description: Translates a design (Figma/screenshot/mockup) into pixel-faithful, responsive, token-driven frontend code, then visually diffs the result; used when building UI from a visual spec.
when_to_use: When the user provides a Figma link, screenshot, or mockup and wants it built as a faithful, responsive component/page — and wants the output visually verified against the design.
---

## When to Use

Invoke when the deliverable is **code that reproduces a given visual spec** and you have a concrete source to match against:

- A Figma link/frame, a screenshot, or a static mockup image of a component or page.
- The user says "build this", "implement this design", "make it match", "pixel-perfect", or attaches an image.
- Faithfulness matters — the output will be compared back to the source.

Do NOT use when:
- There is **no source design** and you're inventing one → use `frontend-design` instead (this skill reproduces; it does not originate).
- The work is logic/data only with no visual surface, or a pure refactor with no rendered change.

This skill orchestrates. It hands structure off to `build-react-component` and styling off to `style-responsive-tailwind`, then owns the **extract → map → build → visual-diff** loop around them.

## Steps

1. **Extract the design intent into explicit values — never eyeball into code.** Read the source and write down, as a short table, the actual numbers before touching the editor:
   - **Spacing scale** — list every gap/padding/margin you see; cluster them (e.g. 4/8/12/16/24/32) so you reuse a scale instead of 13 one-off pixel values.
   - **Type ramp** — for each text role: font-family, size, weight, line-height, letter-spacing.
   - **Color tokens** — every fill/border/text color as hex; note semantic role (bg, surface, border, text-primary, text-muted, accent).
   - **Radii / shadows / borders** — corner radii, each box-shadow (x/y/blur/spread/color), border widths.
   - **Breakpoints & layout** — what reflows, stacks, hides, or resizes between mobile/tablet/desktop. If only one viewport is given, infer the responsive intent and state your assumption.
   - For Figma: pull exact values from the inspect/dev panel (or Figma MCP `get_design_context` + `get_screenshot`), don't trace from a screenshot. For a raw screenshot: sample colors with a picker, measure spacing against known reference elements — do not guess hex from memory.

2. **Map every extracted value to existing tokens — reuse, never invent.** Open the project's `tailwind.config`/theme, CSS custom properties, and design-system components FIRST. For each extracted value, bind it to the nearest existing token (`bg-surface`, `text-muted`, `rounded-lg`, `shadow-card`, `space-y-4`). Only add a new token when nothing within ~1–2px/one weight step exists, and add it to the theme config — never hardcode an arbitrary `#3B7AF2` or `gap-[13px]` inline. If the project has a component for it (button, input, card, badge), extend that component rather than rebuilding the markup.

3. **Build the structure** by handing off to `build-react-component`: semantic HTML, correct element nesting matching the design's visual hierarchy, props for the variable parts (text, state, slots), accessible roles/labels. Keep markup minimal — one wrapper per visual group the design actually shows, no decorative `<div>` soup.

4. **Apply styling** by handing off to `style-responsive-tailwind`, feeding it the token map from step 2. Translate the design's auto-layout/flex/grid into Tailwind layout utilities. Match spacing, type, color, radius, shadow to the mapped tokens — not to raw extracted pixels.

5. **Implement the responsive states the design implies.** Build mobile-first, then layer `md:`/`lg:` for the breakpoints from step 1. Reproduce every reflow the design shows (stack→row, sidebar collapse, grid column count, font-size step). If a viewport wasn't designed, make a sensible scale and leave a `// responsive: tablet inferred` comment — don't silently ship an untested breakpoint as if it were specified.

6. **Add micro-interactions/animation only where the design specifies them.** Hover/active/focus/disabled states, transitions, and motion go in **only if the source shows them** (a hover variant, a motion note, an obvious affordance). Match the designed easing/duration. Do not sprinkle gradient glows, scale-on-hover, fade-ins, or "delight" the design didn't ask for — that's the #1 source of AI-slop drift away from the spec.

7. **Visual-diff loop — render, screenshot, compare, iterate until faithful.** This is the verification gate, not optional polish:
   - Run the app/Storybook (`npm run dev` / `npm run storybook`) and get the component's URL.
   - `mcp__chrome-devtools__navigate_page` to it. For each designed breakpoint set the viewport with `mcp__chrome-devtools__emulate` (e.g. `viewport: "390x844x3,mobile"` for phone, `"1440x900x1"` for desktop) or `resize_page`.
   - `mcp__chrome-devtools__take_screenshot` (set `format: "png"`, `fullPage: true` for pages) at each breakpoint, saving to a `filePath`.
   - Open the screenshot next to the source mock and compare **spacing, alignment, type, color, radius, shadow** point by point. Note every mismatch as a concrete delta ("card padding 24px in design, 16px rendered"; "heading 600 in design, 700 rendered").
   - Fix the specific deltas, re-screenshot, repeat. Stop when nothing material differs — not after the first render.

## Common Errors

- **Coding straight from a screenshot without extracting values.** You end up with vibes-based spacing and invented hex colors. Always do step 1's value table first; for Figma always read inspect/dev-mode numbers.
- **Inventing tokens that already exist.** Hardcoding `gap-[13px]`, `text-[#1F2937]`, `rounded-[10px]` when `gap-3`, `text-gray-800`, `rounded-lg` are right there. Map to the theme first; arbitrary `[...]` values are a smell.
- **Treating Figma's exported React/Tailwind as final code.** The export is a *representation of the design*, not house style — it's verbose, absolute-positioned, and ignores your component library. Re-author it into project conventions.
- **AI-slop additions.** Adding gradients, glow shadows, hover-scale, fade-in animations, rounded-everything, or emoji the design never contained. If it's not in the source, it doesn't ship. Reproduce, don't embellish.
- **Absolute positioning to "match pixels."** Copying Figma's x/y into `absolute` coordinates produces a layout that shatters at any other width. Use flow layout (flex/grid) that reproduces the *relationship*, not the coordinates.
- **Declaring done after one render.** First render is never faithful. Skipping the iterate part of the visual-diff loop is how 90%-right ships as "matched."
- **Only checking one viewport.** The desktop looks perfect, mobile overflows. Screenshot every designed breakpoint, not just the one you developed in.
- **Stale dev server / cache.** Editing styles but screenshotting an old build → phantom mismatches. Confirm HMR applied (or `navigate_page` with `ignoreCache`) before trusting a diff.
- **Drift from forgotten interactive states.** Design shows a hover/disabled variant; you build only the default. Re-screenshot with the state triggered (or via the component's prop) to verify those too.

## Verify

- [ ] Step-1 value table exists (spacing, type ramp, colors, radii/shadows, breakpoints) and every code value traces back to it.
- [ ] No arbitrary `[...]` Tailwind values or inline hex/px that should be a token; new tokens (if any) were added to the theme config, not hardcoded.
- [ ] Existing design-system components were reused/extended where one fit, instead of re-implemented.
- [ ] Layout uses flow (flex/grid), not absolute coordinates copied from the design tool.
- [ ] Every breakpoint the design implies is implemented and was screenshotted; reflows match.
- [ ] Only the interactions/animations present in the source were added — nothing extra.
- [ ] Visual-diff ran via chrome-devtools at each breakpoint; the final screenshots were compared point-by-point to the source and remaining deltas are zero or explicitly justified in a code comment.
- [ ] Saved before/after screenshots (or their paths) are available as evidence — not just a "looks good" claim.
