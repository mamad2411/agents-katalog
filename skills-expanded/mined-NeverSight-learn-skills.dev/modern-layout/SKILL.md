---
name: modern-layout
description: Design modern, clean, maintainable page layouts before implementation. Use when planning React, Next.js, TypeScript, Tailwind CSS, shadcn/ui, or Radix UI pages for B2B SaaS, admin dashboards, developer tools, productivity products, CRM/ERP, and internal tools, including navigation, grids, responsive behavior, component placement, and action areas.
---

# Modern Layout

## When to Use This Skill

Use this skill before implementation when the user needs a page layout, information structure, responsive plan, or component placement strategy. It is suitable for new pages and significant layout revisions.

Produce a layout specification, not implementation code, unless the user explicitly requests implementation.

## Inputs

Identify:

- page purpose and primary user task
- required content, data density, and action priority
- navigation model and surrounding application shell
- user roles, permissions, and workflow states
- target viewport range and mobile requirements
- existing components, tokens, and layout conventions

When inputs are incomplete, state assumptions and choose a conservative B2B SaaS pattern.

## What to Generate

- page structure and application shell placement
- section hierarchy and reading order
- layout grid, container behavior, columns, and gaps
- responsive stacking, collapsing, hiding, and overflow behavior
- component placement and ownership
- header, sidebar, content, filter, and action-area relationships
- empty, loading, error, and permission-state placement

Consider these patterns when they serve the task:

- top navigation with a persistent or collapsible sidebar
- card-based summaries with a clear content hierarchy
- filter and action bars above result sets
- split panels for browse-and-inspect workflows
- detail drawers for contextual inspection without losing list state
- sticky action areas for long forms or review workflows
- clear empty states with one relevant next action

## Decision Rules

1. Start from the primary task and information hierarchy, then choose a layout pattern.
2. Use one dominant page title and one primary action per task context.
3. Align major regions to a shared grid. Prefer a small, repeatable spacing scale over custom gaps.
4. Use cards only when their boundaries communicate grouping, comparison, interaction, or state.
5. Prefer a full page for complex creation or editing, a drawer for contextual detail, and a dialog for short focused decisions.
6. Use split panels when users repeatedly move between a collection and item details.
7. Keep filters near the data they affect and keep applied filters visible.
8. Make important actions available near the relevant content; use sticky actions only when scrolling would otherwise hide them.
9. On narrow screens, preserve task order and primary actions before secondary context.
10. Do not solve wide tables by shrinking text. Plan horizontal scrolling, column priority, row details, or alternate mobile presentation.
11. Preserve existing application-shell conventions unless there is a documented navigation problem.
12. Prefer reusable React layout primitives and existing Tailwind or design-system tokens.

## Responsive Rules

- Define behavior at content-driven breakpoints rather than naming device models.
- Specify which regions stack, collapse, scroll, become drawers, or move below the main content.
- Keep touch targets usable and avoid hover-only controls.
- Ensure sticky regions do not cover content or compete with mobile browser chrome.
- Keep primary actions reachable without duplicating conflicting controls.
- Specify table and chart overflow behavior explicitly.

## Output Format

Use these headings in this order:

### Layout Goal

State the user task, design intent, density target, and key assumptions.

### Page Structure

Describe the application shell and major regions in reading order.

### Section Breakdown

For each section, state its purpose, content, primary action, and relationship to adjacent sections.

### Responsive Behavior

Describe layout changes from wide to narrow viewports, including navigation, actions, tables, drawers, and overflow.

### Component Map

Map each region to reusable components. Use likely shadcn/ui or Radix UI primitives only when they fit established project patterns.

### Implementation Notes

Document grid constraints, token usage, state placement, accessibility considerations, and unresolved product decisions. Do not include code unless requested.

## Anti-Patterns to Avoid

- Choosing a dashboard template before understanding the task.
- Wrapping every section in a card.
- Creating multiple equally prominent primary actions.
- Using arbitrary widths, gaps, or breakpoints without content rationale.
- Hiding essential actions on mobile.
- Using dialogs for complex forms or drawers for unrelated navigation.
- Making entire pages scroll horizontally.
- Treating an empty white region as intentional whitespace when it breaks information balance.
- Producing pixel-perfect implementation details without confirming the design system.
