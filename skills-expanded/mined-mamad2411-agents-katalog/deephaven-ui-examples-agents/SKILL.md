# Agent Instructions

This file provides guidance for AI coding agents working on this repository.

## Repository Overview

This repository contains example applications and custom components built with [deephaven.ui](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui), a Python framework for building reactive user interfaces in Deephaven.

## Project Structure

```
deephaven-ui-examples/
├── README.md                 # Project documentation
├── AGENTS.md                 # This file - agent instructions
├── PLAN.md                   # Project scaffolding plan
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── requirements-dev.txt      # Development dependencies
├── setup.sh                  # Setup script
├── pytest.ini                # Pytest configuration
├── scripts/
│   ├── start_server.py       # Start Deephaven server
│   └── run_example.py        # Run a specific example
├── tests/
│   ├── conftest.py           # Shared pytest fixtures
│   └── e2e/
│       └── conftest.py       # Playwright fixtures
└── examples/
    └── example-name/
        ├── PLAN.md           # Design plan (create FIRST before coding)
        ├── README.md         # Usage instructions and screenshots
        ├── app.py            # Main example code
        ├── __init__.py       # Package init
        ├── unit/             # Unit tests for this example
        │   └── test_unit.py  # Use unique names to avoid conflicts
        └── e2e/              # E2E tests for this example
            └── test_*.py
```

## Creating a New Example

When creating a new example, follow this workflow:

1. **Create the example folder**: `examples/example-name/`
2. **Create PLAN.md FIRST**: Outline what we're building before writing code
3. **Implement the example**: Write the Python code
4. **Create README.md**: Document usage, include screenshots if possible
5. **Update root README.md**: Add the example to the examples table

### PLAN.md Template

```markdown
# Example Name

## Goal

What are we trying to demonstrate or build?

## Features

- Feature 1
- Feature 2

## Implementation Details

- Key technical decisions
- Components to create
- Data sources needed

## UI Layout

Description or ASCII mockup of the intended layout

## Dependencies

Any special dependencies or Deephaven features required
```

### Example README.md Template

```markdown
# Example Name

Brief description of what this example demonstrates.

## Screenshot

![Screenshot](screenshot.png)

## Features

- Feature 1
- Feature 2

## Usage

\`\`\`python
exec(open('/data/examples/example-name/main.py').read())
\`\`\`

## How It Works

Explanation of the key concepts demonstrated.
```

## Key Conventions

### Custom Components

- Custom components are defined using the `@ui.component` decorator
- Component functions should have clear type hints for parameters
- Follow the pattern:

```python
from deephaven import ui

@ui.component
def component_name(param: type) -> ui.Element:
    """Brief description of the component.

    Args:
        param: Description of the parameter.

    Returns:
        A UI element displaying...
    """
    # Component logic here
    return ui.element(...)
```

### Code Style

- Use Python type hints
- Include docstrings for components explaining their purpose and parameters
- Follow PEP 8 style guidelines
- Use snake_case for file names and function names
- Use kebab-case for folder names

## Maintenance Tasks

When making changes to this repository:

1. **Update README.md** - Keep the examples table and contents current
2. **Update AGENTS.md** - Add new directories/files to the project structure
3. **Document new components** - Add docstrings and update relevant documentation
4. **Create PLAN.md first** - Always plan before implementing a new example

## Running Code During Development

When iterating on example code with a running Deephaven server, **prefer using the Deephaven MCP tools** over restarting the server:

1. **Use `mcp_deephaven_vs__runCodeFromUri`** to execute updated Python files directly on the running server
2. This allows you to make changes to `app.py`, run the code, and see changes immediately without restarting
3. After running updated code, refresh the iframe in the browser to see the changes

Example workflow:
1. Start the server: `python scripts/run_example.py example-name`
2. Open the iframe URL in the browser
3. Make code changes to `app.py`
4. Run the updated code using `mcp_deephaven_vs__runCodeFromUri` with the file URI
5. Refresh the iframe to see changes

This is much faster than restarting the server for each change.

## Running Tests

### Unit Tests

Unit tests can be run directly:

```bash
python -m pytest examples/example-name/unit/ -v
```

### E2E Tests

**IMPORTANT: Always run e2e tests in a background terminal.** E2E tests require a running Deephaven server. If you run e2e tests in a foreground terminal, it will block and potentially kill the server process that was started for manual testing.

**NEVER run `sleep` commands in the foreground terminal.** Running `sleep` will kill any running server or test process. If you need to wait for output, use `get_terminal_output` to check on background processes instead.

```bash
# Start the server first (in a separate terminal or background)
python scripts/run_example.py example-name

# Run e2e tests in a BACKGROUND terminal
DH_PSK=<psk_from_server_output> python -m pytest examples/example-name/e2e/ -v
```

The PSK (pre-shared key) is displayed in the server output when it starts.

## Viewing Demos

When opening a link to view an example demo in the browser, **always use the iframe/widget URL pattern** instead of the main Deephaven UI URL:

```
http://localhost:10000/iframe/widget/?name=WIDGET_NAME&psk=PSK
```

- `WIDGET_NAME` is the variable name of the widget exported in `app.py` (e.g., `chart_builder_demo`)
- `PSK` is the pre-shared key shown in the server output

For example, for chart-builder:

- ✅ Correct: `http://localhost:10000/iframe/widget/?name=chart_builder_demo&psk=ABC123`
- ❌ Incorrect: `http://localhost:10000/?psk=ABC123`

The iframe/widget URL directly displays the widget without the Deephaven IDE chrome, providing a cleaner view for demos.

## Resources

- [deephaven.ui Documentation](https://deephaven.io/core/docs/how-to-guides/user-interface/overview/)
- [deephaven.ui GitHub](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui)
- [deephaven.ui GitHub](https://github.com/deephaven/deephaven-plugins/tree/main/plugins/ui)
