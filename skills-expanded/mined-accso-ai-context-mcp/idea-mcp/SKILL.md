---
name: idea-mcp
description: "Use whenever the user says to use the IntelliJ IDEA MCP / JetBrains IDE MCP tools, or mentions idea_* tools, working inside an open IntelliJ IDEA project, or any task that should go through the IDE (reading/searching/editing code, building, running, VCS, refactoring, or debugging) instead of raw shell/file tools. This is the entry point that routes to the right specialized guidance."
---

# IntelliJ IDEA MCP - Router

This is the entry point for all work done through the IntelliJ IDEA MCP server. It does not contain the detailed tool guidance itself - it routes to a bundled reference file for the job at hand. Read the matching reference below before calling any `idea_*` tool.

## Core principle
IDEA MCP tools operate on the **live IDE index** (semantic, not text-based). Prefer them over shell/grep/cat whenever the project is open in the IDE. Use them for precise, targeted operations once you know (or can find) the file/symbol in question.

## Pick the right guidance

| Task | Read |
|---|---|
| Find/understand code: symbol lookup, usages, file structure, project dependencies/modules, compile errors/warnings | **`references/explore.md`** |
| Change code: create/edit files, apply text edits, reformat, rename/extract/move/change-signature refactorings | **`references/edit.md`** |
| Build the project, run configurations or tests, use the IDE terminal, VCS status/diff, run notebooks, generate/run custom inspections | **`references/ops.md`** |
| Working inside an IntelliJ **plugin** project or the JetBrains **platform monorepo** itself (extension points, plugin.xml, threading/lock requirements) | **`references/plugin-dev.md`** |
| Need **runtime** evidence: breakpoints, stepping, stack/frame values, expression evaluation, confirming whether code is reached | **`references/debugger.md`** |

Read only the reference(s) needed for the current step - don't read all of them upfront. A single task often chains several: e.g. read `references/explore.md` to locate the bug -> read `references/debugger.md` to confirm root cause -> read `references/edit.md` to fix it -> read `references/ops.md` to build/test.

## Workflow

1. Classify the request using the table above.
2. Read the matching file under `references/` in this skill before calling any tool it covers.
3. Each reference file opens with its own **Activation Gate**: a check of which tools must actually be available in the current MCP session (and, for `references/plugin-dev.md`, whether the project even applies) before that guidance should be used. Respect it - if a gate fails, state the blocker explicitly instead of silently falling back to a different toolset or guessing tool names.
4. If the task spans multiple phases (explore -> debug -> fix -> verify), read each piece of guidance in turn as you reach that phase, in the order the work actually proceeds.
5. Never fall back to shell/file tools for something an `idea_*` tool already covers - the IDE-native tool understands language semantics (imports, references, code style) that text tools don't.
6. Always pass `projectPath` when known, to avoid ambiguous resolution across multiple open projects.

## When NOT to use this router
- Open-ended "what does this module/service do?" questions with no specific target - prefer whatever semantic/context search tools are available for broad exploration, and only switch to IDEA MCP once you have a concrete file/symbol target.
