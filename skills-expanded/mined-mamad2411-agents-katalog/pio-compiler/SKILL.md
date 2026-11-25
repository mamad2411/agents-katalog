# Project Rules for pio_compiler

## Installation
1. Ensure the `uv` tool is available on your system. If not, run:
   - macOS: `brew install uv`
   - Linux (with pip): `pipx install uv` or `pip install uv`
2. From the project root execute:
   ```bash
   bash install
   ```
   The script will create a local virtual environment using **uv** and install the package in editable mode with development extras.

## Running the CLI
After activating the environment (`source .venv/bin/activate`) or by relying on `uv run`, you can launch the CLI:
```bash
uv run poi-compiler [args]
```
(Currently the CLI only prints a placeholder message.)

## Linting (MANDATORY)
Linting must be executed frequently and is **required** before the project is considered finished.
Run:
```bash
bash lint
```
The script delegates to **uv run** to execute `ruff`, `black`, `isort`, and `pyright`.

## Testing
Execute the test-suite with:
```bash
bash test
```
This script invokes **uv run pytest** (parallel with xdist). All tests must pass before declaring completion.

• Tests that run longer than 5 seconds belong in `tests/unit`; shorter tests go in `tests/integration`.

### CLI Testing Convention
When writing *integration* or *end-to-end* tests for the command-line interface **always** invoke the *console-script* entry point, e.g.:

```bash
tpo tests/test_data/examples/Blink --native
```

Using the real shell command ensures that the packaging metadata (entry-points) remains correct and avoids brittle invocations such as `python -m pio_compiler.cli`.

• Do **not** build argument lists like `cmd_args: list[str]` for `subprocess.run`. Instead, supply the *entire* command line as a single **string** and execute it with `shell=True` if needed. This keeps the tests closer to how end-users will interact with the tool.

## Pre-finish checklist
Before marking a task as finished you **MUST** run:
```bash
bash lint
bash test
```
and ensure both commands exit successfully.

## Test-Driven Development (TDD)
- For every new piece of functionality, **write failing tests first** that capture the desired (idealised) public API or behaviour.
- Only after the tests are in place should you implement or modify code to make those tests pass.
- Iterate until the test-suite is green before moving on to new work.
