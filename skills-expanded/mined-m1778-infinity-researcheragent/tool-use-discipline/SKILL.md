---
name: tool-use-discipline
description: Strict guidelines for tool invocation, parameter formatting, parallelism, and preventing recursive or wasteful tool loops.
license: MIT
---

# Tool-Use Discipline Standards

This skill enforces reliable, deterministic tool execution across all models, preventing malformed tool calls, wasted roundtrips, and tool thrashing.

## Golden Rules for Tool Invocation

### 1. Batch Independent Operations
- Never execute sequential roundtrips for independent reads, searches, or checks.
- If you need to read 3 files, pass all 3 in a single `read_files` call.
- If executing multiple non-dependent verification commands, run them in one batched command call.

### 2. Guard Against Hallucinated Parameters
- Inspect tool parameter schemas before passing arguments.
- Do NOT invent optional arguments that do not exist in the tool declaration.
- Always provide valid absolute paths for filesystem tools.

### 3. Read-Before-Write (Inspection Prerequisite)
- **NEVER** edit a file without reading the existing lines first.
- Always check line bounds and verify exact character matches for `old_text` before submitting replacement edits.
- Keep edit chunks small and focused ($< 6000$ characters) to avoid timeout and truncation.

### 4. No Command Guessing
- Verify environment tool availability (`git`, `node`, `npm`, `python3`) before invoking complex pipelines.
- Non-interactive mode must always be enforced (pass `--no-pager`, `-y`, `--batch`, or equivalent flags).

### 5. Validate Outputs Immediately
- After executing a write or edit tool, verify that the file actually contains the expected content and passes lint/build checks.
- If a tool returns an error, STOP and read the error message before trying the exact same call again.
