---
name: dhtmlx-js-gantt
description: >
  Builds and integrates core DHTMLX JavaScript Gantt into JavaScript or TypeScript
  applications. Covers setup, initialization, lifecycle, gantt.parse/gantt.load,
  templates, events, plugins, DataProcessor, task/link CRUD, projects/summary
  tasks, milestones, multiple instances, resources, calendars, undo/redo, row
  reorder, sortorder, baselines, critical path, locale/i18n, styling, and
  theming for dhtmlx-gantt (MIT Community edition at v10+, GPL Standard at v9.x),
  @dhx/trial-gantt, and @dhx/gantt (Professional). Applies when working with
  gantt charts, project timelines, task dependencies, task CRUD, summary tasks,
  milestones, resource panels, working calendars, lightboxes, workload views,
  baselines, or weekend highlighting, regardless of whether "DHTMLX" is mentioned
  by name. Provides verified API guidance rather than guessing core Gantt APIs
  and surfaces edition limits before scaffolding.
---

## Source Of Truth

Use only:
1. The current project's files, structure, and established patterns
2. DHTMLX MCP for core Gantt API details: https://docs.dhtmlx.com/mcp
3. Official DHTMLX Gantt docs as fallback: https://docs.dhtmlx.com/gantt/

Never invent config names, template callbacks, event names, method signatures, data shapes, or backend behavior.

If any core Gantt API detail is unclear, resolve it through DHTMLX MCP before writing code.

## Preflight

Before writing code, identify:
- **delivery**: npm package (`dhtmlx-gantt`, `@dhx/trial-gantt`, `@dhx/gantt`) — check `package.json`, imports, lockfiles. Or script tag / CDN — check `<script>` tags in HTML, vendored `dhtmlxgantt.js`, the `@license` banner inside that file, or the runtime `gantt.license` / `gantt.version` fields.
- **edition**: the free `dhtmlx-gantt` package is **MIT Community at v10+** and **GPL Standard at v9.x** — resolve which by version (`gantt.version` / lockfile), since the package name is shared (`gantt.license` is `"mit"` vs `"gpl"`). `@dhx/trial-gantt` and `@dhx/gantt` are Professional. The two free editions have *different* feature sets — MIT adds projects/milestones/custom types/multiple instances but drops undo, markers, multiselect, unscheduled tasks, the new-task placeholder, working-time calendars, and WBS. See [references/editions.md](references/editions.md) for detection and the per-edition feature matrix.
- **runtime**: plain JavaScript, TypeScript, Vite, browser-only `<script>`, or another app setup
- **outbound changes**: no persistence, `gantt.createDataProcessor`, or custom backend/API clients
- **inbound changes**: none, hard reload (`gantt.clearAll` + `gantt.parse`), or incremental updates via `gantt.silent`-wrapped API calls — see [references/data-and-crud.md](references/data-and-crud.md). For real-time streams use `gantt.ext.liveUpdates` — see [references/live-updates.md](references/live-updates.md).

## Workflow

1. Confirm the installed DHTMLX Gantt package and import path.
2. Decide the outbound and inbound change strategies before implementing CRUD or external sync.
3. Read only the reference file needed for the task:
   - Editions (MIT Community / GPL Standard / PRO), version-based detection, and the per-edition feature matrix: [references/editions.md](references/editions.md)
   - Setup: [references/setup.md](references/setup.md)
   - CRUD, state, and persistence: [references/data-and-crud.md](references/data-and-crud.md)
   - Failure cases and guardrails: [references/known-failures.md](references/known-failures.md)
   - Advanced patterns (plugins, reorder, resources, baselines, critical path, zoom, undo/redo, schema): [references/advanced-patterns.md](references/advanced-patterns.md)
   - Real-time / multi-user / external change streams (`gantt.ext.liveUpdates`): [references/live-updates.md](references/live-updates.md)
   - Styling, theming, CSS variables, selectors, and template-based visual customization: [references/styling-and-theming.md](references/styling-and-theming.md)
4. Use DHTMLX MCP before relying on advanced or unfamiliar APIs.
5. Implement with documented APIs only.

## MCP Server

This skill relies on DHTMLX MCP for API verification. If the `dhtmlx-mcp` tool is not available, ask the user to add it:

Claude Code:
```bash
claude mcp add --transport http dhtmlx-mcp https://docs.dhtmlx.com/mcp
```

Codex:
```bash
codex mcp add dhtmlx-mcp --url https://docs.dhtmlx.com/mcp
```

If MCP is not available, use the official docs at https://docs.dhtmlx.com/gantt/ as fallback.

## Consult MCP First For

Consult DHTMLX MCP before using or changing:
- template callbacks you have not already verified
- lifecycle patterns around multiple instances or repeated mount/unmount
- advanced DataProcessor modes, delete confirmation, resources, or assignments
- row reorder config, events, and event signatures
- resource panel, resource datastore, resource timeline, or histogram APIs
- working calendar rules and work-time helpers
- lightbox section types and option-list patterns
- CSS variable names beyond the current project usage
- `gantt.plugins({...})` extension loading and the matching `gantt.ext.*` surfaces (critical path, marker, tooltip, keyboard navigation, undo, export, auto-scheduling)
- locale and i18n customization via `gantt.i18n.setLocale` and `gantt.locale.labels.*`
- baseline render templates and baseline data shape
- `gantt.ext.liveUpdates` (`RemoteEvents`, `remoteUpdates`) and the multi-user backend WebSocket protocol

## Hard Rules

- The Gantt container must have explicit height.
- Import the matching Gantt CSS.
- Use the app theme as the single source of truth.
- Prefer documented config, templates, events, and methods over undocumented internals.
- Keep DHTMLX init/parse/events/DataProcessor cleanup in one lifecycle boundary.
- Normalize date values before persistence.
- Build backend payloads explicitly from normalized task/link models.
- Return `{ id: databaseId }` or `{ tid: databaseId }` after creates when the backend assigns a real id.
- When applying external changes via `gantt.addTask` / `updateTask` / `deleteTask` (or link/datastore equivalents), wrap them in `gantt.silent(...)` so they do not echo back through the DataProcessor.
- Treat row reorder as a dedicated batch flow, not a normal single-task update.
- Gantt template return values (`task_text`, `tooltip_text`, column `template`, scale formatters, etc.) are injected as raw HTML. Sanitize or HTML-escape every user-supplied string before it enters Gantt (or in the template) — never trust task text, descriptions, resource names, or any other free-text field to be safe.
- Before scaffolding a feature, confirm it exists in the *detected edition* (see [references/editions.md](references/editions.md)). If it does not — a PRO feature on either free install, **or** a Standard/GPL feature (undo, markers, multiselect, unscheduled tasks, new-task placeholder, working-time calendars, WBS) on a **MIT Community** install — warn the user *before* scaffolding, naming the edition(s) that support it and the upgrade/switch path, then still scaffold the requested code. Do not silently substitute or omit it.

## Quick Checklist

- [ ] Correct package identified
- [ ] Edition determined (MIT vs GPL resolved by version) and any feature unavailable in that edition flagged
- [ ] Matching CSS import used
- [ ] Explicit height provided
- [ ] Outbound and inbound change strategies decided
- [ ] Dates normalized before persistence
- [ ] DataProcessor return values handled
- [ ] Advanced APIs verified with MCP
