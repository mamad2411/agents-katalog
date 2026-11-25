---
name: python-textual
description: Building modern TUIs with Python Textual framework
license: MIT
metadata:
  audience: python-developers
  category: tui-development
---

# Skill: Python Textual

## What I do
Build sophisticated Terminal User Interface (TUI) applications with Python Textual - a modern, async-powered framework for creating rich interactive terminal apps.

## When to use me
When building complex terminal UIs with widgets, layouts, animations, mouse support, and real-time updates. Ideal for dashboards, data viewers, editors, and interactive tools.

## Core Concepts

### Textual Architecture
```
App
├── Screen (one or more)
│   ├── CSS (styling)
│   └── Widgets (compose)
└── Reactive Variables (state)
```

### Installation
```bash
pip install textual rich
```

## Basic App Structure

### Minimal Textual App
```python
from textual.app import App, ComposeResult
from textual.widgets import Static

class MyApp(App):
    CSS = """
    Screen {
        background: dark;
        align: center middle;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Static("Hello, Textual!")

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

### With Widgets
```python
from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Log

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter your name")
        yield Button("Click me!")
        yield Log()

    def on_button_pressed(self) -> None:
        self.query_one(Log).write_line("Button clicked!")
```

## Widgets Library

### Common Widgets
| Widget | Purpose |
|--------|---------|
| `Static` | Display text |
| `Button` | Clickable buttons |
| `Input` | Text input field |
| `Checkbox` | Toggle options |
| `Select` | Dropdown selection |
| `Switch` | On/off toggle |
| `ListView` | Scrollable list |
| `DataTable` | Tabular data |
| `Tree` | Hierarchical data |
| `Tabs` | Tabbed interface |
| `Log` | Scrollable text log |
| `ProgressBar` | Progress indicator |
| `RichLog` | Rich-formatted log |
| `DirectoryTree` | File browser |
| `Pretty` | Pretty-printed data |

## Layout System

### Layout Modes
```python
# Horizontal layout
container.horizontal()

# Vertical layout  
container.vertical()

# Grid layout
container.grid(columns=3)

# Dock layout (edge placement)
header.dock("top")
sidebar.dock("left")
```

### Alignment & Sizing
```python
widget.align("center", "middle")  # horizontal, vertical
widget.overflow("hidden")         # scroll, hide, auto
widget.styles.width = "20"       # exact width
widget.styles.width = "50%"       # percentage
widget.styles.height = "auto"
```

## Styling (CSS)

### Inline CSS
```python
class MyWidget(Static):
    CSS = """
    MyWidget {
        background: $primary;
        color: white;
        padding: 2 4;
        border: solid $accent;
        border-radius: 4;
    }
    
    MyWidget:hover {
        background: $accent;
    }
    """
```

### Key CSS Properties
```
background: dark | #ff0000 | $variable
color: white | #00ff00 | $primary
padding: 1 2 3 4  (top right bottom left)
margin: 1 2 3 4
border: solid | dashed | none
border-radius: 0 4
align: center middle | left top | right bottom
width: 20 | 50% | auto
height: 3 | 10% | 1fr
```

### Color Variables
```python
app = MyApp()
app.colors驾()

CSS_VARIABLES = {
    "primary": "#0078D4",
    "secondary": "#6B6B6B", 
    "accent": "#FFB900",
    "background": "#1E1E1E",
    "text": "#FFFFFF"
}
```

## Reactive State

### Defining Reactive Variables
```python
from textual.reactive import reactive

class CounterApp(App):
    count = reactive(0)
    
    def compose(self) -> ComposeResult:
        yield Static(id="counter")
        yield Button("+", id="increment")
    
    def on_mount(self) -> None:
        self.update_counter()
    
    def watch_count(self) -> None:
        self.update_counter()
    
    def update_counter(self) -> None:
        self.query_one("#counter", Static).update(f"Count: {self.count}")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "increment":
            self.count += 1
```

## Events & Actions

### Event Handling
```python
def on_mount(self) -> None:        # App/widget mounted
def on_ready(self) -> None:         # Initial render complete
def on_unmount(self) -> None:      # App/widget removed

def on_key(self, event: Key) -> None:
    if event.key == "q":
        self.exit()
```

### Actions
```python
class MyApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+b", "toggle_sidebar", "Toggle Sidebar"),
    ]
    
    def action_quit(self) -> None:
        self.exit()
    
    def action_toggle_sidebar(self) -> None:
        # Toggle sidebar visibility
        pass
```

## Async Operations

### Async Methods
```python
async def fetch_data(self) -> None:
    self.query_one("#status", Static).update("Loading...")
    
    async with self.batch_update():
        # Batch UI updates
        data = await self.fetch_from_api()
        self.query_one("#data", DataTable).update(data)
    
    self.query_one("#status", Static).update("Done!")
```

## Key Methods

| Method | Purpose |
|--------|---------|
| `compose()` | Return widgets to display |
| `on_mount()` | Called when app/widget mounts |
| `watch_*()` | React to variable changes |
| `query_one()` | Find first matching widget |
| `query()` | Find all matching widgets |
| `push_screen()` | Navigate to screen |
| `screen_stack` | Current navigation stack |

## Running the App

```python
# Basic run
app.run()

# With options
app.run(title="My App", size=(80, 24))

# Test mode
async def test_my_app():
    async with MyApp().run_test() as pilot:
        await pilot.click("#button")
        assert pilot.app.query_one("#result").idle
```

## Textual CLI

```bash
# Run a textual app
textual run my_app.py

# Development mode with hot reload
textual run --dev my_app.py

# Serve app in browser
textual run --browser my_app.py
```

## Best Practices

1. **Use CSS classes** for reusable styles
2. **Batch updates** with `batch_update()` for performance
3. **Reactive variables** for state management
4. **Action methods** for keybindings
5. **Widget IDs** for reliable queries
6. **Async for I/O** operations
7. **Test with `run_test()`** for CI/CD
