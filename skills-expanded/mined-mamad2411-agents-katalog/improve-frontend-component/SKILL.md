---
name: improve-frontend-component
description: Plan frontend component refactoring opportunities by reading a repo or user-selected area and recommending where to apply the frontend-component skill. Use when the user wants suggestions, a planning pass, or an audit for splitting React/Vue/Svelte/HTML UI into clearer components before implementation.
---

# Improve Frontend Component Structure

This is a planning skill. Do not edit code unless the user explicitly asks to implement a selected suggestion.

Use this skill to inspect a frontend codebase or a user-selected repo area, then recommend where and how to apply the `frontend-component` skill.

## Process

### 1. Establish scope

Use the user's selected repo, path, PR, screenshot, or stated product area as the scope. If no scope is given, inspect the current repo and find likely frontend entry points.

Prefer reading:

- package files and framework config to identify React/Vue/Svelte/HTML structure
- route/page directories
- large or product-critical UI files
- CSS/style entry points related to those UI files
- nearby tests or stories if present

Use an Explore agent when the repo is large or unfamiliar. Ask it to map frontend pages, oversized UI files, mixed-concern components, and CSS ownership patterns.

### 2. Identify component-structure friction

Look for opportunities that match `frontend-component` guidance:

- page files mixing orchestration, route/query state, data fetching, tabs, forms, and provider/section-specific markup
- tabs or mutually exclusive branches with all panel markup inline
- product sections that have clear names but no component boundary
- repeated cards/forms/status rows that are stable enough to extract
- provider-specific UI logic mixed together in one component
- CSS files whose ownership no longer matches the UI structure
- flat `components/` folders containing domain-specific pieces that should live near the screen/product area

Avoid suggestions based only on line count. Prioritize changes that would make the product structure easier to scan and maintain.

### 3. Present suggestions, not code

Return a numbered planning list. For each suggestion include:

- **Area** — product area and relevant files
- **Current friction** — what makes the UI hard to scan or change
- **Suggested split** — proposed component/file boundaries using product-language names
- **Why it helps** — how the parent page becomes clearer and which concerns become isolated
- **CSS note** — whether styles should remain, split, or be reordered to preserve cascade
- **Risk / check** — build, typecheck, visual regression, or interaction to verify

When helpful, include a small target tree, for example:

```txt
settings/
  SettingsPage.tsx
  connections/
    ConnectionsPanel.tsx
    GoogleConnectionPanel.tsx
    OutlookConnectionPanel.tsx
```

Do not propose generic names like `MainContent`, `SectionView`, or `TabContent` when product-language names are available.

### 4. Ask for selection

End by asking which suggestion the user wants to implement or explore further.

If the user chooses one, switch to `frontend-component` for implementation guidance unless they still want planning only.

## Output shape

Use this compact format:

```md
## Frontend component improvement opportunities

1. **[Short name]**
   - **Area:** ...
   - **Current friction:** ...
   - **Suggested split:** ...
   - **Why it helps:** ...
   - **CSS note:** ...
   - **Risk / check:** ...

Which one should we take into implementation?
```
