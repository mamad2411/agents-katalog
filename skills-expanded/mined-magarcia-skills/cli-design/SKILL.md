---
name: cli-design
description: >
  Guide for building delightful, human-first command-line tools with proper
  command structure, output formatting, error handling, configuration, and
  extensibility. Use when creating CLI tools, adding subcommands, designing
  CLI output, handling errors in CLIs, or reviewing CLI code for UX issues.
---

# CLI Design

Build command-line tools that feel solid, communicate clearly, and compose well with the Unix ecosystem.

## When to use

- Creating a new CLI tool or adding subcommands
- Designing output format (human, JSON, LLM)
- Implementing error handling and exit codes
- Adding authentication, configuration, or plugin systems
- Reviewing CLI code for usability issues

## Core philosophy

1. **Human-first, machine-compatible** -- design for humans, then ensure machines can consume output
2. **Conversation, not interrogation** -- each invocation is a turn in a dialogue; suggest corrections, show next steps
3. **Consistency over novelty** -- follow conventions (`--help`, `-v`, `--output json`, exit codes)
4. **Say just enough** -- concise by default, verbose via flags
5. **Robustness as a feeling** -- fast startup, clear feedback, no hanging, no cryptic stack traces

## Rule index

Rules are organized by domain and impact. See the linked reference for full details with examples.

| # | Domain | Rule | Impact | Reference |
|---|--------|------|--------|-----------|
| 1 | Command | Use `tool <noun> <verb> [flags]` for multi-resource CLIs | CRITICAL | [command-structure](references/command-structure.md) |
| 2 | Command | Keep subcommand nesting to 2 levels max | HIGH | [command-structure](references/command-structure.md) |
| 3 | Command | Prefer flags over positional args (self-documenting, order-independent) | HIGH | [command-structure](references/command-structure.md) |
| 4 | Command | Every flag has a long form; common ones also get a short form | MEDIUM | [command-structure](references/command-structure.md) |
| 5 | Command | Support global flags: `--help`, `--version`, `--verbose`, `--output`, `--no-color`, `--quiet` | CRITICAL | [command-structure](references/command-structure.md) |
| 6 | Output | Detect TTY -- adapt output to terminal vs pipe | CRITICAL | [output-design](references/output-design.md) |
| 7 | Output | stdout for data, stderr for messages/progress/errors | CRITICAL | [output-design](references/output-design.md) |
| 8 | Output | Support `--output json` with stable schema | CRITICAL | [output-design](references/output-design.md) |
| 9 | Output | Support `--output llm` for agent-friendly consumption | HIGH | [output-design](references/output-design.md) |
| 10 | Output | Use color for scannability, not decoration; respect `NO_COLOR` | MEDIUM | [output-design](references/output-design.md) |
| 11 | Output | Show spinners/progress for long operations on stderr | HIGH | [output-design](references/output-design.md) |
| 12 | Help | Show concise summary when run with no args; full help on `--help` | CRITICAL | [help-system](references/help-system.md) |
| 13 | Help | Lead with examples in help text | HIGH | [help-system](references/help-system.md) |
| 14 | Help | Suggest corrections on typos and next steps after actions | HIGH | [help-system](references/help-system.md) |
| 15 | Help | Provide shell completion for bash, zsh, fish, powershell | MEDIUM | [help-system](references/help-system.md) |
| 16 | Errors | Every error answers: what happened, why, and what to do | CRITICAL | [error-handling](references/error-handling.md) |
| 17 | Errors | Use namespaced error codes (`AUTH-003`, `NET-001`) | HIGH | [error-handling](references/error-handling.md) |
| 18 | Errors | Define clear exit code mapping (0=success, 1=general, 2=usage, etc.) | HIGH | [error-handling](references/error-handling.md) |
| 19 | Errors | Never show raw stack traces; log to debug file | HIGH | [error-handling](references/error-handling.md) |
| 20 | Interactive | Prompt for missing args only when stdin is TTY; fail with `--no-input` | HIGH | [interactivity](references/interactivity.md) |
| 21 | Interactive | Confirm destructive actions; support `--yes` to bypass | CRITICAL | [interactivity](references/interactivity.md) |
| 22 | Config | Follow XDG Base Directory (`~/.config/mycli/`) on all platforms | HIGH | [configuration](references/configuration.md) |
| 23 | Config | Precedence: flags > env vars > project config > user config > defaults | HIGH | [configuration](references/configuration.md) |
| 24 | Auth | Support tokens through environment, stored credentials, and interactive login; never command-line flags | HIGH | [authentication](references/authentication.md) |
| 25 | Extend | Use `mycli-<name>` executable pattern for plugins | MEDIUM | [extensibility](references/extensibility.md) |
| 26 | Perf | Target <100ms cold start; defer work until needed | HIGH | [performance](references/performance.md) |
| 27 | Perf | Print something within 100ms; responsiveness > raw speed | HIGH | [performance](references/performance.md) |
| 28 | Dist | Ship single static binary when possible | HIGH | [distribution](references/distribution.md) |
| 29 | Dist | Support `--version` with version, commit hash, build date | MEDIUM | [distribution](references/distribution.md) |
| 30 | Test | Integration-test full CLI invocations (stdout, stderr, exit codes) | HIGH | [testing](references/testing.md) |
| 31 | Robust | Handle SIGINT (exit 130), SIGTERM (exit 143), SIGPIPE (exit silently) | HIGH | [testing](references/testing.md) |
| 32 | Robust | Validate input early, bail before state changes | HIGH | [error-handling](references/error-handling.md) |
| 33 | Robust | Design for crash-only: avoid cleanup requirements on exit | MEDIUM | [testing](references/testing.md) |
| 34 | Security | Never accept secrets via flags (visible in `ps`, shell history) | CRITICAL | [configuration](references/configuration.md) |
| 35 | Future | Keep changes additive; deprecate before removing | HIGH | [distribution](references/distribution.md) |

## Workflow

When building or reviewing a CLI tool:

1. **Read the relevant reference files** for the domains you're working on
2. **Apply rules by impact** -- CRITICAL first, then HIGH, then MEDIUM
3. **Use the [checklist](references/checklist.md)** before shipping

## Additional references

- [Philosophy deep dive](references/philosophy.md) -- expanded principles with rationale
- [Pre-launch checklist](references/checklist.md) -- verification checklist before shipping
