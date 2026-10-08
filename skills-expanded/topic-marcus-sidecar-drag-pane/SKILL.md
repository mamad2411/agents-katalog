---
name: drag-pane
description: >
  Drag-and-drop pane resizing implementation for two-pane plugin layouts.
  Covers mouse event handling via the internal/mouse package, hit region
  registration, drag delta calculation, width clamping, state persistence,
  and pane layout management. Use when working on pane resizing, drag
  interactions, layout management, or adding drag-to-resize to a new plugin.
---

# Drag-to-Resize Pane Implementation

## Overview

Add drag-to-resize support for two-pane plugin layouts (sidebar + main content). Users click and drag the divider between panes to resize them.

## Prerequisites

- Plugin already has a two-pane layout (sidebar + main content)
- State persistence functions exist in `internal/state/state.go` (each plugin has its own getter/setter)
- Familiarity with `internal/mouse` package

## Existing Implementations

| Plugin | State Functions | Mouse File |
|--------|----------------|------------|
| FileBrowser | `GetFileBrowserTreeWidth()` / `SetFileBrowserTreeWidth()` | `internal/plugins/filebrowser/mouse.go` |
| GitStatus | `GetGitStatusSidebarWidth()` / `SetGitStatusSidebarWidth()` | `internal/plugins/gitstatus/mouse.go` |
| Conversations | `GetConversationsSideWidth()` / `SetConversationsSideWidth()` | `internal/plugins/conversations/mouse.go` |
| Workspace (project) | `GetWorkspaceSidebarWidth()` / `SetWorkspaceSidebarWidth()` | `internal/plugins/workspace/view_list.go` |
| Sessions (global workspace) | `GetWorkspaceSidebarWidth()` / `SetWorkspaceSidebarWidth()` | `internal/overview/workspaces.go` |

## Windowing parity: project and global workspaces are one feature

The project workspace (`internal/plugins/workspace`) and the global Workspaces
browser shown as **Sessions** in the navbar (`internal/overview`) are two
projections of the same windowing model. They are not independent surfaces that
happen to look similar.

**If a change affects panes, splits, drag handles, pane borders, focus chrome,
or pane hit regions in one of them, it affects the other.** The rule is
structural, not a habit to remember:

- `internal/panelayout` owns pane-tree structure and geometry.
- `internal/paneframe` owns presentation: chrome geometry (`Inset`, `Geometry`),
  the leaf border states (`Chrome`, `WrapLeaf`), the drag handle
  (`RenderDividerHandle`, `DividerHitBox`, `HandleStateFor`), the compositor
  (`Compose`, `ComposeLeaf`, `RenderContent`), the chrome-aware floors
  (`ChromeFloors`), and the one order hit regions are registered in
  (`RegisterRegions`), and click-to-focus (`LeafAt`, `FocusLeafAt`).
- Each surface implements `paneframe.Host` and `paneframe.RegionSink` in exactly
  one file: `internal/plugins/workspace/pane_host.go` and
  `internal/overview/pane_host.go`.

**Focus is one value, answered from geometry.** `Host.Focus()` draws the ring and
`Host.SetFocus()` moves it; there is no third place a surface may record who is
being typed into, so a surface whose live terminal holds the keyboard separately
gives it up inside its own focus setter (`workspace.setFocusTarget`,
`overview.focusPreviewLeaf`). A pointer moves focus through
`paneframe.FocusLeafAt`, which resolves the leaf from its OUTER **box**, not from
the hit region the press landed on — a terminal leaf owns no click-to-focus
region, because its presses belong to the live pane and are forwarded to tmux.
`FocusLeafAt` moves focus and nothing else, so the press still reaches whichever
region claimed it, and it declines the divider's widened target so a press one
cell off a handle resizes without also re-focusing. Hanging focus off the region
handlers instead is td-43db92: one focus call per leaf kind, and the ring drawn
on a neighbour for the kind nobody remembered.

