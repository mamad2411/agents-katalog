---
name: auto-fix
description: Detect lint/test failures, send context to external AI CLIs for fixes, apply patches, and verify in a loop.
version: 1.1.0
author: boiled-claw
tags:
  - auto-fix
  - ai-cli
  - lint
  - testing
  - ci
---

# Auto-Fix Skill

You are an automated fix orchestrator. You detect lint or test failures, send the failure context to an external AI CLI for code fixes, apply the suggested changes, and re-verify until the issue is resolved or the retry limit is reached.

## Runtime Requirements

This skill is designed for **root agent execution** — it requires built-in tools
(`run_shell`, `write_file`, `read_file`) that are available to the root agent.
Use `skill_execute("auto-fix")` to load the instructions, then follow them
with the root agent's tools.

> **Note:** `skill_spawn` creates dynamic agents with MCP toolsets only, which
> do not include `run_shell` or `write_file`. Until built-in tool injection is
> supported for dynamic agents, use `skill_execute` instead.

## Supported External CLIs

| CLI | Non-interactive Command | Prompt Transport |
|-----|------------------------|-----------------|
| Claude Code | `claude -p` | stdin |
| OpenAI Codex | `codex exec -` | stdin (`-` = read from stdin) |
| Gemini CLI | `gemini` | stdin |

## Utility Script

Use `skills/_utils/run_ai_cli.py`. Prompts are passed via **stdin** (not argv)
to avoid OS argument-size limits on large error context.

```bash
python3 skills/_utils/run_ai_cli.py --detect
python3 skills/_utils/run_ai_cli.py --cli claude --prompt-file /tmp/bc_fix_prompt.txt --timeout 120
```

## Workflow

### 1. Detect Failures

Run the user-specified check command (or auto-detect) via `run_shell`:

```bash
ruff check .                   # Python lint
pytest -x --tb=short           # Python test
mypy src/                      # Python type check
eslint .                       # JS/TS lint
tsc --noEmit                   # TS type check
```

Capture stdout + stderr and the exit code. If exit code is 0, report success and stop.

### 2. Parse Failure Context

Extract from the failure output:
- **File path** and **line number** of each error
- **Error message** / **test name**
- **Error category** (syntax, type, import, assertion, etc.)

Read the relevant source files around error locations via `read_file`.

### 3. Build Fix Prompt

Write to `/tmp/bc_fix_prompt.txt` using `write_file`:

```
Fix the following errors in this codebase.

## Errors
{parsed error list with file:line and message}

## Relevant Source Code

### {file1}:{start_line}-{end_line}
```{language}
{source code}
```

## Instructions
- Output ONLY the corrected code blocks, prefixed with the file path.
- Do not change unrelated code.
- Preserve existing style and formatting.
- Format as:

### {filepath}
```{language}
{corrected full file content or relevant section}
```
```

Never include `.env`, secrets, or credential content.

### 4. Send to External AI CLI

Use the utility script — the prompt is piped via stdin:

```bash
python3 skills/_utils/run_ai_cli.py --cli claude --prompt-file /tmp/bc_fix_prompt.txt --timeout 120
```

Parse the response to extract file paths and corrected code blocks.

### 5. Apply Fixes

For each corrected code block:
1. Read the original file (record content for revert).
2. Apply the fix via `write_file`.

### 6. Verify (Loop)

Re-run the original check command.

**Loop conditions:**
- **Pass (exit 0):** Report success with change summary. Stop.
- **Fail (same errors):** Fix didn't work. Try a different CLI or refine prompt. Max 3 retries.
- **Fail (new errors):** Regression introduced. Revert the last change and retry.
- **Max retries reached:** Report current state, list remaining errors, suggest manual fixes.

### 7. Report

```markdown
## Auto-Fix Report

### Status: {FIXED / PARTIALLY_FIXED / FAILED}

### Check Command
`{command}`

### Iterations
| # | CLI Used | Errors Before | Errors After | Result |
|---|----------|---------------|--------------|--------|
| 1 | Claude   | 5             | 2            | partial |
| 2 | Codex    | 2             | 0            | fixed   |

### Changes Made
- `src/foo.py:42` — Fixed missing return type annotation
- `src/bar.py:15-20` — Replaced deprecated API call

### Remaining Issues (if any)
- `src/baz.py:99` — Complex logic error, needs manual review
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_retries | 3 | Maximum fix-verify iterations |
| check_command | auto-detect | The lint/test command to run |
| preferred_cli | auto | Which AI CLI to use first |
| revert_on_regression | true | Revert if new errors are introduced |
| timeout_per_cli | 120 | Seconds to wait for CLI response |

## Guardrails

- **Max 3 retries** to prevent infinite loops.
- **Revert on regression**: If a fix introduces more errors than it solves, revert immediately.
- **No destructive changes**: Never delete files or remove large code sections without user approval.
- **Scope control**: Only modify files directly related to reported errors.
- **Backup**: Record original content before applying fixes.
- Never send `.env`, secrets, or credential files to external CLIs.

## Usage Examples

```
# Auto-fix lint errors (root agent reads and follows)
skill_execute("auto-fix")
# then: "Fix all ruff lint errors in this project"

# Auto-fix with specific CLI
skill_execute("auto-fix")
# then: "Fix the failing pytest tests using Claude CLI"
```
