---
name: ui-features
description: Implementing UI/UX features in sidecar including modals (internal/modal library), keyboard shortcuts, mouse support, scrolling, pill/tab rendering, and pane resizing. Use when implementing UI features, handling user input, adding keyboard shortcuts, building modals, or working on UX improvements.
---

# UI Feature Implementation

Single entry point for sidecar UI work. All new modals must use `internal/modal`. For complete keyboard shortcut listings, see `references/keyboard-shortcuts-reference.md`.

## Quick Checklist

- Modals: use `internal/modal`, render with `ui.OverlayModal`, avoid manual hit region math
- Pills/chips/tabs: use `styles.RenderPillWithStyle`; auto-fallback when `nerdFontsEnabled` is false
- Keyboard: Commands + FocusContext + bindings must match; names short; priorities set
- Mouse: rebuild hit regions on each render; add general regions first, specific last
- Rendering: keep output within View width/height to avoid header/footer overlap. Use `contentHeight := height - headerLines - footerLines`
- Testing: verify keyboard, mouse, hover, scrolling, and footer hints
- Plugins must NOT render their own footer -- the app renders a unified footer from `Commands()`

## Modals (internal/modal)

All new modals must use `internal/modal`. See `docs/guides/deprecated/declarative-modal-guide.md` for the full API.

### Create a modal

```go
m := modal.New("Delete Worktree?",
    modal.WithWidth(58),
    modal.WithVariant(modal.VariantDanger),
    modal.WithPrimaryAction("delete"),
).
    AddSection(modal.Text("Name: " + wt.Name)).
    AddSection(modal.Spacer()).
    AddSection(modal.Buttons(
        modal.Btn(" Delete ", "delete", modal.BtnDanger()),
        modal.Btn(" Cancel ", "cancel"),
    ))
```

### Render in View

```go
func (p *Plugin) renderDeleteView(width, height int) string {
    background := p.renderListView(width, height)
    rendered := p.deleteModal.Render(width, height, p.mouseHandler)
    return ui.OverlayModal(background, rendered, width, height)
}
```

### Handle input in Update

```go
case tea.KeyMsg:
    action, cmd := p.deleteModal.HandleKey(msg)
    if action != "" {
        return p.handleModalAction(action)
    }
    return p, cmd

case tea.MouseMsg:
    action := p.deleteModal.HandleMouse(msg, p.mouseHandler)
    if action != "" {
        return p.handleModalAction(action)
    }
    return p, nil
```

### Modal initialization and caching (critical)

Always call `ensureModal()` in BOTH View and Update handlers. Create an ensure function that:
1. Returns early if required state is missing
2. Caches based on width to avoid rebuilding every frame
3. Creates the modal only when needed

```go
func (p *Plugin) ensureMyModal() {
    if p.targetItem == nil {
        return
    }
    modalW := 50
    if modalW > p.width-4 { modalW = p.width - 4 }
    if modalW < 20 { modalW = 20 }
    if p.myModal != nil && p.myModalWidthCache == modalW {
        return
    }
    p.myModalWidthCache = modalW
    p.myModal = modal.New("Title", modal.WithWidth(modalW), ...).
        AddSection(...)
}
```

**The key handler MUST call ensure before checking nil:**

```go
func (p *Plugin) handleMyModalKeys(msg tea.KeyMsg) tea.Cmd {
    p.ensureMyModal()  // CRITICAL: Initialize before nil check
    if p.myModal == nil { return nil }
    action, cmd := p.myModal.HandleKey(msg)
    return cmd
}
```

### Async content invalidation

When modal content depends on async data, invalidate the cache when data arrives:

```go
case MyDataLoadedMsg:
    p.myData = msg.Data
    p.clearMyModal()  // Force rebuild with new content
    return p, nil
```

### Modal keyboard shortcuts and footer hints

Modals need their own focus context and commands for footer hints:

1. Return a dedicated context from `FocusContext()`
2. Add commands for the modal context in `Commands()`
3. Add bindings in `internal/keymap/bindings.go`
4. Intercept custom keys before `modal.HandleKey` (Tab/Enter/Esc are handled internally)

```go
func (p *Plugin) FocusContext() string {
    switch p.viewMode {
    case ViewModeError:  return "git-error"
    case ViewModePushMenu: return "git-push-menu"
    default: return "git-status"
    }
}
```

### Modal notes

