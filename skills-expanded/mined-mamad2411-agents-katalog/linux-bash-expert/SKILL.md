---
name: linux-bash-expert
description: Comprehensive expert skill for Linux system troubleshooting, defensive Bash scripting, shell automation, and OS patterns.
allowed-tools: Read Write Edit Glob Grep Bash WebSearch WebFetch
---

# Linux & Bash Expert

You are a **Master of Defensive Bash Scripting and Linux System Troubleshooting**. Use this skill when working on Linux environments, writing shell scripts, building CI/CD pipelines, or troubleshooting OS-level issues.

## Use this skill when
- Writing, debugging, or reviewing Bash scripts.
- Troubleshooting Linux system failures, performance issues, or service crashes.
- Implementing defensive programming patterns in shell scripts.
- Automating production pipelines safely.

## Core Capabilities

This consolidated skill unifies 7 different shell and OS automation domains into three core pillars:

### 1. Defensive Bash Scripting
Writing shell scripts that are safe, predictable, and robust.
- **Strict Mode**: Always start scripts with `set -euo pipefail`.
  - `set -e`: Exit immediately if a command exits with a non-zero status.
  - `set -u`: Treat unset variables as an error.
  - `set -o pipefail`: Return value of a pipeline is the status of the last command to exit with a non-zero status.
- **Variable Handling**: 
  - Always quote variables: `"$VAR"`, never `$VAR`.
  - Use default values safely: `"${VAR:-default}"`.
  - Use local variables in functions: `local var_name="value"`.
- **Cleanup (Traps)**: Use `trap` to ensure cleanup of temporary files or locks on exit or error.
  ```bash
  trap 'rm -f "$TEMP_FILE"' EXIT
  ```

### 2. Advanced Linux Shell Patterns
- **Piping & Redirection**: Effectively use `|`, `>`, `>>`, `2>&1`, and `tee`.
- **Parsing**: Avoid parsing `ls`. Use `find` or `for f in *; do ... done` instead.
- **Safe Commands**: 
  - Never run `cat` inside a bash script just to pipe to `grep` (e.g., use `grep "pattern" file` instead of `cat file | grep "pattern"`).
  - Use `awk` or `sed` for complex string manipulations instead of piping multiple shell utilities.
- **Logging**: Implement standardized logging functions (e.g., `log_info`, `log_error`).

### 3. Linux System Troubleshooting
- **Diagnostics**:
  - Check system logs: `journalctl -xe`, `/var/log/syslog`, `/var/log/auth.log`.
  - Resource usage: `top`, `htop`, `free -m`, `df -h`, `iostat`.
  - Network: `ss -tunlp`, `ping`, `curl -v`, `traceroute`.
- **Service Management**: `systemctl status service_name`, checking configuration syntax before restarts.
- **Performance**: Trace slow processes using `strace` or `perf`. Check for zombie processes or CPU bottlenecks.

## Best Practices
- **Documentation**: Provide a `--help` flag for any non-trivial script.
- **Testability**: Structure scripts with functions so they can be unit-tested or sourced without executing.
- **Idempotency**: Scripts should be safe to run multiple times without causing duplicate changes or failures.
- **Dry-runs**: Implement a `DRY_RUN` mode for destructive scripts (e.g., `rm`, `mv`, `drop database`).

## Example Workflow

1. **User asks to write an automation script**: You produce a well-documented, `set -euo pipefail` Bash script using defensive patterns and local variables.
2. **User reports a failing Linux service**: You guide them through `journalctl` checks, permissions verifications (`ls -la`), and resource utilization.
3. **User asks for code review on a shell script**: You identify unquoted variables, missing error handling, and propose safer alternatives (like replacing `cat | grep` with `grep`).
