---
name: worklog-design
description: >
  Design and UI skill for the Worklog desktop project manager.
  Stack: SvelteKit 5 (Svelte Runes), Tauri v2, carbon-components-svelte, TypeScript, Bun.
  Use whenever building, refactoring, or extending Worklog's UI — new views, components,
  layouts, theming, or visual polish aligned with the Carbon Design System and the
  local-first desktop product philosophy.
---

# Worklog Design Skill

## Project Identity

Worklog is a **local-first, keyboard-driven desktop project manager** for small dev teams.

Core qualities that should always be felt in the UI:

| Quality | What it means in practice |
|---|---|
| **Fast** | Instant feedback. No loading skeletons for local SQLite data. Transitions ≤ 150 ms. |
| **Keyboard-first** | Every action reachable without a mouse. Shortcuts visible in tooltips. |
| **Dense, not cluttered** | Information-rich layout typical of desktop apps. Prefer compact Carbon sizing. |
| **Local-first transparency** | No cloud metaphors. Workspace = folder on disk. |
| **Small team focus** | No enterprise complexity. One workspace, one team, clear hierarchy. |

---

## Stack Constraints

### SvelteKit 5 + Svelte Runes
- Components use `$state`, `$derived`, `$effect` — no `writable()` stores for new code.
- Layouts own scope: workspace scope in `+layout.svelte`, board scope in nested layouts.
- Use `$page` from `$app/stores` for route params; prefer typed params via `RouteParams`.
- Async data goes in `+page.ts` / `+layout.ts` `load()` functions, not inline `onMount`.
- Avoid `onMount` for data fetching; it causes flash-of-empty-content in Tauri webview.

### Tauri v2
- All persistence calls go through Tauri SQL plugin (`@tauri-apps/plugin-sql`) via the repository layer in `src/lib/db/`.
- **Never** call the repository directly from a component — always go through a hook in `src/lib/hooks/`.
- Tauri `invoke` for custom Rust commands (e.g., Git sync, file system operations).
- Window is frameless; the app shell owns the drag region and custom title bar area.
- No `localStorage`, `sessionStorage`, or IndexedDB — SQLite is the source of truth.
- File paths use Tauri path API (`appDataDir`, `join`) — never hardcode OS paths.

### carbon-components-svelte
- Theme: use **Gray 90** (`g90`) dark theme as the default — it matches the existing dark shell.
  - Import in `app.html` or root `+layout.svelte`: `import 'carbon-components-svelte/css/g90.css'`
  - For light mode support, dynamically swap to `g10`.
- Use `optimizeImports` from `carbon-preprocess-svelte` in `svelte.config.js` to avoid slow dev builds.
- Prefer Carbon's compact density tokens: `size="sm"` on buttons/inputs inside panels.
- **Do not fight Carbon's CSS custom properties** — override with `--cds-*` tokens, never with `!important` hacks.
- Common components to reach for first:

| Use case | Carbon component |
|---|---|
| Sidebar nav | `SideNav`, `SideNavItems`, `SideNavLink`, `SideNavMenu` |
| Command palette / search | `Search` + custom modal overlay |
| Ticket cards | `Tile`, `ClickableTile` |
| Modals / dialogs | `Modal` |
| Forms | `TextInput`, `TextArea`, `Select`, `Toggle`, `Checkbox` |
| Tags / labels | `Tag` |
| Data tables | `DataTable`, `Toolbar`, `ToolbarSearch` |
| Notifications | `InlineNotification`, `ToastNotification` |
| Buttons | `Button`, `IconButton` |
| Context menus | `OverflowMenu`, `OverflowMenuItem` |
| Tooltips | `Tooltip`, `TooltipDefinition` |
| Progress / loading | `InlineLoading`, `SkeletonText` |

---

## Layout Architecture

```
AppShell (root +layout.svelte)
├── TitleBar          ← custom drag region, app name, window controls
├── SideNav           ← workspaces list + board tree
│   ├── WorkspaceHeader
│   ├── BoardTree     ← per-board SideNavLink with right-click OverflowMenu
│   └── NavFooter     ← settings link, sync status badge
└── MainContent       ← <slot /> — swapped by nested routes
    ├── KanbanView    ← /boards/[id]
    ├── TableView     ← /boards/[id]/table
    ├── TimelineView  ← /boards/[id]/timeline
    └── SettingsView  ← /settings/[tab]
```