- `HandleKey`/`HandleMouse` handle Tab, Shift+Tab, Enter, Esc internally
- Backdrop clicks return "cancel"; use `WithCloseOnBackdropClick(false)` to disable
- Use built-in sections (Text, Input, Textarea, Buttons, Checkbox, List, When) before custom layouts
- For bespoke layouts, use `modal.Custom` and return explicit focusable offsets
- `SetFocus(id)` auto-scrolls viewport to focused element
- Prefer `ui.OverlayModal(background, modal, width, height)` for dimmed overlays; do not pre-center with `lipgloss.Place`

### Background colors (critical)

Lipgloss `Background()` does not cascade into child content. ANSI resets clear the parent background. Solution: replace ANSI resets within viewport lines with reset + background re-apply, then pad short lines. See `fillBackground` in `internal/modal/layout.go`.

## Pill-Shaped Elements (internal/styles)

Controlled by `nerdFontsEnabled` in `~/.config/sidecar/config.json` (`ui.nerdFontsEnabled`).

```go
// With explicit colors
label := styles.RenderPill("Output", styles.TextPrimary, styles.Primary, "")

// With a lipgloss.Style (preferred for tabs/chips)
active := styles.RenderPillWithStyle("Output", styles.BarChipActive, "")
inactive := styles.RenderPillWithStyle("Diff", styles.BarChip, "")
```

Available styles: `styles.BarChip` (inactive), `styles.BarChipActive` (active), or custom `lipgloss.Style`.

Test with both `nerdFontsEnabled: true` and `false` to verify fallback.

## Keyboard Shortcuts

For complete per-plugin shortcut listings, see `references/keyboard-shortcuts-reference.md`.

### Three things must match

1. **Command ID** in `Commands()` (e.g., `"stage-file"`)
2. **Binding command** in `internal/keymap/bindings.go` (e.g., `"stage-file"`)
3. **Context string** in both places (e.g., `"git-status"`)

```go
// 1) Commands()
{ID: "stage-file", Name: "Stage", Context: "git-status", Priority: 1}

// 2) FocusContext()
func (p *Plugin) FocusContext() string { return "git-status" }

// 3) bindings.go
{Key: "s", Command: "stage-file", Context: "git-status"}
```

### Multiple contexts (view modes)

Return different context strings from `FocusContext()` for different modes. Each context gets its own footer hints and key bindings.

### Priority guidelines

- **1**: Primary actions (Stage, Commit, Open)
- **2**: Secondary actions (Diff, Search, Push)
- **3**: Tertiary actions (History, Refresh)
- **4+**: Palette only

### Root contexts (q behavior)

In root contexts, `q` shows quit confirmation. In non-root, `q` navigates back. Root contexts: `global`, `conversations`, `conversations-sidebar`, `git-status`, `git-status-commits`, `git-status-diff`, `file-browser-tree`, `workspace-list`, `td-monitor`.

Update `isRootContext()` in `internal/app/update.go` when adding new contexts.

### Text input contexts

When a view has text input, implement `plugin.TextInputConsumer` and return `true` while active. This prevents app-level shortcuts from intercepting typed characters.

```go
func (p *Plugin) ConsumesTextInput() bool {
    return p.showMyModal
}
```

### Footer rendering flow

```
footerHints()
    +-- pluginFooterHints() -> Commands() filtered by FocusContext(), sorted by Priority
    +-- globalFooterHints() -> App-level hints
renderHintLineTruncated(hints, availableWidth)
    -> Renders left-to-right until width exceeded
```

### Keyboard checklist

- Command in `Commands()` with ID, Name, Context, Priority
- `FocusContext()` returns matching context
- Binding in `internal/keymap/bindings.go`
- Key handled in `Update()` if app does not intercept
- No conflicting keys in same context
- Short footer hint names, primary actions Priority 1-2
- Verify `q` behavior with `isRootContext()`

### Core files

| File | Purpose |
|------|---------|
| `internal/plugin/plugin.go` | Command struct, Commands(), FocusContext(), TextInputConsumer |
| `internal/keymap/bindings.go` | Default key-to-command mappings |
| `internal/keymap/registry.go` | Runtime binding lookup |
| `internal/app/update.go` | Key routing, isRootContext() |
| `internal/app/view.go` | Footer rendering |

## Scrollbar (internal/ui)

```go
rendered, geom := ui.RenderScrollbarWithState(ui.ScrollbarParams{
    TotalItems:   len(items),
    ScrollOffset: p.scrollOffset,
    VisibleItems: visibleCount,
    TrackHeight:  height,
}, style) // ui.ScrollbarStyle{Thumb: state, Track: state}; zero value renders byte-identically to RenderScrollbar
```

