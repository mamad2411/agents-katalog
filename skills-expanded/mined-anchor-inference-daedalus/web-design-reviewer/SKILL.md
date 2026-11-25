---
name: web-design-reviewer
description: Visual inspection of a live site with headless Chromium to find and fix layout, responsive, consistency and CSS/accessibility issues at source level. Not for automated E2E testing.
requires: playwright, ImageView
---
# Web Design Reviewer

Use this skill for visual QA and source-level fixes after a page is already running. This is not the right skill for functional automation or regression suites.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Reviewing a live page for layout or spacing defects
- Checking responsive behavior at a few critical widths
- Comparing a page to a design system or visual target
- Tracing a visible issue back to CSS, Tailwind classes, or component structure

## Recommended Workflow

1. Open the page with Python Playwright: it and its Chromium are installed for the shell's `python3`, so
   run the script as `python3 review.py` — never `uv add`, `uv run` or `playwright install` it. See
   `Skill(skill="webapp-testing")` for the server helper.
2. Capture the current state before editing.
3. Test desktop and mobile widths.
4. Fix the source code, then re-check the same viewports.

## Capturing evidence with Playwright

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, name in ((1440, "desktop"), (360, "mobile")):
        page = browser.new_page(viewport={"width": width, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("requestfailed", lambda r: errors.append(f"{r.url}: {r.failure}"))
        page.goto("http://localhost:5173", wait_until="networkidle")
        page.screenshot(path=f"review-{name}.png", full_page=True)
        print(name, page.locator("body").inner_text()[:200], errors)
    browser.close()
```

- Look at every screenshot with `ImageView` before judging; a screenshot that was not viewed is not evidence.
- `page.accessibility.snapshot()` gives the accessible structure; `page.evaluate` reads computed styles for contrast and overflow checks.
- Capture console and network failures with the hooks above before proposing visual fixes.

## Anti-Patterns

- Starting from a generic template without adapting it: The output may look polished but still miss the real audience or medium.
- Ignoring final render or export review: Layout bugs often appear only after the asset is opened in its destination tool.
- Fixing content and presentation in one pass: It becomes hard to tell whether a problem is structural or visual.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Web Design Reviewer guidance is tied to a concrete route, component, screen, or design artifact.
2. Pass/fail: Component states cover loading, empty, error, success, and responsive breakpoints where applicable.
3. Pass/fail: Accessibility, visual hierarchy, and interaction behavior are reviewed against the shared component rubric.
4. Pressure-test scenario: Review the component on a narrow mobile viewport, keyboard-only path, and slow-loading state.
5. Success metric: Zero generic UI approval; every approval cites rendered behavior or source evidence.

## Review Checklist

- [ ] No overflow or clipped content at target widths
- [ ] Interactive controls remain visible and reachable
- [ ] Text contrast and focus states are acceptable
- [ ] Repeated components use consistent spacing, typography, and color
- [ ] Fixes were verified visually after the code change

## References & Resources

### Documentation
- [Visual Checklist](./references/visual-checklist.md) - High-signal items for layout, contrast, spacing, and responsive review
- [Framework Fixes](./references/framework-fixes.md) - Typical fix locations for CSS, Tailwind, CSS modules, and component styles

### Scripts
- [CSS Risk Audit](./scripts/css-risk-audit.py) - Scan CSS and front-end source for risky fixed widths, viewport traps, and overflow patterns

## Related Skills

- [frontend-design](../frontend-design/SKILL.md): Use it when the workflow also needs UI composition and front-end design direction.
- [stitch-design](../stitch-design/SKILL.md): Use it when the workflow also needs turning interface designs into implementation-ready assets.
- [canvas-design](../canvas-design/SKILL.md): Use it when the workflow also needs visual composition and presentation-ready diagram work.
