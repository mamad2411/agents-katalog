# .windsurfrules

## General rules to follow

- When starting a new chat session, capture the current timestamp from the client system using the `run_terminal_cmd` tool with `date "+%Y-%m-%d %H:%M:%S %z"` to ensure accurate timestamps are used in logs, commits, and other time-sensitive operations.
- When starting a new chat session, get familiar with the build and test guide (refer to docs/rules/testing-and-build-guide.md).
- When starting a new task, first check which markdown plan we are currently working on (see docs/refactoring/README.md for more details). In case of doubt, ask the user for clarification on which plan to follow in current session.
- After any code changes, follow these steps in order:
  1. Apply linting and formatting to ensure code quality
  2. If changes involve the MCP server or client components, rebuild and reinstall:

     ```bash
     hatch build && hatch run pip uninstall chroma-mcp-server -y && hatch run pip install 'dist/chroma_mcp_server-<version>-py3-none-any.whl[client,dev]'
     ```

     (Replace `<version>` with the actual version number)
  3. Run tests with coverage using the test script:

     ```bash
     ./scripts/test.sh -c -v
     ```

     You can also run tests for specific files or modules:

     ```bash
     ./scripts/test.sh -c -v tests/tools/test_auto_log_chat_bridge.py
     ```

     Or target a specific Python version:

     ```bash
     ./scripts/test.sh -c -v --python 3.11 tests/tools/
     ```

     To automatically track test failures and transitions for validation evidence:

     ```bash
     ./scripts/test.sh -c -v --auto-capture-workflow
     ```

  4. Verify all tests pass and coverage meets or exceeds 80%
  5. Fix any issues and repeat steps 1-4 until all tests pass
  6. For MCP server changes, remind the user to manually reload the MCP server in their IDE before continuing with any MCP tools usage
- Maintain test coverage at >= 80% in total and cover all relevant code paths to avoid runtime errors and regressions.
- Always finish each output listing which rulesets have been applied in your implementation.

## Rules to apply based on file types

- For markdown files (`*.md`, `*.mdc`): Apply rules from `docs/rules/markdown-rules.md`
- For Python files (`*.py`): Apply rules from `docs/rules/python-github-rules.md`

## Always apply the following memory and logging rules

- Session memory management: See docs/rules/memory-integration-rules.md
- Automated chat logging: See docs/rules/auto_log_chat.md

## Note: Each of these rule files contains detailed instructions that should be followed