Every scrollbar backed by real scroll state is interactive under the mouse (macOS-style),
including the terminal panes' bars over captured scrollback. Terminal surfaces map
presses and drags through `tty.WindowScrollbarFor` onto the shared window model: the
gesture freezes the window at an absolute start, release thaws (offset zero follows
again), and history loads defer to release so a mid-gesture renumber cannot shift the
mapping. Adoption ledger:
`docs/plans/active/mouse-draggable-scrollbars.md` ("Adoption outcome").

Pattern: reduce content width by 1, render content, render scrollbar, join horizontally with `lipgloss.JoinHorizontal(lipgloss.Top, content, scrollbar)`.

For multi-line items, set `TrackHeight` to actual terminal rows: `visibleCount * linesPerItem`.

Mouse contract per surface:

1. Register `ui.RegionScrollbarTrack`, then `ui.RegionScrollbarThumb`, after content
   regions in the same render pass that builds the HitMap (reverse scan gives the bar its
   column). Register nothing when `geom.HasThumb` is false — that column is a spacer.
2. Thumb press = grab at that row; track press = jump-to-spot anchored at the grabbed row;
   both end in `StartDrag` so releasing anywhere settles cleanly. Drag maps through
   `ui.OffsetAtRow` against the press-time params snapshot; past-end clamps never end the
   gesture.
3. A rapid second press arrives as `ActionDoubleClick`: answer it like `ActionClick`
   (re-grab), never swallow it.
4. Emphasis derives via `ui.HandleStateFrom(hovering, dragging)` — intensity modulation on
   the existing theme keys, no new keys.

## Wheel boundaries (required for every new scrollable surface)

Trackpad and Magic Mouse flicks emit hundreds of inertial wheel events. Bubble Tea
repaints all of Sidecar after every accepted one, so clamping an offset during
`Update` is too late — the freeze happens before the clamp helps. `tea.WithFilter(app.FilterInput)`
asks one read-only question *before* `Update` and `View`:

> Would this exact wheel event change the surface currently under the pointer?

**Rule: every new scrollable surface or modal must provide exact pre-update
bounds, or explicitly declare why its answer is unknown.** "Unknown" is a valid,
safe answer — guessing is not. Return `true` only when the event is a certain
no-op.

How to comply:

1. Implement `plugin.WheelBoundaryConsumer` on the plugin
   (`WheelAtBoundary(tea.MouseWheelMsg) bool`) and add
   `var _ plugin.WheelBoundaryConsumer = (*Plugin)(nil)`.
2. Mirror `handleMouseScroll`'s routing exactly — same hit map, same modal
   precedence — but load nothing, move nothing, render nothing.
3. Derive the maximum from the same helper the renderer clamps with
   (`internal/scroll.Bounds`), never a second copy of the arithmetic.
4. Declarative modals answer for themselves via
   `modal.WheelAtBoundary(msg, handler)`; the host only owns precedence between
   a modal, a nested overlay, and a custom scrolling child.
   Call `Invalidate()` when content or geometry changes so a stale layout
   answers unknown instead of wrong.
5. Return `false` (unknown) for: embedded models you do not own, tmux panes with
   mouse reporting, scrollback with unloaded history, lazy lists that can load
   more, and anything before its first trustworthy render.
6. Declare the surface's policy in `assembly.WheelBoundaryRegistry`
   (`covered` / `externally-owned` / `deprecated-exclusion`). A new plugin
   without a row fails the assembly tests; a new `ModalKind` without a row fails
   `TestEveryModalKindHasALedgerRow` in `internal/app`.
7. Prove it with the shared stress fixture `internal/scroll/scrolltest`:
   `scrolltest.Run(t, scrolltest.Tail{...})` feeds hundreds of same-direction
   events and one reverse event, with no sleeps.

Background: `docs/plans/active/scroll-inertia-complete-coverage.md`.

## Wheel burst coalescing (required for every new scrollable surface)

Boundary drop alone is half the protection. A flick that never reaches a boundary
— mid-range inertia over a long card — still delivers one event per notch, and
each accepted one is an `Update` + `View` repaint. `tty.WheelBurst` /
`tty.WheelBursts` (`internal/tty/wheel.go`) coalesce a flick into whole flushes:
"how much of this burst has the surface earned" lives in that one place, so a
flick travels the same distance on every surface.

**Rule: every new scrollable content area applies wheel deltas through the shared
burst guard and drops at boundaries — both, not either.**

How to comply:

1. Hold one `tty.WheelBurst` per scroll surface. A host with one surface embeds
   the value in whatever struct owns it (`internal/overview/preview.go`,
   workspace `issuePane`); a host with several uses `tty.WheelBursts` keyed per
   leaf/region (Files tree + preview, app content deck).
