---
name: charm-tui
license: CC-BY-4.0
description: >-
  Build terminal user interfaces with the Go Charm ecosystem (Bubbletea v2,
  Bubbles v2, Lip Gloss v2, Fang v2). Use when creating TUI applications,
  adding interactive terminal components, styling terminal output, building
  CLI tools with polished help screens, or when the user asks about
  Bubbletea, Bubbles, Lip Gloss, or Fang. Also trigger when reviewing or
  refactoring existing Charm-based code.
compatibility: >-
  Requires Go 1.26+ for the latest set (bubbletea v2.0.10, bubbles v2.2.1,
  lipgloss v2.0.6, fang v2.0.1, teatest v2 pseudo-version
  v2.0.0-20260927004216-9c77d672503d); checked 2026-09-29. Pinning
  bubbletea <= v2.0.9 allows Go 1.25.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Charm TUI Skill

Build correct, idiomatic terminal UIs with the Charm ecosystem.

---

## Import Paths — Anti-Hallucination Guard

> **WARNING:** Bubbletea, Bubbles, Lip Gloss, and Fang v2 moved to the `charm.land`
> vanity domain. **Do NOT use** `github.com/charmbracelet/{bubbletea,bubbles,lipgloss,fang}`
> — those are v0/v1. **Exception:** teatest v2 lives at
> `github.com/charmbracelet/x/exp/teatest/v2` (there is no `charm.land` teatest).

| Library         | Correct v2 Import Path                        |
|-----------------|-----------------------------------------------|
| Bubbletea       | `charm.land/bubbletea/v2`                     |
| Bubbles         | `charm.land/bubbles/v2/<name>`                |
| Lip Gloss       | `charm.land/lipgloss/v2`                      |
| Fang            | `charm.land/fang/v2`                          |
| teatest         | `github.com/charmbracelet/x/exp/teatest/v2`   |

Always alias bubbletea: `tea "charm.land/bubbletea/v2"`.

**Verify canonical API:** if the project's `go.mod` pins other versions or a symbol
differs from these references, check `go doc charm.land/bubbletea/v2 <Symbol>` (or
pkg.go.dev) instead of trusting the references. Do not silently upgrade the user's modules.

---

## Quick Start — Counter App

