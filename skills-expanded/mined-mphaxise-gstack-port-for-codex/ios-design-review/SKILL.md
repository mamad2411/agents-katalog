---
name: ios-design-review
description: Run a visual design audit for an iOS app using available simulator or device evidence.
---

# iOS Design Review

Use this skill when the user asks for an iOS visual design audit, Human Interface Guidelines pass, or screen-by-screen design critique.

## Workflow

1. Discover the app target, scheme, and available runtime.
2. Capture screenshots from real device or simulator evidence.
3. Evaluate:
   - navigation clarity
   - layout and spacing
   - typography
   - accessibility and Dynamic Type resilience
   - contrast
   - platform idioms
   - consistency with `DESIGN.md` or local design docs
4. Produce findings ordered by severity.
5. If the user asked for fixes, make scoped UI changes and verify with fresh screenshots.

## Guardrails

- Do not claim real-device coverage when only simulator evidence was used.
- Do not make visual changes without checking existing app design patterns.
- Keep screenshots and findings tied to exact screens.
