---
name: design-system-hotels-by-hilton
description: Creates implementation-ready design-system guidance with tokens, component behavior, and accessibility standards. Use when creating or updating UI rules, component specifications, or design-system documentation.
---

<!-- TYPEUI_SH_MANAGED_START -->

# Hotels by Hilton

## Mission
Deliver implementation-ready design-system guidance for Hotels by Hilton that can be applied consistently across marketing site interfaces.

## Brand
- Product/brand: Hotels by Hilton
- URL: https://www.hilton.com/en/
- Audience: buyers, teams, and decision-makers
- Product surface: marketing site

## Style Foundations
- Visual style: structured, accessible, implementation-first
- Main font style: `font.family.primary=Hilton Sans`, `font.family.stack=Hilton Sans, system-ui, -apple-system, BlinkMacSystemFont, Inter, Arial, Helvetica Neue, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji`, `font.size.base=16px`, `font.weight.base=400`, `font.lineHeight.base=22px`
- Typography scale: `font.size.xs=14px`, `font.size.sm=16px`, `font.size.md=18px`, `font.size.lg=20px`, `font.size.xl=30px`, `font.size.2xl=36px`, `font.size.3xl=48px`, `font.size.4xl=60px`
- Color palette: `color.text.primary=#0a0a0a`, `color.text.secondary=#ffffff`, `color.text.tertiary=#f0e9e6`, `color.border.muted=#002f61`, `color.surface.base=#000000`, `color.surface.strong=#e5e5e5`, `color.border.default=#e5e7eb`, `color.border.strong=rgba(0, 0, 0, 0) rgb(229, 231, 235)`
- Spacing scale: `space.1=1.3px`, `space.2=4px`, `space.3=8px`, `space.4=12px`, `space.5=16px`, `space.6=20px`, `space.7=24px`, `space.8=26.39px`
- Radius/shadow/motion tokens: `radius.xs=24px`, `radius.sm=32px`, `radius.md=1000000px` | `shadow.1=rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.5) 0px 2px 4px 0px inset` | `motion.duration.instant=150ms`, `motion.duration.fast=500ms`

## Accessibility
- Target: WCAG 2.2 AA
- Keyboard-first interactions required.
- Focus-visible rules required.
- Contrast constraints required.

## Writing Tone
concise, confident, implementation-focused

## Rules: Do
- Use semantic tokens, not raw hex values in component guidance.
- Every component must define required states: default, hover, focus-visible, active, disabled, loading, error.
- Responsive behavior and edge-case handling should be specified for every component family.
- Accessibility acceptance criteria must be testable in implementation.

## Rules: Don't
- Do not allow low-contrast text or hidden focus indicators.
- Do not introduce one-off spacing or typography exceptions.
- Do not use ambiguous labels or non-descriptive actions.

## Guideline Authoring Workflow
1. Restate design intent in one sentence.
2. Define foundations and tokens.
3. Define component anatomy, variants, and interactions.
4. Add accessibility acceptance criteria.
5. Add anti-patterns and migration notes.
6. End with QA checklist.

## Required Output Structure
- Context and goals
- Design tokens and foundations
- Component-level rules (anatomy, variants, states, responsive behavior)
- Accessibility requirements and testable acceptance criteria
- Content and tone standards with examples
- Anti-patterns and prohibited implementations
- QA checklist

## Component Rule Expectations
- Include keyboard, pointer, and touch behavior.
- Include spacing and typography token requirements.
- Include long-content, overflow, and empty-state handling.

## Quality Gates
- Every non-negotiable rule must use "must".
- Every recommendation should use "should".
- Every accessibility rule must be testable in implementation.
- Prefer system consistency over local visual exceptions.

<!-- TYPEUI_SH_MANAGED_END -->