`Host.Layout()` must answer the tree the surface last **drew**, not one it could
place. A view that replaces the preview — the kanban board, a modal — draws no
tree, and geometry that outlives the frame lets a click on whatever is drawn
there move pane focus instead. The project plugin records the layout beside the
hit regions it earned (`paneFrame`/`paneFrameDrawn`, cleared with the hit map at
the top of `View`); the global browser's `previewPeerBox()` already refuses when
the preview is not drawn.

**Do not add a second compositor, a second border rule, or a second divider
renderer.** If a behaviour belongs to windowing, it goes in `paneframe`; if it
belongs to one surface's content, it goes in that surface's host file. Both
surfaces then get it at once.

Tests that hold this: `internal/paneframe/paneframe_test.go`,
`internal/plugins/workspace/pane_peer_chrome_test.go`, and
`internal/overview/pane_peer_chrome_test.go`.

### The header's layout button is part of the same model

A pane can be **moved**, not only resized, and that entry point lives in the same
chrome the drag handle does. `internal/panereposition` owns the shared
interaction policy — the modal controller, the header adapter, the structural
fingerprint, and the graft helpers — while `panelayout.PlanMove`/`ApplyMove` own
the structure. There are three hosts, and all three get it: project Workspaces,
global Sessions, and the app content decks.

- **Reserve.** `panereposition.ReserveMovableHeader(width, movable, hasClose)`
  wraps `ui.ReserveHeaderControls` and returns the tab strip's width plus each
  control's column. Each host binds it once per frame in its own
  `reserveHeader`/`composeHeader` pair, and every header renderer, tab strip and
  region on that surface goes through those — a strip laid out for one reserve
  while the header composes another is how a tab click lands on the wrong tab.
  The **drop order as the row narrows is layout first, close `×` last**,
  all-or-nothing per control: a clipped button is a target whose meaning cannot
  be recovered.
- **`movable` comes from the tree** (`panereposition.Movable`): false with no
  tree, and false for a tree of one leaf, because `PlanMove` refuses every
  destination on a single leaf. A header with no leaf also used to compare hover
  against leaf `0`, which every un-hovered header matches, and painted a
  permanently hovered button.
- **Register.** `paneframe.RegionSink.Layout(node, hit)` is registered **after
  `Title` and before `Close`** — one rung earlier than the close button, for the
  reason `RegisterRegions` already documents. Regions are tested in reverse
  order, so `Close` keeps the cell it occupies and `Layout` still outranks the
  title strip beneath it. Each host binds it in its own `pane_host.go` beside
  the close region, with the same hover tracking.
- **Do not add a second one.** A click on `⊞` and the `M` key open the *same*
  `panereposition.Controller`; the controller edits a clone and commits
  atomically, so no host mutates a live tree from a mouse handler. `sidecar
  layout move` is the third caller of the same planner.

A zoomed leaf is drawn through the shared compose/register path, so the visible
`⊞` and its hit region come from the same placement — the regression that made a
zoomed Primary's button unclickable on one surface and not the other.

## Implementation Steps

### Step 1: Add Mouse Handler to Plugin Struct

```go
import "github.com/marcus/sidecar/internal/mouse"

type Plugin struct {
    // ... other fields
    mouseHandler *mouse.Handler
    sidebarWidth int  // Current sidebar width (persisted)
}

func New() *Plugin {
    return &Plugin{
        mouseHandler: mouse.NewHandler(),
    }
}
```

### Step 2: Define Hit Region Constants

```go
const (
    regionSidebar     = "sidebar"
    regionMainPane    = "main-pane"
    regionPaneDivider = "pane-divider"
    dividerWidth      = 1  // Visual divider width
)
```

### Step 3: Initialize Width on First Render (NOT in Init)

**Important:** Do NOT load width in `Init()` - plugin dimensions (`p.width`) are not available yet. Initialize lazily on first render:

```go
func (p *Plugin) renderTwoPane() string {
    p.mouseHandler.HitMap.Clear() // CRITICAL: clear every render

    if p.sidebarWidth == 0 {
        p.sidebarWidth = state.GetYourPluginSidebarWidth()
        if p.sidebarWidth == 0 {
            available := p.width - dividerWidth
            p.sidebarWidth = available * 30 / 100 // Default 30%
        }
    }
    // ... rest of render
}
```

