---
name: python-cli
description: "When to activate: Typer, Click, argparse, CLI applications, rich output, progress bars, configuration files"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python CLI Patterns

## Typer (Recommended)
```python
import typer
from typing import Annotated
from pathlib import Path
from rich.console import Console
from rich.progress import track

app = typer.Typer(help="My CLI tool", no_args_is_help=True)
console = Console()

@app.command()
def process(
    input_file: Annotated[Path, typer.Argument(help="Input file path")],
    output_dir: Annotated[Path, typer.Option("--out", "-o", help="Output directory")] = Path("."),
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
    workers: Annotated[int, typer.Option("--workers", "-w", min=1, max=32)] = 4,
) -> None:
    """Process input file and write results to output directory."""
    if not input_file.exists():
        console.print(f"[red]Error:[/red] File not found: {input_file}")
        raise typer.Exit(code=1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    items = list(input_file.read_text().splitlines())
    for item in track(items, description="Processing..."):
        result = do_work(item)
        (output_dir / f"{item}.json").write_text(result)
    
    console.print(f"[green]Done.[/green] Wrote {len(items)} files to {output_dir}")

# Sub-commands
@app.command("validate")
def validate_cmd(path: Path) -> None:
    """Validate the configuration."""
    ...

if __name__ == "__main__":
    app()
```

## Rich Output Patterns
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

def print_table(data: list[dict]) -> None:
    table = Table(title="Results", show_header=True, header_style="bold blue")
    table.add_column("Name", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Duration", justify="right")
    
    for row in data:
        status_style = "green" if row["status"] == "ok" else "red"
        table.add_row(
            row["name"],
            f"[{status_style}]{row['status']}[/{status_style}]",
            f"{row['duration']:.2f}s",
        )
    
    console.print(table)

# Error output goes to stderr
console.print("[red]Error:[/red] Something went wrong", style="bold", file=console.stderr)
```

## Configuration via Files
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
import tomllib

class CLIConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYTOOL_",
        env_file=".env",
    )
    
    api_url: str = "https://api.example.com"
    timeout: int = 30

def load_config(config_path: Path | None) -> CLIConfig:
    if config_path and config_path.exists():
        with open(config_path, "rb") as f:
            toml_data = tomllib.load(f)
        return CLIConfig(**toml_data.get("tool", {}).get("mytool", {}))
    return CLIConfig()
```
