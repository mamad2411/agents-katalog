---
name: interface
description: Compose bespoke TypeScript components into complete, functional application views and dashboards with working client-side state.
argument-hint: "--workspace <run-path> --contract <contract-path> --target <target-path>"
---

# Application Interface Composition

Replace `<plugin-root>` in CLI examples with the absolute directory two levels above this skill file (`skills/interface/SKILL.md`); Claude Code may use `${CLAUDE_PLUGIN_ROOT}` instead. Never execute the literal placeholder.

Composes discrete atomic and molecular components into complete, cohesive application views, dashboards, and settings screens. The composition engine synthesizes layout craft from `interface-design`, ensuring visual rhythm, structured content grouping, and working client-side state.

## CLI Context

Uses the project-owned run workspace and contract generated in earlier stages:
```bash
node "<plugin-root>/scripts/cli.mjs" status --workspace "<workspace-path>"
```

## Interface Craft & Architecture Standards

### 1. Visual Hierarchy & Information Density
Adhere to the principles in `references/upstream/interface-design-main/.claude/skills/interface-design/SKILL.md`:
- **Typography Scale**: Intentional typographic contrast. Display headings for landmark sections, crisp medium-weight labels for data tables and controls, and readable muted text for secondary metadata.
- **Rhythm and Grouping**: Group related controls and metrics with structured visual boundaries (1px subtle border, subtle background shift) rather than floating card soup with deep shadows.
- **Data Density**: Balance whitespace and compactness. Administrative and analytics surfaces prioritize clear data scanning, readable numbers, and tabular alignment over oversized empty padding.

### 2. Working Client-Side State and Interactivity
Composed interfaces must provide fully functional local state:
- **Filtering, Sorting & Pagination**:
  - Data tables and list views implement working client-side sort handlers for text and numeric columns.
  - Search inputs filter table rows in real-time with debouncing.
  - Pagination controls update active page index and slice data accordingly.
- **Form State & Asynchronous Submissions**:
  - Forms maintain controlled input values and validate required fields before submission.
  - Submit handlers simulate realistic asynchronous API calls with loading states (`aria-busy="true"`), disabling submission buttons to prevent double-clicks.
  - Display inline validation errors for invalid inputs and top-level banner alerts for submission failures.
- **Modal & Overlay Management**:
  - Modal dialog triggers manage open/close state cleanly.
  - Confirmation dialogs wire confirm/cancel callbacks to update parent view data.
- **No Dead Placeholders**: Never emit empty callbacks `onClick={() => {}}` or dead anchors `href="#"`. Expose strongly-typed callbacks (`onSave`, `onFilterChange`, `onRowAction`) for parent application integration.

### 3. Accessible Landmark Structure
Structure view markup using semantic HTML5 landmarks:
- `<nav aria-label="Main Navigation">`: Application sidebars and top bars.
- `<main>`: Primary content area.
- `<header>`: Page title, breadcrumbs, and contextual action buttons.
- `<section aria-labelledby="section-title-id">`: Grouped view cards and widgets.
- `<aside>`: Secondary contextual sidebars or activity feeds.

### 4. Memory Persistence (`system.md`)
When working in a target repository with `.interface-design/system.md`, update the system memory to record newly introduced views, component compositions, and reusable view layout patterns.
