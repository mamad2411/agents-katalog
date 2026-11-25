---
name: command-authoring
description: Write or refactor Claude Code slash commands (files in commands/<ns>/<cmd>.md). Use when the user asks to "create a slash command", "add /<name>", "write a command file", "make a /command", "turn this workflow into a command", "argument hints", "allowed-tools", or when packaging a repeatable workflow as a one-keystroke invocation. Covers frontmatter, $ARGUMENTS parsing, @-imports for context files, and orchestration patterns.
---

# Slash Command Authoring

A slash command is a markdown file at `commands/<namespace>/<name>.md`. Invoked as `/namespace:name [args]`.

## Frontmatter

```yaml
---
name: <namespace>:<cmd>
description: One-line what the command does. Shows in /help.
argument-hint: "[arg1] [arg2]"   # what $ARGUMENTS will contain
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
---
```

`allowed-tools` is an **allowlist** — if set, the command runs with only these. Omit to inherit the session's tools. Prefer allowlists for safety.

## Body structure

```markdown
<objective>
One paragraph: what the command produces and what files it touches.
</objective>

<execution_context>
@${CLAUDE_PLUGIN_ROOT}/<plugin>/references/<doc>.md
@${CLAUDE_PLUGIN_ROOT}/<plugin>/templates/<template>.md
</execution_context>

<context>
Arguments: $ARGUMENTS
Parse as: <describe>
</context>

<process>
Numbered steps. Each step is either:
- Read a file
- AskUserQuestion to fill a gap
- Task-spawn a specialist (by subagent_type)
- Write an output file
</process>

<output>
Files created/modified + a 5-line summary.
</output>
```

## `@`-imports

`@<path>` in the body loads the file contents inline at command expansion time. Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths. Use this to pull in long reference docs, templates, and few-shot examples so the command body itself stays short.

## $ARGUMENTS

Raw string of everything after the command name. Parse it in the body prose — the model handles extraction. For multi-arg commands, document the expected format in `argument-hint`.

## Orchestration commands vs. task commands

- **Task command**: does one thing inline (e.g., `/note`, `/status`).
- **Orchestration command**: spawns multiple specialists (e.g., `/agents-architect:new`, GSD's `/gsd:plan-phase`). Includes gates, approvals, and aggregates specialist output.

Orchestrators should **always** use the Task tool, not inline the specialist's work.

## Design principles

1. **Idempotent**: running the command twice produces the same result. Check for existing state before creating.
2. **Explicit gates**: any non-trivial action (writing >1 file, destructive ops) gets `AskUserQuestion` confirmation.
3. **Short body, deep imports**: command body under 100 lines; push detail into `@`-imported references.
4. **State on disk**: commands that span turns write checkpoint files (`.planning/STATE.md`, `.arch/state.json`) rather than relying on context.

## References

- @../../agents-architect/references/anthropic-best-practices.md
- @../../agents-architect/templates/command.template.md

## Output

Produce `commands/<ns>/<name>.md` with correct frontmatter, XML-structured body, @-imports for heavy context, and a short exit summary spec.
