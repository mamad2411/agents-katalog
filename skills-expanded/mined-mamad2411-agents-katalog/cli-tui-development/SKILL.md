---
name: cli-tui-development
description: Building CLI applications and Terminal User Interfaces (TUIs)
license: MIT
metadata:
  audience: developers
  category: development
---

# Skill: CLI/TUI Development

## What I do
- Build command-line interface (CLI) applications
- Create Terminal User Interface (TUI) applications
- Design interactive terminal experiences
- Structure CLI architecture with subcommands
- Handle user input, prompts, and interactive workflows

## When to use me
When building terminal-based applications, CLIs for tools/libraries, TUIs for data visualization, or interactive command-line tools.

## Key Concepts

### CLI vs TUI
- **CLI**: Command-line interface - text-based commands and arguments
- **TUI**: Terminal User Interface - interactive UI with widgets, menus, mouse support

### Architecture Patterns
```
CLI Structure:
├── main command
│   ├── subcommand --option <arg>
│   ├── subcommand --flag
│   └── subcommand <arg>

TUI Structure:
├── App
│   ├── Layout
│   │   ├── Header
│   │   ├── Sidebar
│   │   └── Content
│   └── Widgets
│       ├── Button
│       ├── Input
│       ├── List
│       └── Table
```

### Color & Styling
- ANSI escape codes for terminal colors
- 256-color palette support
- Truecolor (24-bit) for modern terminals
- Rich/Textual CSS-like styling

## Language Ecosystem

### Python
- **Textual**: Modern async TUI framework (built on Rich)
- **Rich**: Rich text output, tables, progress bars
- **Click**: CLI framework with decorators
- **Typer**: Type-hint based CLI (built on Click)
- **Curses/ncurses**: Low-level TUI (classic)

### JavaScript/TypeScript
- **Inquirer.js/@inquirer**: Interactive prompts
- **Commander.js**: CLI argument parsing
- **Yargs**: CLI builder with chains
- **Chalk**: Terminal string styling
- **oclif**: Heroku's CLI framework

### Rust
- **Ratatui**: Rust TUI library
- **Cursive**: Rust TUI framework
- **Clap**: CLI argument parsing
- **Bubble Tea**: Elm-inspired TUI (Golang)

### Go
- **Bubble Tea**: TUI framework
- **Cobra**: CLI framework
- **Lip Gloss**: Styled terminal output

## Best Practices

1. **Structure commands logically** - Use groups/subcommands
2. **Provide helpful output** - Rich formatting, tables, progress
3. **Handle errors gracefully** - Clear error messages
4. **Support shell completion** - Bash, Zsh, Fish, PowerShell
5. **Test CLI behavior** - Use testing utilities
6. **Cross-platform support** - Windows compatibility matters
7. **Respect terminal capabilities** - Detect color support

## Example Stack Choices

### Python TUI (Modern)
```bash
pip install textual rich
```

### Python CLI (Modern)
```bash
pip install typer rich
```

### JavaScript CLI
```bash
npm install @inquirer/prompts commander chalk
```
