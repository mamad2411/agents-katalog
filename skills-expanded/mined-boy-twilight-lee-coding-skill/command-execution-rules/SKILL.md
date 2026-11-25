---
name: command-execution-rules
description: "Apply safe command-execution and Python-first automation rules when executing shell or system commands, or when writing, modifying, reviewing, or debugging command runners and automation scripts. Use direct commands for simple fixed invocations and Python subprocess for orchestration, parsing, dynamic arguments, or reusable workflows. Do not apply this skill to Python code that does not execute external commands."
---

# Command Execution Rules

Use the simplest safe execution method that fits the task. Preserve the user's authorization boundaries, repository instructions, working directory, and existing implementation language.

## Required Reference Loading

Loading this entrypoint is sufficient only for simple fixed command execution. Read [Command Execution Examples](references/command-execution-examples.md) in full before implementing or reviewing a reusable command runner, handling subprocess output or timeouts, composing dynamic command arguments, or making a failure-sensitive choice between direct execution, Python orchestration, and shell scripting. Do not claim the reference was loaded without opening it; when uncertain whether it applies, read it.

## Working Process

1. Inspect the relevant repository instructions, available executables, working directory, runtime targets, and check configuration before executing or changing command-related code.

2. Choose between direct execution, Python orchestration, and shell-specific scripting using the criteria below. Do not add a Python wrapper when a direct fixed command is clearer and equally safe.

3. Keep arguments as data rather than interpolating them into executable source. Treat paths, patterns, branch names, URLs, and user-provided values as untrusted command arguments.

4. Check completion state and return code, preserve useful stdout and stderr, and report commands or checks that could not be run rather than implying success.

5. Run focused verification proportional to the change. For reusable command runners, verify the relevant success, nonzero-exit, startup-failure, and timeout paths.

## Choose the Execution Method

### Direct command execution

Execute a command directly when it is a single, fixed invocation such as `git status`, `rg --files`, or a project-defined test or build command.

- Pass the working directory through the execution tool instead of changing directories inside a compound command.
- Prefer an argument-list API when the tool provides one. If the tool accepts only a shell command string, quote for the actual shell and avoid inserting untrusted values.
- Do not wrap a direct command in `python -c` merely to satisfy a Python-first preference. Extra parsing layers increase quoting and encoding risk, especially on Windows and with non-ASCII paths.
- Use pipelines, redirection, wildcard expansion, environment assignment, or other shell syntax only when those semantics are actually needed.

### Python orchestration

Prefer Python standard-library APIs when the task involves multiple commands, branching, output parsing, file processing, dynamic arguments, reusable automation, or consistent cross-platform behavior.

- Use `pathlib` for paths and `subprocess` for external tools.
- Use `python -X utf8 -c` only for short, readable operations whose source and arguments can be quoted safely. Use a `.py` script for multiline, reusable, or failure-sensitive logic.
- Invoke external tools with an argument list and `shell=False` unless shell semantics are an explicit requirement.
- Use `sys.executable` when launching the current Python interpreter.
- Do not replace the project's implementation language with Python; apply the appropriate language Skill to project code.

### Shell-specific scripting

Use PowerShell, Bash, Batch, or another shell when the task genuinely depends on that shell's built-ins or language semantics. Keep the script scoped to the chosen shell, quote dynamic values correctly, and explain the fallback when Python would normally be expected.

## Command Results and Failures

For ordinary interactive command execution, inspect the tool's completion state, return code, stdout, and stderr. A separate structured result object is not required.

For reusable command runners or machine-consumed automation, return consistent fields for success, nonzero exit, startup failure, and timeout:

| Field | Type | Meaning |
| --- | --- | --- |
| `success` | `bool` | True only when the command completed with exit code zero |
| `return_code` | `int \| None` | Actual exit code, or `None` when none is available |
| `output` | `str` | Captured stdout, including partial output when available |
| `errors` | `str` | Captured stderr and necessary exception context |

When implementing a Python runner:

1. Prefer `subprocess.run` with an argument list, `shell=False`, an explicit `cwd`, a proportionate timeout, and `check=False` when the caller interprets the result.

2. Capture stdout and stderr when the caller needs them. Use the encoding guaranteed by the invoked tool; prefer UTF-8 for controlled tools and protocols, but do not assume every Windows executable emits UTF-8. Use replacement decoding only for human-readable diagnostics, not structured data.

3. Handle `OSError` and `subprocess.TimeoutExpired`. If using `check=True`, also handle `subprocess.CalledProcessError`. Preserve partial output and useful failure context.

4. Determine success from completion state and return code, not from whether stderr contains text. Interpret documented nonzero statuses at the caller, such as `rg` returning 1 when no matches are found.

## Automation Script Quality

Apply these rules to command-execution helpers and automation scripts, not unrelated Python application code.

- Organize nontrivial scripts into focused functions with useful type hints and documentation.
- Use a `main()` entry point and `if __name__ == "__main__":` so importing a reusable module does not execute commands.
- Catch errors at the layer responsible for reporting or recovery; preserve context and avoid empty exception handlers.
- Avoid fixed drive letters, hard-coded interpreter paths, silent failures, unconditional success messages, and unnecessary debug output.
- Match the repository's supported Python version and run focused checks after changes.
