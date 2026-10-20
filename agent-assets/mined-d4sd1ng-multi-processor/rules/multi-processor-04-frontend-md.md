---
name: Atomizer Frontend Rules
globs: ["**/*.html", "**/*.css", "**/*.js", "**/frontend/**/*", "**/control_panel*"]
alwaysApply: false
description: Rules for the Bootstrap Atomizer Control Panel.
---

# Atomizer Frontend Rules

The Atomizer frontend is not a classic dashboard.

It is a compact Bootstrap Control Panel for guided work.

## Core UI rules

- Use Bootstrap.
- Do not use Streamlit.
- Do not build a full-screen admin dashboard.
- Do not create a table-heavy technical view as the main interface.
- Do not create multiple large dashboard sections.
- Use exactly one central display field.
- The displayed content changes based on the selected workflow step.
- The start view must fit on one screen without scrolling in normal desktop layout.

## Required workflow

The user must always see the red thread:

1. Eingang
2. Assets
3. Review
4. Übergabe
5. Abschluss

The process bar must be horizontal.

Show clearly:

- current step
- completed steps
- locked steps
- next action
- open reviews
- ready handoffs
- blocked assets
- errors

## Layout structure

Everything must be inside one main Bootstrap card.

Do not place loose controls below the panel.

The panel must contain:

- header
- compact navigation
- run actions
- horizontal process bar
- status strip
- next action area
- one central display field
- optional detail/collapse/modal controls

## Navigation

Use compact navigation:

- Start
- Review
- Assets
- Übergabe
- Fehler

Do not place navigation as loose browser-default buttons.

## Run controls

Run controls must not dominate the start view.

Use:

- `Run wählen`
- `Neuer Run`

as buttons in the panel header or navigation area.

Run selection and new-run forms must be inside:

- modal
- collapse
- or the central display field after selection

Never leave run-management controls visibly floating under the panel.

## Buttons

Use Bootstrap button classes.

Examples:

- primary action: `btn btn-primary`
- secondary action: `btn btn-outline-secondary`
- warning/review: `btn btn-warning`
- danger/block: `btn btn-danger`
- success/ready: `btn btn-success`
- details: `btn btn-link`

Do not use unstyled browser-default buttons.

## Main interaction rule

Every state must show:

1. Status
2. Short explanation
3. One obvious next action
4. Secondary actions only when needed

Examples:

- Review open => `Jetzt prüfen`
- Ready for creator => `Handoff anzeigen` or `Für Creator kopieren`
- Blocked => `Problem anzeigen`
- No run selected => `Run wählen` or `Neuen Run starten`

## Central display field

The central display field shows only one context at a time:

- Start summary
- Current review item
- Asset list
- Handoff package
- Error detail
- Run selection
- New run form
- Source references
- Problem detail

Do not show all contexts at once.

## Technical details

Technical details are secondary.

Show them only through:

- Details
- Quellen
- Problem anzeigen
- Erweitert

Do not make Run IDs, atoms, raw JSON, model calls or logs dominant in the main UI.

## Hard prohibitions

- No publishing button.
- No auto-publish action.
- No TXT export.
- No CSV export.
- No duplicate backend logic.
- No duplicate export logic.
- No separate storage logic.
- No charts unless explicitly requested later.
- No large monitoring view.

## Visual acceptance criteria

The page is unacceptable if:

- Bootstrap styling is not visible.
- Buttons look like browser defaults.
- process steps are vertical.
- controls are outside the main card.
- run selection is visible below the panel.
- the start view requires scrolling.
- more than one main content area is visible.
- the user cannot identify the next action immediately.
