---
name: tailwind-frontend-specialist
description: Use this skill when the task is about building or refining frontend UI with Tailwind CSS, including layout, responsive behavior, utility classes, component structure, accessibility, visual polish, and consistency with an existing design system.
---

# Tailwind Frontend Specialist

## Overview

This skill is for creating and refining frontend interfaces with Tailwind CSS while preserving clean markup, responsive behavior, and consistent visual language.

## When To Use

Use this skill when the user asks for work involving:

- Tailwind utility classes and component styling
- Responsive layouts, spacing systems, and typography
- Django templates, HTML fragments, or frontend components styled with Tailwind
- Accessibility, interaction states, and visual hierarchy
- Refactoring messy utility usage into clearer component patterns

## Working Style

- Inspect the existing UI patterns before introducing new ones.
- Prefer semantic HTML with Tailwind classes instead of div-heavy markup.
- Keep utility usage intentional; avoid class noise when extraction or reuse is warranted.
- Preserve a coherent spacing, color, and typography system.
- Ensure mobile and desktop behavior are both considered.

## Implementation Rules

- Start from structure and information hierarchy before polishing visuals.
- Use layout primitives consistently: flex, grid, container widths, gaps, and padding.
- Handle hover, focus, active, disabled, and dark-mode states only if the project already supports them or the task requires them.
- Favor reusable template partials or components when the same pattern repeats.
- Do not add inline styles unless the codebase already relies on them.

## Review Checklist

- Is the interface readable and visually consistent?
- Does it respond well across common breakpoints?
- Are focus states and keyboard navigation preserved?
- Are utility classes understandable rather than accidental?
- Does the change match the project's existing frontend direction?

