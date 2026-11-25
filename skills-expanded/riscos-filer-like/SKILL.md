---
name: riscos-filer-like
description: Create, review, or extend a RISC OS filer-like window interface: a Wimp window that presents selectable objects in a grid or list, redraws items on demand, supports alternate view formats, hit-testing, scrolling, and window resizing around object geometry. Use when building a file browser, media browser, picker, launcher, or any object-view modelled on the desktop Filer without needing to clone the real Filer protocol.
metadata:
  author: gerph@gerph.org
license: MIT
---
# RISC OS filer-like interfaces

Use this skill when the task is to build or reason about a Filer-style object browser in a Wimp window.

This skill is about the UI structure and behaviour of a filer-like view, not about the desktop Filer message protocol itself.

# Public references

* Wimp PRM chapter: `http://www.riscos.com/support/developers/prm/wimp.html`
* Use the `riscos-wimp` skill alongside this one for Wimp event-loop, redraw, nested-window, and user-message rules.

# Core model

Treat a filer-like view as three layers:

* an object model: items, metadata, selection, highlight, sort order, and view state
* a geometry model: item width, item height, spacing, columns, rows, and visible area
* a Wimp shell: one window whose extent, open position, redraw path, and input routing are derived from the first two layers

Keep these layers separate. Most regressions come from mixing item metadata, drawing code, and Wimp geometry updates into one path.

# Read this reference

Read `references/design.md` before changing behaviour. It covers:

* item and window geometry
* redraw and hit-testing
* selection and highlight state
* multiple view formats
* resizing and scrolling
* review traps

Then read only the next layer you need:

* `references/wimp-structure.md`: how to map the filer-like model onto Wimp windows, poll events, redraw handlers, and per-item invalidation
* `references/plotting.md`: text, sprite, colour, and overlay plotting conventions for object cells, with routing to `riscos-output` when lower-level graphics detail is needed
* `references/filesystem-integration.md`: how to populate a filer-like model from a real filesystem, keep it sortable, and decide what should be cached or refreshed

# Default workflow

1. Identify the item model: what one object is, what metadata is shown, and which states affect appearance.
2. Define the geometry model before writing redraw code.
3. Decide how many view formats exist and which metadata each one exposes.
4. Make hit-testing and redraw use the same geometry rules.
5. Make window extent and open-state updates derive from item count, columns, and spacing rather than from ad hoc coordinates.
6. Add focused redraw paths for one item, visible region, and full relayout.
7. Only then wire in keyboard and mouse navigation.

# Optional implementation patterns

These are optional patterns seen in real filer-like interfaces. They are not the canonical design for this UI shape, but they are useful techniques to consider when the problem matches.

* keep redraw registration state in a separate helper object that stores pointers to the live layout metrics such as item count, column count, item width, and item height, so relayout can update shared state without having to recreate the redraw handler
* distinguish between cell advance and painted width when detailed views have a small icon-and-label region plus extra metadata columns; this makes it possible to keep grid stepping stable while still supporting narrower single-item redraws
* snap the visible window width to an integer number of object cells after relayout if the interface should avoid partially visible trailing columns
* treat transient menu selection separately from persistent selection so menu clicks can temporarily expose object actions without committing normal selection state
* model a root view and derived child views separately when a filer-like browser can open subwindows for the selected object set; key child views by stable object identity rather than raw item index, and rebind them after resort or refresh

Use these as design options, not requirements. If a pattern only solves a quirk of one application, keep it out of the core model.

# Review workflow

Check these first:

* redraw code and hit-testing disagree about item bounds
* column count or row count is derived differently in layout and redraw paths
* item-size or view-format changes recreate windows without restoring focus or nested-window state
* selection, highlight, and shaded states are coupled so tightly that one visual change breaks another
* scrolling logic does not guarantee the focused item becomes visible
* width calculations are based on stale text metrics or only the first few items
* large redraws repaint the whole extent when only a visible subset is needed
* implementation-specific workarounds have leaked into the main geometry model instead of being isolated as optional or temporary behaviour
