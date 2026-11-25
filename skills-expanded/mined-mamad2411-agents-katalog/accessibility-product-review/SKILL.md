---
name: accessibility-product-review
description: Review product accessibility and inclusive UX for web, mobile, desktop, SaaS, games, developer tools, checkout, onboarding, settings, forms, dashboards, notifications, motion, keyboard, screen reader, touch, color contrast, focus, error recovery, cognitive load, reduced motion, captions, localization, and assistive technology compatibility. Use when designing, building, or auditing product flows for accessible, usable, modern experiences.
---

# Accessibility Product Review

Use this skill to make accessibility a product-quality system, not a late checklist.

## Workflow

1. Identify the user flow, platforms, input modes, assistive tech assumptions, risk level, and business-critical tasks.
2. Read `references/accessibility-product-systems.md`.
3. Audit task completion across keyboard, screen reader semantics, touch, visual contrast, focus, motion, errors, content clarity, and recovery.
4. Separate blockers, high-impact usability issues, design-system fixes, and polish.
5. Produce an accessibility risk matrix, fixes, validation plan, and regression checks.

## Guardrails

- Do not trade accessibility away for visual polish, animation, or conversion pressure.
- Do not claim compliance from static review alone; require user-flow testing and assistive-tech checks where risk is material.
- Do not hide inaccessible critical actions behind alternatives that are harder, paid, or support-only.

## Output format

```text
Flow/platforms:
Critical tasks:

Findings:
- P0 <blocker> -> affected users, fix, validation
- P1 <issue> -> fix, validation

System fixes:
- design token/component/pattern change

Validation:
- keyboard, screen reader, touch, contrast, motion, error, mobile/desktop
```
