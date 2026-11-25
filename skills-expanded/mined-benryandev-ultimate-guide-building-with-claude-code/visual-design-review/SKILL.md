---
name: visual-design-review
description: Iterative visual design review process using Playwright Plus MCP for parallel browser screenshots and AI analysis. Use when reviewing UI/UX quality, running design loops, or validating responsive design.
context: fork
disable-model-invocation: true
---

# Visual Design Review Loop

Run an iterative design review on the specified pages using the Playwright Plus MCP (https://github.com/vibe-coding-labs/playwright-plus-mcp) for browser automation.

## Step 1: Capture Screenshots
For each page specified in $ARGUMENTS (or all main routes if none specified):

1. Navigate to the page using Playwright Plus MCP (`browser_navigate`)
2. Capture screenshots at 4 breakpoints using `browser_resize` + `browser_take_screenshot`: 375x812, 768x1024, 1280x800, 1920x1080
3. If the project has dark mode, capture both light and dark variants
4. For pages with ScrollTrigger animations, use `browser_evaluate` to inject force-visible CSS before capture
5. Playwright Plus MCP supports parallel work -- capture multiple breakpoints concurrently where possible

## Step 2: Analyse
Run both analysis skills on each screenshot set:
- `/frontend-design` -- Layout, spacing, typography, visual hierarchy
- `/ui-ux-pro-max` -- Usability, accessibility, interaction patterns

Score each page on 4 dimensions (1-10):
- Design quality
- Usability
- Creativity
- Content

## Step 3: Report
Generate a structured report listing:
- Page name and breakpoint
- Scores for each dimension
- Specific issues found (with severity: critical/major/minor)
- Recommended fixes (in priority order)

## Step 4: Iterate
After fixes are applied, repeat Steps 1-3. Target: 3-5 cycles maximum.
Stop when all scores are >=9/10 or when improvement per cycle drops below 0.2.