**Key layout rules:**
- The sidebar is fixed-width (`240px` default, resizable via CSS variable `--worklog-sidebar-width`).
- The title bar drag region must use `-webkit-app-region: drag` with interactive elements set to `-webkit-app-region: no-drag`.
- Never use full-page loading states — local SQLite is fast; show stale data instantly, then update.

---

## Design Tokens & Custom Properties

Override or extend Carbon tokens at `:root` in `src/app.css`:

```css
:root {
  /* Sidebar */
  --worklog-sidebar-width: 240px;
  --worklog-sidebar-bg: var(--cds-ui-background);     /* matches g90 */

  /* Kanban columns */
  --worklog-column-width: 280px;
  --worklog-column-gap: 12px;

  /* Ticket card */
  --worklog-card-radius: 2px;                          /* Carbon is square-ish */
  --worklog-card-padding: 12px;

  /* Status colors — extend Carbon's semantic palette */
  --worklog-status-backlog:     var(--cds-text-02);
  --worklog-status-todo:        var(--cds-interactive-01);
  --worklog-status-in-progress: #f1c21b;               /* Carbon yellow-30 */
  --worklog-status-done:        #42be65;               /* Carbon green-40 */

  /* Priority */
  --worklog-priority-low:       var(--cds-text-02);
  --worklog-priority-medium:    var(--cds-interactive-01);
  --worklog-priority-high:      #ff832b;               /* Carbon orange-40 */
  --worklog-priority-critical:  var(--cds-support-error);

  /* Typography — Carbon uses IBM Plex by default; Worklog inherits this */
  --worklog-font-mono: 'IBM Plex Mono', monospace;

  /* Zoom — controlled by app settings (50%–200%) */
  --worklog-zoom: 1;
}
```

Apply zoom at the app shell level:
```css
#app-shell {
  zoom: var(--worklog-zoom);   /* Tauri webview supports this */
}
```

---

## Component Patterns

### Kanban Board

```svelte
<!-- KanbanBoard.svelte -->
<script lang="ts">
  import { Tag, OverflowMenu, OverflowMenuItem } from 'carbon-components-svelte';
  import type { Ticket } from '$lib/db/types';

  let { columns }: { columns: KanbanColumn[] } = $props();
</script>

<div class="kanban-board">
  {#each columns as col}
    <div class="kanban-column">
      <header class="col-header">
        <span class="col-title">{col.label}</span>
        <Tag size="sm">{col.tickets.length}</Tag>
      </header>
      <div class="col-body">
        {#each col.tickets as ticket (ticket.id)}
          <TicketCard {ticket} />
        {/each}
      </div>
    </div>
  {/each}
</div>

<style>
  .kanban-board {
    display: flex;
    gap: var(--worklog-column-gap);
    height: 100%;
    overflow-x: auto;
    padding: 16px;
  }
  .kanban-column {
    flex: 0 0 var(--worklog-column-width);
    display: flex;
    flex-direction: column;
    background: var(--cds-ui-01);
    border: 1px solid var(--cds-ui-03);
  }
  .col-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    border-bottom: 1px solid var(--cds-ui-03);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--cds-text-02);
  }
  .col-body {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 8px;
  }
</style>
```

### Ticket Card

```svelte
<!-- TicketCard.svelte -->
<script lang="ts">
  import { Tag, OverflowMenu, OverflowMenuItem } from 'carbon-components-svelte';
  import type { Ticket } from '$lib/db/types';

  let { ticket, onSelect, onMove }: {
    ticket: Ticket;
    onSelect: (id: string) => void;
    onMove: (id: string, direction: 'next' | 'prev') => void;
  } = $props();

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'm') onMove(ticket.id, 'next');
    if (e.key === 'Escape') { /* close panel */ }
  }
</script>

<div
  class="ticket-card"
  tabindex="0"
  role="button"
  aria-label="Ticket: {ticket.title}"
  onclick={() => onSelect(ticket.id)}
  onkeydown={handleKeydown}
>
  <div class="ticket-header">
    <span class="ticket-id">{ticket.id.slice(0, 8)}</span>
    <OverflowMenu size="sm" flipped>
      <OverflowMenuItem text="Move forward" on:click={() => onMove(ticket.id, 'next')} />
      <OverflowMenuItem text="Move back"    on:click={() => onMove(ticket.id, 'prev')} />
      <OverflowMenuItem text="Delete"       danger />
    </OverflowMenu>
  </div>
  <p class="ticket-title">{ticket.title}</p>
  <div class="ticket-meta">
    {#if ticket.priority}
      <Tag size="sm" type="outline"
        style="--tag-color: var(--worklog-priority-{ticket.priority})">
        {ticket.priority}
      </Tag>
    {/if}
    {#if ticket.due_date}
      <span class="ticket-date">{formatDate(ticket.due_date)}</span>
    {/if}
  </div>
</div>

<style>
  .ticket-card {
    background: var(--cds-ui-02);
    border: 1px solid var(--cds-ui-03);
    border-radius: var(--worklog-card-radius);
    padding: var(--worklog-card-padding);
    cursor: pointer;
    transition: border-color 120ms ease, background 120ms ease;
  }
  .ticket-card:hover,
  .ticket-card:focus-visible {
    border-color: var(--cds-interactive-01);
    outline: none;
    background: var(--cds-hover-ui);
  }
  .ticket-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
  }
  .ticket-id {
    font-family: var(--worklog-font-mono);
    font-size: 0.6875rem;
    color: var(--cds-text-03);
  }
  .ticket-title {
    font-size: 0.875rem;
    line-height: 1.4;
    color: var(--cds-text-01);
    margin: 0 0 8px;
  }
  .ticket-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }
  .ticket-date {
    font-size: 0.6875rem;
    color: var(--cds-text-03);
    font-family: var(--worklog-font-mono);
  }
</style>
```

