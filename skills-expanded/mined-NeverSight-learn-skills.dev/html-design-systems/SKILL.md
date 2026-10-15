---
name: html-design-systems
description: "Use when design tokens, components, variants, or states should be reviewed visually in a self-contained HTML token sheet, contact sheet, or component matrix."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [html, artifacts, visualization]
    related_skills: [html-artifact-foundation, design-md, popular-web-designs, claude-design]
---

# HTML Design Systems

## Overview

This skill creates self-contained HTML artifacts for visual review of tokens, components, variants, and states. It builds on `html-artifact-foundation`: keep the shared single-file, accessibility, responsive, print, attribution, and verification rules centralized there, and use this skill for the category-specific structure.

For diagrams and diagram-like visualizations, inherit the foundation default: Catppuccin Mocha dark theme unless the user asks otherwise.

Local examples: `examples/05-design-system.html`, `examples/06-component-variants.html`. The guidance below distills reusable patterns; copied examples preserve the upstream Apache-2.0 notice.

## When to Use

Use this skill when:
- the user needs to inspect colors, type, spacing, radii, elevation, or motion tokens
- components need a state/variant matrix for visual QA
- a design system concept should be demonstrated without creating a formal DESIGN.md
- stakeholders need to compare component treatments side by side

Do not use this skill when a plain markdown answer is enough, when the requested deliverable is a production app implementation, or when a more specialized peer skill is a better fit.

## Inputs to Gather

Use the foundation input checklist first. Additionally gather:

- existing brand tokens, CSS variables, screenshots, DESIGN.md, or UI components
- components and states that must be represented: default, hover, focus, disabled, loading, error
- contrast/accessibility requirements and supported themes
- whether the output is a rendered review sheet or a formal token/spec deliverable

Evidence gate: do not render factual claims until you have the underlying source, or label the panel as an assumption/draft.

## Relationship to Other Skills

Use `design-md` when the deliverable is a formal DESIGN.md token spec. Use `popular-web-designs` for style vocabulary inspired by known products. Use `claude-design` for broader one-off visual design work. Use this skill for browser-rendered token sheets, component contact sheets, and state/variant matrices.

## Artifact Anatomy

- Token sheet: colors with hex/usage/contrast notes, type scale, spacing ramp, radii/elevation.
- Component contact sheet: buttons, cards, forms, navigation, empty states.
- Variant/state matrix: rows are components or variants; columns are default, hover, focus, disabled, loading, error, success.
- Usage guidance: do/don't examples and when each token applies.
- Accessibility panel: contrast notes and focus-state examples.

## Implementation Workflow

1. Apply `html-artifact-foundation` for document skeleton, accessibility, responsive, print, attribution, and verification rules.
2. Gather the category-specific inputs above and write a short evidence list before composing the page.
3. Choose one primary artifact type from this skill; avoid mixing every pattern into one page.
4. Build the category-specific anatomy below with semantic sections and CSS variables.
5. Add JavaScript only for the category-specific interaction/export/navigation behavior described here.
6. Verify using the foundation checklist plus the category-specific checklist below.

## Prompt Template

```text
Create a self-contained HTML artifact for: [goal].
Audience: [reader/operator].
Source evidence to use: [files, diffs, notes, data, screenshots].
Artifact type: [choose one from this skill].
Must show: [required sections or states].
Interaction/export needs: [tabs, filters, copy JSON, keyboard deck, none].
Constraints: single local HTML file; embedded CSS/JS only; semantic HTML; accessible controls; responsive layout; no unsupported claims.
Verification: save to [path], run static checks, and if interactive open locally and check console errors.
```

## HTML/CSS/JS Patterns

Represent tokens as CSS variables in `:root`, then consume those variables in specimens. Use real HTML controls for component states when possible. For forced states, add explicit labels like `.is-hover-demo` rather than pretending hover is active. Separate token-reference artifacts from formal token specs; use `design-md` if the deliverable is `DESIGN.md`.

## Verification Checklist

- [ ] Foundation checklist passed: complete HTML document, accessibility basics, responsive behavior, and appropriate print/export behavior.
- [ ] Category trigger fits this skill and the relationship notes above rule out a better peer skill.
- [ ] Category-specific source evidence was gathered before rendering factual content.
- [ ] Artifact anatomy includes the required category sections and omits irrelevant decorative panels.
- [ ] Any category-specific JavaScript interaction/export/navigation works and has no console errors.
- [ ] Factual claims are tied to source notes or labeled assumptions.

## Common Pitfalls

- Duplicating the foundation skill instead of keeping this category focused.
- Creating an attractive but unsupported artifact with invented data.
- Adding controls that do not change anything meaningful.
- Letting dense layouts become unreadable on narrow screens.
- Making only a color palette and calling it a design system. Include type, spacing, states, and usage.
- Using fake states that cannot be distinguished from production classes.
- Omitting contrast/focus checks for interactive components.