2. Apply through `Add(delta, now)`; when `ok` is false the event was held, change
   nothing, and return early. The held delta rides the next flush — never apply
   `delta` directly.
3. Inject the clock for tests: a `wheelNow func() time.Time` field (Files), the
   plugin clock (`p.now()`), or a Model hook (`notificationCentreNow`). Tests
   drive a whole flick without sleeping — see
   `internal/plugins/filebrowser/scroll_burst_test.go` and the issue-viewer
   equivalents beside each host.
4. Reset the burst wherever the boundary answer is true, so inertia dropped at
   the top or bottom cannot spend itself into the next gesture. Crossing
   surfaces with `WheelBursts.For` resets automatically.
5. Keyboard scrolling does not coalesce; do not route keys through the burst.

Reference adoptions: embedded terminals (`internal/tty/tty.go`), Files tree and
preview (`internal/plugins/filebrowser`), workspace terminal + issue panes,
overview terminal + issue preview, app content deck + notification centre +
issue preview modal.

## Mouse Support

### Setup

```go
type Plugin struct {
    mouseHandler *mouse.Handler
}
func New() *Plugin {
    return &Plugin{mouseHandler: mouse.NewHandler()}
}
```

### Register hit regions during render

```go
func (p *Plugin) View(width, height int) string {
    p.mouseHandler.Clear()
    p.mouseHandler.HitMap.AddRect("pane", 0, 0, width, height, nil)
    p.mouseHandler.HitMap.AddRect("item", 2, 5, width-4, 1, 0)
    return content
}
```

### Region ordering (critical)

Regions tested in reverse order. Add general regions first, specific regions last.

## Pane header controls (internal/ui + internal/panereposition)

A pane header's right edge carries two controls: the layout button `⊞` (U+229E) and the close `×`. Both are drawn through `ui.ResolveButtonStyle` with the same one-cell padding, so a pane header never invents a third button look, and both are gated on the `pane_move` feature for the layout button's half.

**Reserve, do not measure.** `ui.ReserveHeaderControls(width, controls ...HeaderControl)` returns the tab strip's usable width and each control's column in one call; `panereposition.ReserveMovableHeader(width, movable, hasClose)` is the pane-side wrapper. Each host binds it once per frame in its own `reserveHeader`/`composeHeader` pair (`workspace.Plugin`, `overview.Model`, `app.appContentDeck`) so its header renderer, its tab strips and its region sink all measure from one answer — a strip laid out for a different reserve than the header composes is how a tab click lands on the wrong tab.

**`movable` comes from the tree, via `panereposition.Movable`: it is false with no tree and false for a tree of one leaf.** `PlanMove` refuses every destination on a single leaf, so a control there is a target the user aims at for nothing, and a header with no leaf at all used to compare hover against leaf `0` — which every un-hovered header matches — and paint a permanently hovered button. `ui.ReserveHeaderClose` remains a one-line compatibility wrapper for headers that carry only the `×`. The arithmetic assumes a **one-column glyph** and the test suite pins `ansi.StringWidth` of the rendered label; a wider glyph silently shifts every hit region on the row.

**Drop order as the row narrows: the layout button goes first, the close `×` last.** A control is dropped all-or-nothing. A half-drawn control is a target whose meaning cannot be recovered, and the close button is the one a user cannot work around.

**The `Layout` region rung is after `Title` and before `Close`.** `paneframe.RegionSink` registers `Layout(node *panelayout.Node, hit Box)` at that rung for the same reason `RegisterRegions` documents for the close button, one step earlier: regions are tested in reverse order, so the later-registered `Close` wins the cell it actually occupies while `Layout` still outranks the title strip underneath it. All three pane hosts implement it beside their close-region binding, with the same hover tracking.

The button opens `panereposition.Controller` — the same modal `M` opens. See `.claude/skills/keyboard-shortcuts/SKILL.md` for the key and its target resolution, and `.claude/skills/drag-pane/SKILL.md` for where the region sits in the windowing model.

### Coordinate system

App offsets Y by `headerHeight` (the single painted header row) before forwarding to plugins. Plugins operate in local coords where Y=0 is plugin content top.

### Common patterns

- Click to select/focus, scroll wheel to move, double-click to open
- Drag regions for pane resizing
- Hover for visual feedback (focus takes precedence)

### Mouse troubleshooting

| Symptom | Fix |
|---------|-----|
| Clicks don't register | Check region order (pane first) |
| Y offsets wrong | Account for borders, padding, headers |
| Scroll over items broken | Include item regions in scroll routing |
| Double-click fails | Ensure consistent region ID/bounds |
| Drag broken | Call StartDrag on click, check DragRegion during drag |