### Step 4: Handle MouseMsg in Update

```go
func (p *Plugin) Update(msg tea.Msg) (plugin.Plugin, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.MouseMsg:
        return p.handleMouse(msg)
    }
}
```

### Step 5: Create mouse.go with Handlers

```go
func (p *Plugin) handleMouse(msg tea.MouseMsg) (*Plugin, tea.Cmd) {
    action := p.mouseHandler.HandleMouse(msg)
    switch action.Type {
    case mouse.ActionClick:
        return p.handleMouseClick(action)
    case mouse.ActionDrag:
        return p.handleMouseDrag(action)
    case mouse.ActionDragEnd:
        return p.handleMouseDragEnd()
    }
    return p, nil
}

func (p *Plugin) handleMouseClick(action mouse.MouseAction) (*Plugin, tea.Cmd) {
    if action.Region == nil {
        return p, nil
    }
    switch action.Region.ID {
    case regionSidebar:
        p.activePane = PaneSidebar
    case regionMainPane:
        p.activePane = PaneMain
    case regionPaneDivider:
        p.mouseHandler.StartDrag(action.X, action.Y, regionPaneDivider, p.sidebarWidth)
    }
    return p, nil
}

func (p *Plugin) handleMouseDrag(action mouse.MouseAction) (*Plugin, tea.Cmd) {
    if p.mouseHandler.DragRegion() != regionPaneDivider {
        return p, nil
    }
    startValue := p.mouseHandler.DragStartValue()
    newWidth := startValue + action.DragDX

    // Clamp to bounds
    // NOTE: Offset varies by plugin (border styling differences):
    // GitStatus: -5, FileBrowser: -6, Conversations: -5, Workspace: just dividerWidth
    available := p.width - 5 - dividerWidth
    minWidth := 25
    maxWidth := available - 40
    if newWidth < minWidth {
        newWidth = minWidth
    } else if newWidth > maxWidth {
        newWidth = maxWidth
    }
    p.sidebarWidth = newWidth
    return p, nil
}

func (p *Plugin) handleMouseDragEnd() (*Plugin, tea.Cmd) {
    _ = state.SetYourPluginSidebarWidth(p.sidebarWidth)
    return p, nil
}
```

### Step 6: Register Hit Regions in Render

**This is where most bugs occur.** Follow this pattern exactly:

```go
func (p *Plugin) renderTwoPane() string {
    p.mouseHandler.HitMap.Clear() // CRITICAL: clear every render

    available := p.width - 5 - dividerWidth
    sidebarWidth := p.sidebarWidth
    if sidebarWidth == 0 {
        sidebarWidth = available * 30 / 100
    }
    if sidebarWidth < 25 {
        sidebarWidth = 25
    }
    if sidebarWidth > available-40 {
        sidebarWidth = available - 40
    }
    mainWidth := available - sidebarWidth
    p.sidebarWidth = sidebarWidth

    // ... render panes and divider ...

    // CRITICAL: Register in priority order (last = highest priority)
    p.mouseHandler.HitMap.AddRect(regionSidebar, 0, 0, sidebarWidth, p.height, nil)
    mainX := sidebarWidth + dividerWidth
    p.mouseHandler.HitMap.AddRect(regionMainPane, mainX, 0, mainWidth, p.height, nil)
    // Divider LAST = highest priority
    dividerX := sidebarWidth
    dividerHitWidth := 3 // Wider than visual for easier clicking
    p.mouseHandler.HitMap.AddRect(regionPaneDivider, dividerX, 0, dividerHitWidth, p.height, nil)

    return content
}
```

### Step 7: Render Visible Divider

Never hand-roll a divider. Use the shared handle so hover and drag colouring,
the one-cell inset at each end, and the theme blend are the same everywhere:

```go
divider := ui.RenderHandle(paneHeight, true, ui.HandleStateFrom(p.hoverDivider, dragging))
```

Inside a pane tree, go through the frame instead, which picks the axis and the
per-split state for you:

