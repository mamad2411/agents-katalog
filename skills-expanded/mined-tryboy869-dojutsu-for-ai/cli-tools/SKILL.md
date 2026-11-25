---
name: cli-tools
description: "Apply when building CLI tools, command-line interfaces, or scripts meant to be run in terminal. Covers: Click/Typer patterns, argument parsing, progress display, config files, distribution. Trigger for: CLI, command line, terminal, script, Click, Typer, argparse."
---

# CLI TOOLS — Production Patterns

## Typer (preferred — type-safe Click wrapper)
```python
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(help="Senjutsu CLI — Precision Absolute Coding Agent")
console = Console()

@app.command()
def run(
    task: str = typer.Argument(..., help="The development task to accomplish"),
    api_key: str = typer.Option(None, "--api-key", "-k",
                                envvar="GROQ_API_KEY", help="Groq API key"),
    provider: str = typer.Option("groq", "--provider", "-p",
                                 help="LLM provider: groq or openai"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Run the Precision Absolute pipeline on a task."""
    if not api_key:
        console.print("[red]Error: API key required (--api-key or GROQ_API_KEY)[/red]")
        raise typer.Exit(1)
    
    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as p:
        t = p.add_task("Running Byakugan analysis...")
        result = run_pipeline(task, api_key)
        p.remove_task(t)
    
    console.print(result.execution)

if __name__ == "__main__":
    app()
```

## Config File Pattern
```python
from pathlib import Path
import json

CONFIG_PATH = Path.home() / ".config" / "myapp" / "config.json"

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text())

def save_config(data: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))

@app.command()
def configure(api_key: str = typer.Option(..., prompt="Groq API Key")):
    """Save configuration."""
    save_config({"api_key": api_key})
    console.print("[green]✅ Config saved[/green]")
```

## Exit Codes (POSIX standard)
```python
# 0 = success
# 1 = general error
# 2 = misuse of command (wrong args)
raise typer.Exit(code=0)  # success
raise typer.Exit(code=1)  # error
```

## Output Rules
```python
# stdout = actual output (pipeable)
print(result.json())       # goes to stdout — can be piped

# stderr = status messages (don't pollute stdout)
console.print("[dim]Processing...[/dim]", stderr=True)

# Rich for interactive, plain text for scripts
if sys.stdout.isatty():
    console.print("[green]✅ Done[/green]")
else:
    print("done")  # plain text when piped
```

## Forbidden
❌ No `--help` documentation on args
❌ Mixing stdout/stderr (status to stdout breaks piping)
❌ No exit codes (caller can't detect failure)
❌ Config hardcoded in script (use config file or env vars)
❌ No `--dry-run` for destructive operations
