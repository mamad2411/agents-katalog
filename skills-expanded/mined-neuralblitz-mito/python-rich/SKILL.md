---
name: python-rich
description: Creating beautiful terminal output with Python Rich library
license: MIT
metadata:
  audience: python-developers
  category: terminal-output
---

# Skill: Python Rich

## What I do
Create rich, formatted terminal output with Python Rich library - including colored text, tables, progress bars, syntax highlighting, and beautiful console applications.

## When to use me
When enhancing terminal output with colors, tables, progress bars, Markdown rendering, or building rich CLI applications without a full TUI framework.

## Installation
```bash
pip install rich
```

## Basic Usage

### Simple Colored Output
```python
from rich import print as rprint
from rich.console import Console
from rich.theme import Theme

console = Console()

# Simple colored text
rprint("[red]This is red[/red]")
rprint("[bold blue]Bold blue[/bold blue]")
rprint("[yellow on black]Yellow on black[/yellow on black]")

# Combinations
rprint("[bold][italic][underline]All styles[/underline][/italic][/bold]")
```

### Console Object
```python
from rich.console import Console

console = Console()

# Print with styling
console.print("Hello, World!", style="bold green")

# Different output streams
console_err = Console(stderr=True)  # For warnings/errors
console_err.print("[red]Error![/red]", stderr=True)

# Width control
console = Console(width=80)
console = Console(force_terminal=True)
```

## Color Reference

### Named Colors
```
black, red, green, yellow, blue, magenta, cyan, white
bright_black (gray), bright_red, bright_green, bright_yellow
bright_blue, bright_magenta, bright_cyan, bright_white
```

### RGB & Hex Colors
```python
from rich.color import Color

# RGB
console.print("[color(255,128,0)]Orange text[/color]")

# Hex
console.print("[#FF8800]Orange text[/#FF8800]")

# With Color class
color = Color.from_rgb(255, 128, 0)
console.print(f"[{color}]Orange text[/{color}]")
```

## Text Styles

| Style | Description |
|-------|-------------|
| `bold` | Bold text |
| `italic` | Italic text |
| `underline` | Underlined |
| `strike` | Strikethrough |
| `blink` | Blinking text |
| `reverse` | Reversed colors |
| `dim` | Dimmed text |
| `bold not dim` | Bold and not dim |

### Combinations
```python
console.print("[bold red]Bold Red[/bold red]")
console.print("[bold italic underline]All combined[/bold italic underline]")
```

## Tables

### Basic Table
```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Users")
table.add_column("Name", style="cyan", no_wrap=True)
table.add_column("Email", style="magenta")
table.add_column("Role", style="green")

table.add_row("Alice", "alice@example.com", "Admin")
table.add_row("Bob", "bob@example.com", "User")
table.add_row("Charlie", "charlie@example.com", "User")

console.print(table)
```

### Advanced Table
```python
from rich.table import Table

table = Table(
    title="Sales Report",
    show_header=True,
    header_style="bold magenta",
    border_style="bright_blue",
    row_styles=["", "dim"]
)

table.add_column("Product", justify="left")
table.add_column("Q1", justify="right")
table.add_column("Q2", justify="right")
table.add_column("Total", justify="right", style="bold green")

table.add_row("Widget A", "$10,000", "$12,000", "$22,000")
table.add_row("Widget B", "$8,000", "$9,500", "$17,500")
table.add_row("Widget C", "$15,000", "$14,000", "$29,000")

console.print(table)
```

## Progress Bars

### Simple Progress
```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("[cyan]Processing...", total=100)
    for i in range(100):
        progress.advance(task)
        # Do work...
```

### Multiple Tracks
```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    console=console
) as progress:
    
    task1 = progress.add_task("[red]Download", total=100)
    task2 = progress.add_task("[green]Process", total=100)
    
    for i in range(100):
        progress.advance(task1)
        if i % 2 == 0:
            progress.advance(task2)
```

### File Download Simulation
```python
from rich.progress import Progress, DownloadColumn, TransferSpeedColumn

with Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    DownloadColumn(),
    TransferSpeedColumn(),
    console=console
) as progress:
    task = progress.add_task("Download", total=1000000)
    for chunk in download_chunks():
        progress.advance(task, len(chunk))
```

## Syntax Highlighting

### Code Highlighting
```python
from rich.syntax import Syntax
from rich.console import Console

console = Console()

code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Result: {result}")
"""

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
```

### Themes
```
monokai, github-dark, dracula, nord, one-dark, vim, etc.
```

## Panels & Boxes

### Panels
```python
from rich.panel import Panel
from rich.text import Text

console = Console()

text = Text("Welcome to my application!", style="bold green")
panel = Panel(text, title="Info", border_style="blue")
console.print(panel)

# Without title
console.print(Panel("Simple panel", style="red"))
```

### Boxes
```python
from rich.box import Box, DOUBLE, ROUNDED

console.print(
    "Content in rounded box",
    box=ROUNDED,
    border_style="cyan"
)
```

## Tree View

```python
from rich.tree import Tree
from rich.console import Console

console = Console()

tree = Tree("📁 Project", guide_style="bold blue")

src = tree.add("📂 src", style="cyan")
src.add("📄 main.py")
src.add("📂 utils", style="green")
src.add("📄 helpers.py")

tests = tree.add("📂 tests", style="yellow")
tests.add("📄 test_main.py")

console.print(tree)
```

## Markdown Rendering

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()

md = """
# Heading 1
## Heading 2

This is **bold** and this is *italic*.

- List item 1
- List item 2

```python
print("code block")
```
"""

console.print(Markdown(md))
```

## Logging

```python
from rich.logging import RichHandler
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("myapp")
log.debug("Debug message")
log.info("Info message")
log.warning("Warning message")
log.error("Error message")
```

## Live Display

### Dynamic Updates
```python
from rich.live import Live
from rich.table import Table

with Live(build_table(), refresh_per_second=4) as live:
    for _ in range(10):
        # Update table
        live.update(build_table())
```

### Status Spinner
```python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn

console = Console()

with console.status("[bold green]Working on something..."):
    time.sleep(2)
    console.print("[green]Done!")
```

## Pretty Printing

### Dict/Object Pretty Print
```python
from rich.pretty import pprint
from rich.console import Console

console = Console()

data = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "JavaScript"],
    "active": True
}

pprint(data, console=console, expand_all=True)
```

## Bar Charts

```python
from rich.console import Console
from rich.bar import Bar

console = Console()

console.print(Bar(50, width=30, color="cyan"))
```

## Column Layout

```python
from rich.console import Console
from rich.columns import Columns

console = Console()

columns = Columns([
    "[bold]Name[/bold]\nAlice\nBob\nCharlie",
    "[bold]Role[/bold]\nAdmin\nUser\nUser"
], equal=True, expand=True)

console.print(columns)
```

## Best Practices

1. **Use Console object** for consistent styling
2. **Close tags properly** `[/red]` or use context manager
3. **Test terminal compatibility** - not all terminals support all styles
4. **Respect user preferences** - check `Console.options.no_color`
5. **Width matters** - use `console.width` for responsive layouts
6. **Combine with Click/Typer** for complete CLI applications