```go
package main

import (
	"fmt"
	"os"

	tea "charm.land/bubbletea/v2"
)

type model struct {
	count int
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch msg.String() {
		case "up", "k":
			m.count++
		case "down", "j":
			m.count--
		case "ctrl+c", "q":
			return m, tea.Quit  // tea.Quit — no parentheses
		}
	}
	return m, nil
}

func (m model) View() tea.View {
	s := fmt.Sprintf("Count: %d\n\nup/k: increment • down/j: decrement • q: quit\n", m.count)
	return tea.NewView(s)
}

func main() {
	if _, err := tea.NewProgram(model{}).Run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

Key v2 patterns shown:
- `Init() tea.Cmd` — returns nil for no startup command
- `Update(tea.Msg) (tea.Model, tea.Cmd)` — type-switch on message
- `View() tea.View` — returns `tea.NewView(string)`, **not** a raw string
- `tea.Quit` — the function reference itself, **no parentheses**
- `tea.KeyPressMsg` — v2 key-press type (`tea.KeyMsg` is an interface matching press and release)
- `msg.String()` — easiest way to match key combinations like `"ctrl+c"`

---

## Core Concepts

### The Elm Architecture (Init / Update / View)
Every Bubbletea program is a Model implementing three methods. Init runs once at startup. Update handles every incoming message and returns a (possibly mutated) model plus an optional async Cmd. View renders the current state to a string, then wraps it in `tea.NewView()`.
→ See [references/architecture.rst](references/architecture.rst) for the full lifecycle, message types, and Cmd functions.

### Messages and Commands
`tea.Msg` is any event: key press, window resize, timer tick, HTTP response. `tea.Cmd` is an async I/O function (`func() tea.Msg`) that runs off the main loop and delivers its result as a message. Never block in Update — use a Cmd instead.
→ See [references/architecture.rst](references/architecture.rst)

### Bubbles Components
Bubbles provides ready-made components (textinput, list, table, viewport, spinner, progress, filepicker, help, and more). Each is an embeddable Model with its own `Update`/`View`. You delegate to them in your parent Update.
→ See [references/components.rst](references/components.rst) for all 14+ components with exact signatures.

### Lip Gloss Styling
Lip Gloss styles are **immutable** — every method returns a new Style. Chain calls, then call `.Render(text)` at the end. Use `lipgloss.Color("hex")` or named constants for colors.
→ See [references/styling.rst](references/styling.rst)

### Layout Composition
`lipgloss.JoinHorizontal` and `lipgloss.JoinVertical` place rendered string blocks side-by-side or stacked. `lipgloss.Place` centers content in a bounding box.
→ See [references/layout.rst](references/layout.rst)

### Composition Patterns
Three approaches for multi-component TUIs: flat (single model, state enum), model-stack (child models as struct fields), hybrid (stack + mode enum). Focus management uses Tab/Shift-Tab cycling.
→ See [references/patterns.rst](references/patterns.rst)

### Testing
`teatest` provides `NewTestModel`, `WaitFor`, and `RequireEqualOutput` for golden-file testing. VHS records `.tape` scripts for visual regression.
→ See [references/testing.rst](references/testing.rst)

### Fang CLI Polish
Fang wraps a Cobra command with styled help, errors, man pages, and shell completions via `fang.Execute(ctx, cobraCmd, opts...)`.
→ See [references/fang.rst](references/fang.rst)

---

## Guidelines

1. **Implement all three methods.** A model missing `Init`, `Update`, or `View` will not compile.
2. **Handle `tea.WindowSizeMsg`.** Store `width` and `height` in your model; recalculate layouts in `View`. Hardcoded dimensions break on resize.
3. **Handle quit keys.** Always include `case "ctrl+c"` (at minimum) → `return m, tea.Quit`.
4. **Use `tea.Quit` without parentheses.** It is a `tea.Cmd` value (a function reference). `tea.Quit()` calls the function and returns a `Msg`, which is wrong.
5. **Use Lip Gloss, not raw ANSI escape codes.** ANSI codes break on terminals without colour support and prevent adaptive theming.
6. **Prefer Bubbles over hand-rolling.** The built-in textinput, list, viewport, etc. handle edge cases (cursor, wrap, filtering) that custom implementations miss.
7. **Delegate child updates.** In parent `Update`, call `child, cmd = child.Update(msg)` and reassign the child field. Forgetting the reassignment is a silent bug.
8. **Use `tea.Batch` for multiple Cmds.** `return m, tea.Batch(cmd1, cmd2)` — never start goroutines manually.
9. **Use `tea.Sequence` for ordered Cmds.** When Cmd B depends on Cmd A completing first.
10. **Set `v.AltScreen = true` in `View()`.** In v2, alt screen is declared on the View struct, not via `tea.WithAltScreen()` in `NewProgram`.
11. **Use `tea.NewView(s)` in View().** The `View()` method returns `tea.View`, not `string`. `tea.NewView(s)` is the constructor.
12. **Match keys with `msg.String()`.** Returns human-readable strings like `"ctrl+c"`, `"shift+enter"`, `"space"` (not `" "`).

---

## Avoid Common Errors

| Anti-Pattern | Correct Pattern |
|---|---|
| `github.com/charmbracelet/bubbletea` | `charm.land/bubbletea/v2` |
| `return m, tea.Quit()` (parens) | `return m, tea.Quit` (no parens) |
| `View() string` | `View() tea.View` |
| `return tea.NewView(s)` (string) → `return s` | Always return `tea.NewView(s)` |
| `case " ":` for space | `case "space":` |
| `case tea.KeyMsg:` for key presses (in v2 an interface matching press and release) | `case tea.KeyPressMsg:` |
| `tea.WithAltScreen()` in NewProgram | `v.AltScreen = true` in View() |
| Blocking I/O in Update | Return a `tea.Cmd` for async I/O |
| Raw goroutines | `tea.Cmd` functions |
| Calling `.Update()` without reassigning | `m.child, cmd = m.child.Update(msg)` |
| Inventing method names | Check [references/components.rst](references/components.rst) |

---

## Reference Files

| File | Contents |
|------|----------|
| [references/architecture.rst](references/architecture.rst) | Model interface, Program lifecycle, all Msg/Cmd types |
| [references/components.rst](references/components.rst) | All 14+ Bubbles components — constructors, fields, methods |
| [references/styling.rst](references/styling.rst) | Lip Gloss Style API, colors, borders, text attributes |
| [references/layout.rst](references/layout.rst) | JoinHorizontal/Vertical, Place, responsive patterns |
| [references/patterns.rst](references/patterns.rst) | Composition strategies, focus management, error handling |
| [references/testing.rst](references/testing.rst) | teatest, golden files, VHS tape scripts |
| [references/fang.rst](references/fang.rst) | Fang v2 + Cobra CLI polish |
| [references/recipes.rst](references/recipes.rst) | 5 complete runnable examples with output mockups |
