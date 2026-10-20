---
description: 
globs: *.py
alwaysApply: false
---
# Rule: Testing and Build Guidelines

**Description:** This rule provides essential instructions for testing and building the project correctly, avoiding common pitfalls with test environment management.

## Testing Guidelines

### Always Use Hatch Test Command

Standard tests should **always** be run via the built-in Hatch `test` command, not directly with pytest or custom wrappers:

```bash
# Run all tests (default matrix, quiet)
hatch test

# Run tests with coverage report (via run-cov alias)
# Select a specific Python version (e.g., Python 3.10):
hatch -e hatch-test.py3.10 run run-cov

# Generate HTML coverage report (via run-html alias)
# Select a specific Python version (e.g., Python 3.10):
hatch -e hatch-test.py3.10 run run-html

# Run tests for a specific Python version only
hatch test --python 3.10

# Combine options and target specific paths
hatch test --cover --python 3.12 tests/tools/
```

### Run tests with automated workflow capture (via run-autocapture alias)

```bash
# Run tests with coverage report and verbose output automatically captured under the hood
hatch test --cover -v

# Check for completed test transitions
hatch run chroma-mcp-client check-test-transitions --workspace-dir .

# Clean up processed test artifacts (specific to the completed workflow file)
hatch run chroma-mcp-client cleanup-test-artifacts `<path/to/test_workflow_complete_TIMESTAMP.json>`
# Note: the `<path/to/test_workflow_complete_TIMESTAMP.json>` is the path to the test workflow complete file, which is created by the `run-autocapture` alias and needs to be provided as an argument to the `cleanup-test-artifacts` command

# Or to clean up all completed workflows at once:
find logs/tests/workflows -type f -name 'test_workflow_complete_*.json' -exec \
  hatch run chroma-mcp-client cleanup-test-artifacts {} \
  ;
```

### Automated Test-Driven Learning

The `--auto-capture-workflow` flag enables the automated test-driven learning system which:

1. Automatically captures test failures with context
2. Monitors for transitions from failure to success after code changes
3. Creates validation evidence linking failures, fixes, and chat history
4. Promotes high-quality fixes to derived learnings

**Setup required before first use:**

```bash
chroma-mcp-client setup-test-workflow --workspace-dir .
```

After running tests with fixes, check for completed workflows:

```bash
chroma-mcp-client check-test-transitions --workspace-dir .
```

For complete details, see the [Automated Test Workflow Guide](../../docs/usage/automated_test_workflow.md).

**Note:** The `--auto-capture-workflow` behavior is automatically applied on all `hatch test`, `run-cov`, and `cov` invocations, so a separate `run-autocapture` alias is no longer necessary.

### Avoid Direct pytest Usage

❌ **Incorrect:**

```bash
python -m pytest tests/
```

✅ **Correct:**

```bash
hatch test
```

Using Hatch ensures:

- The proper Python matrix is used
- Dependencies are correctly resolved
- Environment variables are properly set
- Coverage reports are correctly generated

## Build Guidelines

Build the package using either:

```bash
# Using the provided script (cleans first, being deprecated from 0.3.0 onwards)
./scripts/build.sh

# Or with Hatch directly (recommended)
hatch build
```

This generates the distributable files in the `dist/` directory.

**Development Scripts:** Script aliases such as `build-mcp`, `publish-mcp`, and others are provided only when you install the `devtools` extra. Install via:

```bash
pip install chroma-mcp-server[devtools]
```

Or enable devtools in Hatch by adding `features = ["devtools"]` to your environment settings.

## Installing for IDE and CLI Usage

After modifying and testing the MCP server package, you need to rebuild and install it in the Hatch environment for the changes to take effect in Cursor (or any other IDE) or when using the `chroma-mcp-client` CLI:

### Full Version (with AI models for embeddings)

Use this approach when you need all embedding models available and have configured them in `mcp.json` or `.env`:

```bash
# Replace <version> with the actual version built (e.g., 0.2.7)
hatch build && hatch run pip uninstall chroma-mcp-server -y && hatch run pip install 'dist/chroma_mcp_server-<version>-py3-none-any.whl[full,dev]'
```

### Smaller Version (default embeddings only)

Use this lighter approach for faster installation with only fast and accurate embedding variants:

```bash
# Replace <version> with the actual version built (e.g., 0.2.7)
hatch build && hatch run pip uninstall chroma-mcp-server -y && hatch run pip install 'dist/chroma_mcp_server-<version>-py3-none-any.whl[client,dev]'
```

Please note, that for the MCP to be updated within the IDE, ask the user to manually reload the MCP server as there is no automated way available as of now, before continuing to try to talk to the updated MCP via tools call.

## Development Environment

Remember to activate the Hatch environment before making changes:

```bash
# Using the script (deprecated from 0.3.0 on)
./scripts/develop.sh

# Or directly with Hatch (recommended)
hatch shell
```

## Release Guidelines

When preparing a new release or updating the version:

1. **Update CHANGELOG.md** with the new version information:
   - Add a new section at the top after the `# Changelog` header with the next block of lines, but before the first `## [version] - TIMESTAMP` entry with the new version number and date
   - Document all significant changes under "Added", "Fixed", "Changed", or "Removed" sections
   - Use clear, concise language to describe each change

    ```markdown
    ## [0.2.x] - YYYY-MM-DD

    **Added:**
    - New feature description

    **Fixed:**
    - Bug fix description

    **Changed:**
    - Change description
    ```

2. Ensure the version number is updated in `pyproject.toml`
3. Build the package and verify the correct version appears in the build artifacts
4. Test the new version to ensure all changes worComplete Documentation

For comprehensive instructions, refer to the [Developer Guide](../../docs/developer_guide.md).
