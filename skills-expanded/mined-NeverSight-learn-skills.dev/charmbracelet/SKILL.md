---
name: charmbracelet
description: Build Go terminal user interfaces and interactive CLIs with the Charmbracelet ecosystem, especially Bubble Tea, Bubbles, Huh, Lip Gloss, Wish, Glamour, and Log. Use this skill when the user asks for a TUI, terminal UI, interactive CLI, Bubble Tea model/update/view code, Bubbles widgets, Huh forms, Lip Gloss layout or styling, Wish SSH apps, Glamour markdown rendering, or a polished Go terminal app.
version: 1.0.0
source: local
license: MIT
---

Use this skill to build modern Go CLIs with the Charmbracelet stack. Default to Bubble Tea for any stateful TUI or interactive terminal flow, then layer in Bubbles, Huh, Lip Gloss, Wish, Glamour, and Log as needed.

## Start Here

- Use `charm.land/.../v2` imports for the current v2 ecosystem.
- Treat Bubble Tea as the app runtime and state machine.
- Treat Bubbles as reusable widgets, not the app shell.
- Treat Lip Gloss as layout and styling.
- Treat Huh as the fastest way to build forms and wizards.
- Treat Glamour as markdown-to-ANSI rendering.
- Treat Log as diagnostics to `stderr` or files, not to the TUI surface.
- Treat Wish as the SSH transport layer for remote terminal apps.

## When To Reach For Which Library

| Need | Use |
|---|---|
| Full TUI, app state, key handling, message loop | `references/bubbletea-core.md` |
| Real app architecture, commands, child models, async patterns | `references/bubbletea-patterns.md` |
| Reusable widgets like `list`, `table`, `textinput`, `viewport`, `help` | `references/bubbles.md` |
| Forms, prompts, wizards, embedded form screens | `references/huh.md` |
| Styling, spacing, borders, color, layout composition | `references/lipgloss.md` |
| SSH-native TUI or remote CLI app | `references/wish.md` |
| Markdown help panes, docs, release notes, previews | `references/glamour.md` |
| Structured CLI logging and diagnostics | `references/log.md` |
| High-level library chooser and API map | `references/api-surface.md` |
| Concrete implementation recipes | `references/common-use-cases.md` |
| Migration issues and footguns | `references/troubleshooting-workarounds.md` |
| Upstream example shortlist | `references/examples.md` |

## Default Build Strategy

1. Start with Bubble Tea when the user asks for a TUI, terminal UI, dashboard, picker, wizard, or interactive CLI.
2. Add Bubbles instead of rebuilding common widgets by hand.
3. Add Lip Gloss once layout or visual hierarchy matters.
4. Add Huh when the interaction is form-heavy.
5. Add Glamour when the app renders markdown content.
6. Add Log for diagnostics, background jobs, or server logs.
7. Add Wish only when the app should run over SSH.

## Core Rules

- Keep business logic separate from the Bubble Tea model.
- Do I/O in `tea.Cmd`, not directly in `Update` or `View`.
- Handle resize with `tea.WindowSizeMsg` and keep layouts responsive.
- Request background color with `tea.RequestBackgroundColor` when styles depend on light/dark mode.
- In Bubble Tea v2, declare terminal behavior in `tea.View` fields like `AltScreen` and `MouseMode`.
- In standalone Lip Gloss or Glamour output, print with Lip Gloss writers so color downsampling works.
- In Wish apps, remember middleware runs in reverse declaration order.
- In Bubble Tea apps, write logs to `stderr` or a file, not to stdout.

## Bubble Tea First Skeleton

```go
package main

import tea "charm.land/bubbletea/v2"

type model struct{}

func (m model) Init() tea.Cmd {
    return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyPressMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        }
    }
    return m, nil
}

func (m model) View() tea.View {
    v := tea.NewView("Hello from Bubble Tea")
    return v
}
```

## Read These Next

- Read `references/bubbletea-core.md` for Bubble Tea's model, commands, messages, and program lifecycle.
- Read `references/bubbletea-patterns.md` for app structure, async work, Cobra integration, and multi-model composition.
- Read `references/troubleshooting-workarounds.md` before migrating old Charmbracelet code or mixing stale examples with v2 code.
