---
name: voyager-test
description: Run pytest suites for Voyager SDK components targeting Axelera AI hardware. Use when the user wants to execute unit tests, integration tests, or coverage reports. Not for testing a model on a video or camera; use voyager-run for that.
argument-hint: "[scope: all|unit|runtime|module|file]"
allowed-tools: Read, Bash, Glob, Grep, Task, mcp__voyager__*
---

# Run Tests

Execute tests for Voyager SDK components targeting Axelera AI hardware

## Instructions

Run tests based on the specified scope: **$ARGUMENTS**

{{INCLUDE common/voyager-sdk-setup.md}}

{{INCLUDE common/voyager-task-integration.md}}

### Step 1: Environment Setup

- Read `.voyager-runtime.json` before choosing tests:
  - `package_for_linux`: run host-safe static/unit checks only and report that
    hardware/runtime tests were not executed.
  - `execute_on_device`: hardware/runtime tests may run when the SDK and device
    are visible.
- The setup include (Step 0/Step 3) activates the SDK environment
  (`venv/` or `axelera-env/`); verify with `python -c "import axelera"`.
- Test configuration lives in the SDK's `pyproject.toml` under
  `[tool.pytest.ini_options]` (testpaths: `tests`, `internal_tools_tests`,
  `run_tests.py`). Plain `pytest` from the SDK root uses those paths.
- Install optional pytest plugins (`pytest-cov`, `pytest-xdist`, `pytest-html`, `pytest-random-order`)
  only when the user approves environment mutation.

### Step 2: Test Scope Identification

Parse test scope from arguments:

- `all`: Run all tests
- `unit`: Run unit tests only
- `runtime`: Run runtime-specific tests
- `<module>`: Run tests for specific module
- `<file>`: Run specific test file
- `<pattern>`: Run tests matching pattern

### Step 3: Running Tests with Pytest

This is the canonical flow; the SDK has no tox configuration.

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_axelera_config.py

# Run specific test function
pytest tests/test_axelera_config.py::test_function_name

# Run tests matching pattern
pytest tests/ -k "config"
pytest tests/ -k "network and not slow"

# Run with verbose output
pytest tests/ -v

# Run with very verbose output (show locals)
pytest tests/ -vv
```

### Step 4: Coverage Reports

```bash
# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term

# View HTML coverage report
xdg-open htmlcov/index.html

# Coverage for specific module
pytest tests/ --cov=axelera/app --cov-report=term-missing
```

### Step 5: Test Categories

**Core SDK Tests:**

```bash
pytest tests/test_axelera_config.py      # Configuration
pytest tests/test_axelera_network.py     # Network handling
pytest tests/test_axelera_pipeline.py    # Pipeline operations
pytest tests/test_axelera_compile.py     # Compilation
```

**Display/UI Tests:**

```bash
pytest tests/test_axelera_display.py
pytest tests/test_axelera_display_cv.py
pytest tests/test_axelera_display_console.py
```

**Operator Tests:**

```bash
pytest tests/test_ax_operator.py
pytest tests/test_axelera_operators_inference.py
```

**Model Tests:**

```bash
pytest tests/test_ax_models_base_torch.py
pytest tests/test_ax_models_decoders_yolo.py
pytest tests/test_ax_models_decoders_ssd.py
```

**Metadata Tests:**

```bash
pytest tests/test_ax_meta.py
pytest tests/test_axelera_meta_base.py
pytest tests/test_axelera_meta_gst.py
```

### Step 6: Code Quality Checks

The SDK configures `black`, `isort`, and `ruff` in `pyproject.toml`. Run them
directly from the SDK root so those settings apply:

```bash
# Format check (no changes written)
black --check .
isort --check-only .

# Auto-format code
black .
isort .

# Lint
ruff check .
```

### Step 7: Running Specific Test Patterns

```bash
# Tests for a specific feature
pytest tests/ -k "yaml"
pytest tests/ -k "decoder"
pytest tests/ -k "stream"

# Exclude slow tests
pytest tests/ -k "not slow"

# Only failed tests from last run
pytest tests/ --lf

# Run last failures first, then the rest
pytest tests/ --ff
```

### Step 8: Debugging Failed Tests

```bash
# Stop on first failure
pytest tests/ -x

# Enter debugger on failure
pytest tests/ --pdb

# Show local variables in tracebacks
pytest tests/ -l

# Capture stdout/stderr
pytest tests/ -s
```

### Step 9: Parallel Test Execution

```bash
# Run tests in parallel (requires pytest-xdist)
pytest tests/ -n auto
pytest tests/ -n 4  # Use 4 workers
```

### Step 10: Test Output and Reporting

```bash
# JUnit XML report (for CI)
pytest tests/ --junitxml=results.xml

# HTML report
pytest tests/ --html=report.html

# Detailed test durations
pytest tests/ --durations=10
```

### Step 11: Common Test Issues

**Import errors:**

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$AXELERA_FRAMEWORK:$PYTHONPATH
```

**Missing dependencies:**

Activate the SDK virtual environment (`source venv/bin/activate`); it carries
the SDK's test dependencies. Add optional pytest plugins only with user
approval.

**Runtime-specific tests failing:**

Runtime tests need an activated venv on a Voyager SDK host with visible
hardware; skip and report them in `package_for_linux` mode.

**Test isolation issues:**

```bash
# Run tests in random order
pytest tests/ --random-order
```

### Step 12: Writing New Tests

When adding new tests:

- Place in `tests/` directory
- Follow naming: `test_<module>.py`
- Use descriptive test function names: `test_<feature>_<scenario>`
- Add appropriate markers for slow/integration tests
- Include both positive and negative test cases

### Step 13: Final Report

Always report:

- Exact suite/command and exit status
- Runtime mode from `.voyager-runtime.json`
- Hardware-dependent tests run or skipped
- Logs, reports, or coverage artifacts produced
- Residual validation gaps before claiming Metis readiness

## Parallel Orchestration

See `common/agent-orchestration.md` for the full lane rules. For this skill:

- Suites that never touch the Metis device may run in parallel, either as
  separate lanes or via `pytest-xdist` (`pytest tests/ -n auto`).
- Device-touching tests run serially in a single lane; exactly one process may
  use the device at a time.
- Parallelize report parsing and coverage summarization after runs finish.
