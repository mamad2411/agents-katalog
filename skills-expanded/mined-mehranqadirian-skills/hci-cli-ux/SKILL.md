---
name: hci-cli-ux
description: Designs and reviews the user experience of command-line tools. Use whenever the user builds or improves a CLI, script with options, or terminal tool and cares about help text, flags and subcommands, error messages, exit codes, progress output, colors, prompts and confirmations, JSON output, piping, or beginner friendliness, even if they only say "my script is hard to use". Tests a real command with a script that checks help, bad options, version, ANSI codes and stdin behavior.
---

# hci-cli-ux

A command-line tool is a user interface for people and for other programs. This skill applies HCI principles to it: clear help, predictable flags, human errors, safe actions and machine-friendly output.

```
hci-cli-ux/
├── SKILL.md
├── scripts/
│   └── check_cli_ux.py           runs --help, --version, a bad option and no arguments; checks the experience
└── references/
    └── cli-guidelines.md         names, help, output, errors, interactivity, config, accessibility, testing
```

## When to use

- Designing a new tool, subcommands or flags
- Improving help text and error messages
- A tool is confusing for beginners or awkward in pipelines and scripts
- Adding progress, colors, prompts, confirmation, `--dry-run` or `--json`
- Reviewing exit codes and stdout versus stderr behavior

## Workflow

1. **Understand the users and uses**: who runs it (beginner, expert, other programs), how often, interactively or in scripts, on which OS.
2. **Test the real tool** if it exists: `python3 scripts/check_cli_ux.py -- ./tool` (add fixed arguments after the command, for example `-- python3 tool.py`). It runs the tool only with `--help`, `--version`, an invalid option and no arguments, with stdin closed and output piped, then reports missing usage and examples, wrong exit codes, errors on stdout, color codes when piped, hanging behavior and absent `--version`. Run it only on tools you trust. Add `--strict` to fail on warnings.
3. **Read the help as a newcomer**: is the first line clear, are examples present and copyable, are common options first?
4. **Review errors**: each says what happened, why if known, and the next step, on stderr with a non-zero exit code. Rewrite the worst ones using the pattern in the reference.
5. **Check output design**: results on stdout, messages on stderr, no color or spinners when piped, `--json` with a stable schema, progress for long work, `NO_COLOR` honored.
6. **Check safety**: `--dry-run`, named confirmations for destructive actions, `--yes` for scripts, no secrets in arguments, clean Ctrl+C.
7. **Map to principles**: visibility of status (progress, summaries), error prevention (dry run, confirmation), recognition over recall (examples, suggestions for typos), consistency (standard flag names), flexibility (short flags, config precedence).
8. **Report** findings, rewritten help and error messages, and what to test by hand with a new user.

## Rules

- Results to stdout, diagnostics to stderr, errors exit non-zero, usage errors exit 2
- `--help` always works, prints to stdout and exits 0; `--version` exists
- Never use color or progress animation when output is not a terminal; honor `NO_COLOR`
- Error messages are human sentences with a next step; stack traces only behind `--debug`
- Safe by default: destructive actions need an explicit flag or confirmation, and `--dry-run` previews them
- Use standard flag names and keep them consistent across subcommands
- Never read secrets from command-line arguments
- Do not run unknown commands to test them; only run tools the user trusts

## What to report back

| Field | Content |
|-------|---------|
| Script results | findings with severity |
| Help review | clarity, examples, order, wording |
| Error review | rewritten messages with exit codes |
| Output and safety | stdout and stderr use, machine output, dry run, confirmations |
| Manual tests left | pipe test, no-color test, beginner run, Windows and Termux behavior |

## Related skills

- `shell-scripting`: write safe shell tools with strict mode and dry run
- `hci-microcopy`: wording of messages, errors and prompts
- `hci-foundations`: principles and evaluation reports
- `hci-desktop-apps`: graphical desktop software
