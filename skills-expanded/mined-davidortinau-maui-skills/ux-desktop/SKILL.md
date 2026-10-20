---
name: ux-desktop
description: "Apply medium-specific UX reasoning for DESKTOP applications (mouse/trackpad plus keyboard, large screen, multi-window). Use alongside ux-first-principles when the target is a desktop app (Windows, macOS, or Linux; native or web-in-a-window) and the decision is affected by input precision, information density, hover, multi-window behavior, or keyboard operation. USE FOR: 'design a desktop app screen', 'lay out this desktop dashboard', 'what should the desktop layout be', pointer-and-keyboard UI, hover affordances, dense data views, resizable and multi-window layouts. DO NOT USE FOR: the invariant principles (use ux-first-principles); phone or tablet layouts (use ux-mobile or ux-tablet); picking colors, fonts, or platform chrome (use a styling/execution skill)."
---

# UX for Desktop

This skill is a thin medium layer. The reasoning (hierarchy, cognitive load, Gestalt, heuristics, accessibility) lives in `ux-first-principles`; read that first or alongside. Here is only what the desktop *medium* changes about applying it — driven by the body-to-device interface, not by which OS it is.

## What defines the desktop medium
A precise pointer (mouse/trackpad), a hardware keyboard, a large high-resolution display viewed at ~50–70cm, and the assumption that your app is one of several windows the user has open and will resize. These four facts change six things.

## The six things that change

1. **Target sizing.** The cursor is effectively a single point and does not occlude its target, so desktop tolerates small, dense controls (toolbar buttons, menu items, compact rows) that would be untappable on touch. You can exploit screen edges and corners as "infinite" targets: the cursor stops at the edge, so a control flush against it is trivially easy to hit (classic menu-bar and corner placements). Spend this density budget on power, not on cramming.

2. **Hover exists — and you can rely on it.** Desktop has a third state between idle and click: hover. Tooltips, hover-reveal controls, previews, and cursor changes are all legitimate and valuable here. Use hover for progressive disclosure of secondary information and affordances. (This is the single biggest thing that does NOT port to touch — see ux-tablet / ux-mobile.)

3. **Information density can be high.** Large screen + precise pointer + close viewing distance means desktop users can scan dense layouts: multi-column data grids, persistent sidebars and inspectors, smaller type, more visible at once. Higher density is a feature here, not clutter — provided hierarchy and grouping (see compositional reference) keep it organized. Keep text line length readable (~50–75 characters) even when width is plentiful.

4. **Multi-window and resize resilience.** Assume the app runs beside others and gets resized to arbitrary dimensions. Layouts must stay usable from narrow to very wide. Secondary windows, palettes, inspectors, and detached panels are available and often better than cramming everything into one surface. Design for "works at 600px wide and at 2400px wide," not one fixed size.

5. **Pointer precision unlocks richer interactions.** Right-click context menus, hover-preview, fine drag-selection, multi-select with modifier keys, resizable columns, and drag-and-drop are all first-class on desktop. Lean on them for efficiency — but never make them the *only* path to an action; provide a visible alternative.

6. **Keyboard is a primary input, not an accessibility afterthought.** Desktop users expect keyboard shortcuts, tab-order navigation, type-ahead, and full keyboard operability. This doubles as accessibility (WCAG Operable). Define a logical focus order, a visible focus indicator, and accelerators for frequent actions (Nielsen #7, Shneiderman #2).

## How principles shift on desktop
- **Fitts's Law:** small targets are fine; edges/corners are powerful; primary actions still deserve prominence.
- **Hick's Law:** you can afford to show more choices at once than on mobile, because scanning a large precise display is cheap — but don't confuse "can" with "should."
- **Progressive disclosure:** hover and side-panels are your disclosure tools; you rarely need to hide things behind a second screen.
- **Recognition over recall:** persistent sidebars/inspectors keep more in view, reducing recall load.

## Render-time platform handoff (NOT design decisions)
The following are mechanical, per-platform substitutions, not things to reason about from principles. In .NET MAUI and similar native frameworks they are largely handled at render time. Do them in styling, not in design:
- Exact control sizing and metrics (e.g., platform-default button heights), system fonts, corner radii, and elevation/material conventions.
- Window chrome, traffic-light vs. min/max/close button placement, menu-bar vs. in-window menu conventions.
- OS-global behaviors: respect the platform's window-management and standard shortcuts (copy/paste, quit, close-window) rather than reinventing them.

**Everything else — including structural choices like sidebar vs. top-nav, modal vs. inspector panel, and how deep the navigation goes — is a design decision. Reason it from first principles and commit to ONE answer that works across desktop platforms. Do not fork the structure per OS.**

## Deliberate scope note
This optimizes for a coherent cross-platform product over maximal single-OS idiomaticity. That is the right trade-off for cross-platform app work. The only case where it bites is an app whose entire value proposition is feeling 100% hand-built-native on one specific OS — a positioning choice, not a correctness issue.
