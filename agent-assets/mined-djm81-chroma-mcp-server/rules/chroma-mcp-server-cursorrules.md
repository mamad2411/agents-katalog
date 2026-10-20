# .cursorrules

## General rules to follow in Cursor

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

<available_instructions>
Cursor rules are user provided instructions for the AI to follow to help work with the codebase.
They may or may not be relevent to the task at hand. If they are, use the fetch_rules tool to fetch the full rule.
Some rules may be automatically attached to the conversation if the user attaches a file that matches the rule's glob, and wont need to be fetched.

markdown-rules: This rule helps to avoid markdown linting errors
python-github-rules: Development rules for python code and modules
</available_instructions>

## Note: Detailed rule instructions are auto-attached from the .cursor/rules directory
