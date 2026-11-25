---
name: modal-or-page
description: "Use when deciding where a flow lives: modal, drawer, sheet, popover, inline expand, or full page - plus dismissal, focus return, and deep-linking."
---


# Where a Flow Lives

Default to a page and make the overlay argue for itself. A page is linkable, back-navigable and scrollable and needs no focus contract; every overlay borrows those properties and pays interest in dismissal rules, focus return, inertness, scroll locking and an invented URL. An overlay earns its place by clearing one of two bars — the context behind it is needed while the flow runs, or the flow is a single decision the user must answer now. This skill decides which container one flow gets and never designs the app's movement graph: tabs, sidebars, breadcrumbs, active state and back behavior are `navigation`, which names none of these six containers. Easing, duration and the enter/exit shape of each container are `motion`; this skill states no timing value.

**Use the overlay primitive the project already has.** Radix, Base UI, Headless UI, Vaul, shadcn/ui and the framework's own `<dialog>` each already implement the focus trap, inertness, scroll lock, Escape handling and portal ordering described below, and each exposes them differently. Detect and configure it; a hand-rolled `position: fixed` div with an `onClick` backdrop reimplements four accessibility contracts badly and silently. If the project has a routed-overlay convention (parallel routes, an intercepting route, a `?panel=` param), every new overlay follows it.

## Decision: pick the container

Cheapest first — stop at the first row that fits.

| Container | Choose it when | Blocks | Routed |
| --- | --- | --- | --- |
| Inline expand / in-place edit | The change is one field or one short list, and the surrounding content is the reference | no | no |
| Popover | A short anchored choice, no internal scroll, nothing lost on dismiss | no | no |
| Modal / dialog | One decision or one step that must be answered before continuing | yes | only if it holds a flow |
| Drawer (side) | A detail opened repeatedly while a list stays visible and operable | no | yes |
| Sheet (bottom) | The narrow-viewport form of a drawer or modal; `gestures` owns the drag physics | yes | yes |
| Full page | Multi-step, needs its own scroll or sub-navigation, or must be resumable | — | always |

Three questions settle it, in order. **Is the context behind it needed while the flow runs?** If no, page. **Will the user reload, share, or be bounced through auth mid-flow?** If yes, route it. **Does it fit without internal scroll and without a second step?** If no, page.

## Decision: dismissal per container

| Container | Escape | Backdrop click | Explicit close | Browser back |
| --- | --- | --- | --- | --- |
| Inline expand | collapses | collapses | optional | no |
| Popover / menu | closes | closes | none | no |
| Modal, clean | closes | closes | `×` | closes if routed |
| Modal, dirty | closes after confirming | disabled | `×` confirms | confirms |
| Drawer | closes | closes | `×` | closes |
| Sheet | closes | closes | swipe down | closes |
| Full page | nothing | nothing | none | leave-guard if dirty |

## Core Principles

1. **If it scrolls inside, it wanted to be a page.** An internal scrollbar creates two scroll contexts and pushes the header or footer buttons out of sight, so the user scrolls to find "Save". Modal content must fit at the smallest supported viewport height. Exception: when the scroll *is* the content rather than the flow — a terms body, or a picker whose search field sits above a result list.

2. **A modal holds one decision or one step.** The moment it grows a second step, a sub-tab, or its own back button, it is a page wearing a backdrop; move it to a route. Exception: a destructive confirm whose second step is only a re-type (`type DELETE to confirm`) — one decision, expressed twice on purpose.

3. **Overlays that hold a flow get a URL; overlays that hold a question do not.** Someone who reloads, shares a link, or returns from an auth bounce must land in the same place — but a URL that resurrects "Are you sure?" is a bug: the question has lost its context. Route modals, drawers and sheets holding a record, an editor or a flow (`/orders?inspect=8412`); never route menus, popovers, tooltips, toasts or confirms. Exception: route the container, not the draft — unsaved input is restored from local state.

4. **Never open a blocking layer from a blocking layer.** Two backdrops compound their dimming, Escape becomes ambiguous, and focus return has to unwind two hops. One blocking layer per screen: a modal needing a confirmation replaces its own content or becomes a page. Exception, exactly one: anchored non-blocking layers inside a modal — select, combobox, date picker, tooltip — each of which must close before the modal does.