```go
handle := paneframe.RenderDividerHandle(divider, host.HandleState(divider.SplitID))
hit := paneframe.DividerHitBox(divider)
```

### Step 8: Add State Persistence

Add plugin-specific functions to `internal/state/state.go`:

```go
// In State struct
YourPluginSidebarWidth int `json:"yourPluginSidebarWidth,omitempty"`

// Getter
func GetYourPluginSidebarWidth() int {
    mu.RLock()
    defer mu.RUnlock()
    if current == nil { return 0 }
    return current.YourPluginSidebarWidth
}

// Setter
func SetYourPluginSidebarWidth(width int) error {
    mu.Lock()
    if current == nil { current = &State{} }
    current.YourPluginSidebarWidth = width
    mu.Unlock()
    return Save()
}
```

## Critical Rules

### Rule 1: Never Reset Width in View()

**WRONG:**
```go
func (p *Plugin) View(width, height int) string {
    p.sidebarWidth = width * 30 / 100 // BUG: Overwrites drag changes every render!
}
```

**CORRECT:** Width is only set when `sidebarWidth == 0`. All other code paths must not unconditionally overwrite it.

### Rule 2: Hit Region X Coordinates

Divider X position = `sidebarWidth`, NOT `sidebarWidth + borderWidth`.

When lipgloss renders `Width(sidebarWidth)`, the pane occupies columns 0 to sidebarWidth-1. The divider starts at column sidebarWidth.

### Rule 3: Hit Region Priority (Registration Order)

`HitMap.Test()` checks regions in **reverse order** - last added = checked first.

The divider region MUST be registered LAST so it takes priority over overlapping pane regions.

```go
// CORRECT ORDER:
p.mouseHandler.HitMap.AddRect(regionSidebar, ...)      // Lowest priority
p.mouseHandler.HitMap.AddRect(regionMainPane, ...)     // Medium priority
p.mouseHandler.HitMap.AddRect(regionPaneDivider, ...)  // HIGHEST priority (last)
```

### Rule 4: Divider Hit Width

Use `dividerHitWidth := 3` (wider than the visual 1-character divider) to make
clicking easier. Inside a pane tree, call `paneframe.DividerHitBox` rather than
widening by hand: a row divider must widen only *upward*, or it masks the header
row — tabs and close button — of the leaf stacked below it.

### Rule 5: Height for Hit Regions

Use `p.height` for hit region height, not `paneHeight` or `paneHeight + 2`.

## Performance Optimization: Hit Region Caching

For plugins with many hit regions, use a dirty flag to avoid rebuilding every render:

```go
type Plugin struct {
    hitRegionsDirty bool
    prevWidth       int
    prevHeight      int
    prevScrollOff   int
}

func (p *Plugin) renderTwoPane() string {
    if p.width != p.prevWidth || p.height != p.prevHeight {
        p.hitRegionsDirty = true
        p.prevWidth = p.width
        p.prevHeight = p.height
    }
    if p.scrollOffset != p.prevScrollOff {
        p.hitRegionsDirty = true
        p.prevScrollOff = p.scrollOffset
    }

    // ... render content ...

    if p.hitRegionsDirty {
        p.mouseHandler.HitMap.Clear()
        // Register all hit regions...
        p.hitRegionsDirty = false
    }
    return content
}
```

Also mark `hitRegionsDirty = true` when:
- View mode changes (toggling list/detail)
- Content changes (items loaded, expanded/collapsed)
- Sidebar visibility toggles

See `internal/plugins/conversations/view_layout.go` and `plugin_input.go` for a complete implementation.

## Debugging

If drag is not working, add temporary logging:

```go
func (p *Plugin) handleMouseClick(action mouse.MouseAction) (*Plugin, tea.Cmd) {
    log.Printf("CLICK x=%d y=%d region=%v", action.X, action.Y, action.Region)
}
```

Common issues:
- **Region is nil or wrong pane:** Check X coordinate calculation and registration order
- **Drag starts but width does not change:** Check that `handleMouseDrag` is being called
- **Width resets after drag:** Search for code that sets `sidebarWidth` unconditionally
