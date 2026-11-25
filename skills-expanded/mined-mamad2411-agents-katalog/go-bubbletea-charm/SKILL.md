---
name: go-bubbletea-charm
description: Use when building Go TUIs with Bubble Tea, lipgloss, and bubbles — MVC update loop, models, messages, performance, charm ecosystem.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [go-essentials, go-concurrency, go-cobra, go-testing]
---

# Go Bubble Tea / charm

**Iron Law: `Update` returns a new model and a `tea.Cmd` — never mutate the receiver, never block, never start a goroutine outside a `tea.Cmd`. Every long operation is a command that emits a message.**

**Versions:** Current `bubbletea v1.x` · `lipgloss v1.x` · `bubbles v0.x` · No LTS series — _charm libraries follow semver but iterate fast. Pin minor versions; expect breaking changes in pre-1.0 deps like bubbles._

## The Elm-style loop (what makes Bubble Tea click)

```go
type model struct{ count int; quitting bool }

func (m model) Init() tea.Cmd { return nil }                          // optional startup cmd

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q": m.quitting = true; return m, tea.Quit
        case "+":           m.count++
        case "-":           m.count--
        }
    case tickMsg:
        return m, tickEvery()                                          // schedule next tick
    }
    return m, nil
}

func (m model) View() string {
    if m.quitting { return "" }                                        // empty view = clean exit
    return fmt.Sprintf("count: %d  (+/- to change, q to quit)\n", m.count)
}

p := tea.NewProgram(model{}, tea.WithAltScreen())
if _, err := p.Run(); err != nil { log.Fatal(err) }
```

`Update` is **pure**. State changes go through the returned model. Side effects (I/O, timers, HTTP) go through `tea.Cmd` — functions that return a `tea.Msg` later.

## Messages and commands

```go
type fetchedMsg struct{ data []byte; err error }

func fetch(url string) tea.Cmd {
    return func() tea.Msg {                                            // runs in its own goroutine
        resp, err := http.Get(url)
        if err != nil { return fetchedMsg{err: err} }
        defer resp.Body.Close()
        b, _ := io.ReadAll(resp.Body)
        return fetchedMsg{data: b}
    }
}

// in Update:
case tea.KeyMsg:
    if msg.String() == "r" { return m, fetch("https://api.example.com") }
case fetchedMsg:
    if msg.err != nil { m.err = msg.err; return m, nil }
    m.body = string(msg.data); return m, nil
```

**Never call `time.Sleep`, `http.Get`, or any blocking call inside `Update`.** It freezes the UI. Wrap it in a `tea.Cmd`. Combine commands with `tea.Batch(cmd1, cmd2)` or run them in sequence with `tea.Sequence(...)`.

## Composable models (lift state up)

```go
type model struct {
    list     list.Model         // bubbles/list
    input    textinput.Model    // bubbles/textinput
    focused  int                // 0 = list, 1 = input
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    if m.focused == 0 {
        m.list, cmd = m.list.Update(msg)
    } else {
        m.input, cmd = m.input.Update(msg)
    }
    return m, cmd
}
```

Each sub-model owns its own `Update`. The parent dispatches based on focus, and threads the returned `tea.Cmd` back up. Don't reach into a sub-model's fields — its API is the message contract.

## lipgloss styling

```go
var (
    titleStyle = lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("#FAFAFA")).
        Background(lipgloss.Color("#7D56F4")).
        Padding(0, 1)
    boxStyle = lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("#874BFD")).
        Padding(1, 2)
)

view := lipgloss.JoinVertical(lipgloss.Left,
    titleStyle.Render("myapp"),
    boxStyle.Render(body),
)
```

`lipgloss.Place` (vertical/horizontal alignment in a fixed area), `JoinHorizontal`/`JoinVertical` for layouts. **Render once, reuse.** Style structs are immutable — `.Foreground(...)` returns a new value, the original is unchanged.

## bubbles components worth knowing

| Component    | Use                                                                |
| ------------ | ------------------------------------------------------------------ |
| `textinput`  | single-line input with cursor, completion hooks                    |
| `textarea`   | multi-line editor                                                  |
| `viewport`   | scrollable region for long content (log tail, markdown view)       |
| `list`       | navigable list with filtering, paging                              |
| `table`      | tabular data with selection                                        |
| `spinner`    | indeterminate progress (combine with a `tea.Cmd` driving the work) |
| `progress`   | determinate progress bar (gradient via lipgloss)                   |
| `paginator`  | page-N-of-M indicator                                              |
| `help`       | auto-generated key-binding help (driven by a `key.Map`)            |
| `filepicker` | file/dir browser                                                   |