5. **Outside-click dismissal is only allowed when nothing is lost.** Clicking the backdrop is a reflex, not a decision; pairing it with data loss means a misplaced click destroys work. While the container is dirty, disable backdrop dismissal and let Escape ask. Exception: a surface with real autosave — nothing is lost, so let it dismiss freely.

6. **Escape closes exactly one layer, and never submits.** Escape is a retreat, so it must be the smallest one available: an anchored popover inside a modal closes first, the modal on the second press. Exception: a deliberately blocking flow — a forced re-auth, a required legal acceptance — may ignore Escape, and must then show an explicit exit control; a layer with no way out is a trap.

7. **Focus opens on the first meaningful control and returns to the exact trigger.** Focus landing on the close button teaches keyboard users that leaving is the fastest thing the dialog offers; focus dumped on `<body>` sends the next Tab to the top of the document. On open, focus the first input or the primary action; on close, call `.focus()` on the trigger. Exception: a read-mostly container focuses itself so arrow keys scroll it. `a11y` owns trap mechanics, `inert` and announcements; this skill owns where focus starts and lands.

8. **When the trigger is gone, focus its successor, never the body.** Deleting a row from inside a drawer destroys the element focus was promised to. Fall back in a fixed order: next surviving sibling, then previous sibling, then the list container. Exception: if the collection is now empty, focus the empty state's primary action — which is why empty states need one.

9. **The narrow viewport promotes the container, it does not shrink it.** A desktop modal rendered at 375px with margins is a page with a decorative border and smaller tap targets. Modal becomes a full page or full-screen sheet, side drawer a bottom sheet, popover a sheet or an inline expansion. Exception: single-decision confirms stay alert dialogs at every width. `responsive` owns where the breakpoint is.

10. **If the user opens it repeatedly in a row, it is not a modal.** A modal forces an open/close cycle per item and hides the list being worked through: triaging twenty records costs forty transitions. Use a non-blocking drawer beside the list, with the list still clickable and arrow-key navigable and the drawer following the selection. Exception: when acting on the row mutates the collection — delete, merge, reassign — block deliberately, because the user should stop.

## Output Format

State the decision as a block, not a paragraph. One line each, no prose:

```
Container: drawer (right, non-blocking)
Because:   rows are inspected in sequence and the list must stay operable
Route:     /orders?inspect=8412  (replace, not push)
Dismissal: Escape, backdrop (clean only), close button, browser back
Focus:     opens on the first field; returns to the originating row, or the next surviving row
```

## Smells and Fixes

| Smell | Fix |
| --- | --- |
| Modal with an internal scrollbar, a sticky footer, or a "Next" button | It is a page; route it and give it real navigation |
| Confirmation opened on top of a modal | Replace the modal's content, or promote it to a page |
| Backdrop click discards a half-filled form | Disable outside-click while dirty; let Escape confirm |
| Reload loses the drawer's selection | The container needed a route |
| Reload reopens "Are you sure?" | Confirms are never routed |
| Escape closes the popover *and* its parent modal | Close only the topmost dismissible layer |
| Focus starts on the `×`, or Tab after closing jumps to the top of the page | Focus the first input on open; return focus to the trigger on close |
| Deleting a row leaves focus on `<body>` | Next surviving sibling, then the container |
| Desktop modal rendered at 375px with margins | Promote it: full page or full-screen sheet |

## Checklist

- [ ] The container is the cheapest row in the ladder that fits
- [ ] Nothing scrolls inside a modal; no modal has a second step
- [ ] Flow-bearing overlays are routed; questions and menus are not
- [ ] One blocking layer only; anchored layers inside it are the sole stack
- [ ] Outside-click dismissal is off whenever something would be lost
- [ ] Escape closes one layer, submits nothing; every blocking layer has a visible exit
- [ ] Focus opens on the first meaningful control, returns to the trigger or its successor
- [ ] The narrow viewport promotes the container rather than shrinking it
- [ ] Background is `inert`; scroll is locked without a layout jump
- [ ] The decision is written as the output block, route and focus target included
