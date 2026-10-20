---
name: dev-cli-tool-developer
description: Guides the agent in developing interactive, user-friendly, and standard command-line interface (CLI) tools.
---

Develop CLI feature for: $ARGUMENTS

Follow these guidelines to design, implement, and verify command-line interfaces, scripts, and automation tools.

> **Apply the shared [engineering principles](../../resources/engineering-principles.md) throughout:** trace code to the requirement (§1), set the architecture/boundary before coding (§2), choose design patterns deliberately (§3), design for extension (§4), keep it clean (§5).

## Step 1: Design POSIX-Compliant Command Interface
Choose a reliable command-line parsing library (e.g., `clap`, `commander`, `click`).
1. **Commands & Subcommands**: Use hierarchical subcommands for different operations (e.g., `tool init`).
2. **Standard Flags**:
   * `-h`, `--help`: Automatically generate clear usage documentation.
   * `-v`, `--version`: Output the current tool version.
   * `-V`, `--verbose`: Enable debug logging.
   * Always provide long-form options (`--file`) for readability in scripts, alongside short-form (`-f`).
3. **Configuration Hierarchy**: Enforce precedence (highest to lowest):
   1. CLI Flags (`--port 8080`)
   2. Environment Variables (`APP_PORT=8080`)
   3. Local Config (`./.apprc`)
   4. User Config (`~/.config/app/config.json` via XDG Base Directory)
4. **Command hierarchy tree (MANDATORY — confirm before coding)**: Output the full command tree and present it via ask-user. Do NOT write implementation code until the user approves.
   ```
   tool
     init                     ← new
       --template <name>
       --force
     deploy                   ← new
       staging                ← new
         --dry-run
       production             ← new
         --confirm (required)
     config
       set <key> <value>      ← reuse existing ConfigService
       get <key>              ← reuse existing ConfigService
   ```
   Mark shared services (e.g., `ConfigService`, `Logger`) as `← reuse` so duplication is visible before code is written.

## Step 2: Input and Output Routing (Stdout vs. Stderr)
Always route console outputs correctly so that the tool integrates nicely with shell scripting (piping):
1. **Stdout (Standard Output)**: Output *only* the direct result of the command (e.g., database tables, query outputs, requested information).
2. **Stderr (Standard Error)**: Output logs, diagnostics, progress spinners, warnings, and error messages here. This ensures shell commands can filter outputs (e.g., `tool status > output.txt` will not save progress logs to the file).
3. **Stdin (Standard Input)**: When appropriate, allow the tool to accept input data from pipes (e.g., `cat input.json | tool parse`).

## Step 3: Terminal UX & Visuals
1. **ANSI Colors**: Use terminal colors to highlight critical status information. Use standard mappings:
   * **Green**: Successful operations.
   * **Red**: Failures and fatal errors.
   * **Yellow**: Warning or action-required alerts.
   * **Cyan/Blue**: Informational or active tasks.
2. **Spinners & Progress Bars**: For synchronous long-running operations, display an active spinner or progress indicator in stderr. Ensure the spinner is disabled when stdout is not a TTY (interactive terminal).
3. **Clean Tabular Data**: Format multi-row results into clean ASCII tables with well-aligned headers.

## Step 4: Exit Codes & Graceful Shutdown
1. **Signal Trapping**: Always listen for `SIGINT` (Ctrl+C) and `SIGTERM`. If received, stop accepting new tasks, release file locks, and close network sockets cleanly before exiting. Do not leave corrupted temporary files.
2. **Exit Codes**: Exit codes are critical for CI/CD pipelines. Never exit with `0` if an operation failed.
   * **`0`**: Command completed successfully.
   * **`1`**: General errors (validation failed, resource not found).
   * **`2`**: Incorrect CLI usage (missing arguments, invalid flags).
   * **`127` / custom**: Specific application failure states.

## Step 5: Code Conventions & Documentation
Instead of hardcoded rules, you MUST apply the specific conventions based on the project's language and framework. Before writing code, consult the appropriate convention file:
- TypeScript/Node.js (Backend): [`typescript-node.md`](../../resources/conventions/typescript-node.md)
- TypeScript/React (Frontend): [`typescript-react.md`](../../resources/conventions/typescript-react.md)
- Rust: [`rust.md`](../../resources/conventions/rust.md)
- Python: [`python.md`](../../resources/conventions/python.md)
- Go: [`go.md`](../../resources/conventions/go.md)

1. **Naming Conventions**: Follow the file suffix rules defined in the convention file.
2. **Business Logic Comments**: Follow the 'Why over How' rule.
3. **Module-level README**: Every newly created module must contain a local `README.md` as mandated by the convention guidelines.

## Step 6: Verification (Definition of Done)
**CRITICAL RULE**: Code is NOT considered "DONE" until it is fully covered by Unit Tests. You must write and verify unit tests before reporting completion.

1. Write unit tests for business logic detached from the terminal wrapper.
2. Write integration/end-to-end tests that run the compiled binary, pass arguments, and verify:
   * Correct exit codes.
   * Expected patterns in `stdout` and `stderr`.
   * Standard error flows when invalid flags are provided.