For very long output use `viewport` — rendering 10k lines per frame is what causes flicker.

## Performance — the only rules you need

- **Don't re-render in `View` unless you have to.** `View` is called on every message; keep it cheap. Pre-compute styled strings, cache static segments.
- **Guard expensive work in `Update`.** A `tea.KeyMsg` arrives ~30/sec when held; don't kick off an HTTP request per keystroke. Debounce with a `tea.Tick`.
- **Use `tea.Batch` for parallel cmds.** Two fetches at once: `return m, tea.Batch(fetch(a), fetch(b))` — both run concurrently.
- **Use `tea.Sequence` for ordered cmds.** Animation A then animation B.
- **Alt-screen mode** (`tea.WithAltScreen`) is required for full-screen TUIs — without it the terminal scrollback gets polluted.
- **Inline mode** (default) is right for ephemeral pickers (`gum confirm`-style) — finishes, leaves no trace.

## Exit codes and clean teardown

```go
finalModel, err := p.Run()
if err != nil { fmt.Fprintln(os.Stderr, err); os.Exit(1) }
m := finalModel.(model)
if m.aborted { os.Exit(130) }                                          // SIGINT convention
```

`tea.Quit` ends the program loop. The last `View()` is rendered (in alt-screen mode it's wiped on exit — render an empty string to avoid a stray banner). For SIGINT propagation: Bubble Tea wires `ctrl+c` to `tea.Quit` by default; intercept it explicitly if you need confirm-on-quit.

## The wider charm ecosystem

| Library        | Use                                                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **bubbletea**  | the runtime                                                                                                            |
| **lipgloss**   | styles + layouts                                                                                                       |
| **bubbles**    | reusable components                                                                                                    |
| **huh**        | form library — drop-in for surveys, wizards; integrates with Bubble Tea via `huh.NewForm(...).WithProgramOptions(...)` |
| **gum**        | shell-callable TUI primitives (`gum confirm`, `gum spinner`) — for shell scripts, not Go programs                      |
| **glamour**    | terminal markdown renderer (good for README previews inside a TUI)                                                     |
| **vhs**        | record TUI demos as GIF/MP4 from a `.tape` script — invaluable for TUI docs                                            |
| **wish**       | SSH-served TUIs (run your Bubble Tea program as a remote shell)                                                        |
| **soft-serve** | self-hosted git over wish                                                                                              |

## Anti-patterns

- Calling `time.Sleep`, `http.Get`, file I/O inside `Update` — freezes UI; wrap in `tea.Cmd`
- Spawning a raw `go func()` from `Update` — escapes the message loop, races against state
- Mutating pointer fields on the receiver model — Bubble Tea expects value semantics; use the returned model
- One giant `Update` switching on dozens of message types — split into sub-models with their own update loops
- Rendering wide content without measuring — `lipgloss.Width(s)` to size dynamically; otherwise borders wrap mid-cell
- Using stdout for logs in a TUI — corrupts the screen; pipe `slog` to a file or use `tea.Printf` for in-program lines
- Forgetting `tea.WithAltScreen()` for full-screen apps — scrollback pollution on exit
- Hard-coded colors without `lipgloss.AdaptiveColor` — looks unreadable on opposite-mode terminals

## Red flags

| Thought                          | Reality                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------ |
| "It freezes when I press Enter"  | You called a blocking function in `Update`; wrap it in `tea.Cmd`                     |
| "The UI is slow on big lists"    | You're rendering all rows in `View`; use `viewport` or `list` with paging            |
| "It works in iTerm but not tmux" | Color support detection — declare profile explicitly with `lipgloss.SetColorProfile` |
| "I'll log to stdout for now"     | Stdout IS the screen in a TUI; use stderr or a file                                  |

## Hand-off

For Cobra subcommands that launch a Bubble Tea program: `Skill(go-cobra)`. For background goroutines wired through `tea.Cmd` (errgroup, cancellation): `Skill(go-concurrency)`. For testing message-loop logic: `Skill(go-testing)`. For Go idioms, error wrapping, modules: `Skill(go-essentials)`.
