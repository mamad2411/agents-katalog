---
name: record
description: Start terminal recording with asciinema. TRIGGERS - record session, capture terminal, start recording.
allowed-tools: Bash, AskUserQuestion, Glob
argument-hint: "[file] [-t title] [-i idle-limit] [--backup] [--append]"
---

# /asciinema-tools:record

Start a terminal recording session with asciinema.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Arguments

| Argument                | Description                        |
| ----------------------- | ---------------------------------- |
| `file`                  | Output path (e.g., `session.cast`) |
| `-t, --title`           | Recording title                    |
| `-i, --idle-time-limit` | Max idle time in seconds           |
| `--backup`              | Enable streaming backup to GitHub  |
| `--append`              | Append to existing recording       |

## Execution

Invoke the `asciinema-recorder` skill with user-selected options.

### Skip Logic

- If `file` provided -> skip Phase 1 (output location)
- If `-t` and `-i` provided -> skip Phase 2 (options)

### Workflow

1. **Preflight**: Check asciinema installed
2. **Location**: AskUserQuestion for output path
3. **Options**: AskUserQuestion for recording options
4. **Generate**: Build and display recording command
5. **Guidance**: Show step-by-step instructions

## Examples

```bash
# Basic recording
/asciinema-tools:record session.cast

# Recording with title and idle limit
/asciinema-tools:record -t "Demo Session" -i 30

# Recording with GitHub backup
/asciinema-tools:record session.cast --backup
```

## Troubleshooting

| Issue                  | Cause             | Solution                                     |
| ---------------------- | ----------------- | -------------------------------------------- |
| asciinema not found    | Not installed     | `brew install asciinema`                     |
| Permission denied      | Output path issue | Check write permissions for output directory |
| Recording not starting | Terminal issue    | Ensure running in interactive terminal       |


## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
