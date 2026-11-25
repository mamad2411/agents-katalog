---
name: bash
version: 1.0.0
description: Execute shell commands in the workspace
uses: []
requires:
  tools: []
  env: []
security:
  risk_level: execute
  capabilities:
    - command:execute
  requires_approval: false
---

# Bash

Execute shell commands in the workspace directory. This skill provides direct access to the operating system shell for running commands, scripts, and system operations.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `bash` is invoked, the executor runs the specified command in a subprocess within the workspace directory and returns the output. The tool schema in tool.yaml defines the external contract; the executor handles execution directly.

## When to Use

- Running version control commands (git operations)
- Executing build scripts (make, npm, pip, cargo, etc.)
- Running tests or linters
- Installing dependencies
- Inspecting system state (processes, ports, disk usage)
- Any command-line operation not covered by a dedicated tool

## Methodology

### 1. Validate the Command

Before executing, verify:
- **Purpose**: Is this command necessary for the current task?
- **Safety**: Could this command cause unintended damage?
- **Scope**: Does the command stay within the workspace directory?
- **Idempotency**: Can this command be safely re-run?

### 2. Set Appropriate Timeout

- Short commands (status, list): 30 seconds or less
- Medium commands (build, test): 120 seconds (default)
- Long commands (full test suite, large installs): up to 600 seconds
- If unsure, use the default — don't set excessively long timeouts

### 3. Execute and Capture Output

- Run the command in the workspace directory
- Capture both stdout and stderr
- Record the exit code
- Respect the timeout — kill if exceeded

### 4. Interpret Results

- **Exit code 0**: Command succeeded — verify output matches expectations
- **Non-zero exit code**: Command failed — examine stderr for error details
- **Timeout**: Command took too long — consider whether the approach is right
- **Empty output**: May be normal (e.g., successful `mkdir`) or may indicate a problem

## Output Format

```
## Command Execution

- Command: [command that was run]
- Exit code: [0 or error code]
- Duration: [time taken]

### Output
[stdout content]

### Errors (if any)
[stderr content]
```

## Quality Criteria

- Commands execute within the workspace directory
- Timeout is set appropriately for the command type
- Destructive commands are blocked or require confirmation
- Output is captured completely (both stdout and stderr)
- Exit codes are checked and errors are reported
- Sensitive data (passwords, tokens) is not exposed in command output

## Common Mistakes

- **Running destructive commands without thinking**: `rm -rf`, `git reset --hard`, `git clean -fd` can destroy work. Always verify scope before running destructive operations.
- **Using overly broad file operations**: `git add .` or `git add -A` stages everything including secrets and build artifacts. Stage specific files instead.
- **Ignoring exit codes**: A command that exits with non-zero failed. Don't assume it worked just because there was output.
- **Setting no timeout**: Long-running commands can hang indefinitely. Always use a reasonable timeout.
- **Exposing secrets in commands**: Don't put passwords, API keys, or tokens in command strings — they appear in process lists and logs.
- **Assuming shell state persists**: Each invocation is a fresh shell. Environment variables, directory changes, and aliases don't carry over between calls.

## Completion

A bash operation is complete when:
- The command has executed and returned
- The exit code has been checked
- Output has been captured and interpreted
- Any errors have been identified and reported