### Command Palette
Worklog's command palette (`Ctrl/Cmd+K`) should use Carbon's `Search` inside a `Modal`:

```svelte
<!-- CommandPalette.svelte -->
<script lang="ts">
  import { Modal, Search } from 'carbon-components-svelte';

  let open = $state(false);
  let query = $state('');
</script>

<svelte:window onkeydown={(e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    open = true;
  }
}} />

<Modal bind:open size="sm" passiveModal modalHeading="" hasScrollingContent>
  <Search bind:value={query} placeholder="Type a command…" autofocus size="lg" />
  <!-- filtered results list -->
</Modal>
```

---

## Interaction & Motion

Worklog is a **productivity tool** — motion must be functional, never decorative:

- **Transitions**: `transition: background 120ms ease, border-color 120ms ease` for hover/focus states.
- **Panel slide-in**: Ticket detail panel should slide in from the right at `200ms ease-out`. Use Svelte's `fly` transition: `transition:fly={{ x: 320, duration: 200 }}`.
- **Column drag-and-drop**: Use `dndzone` from `svelte-dnd-action` — it handles accessibility and keyboard DnD natively.
- **No skeleton loaders**: Local SQLite data is synchronous-ish. Show last-known state immediately; update reactively.
- **Toast notifications**: Use `ToastNotification` for Git sync events (success / failure). Position bottom-right, auto-dismiss after 4 s.

---

## Accessibility (a11y)

Carbon handles most a11y out of the box. Worklog-specific requirements:

- Every interactive Svelte component that isn't a native button must have `role` + `tabindex="0"` + `onkeydown` handler.
- Keyboard shortcut hints: show in `TooltipDefinition` with `align="bottom"`, text like `M — move ticket`.
- Focus management: when ticket detail panel opens, move focus to the panel's close button; when it closes, return focus to the triggering card.
- Use `aria-live="polite"` on the sync status badge in the sidebar.

---

## File Conventions

| File | Purpose |
|---|---|
| `src/app.css` | Global CSS, custom properties, Carbon theme import |
| `src/lib/components/app/` | Domain feature components (KanbanBoard, TicketCard, etc.) |
| `src/lib/components/ui/` | Generic reusable components that wrap or extend Carbon |
| `src/lib/hooks/` | Svelte 5 Runes hooks — data fetching, mutations, reactive state |
| `src/lib/db/` | Repository layer — only place that calls `@tauri-apps/plugin-sql` |
| `src/routes/` | SvelteKit routes; layouts own scope |

---

## Do / Don't

| ✅ Do | ❌ Don't |
|---|---|
| Use Carbon tokens (`--cds-*`) for all colors | Use raw hex colors inside components |
| Put data access in hooks, not components | Call `db.*` directly from a `.svelte` file |
| Use `$state` / `$derived` (Svelte 5 Runes) | Use `writable()` / `readable()` stores |
| Reach for Carbon components first | Rebuild what Carbon already provides |
| Keep transitions ≤ 200 ms | Add decorative animations or loading spinners |
| Use `OverflowMenu` for context actions | Build custom dropdown menus |
| Apply `size="sm"` in dense panel areas | Use default (md) sizing everywhere — too tall |
| Test keyboard navigation on every new component | Ship mouse-only interactions |

