---
name: appmillers-claude-code-design-kit
description: 5-technique Claude Code design upgrade kit from @appmillers — feed premium references, audit against Vercel's guidelines, create a DESIGN.md, generate components from screenshots, and give Claude visual feedback via Playwright. Use any technique independently or run all five for a polished production UI.
---

# 5 Claude Code Design Upgrades

Source: @appmillers
5 techniques · elevate Claude Code from functional to polished

---

## Technique 01 — TASTE SKILL

Feed Claude premium visual references before generating any UI.

**Why:** Claude's first draft defaults to generic patterns. Premium references calibrate its taste for layout, typography, and colour.

**How:**
```
I'm building [describe your app/component].

Here are 3–5 premium design references I want you to draw inspiration from:
- [URL or screenshot 1]
- [URL or screenshot 2]
- [URL or screenshot 3]

Before generating any code, analyse:
1. The layout principles these share
2. The typographic choices (scale, weight, spacing)
3. The colour usage (palette, contrast, accent strategy)
4. The interaction patterns and micro-details

Then generate the component with those aesthetic principles applied.
```

---

## Technique 02 — WEB DESIGN GUIDELINES AUDIT

Audit your UI against Vercel's Web Interface Guidelines.

**Why:** Catches usability, accessibility, and consistency issues that taste alone misses.

**How:**
```
Audit this UI/component against Vercel's Web Interface Guidelines
(https://vercel.com/design/introduction).

Check specifically:
1. Usability — is every action obvious and reachable?
2. Accessibility — contrast ratios, focus states, ARIA labels
3. Consistency — does it match the established system's patterns?
4. Responsiveness — does it degrade gracefully at all breakpoints?

Return a numbered list of issues found, with suggested fixes for each.
Then apply all fixes.
```

---

## Technique 03 — AWESOME DESIGN.md

Create a `DESIGN.md` file so Claude always writes in-system.

**Why:** Without a design spec, Claude reinvents the system on every generation. DESIGN.md anchors every session.

**How:**
```
Create a DESIGN.md file for this project that captures our design system.

Document:
1. **Colours** — primary, secondary, accent, background, surface, text, error, success (hex values)
2. **Typography** — font family, scale (xs/sm/base/lg/xl/2xl/3xl), weights, line-height rules
3. **Spacing** — base unit, scale (4px/8px/12px/16px/24px/32px/48px/64px)
4. **Border radius** — default, sm, lg, full
5. **Shadows** — elevation levels (sm, md, lg)
6. **Buttons** — primary, secondary, ghost, destructive states (default/hover/active/disabled)
7. **Components** — cards, inputs, modals, toasts: consistent padding, border, background rules
8. **Motion** — default duration, easing curves

After creating DESIGN.md, confirm: "DESIGN.md created — I'll reference this in all future UI work."
```

**Usage after creation:**
```
Refer to DESIGN.md and build [component] using our established system.
```

---

## Technique 04 — IMAGE TO CODE

Drop a screenshot and Claude generates matching components.

**Why:** Visual communication is faster and more precise than text descriptions for UI.

**How:**
```
[Attach screenshot of UI you want replicated]

Analyse this design and generate the component that matches it with high fidelity.

Pay attention to:
1. Exact layout structure (flexbox/grid, spacing, alignment)
2. Typography hierarchy (sizes, weights, colours)
3. Interactive states visible in the design
4. Colour palette extracted from the image
5. Component composition (what sub-components make this up)

Output: production-ready code using [React/Vue/plain HTML — specify]. 
Include any CSS/Tailwind classes needed to match the screenshot precisely.
```

---

## Technique 05 — PLAYWRIGHT CLI FEEDBACK LOOP

Give Claude eyes — build → screenshot → inspect → fix.

**Why:** Claude can't see what it builds. Playwright closes the loop: Claude generates, screenshots, inspects the result, and self-corrects.

**Setup (run once):**
```bash
npx playwright install chromium
```

**Prompt:**
```
Use the Playwright CLI to give yourself visual feedback on this UI.

Run this loop:
1. BUILD — generate/update the component
2. SCREENSHOT — take a screenshot of the rendered result at localhost:[port]
   Command: npx playwright screenshot --browser chromium http://localhost:[port] screenshot.png
3. INSPECT — analyse the screenshot: does it match the design intent?
4. FIX — identify the top 3 visual issues and fix them
5. REPEAT — loop until the visual output matches the spec

Stop when the design is production-quality. Show me the final screenshot.
```

---

## Full Kit Prompt (Run All 5 Techniques)

```
I want to upgrade this UI using all 5 Claude Code design techniques:

1. TASTE: Here are my premium reference designs — [attach/link references]. 
   Analyse their design principles before touching any code.

2. GUIDELINES: After generating, audit against Vercel's Web Interface Guidelines.

3. DESIGN.md: Create or update DESIGN.md with the system we're using.

4. IMAGE TO CODE: [Attach screenshot] — replicate this with high fidelity.

5. PLAYWRIGHT LOOP: Screenshot the result, inspect it, fix the top issues.
   Repeat until production-quality.

Start with technique 1 and work through each in order.
```
