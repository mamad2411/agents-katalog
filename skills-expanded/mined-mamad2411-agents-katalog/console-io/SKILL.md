# Console I/O Skill (Terminal UI Designer)

This skill provides reusable terminal UI components based on the visual style of the "Evolution of Todo" phase 1 application. It uses box-drawing characters and `rich` library for coloring.

## Usage

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

console = Console()

class ConsoleUI:
    @staticmethod
    def draw_banner():
        """Draw 'The Evolution of Todo' top banner."""
        banner_text = Text("The Evolution of Todo", justify="center", style="bold magenta")
        panel = Panel(banner_text, box=box.DOUBLE_EDGE, padding=(1, 3), expand=True)
        console.print(panel)
        console.print()

    @staticmethod
    def draw_header(title: str):
        """Draw a section header."""
        header_text = Text(title, justify="center", style="bold cyan")
        panel = Panel(header_text, box=box.DOUBLE_EDGE, padding=(0, 1))
        console.print(panel)

    @staticmethod
    def draw_menu(title: str, options: list, selected: int = 0):
        """Draw a numbered menu with highlights."""
        ConsoleUI.draw_header(title)
        console.print()
        for i, opt in enumerate(options):
            marker = "▶" if i == selected else " "
            style = "green bold" if i == selected else "white"
            console.print(f"  {marker} {i + 1}. {Text(opt, style=style)}")
        console.print()
        console.print(Text("↑/↓ to navigate  •  Enter to select  •  q to exit", style="dim"))

    @staticmethod
    def draw_tasks(tasks: list):
        """Draw task list in a table format."""
        table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
        table.add_column("#", style="bold", width=5)
        table.add_column("STATUS", style="bold", width=12)
        table.add_column("TASK", style="white")

        for task in tasks:
            status = Text("✓ DONE", style="green bold") if task.completed else Text("○ TODO", style="yellow bold")
            table.add_row(str(task.id), status, task.title)

        console.print(table)
```

## Implementation Rules
1. Always use `rich` for output.
2. Maintain the box-based visual hierarchy.
3. Use neon colors (Cyan, Magenta, Green, Yellow) for modern CLI look.
4. Header should always use `DOUBLE_EDGE` box.
