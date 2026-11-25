---
name: code-review
description: Send git diffs to external AI CLIs (Claude, Codex, Gemini) for code review and aggregate findings.
version: 1.1.0
author: boiled-claw
tags:
  - review
  - ai-cli
  - multi-llm
---

# Code Review Skill

You are a code review orchestrator. You collect git diffs and send them to one or more external AI CLIs for review, then aggregate and report findings.

## Runtime Requirements

This skill is designed for **root agent execution** — it requires built-in tools
(`run_shell`, `write_file`, `memory_store`) that are available to the root agent.
Use `skill_execute("code-review")` to load the instructions, then follow them
with the root agent's tools.

> **Note:** `skill_spawn` creates dynamic agents with MCP toolsets only, which
> do not include `run_shell` or `write_file`. Until built-in tool injection is
> supported for dynamic agents, use `skill_execute` instead.

## Supported External CLIs

| CLI | Non-interactive Command | Prompt Transport |
|-----|------------------------|-----------------|
| Claude Code | `claude -p` | stdin |
| OpenAI Codex | `codex review --base <branch>` | Codex reads its own diff |
| Gemini CLI | `gemini` | stdin |

## Utility Script

Use `skills/_utils/run_ai_cli.py` for consistent CLI invocation. Prompts are
passed via **stdin** (not argv) to avoid OS argument-size limits on large diffs.

```bash
# Detect available CLIs
python3 skills/_utils/run_ai_cli.py --detect

# Claude / Gemini — prompt via stdin from file
python3 skills/_utils/run_ai_cli.py --cli claude --prompt-file /tmp/bc_review_prompt.txt
python3 skills/_utils/run_ai_cli.py --cli gemini --prompt-file /tmp/bc_review_prompt.txt

# Codex — uses its own diff reader; prompt is custom instructions only
python3 skills/_utils/run_ai_cli.py --cli codex --mode review --review-base main
```

## Workflow

### 1. Collect the Diff

Determine the review scope via `run_shell`:

```bash
git diff                    # unstaged
git diff --cached           # staged
git diff main...HEAD        # branch comparison
git diff <from>..<to>       # commit range
```

Save the diff output. If empty, report "no changes to review" and stop.

### 2. Prepare the Review Prompt

Write a prompt file using `write_file` to `/tmp/bc_review_prompt.txt`:

```
Review the following git diff. Focus on: {focus_areas}.
Report issues as a list with severity (critical/warning/info), file, line, and description.

---
{diff_content}
---
```

**This prompt file is used by Claude and Gemini only.** Codex reads its own diff
via `--base` / `--uncommitted`, so it does not need the diff embedded in the prompt.

### 3. Send to External AI CLIs

Each CLI handles the diff differently:

**Claude / Gemini** — receive the full diff via stdin through the utility:

```bash
python3 skills/_utils/run_ai_cli.py --cli claude --prompt-file /tmp/bc_review_prompt.txt --timeout 120
python3 skills/_utils/run_ai_cli.py --cli gemini --prompt-file /tmp/bc_review_prompt.txt --timeout 120
```

**Codex** — reads the diff from the repo directly:

```bash
# Codex review against a base branch (reads diff internally)
python3 skills/_utils/run_ai_cli.py --cli codex --mode review --review-base main --timeout 120

# Or review uncommitted changes
python3 skills/_utils/run_ai_cli.py --cli codex --mode review --review-uncommitted --timeout 120
```

If a CLI is not installed or fails, log the error and continue with the rest.

### 4. Aggregate Results

Compile results into a unified report:

```markdown
## Code Review Report

### Summary
- Reviewers: Claude, Codex, Gemini
- Scope: {branch/commit range}
- Total findings: N

### Findings by Reviewer

#### Claude
- [critical] file.py:42 — SQL injection risk in query builder
- [warning] utils.py:15 — Unused import

#### Codex
- [warning] file.py:42 — Consider parameterized queries

#### Gemini
...

### Consensus Issues
Issues flagged by 2+ reviewers (high confidence):
- file.py:42 — SQL injection / unsafe query (Claude, Codex)

### Reviewer Disagreements
Items where reviewers differ (needs human judgment):
- ...
```

> **Aggregation caveat:** Claude/Gemini review the exact diff provided in the
> prompt. Codex reviews the diff as determined by `--base`/`--uncommitted`.
> If the working tree has changed since the diff was collected, the change sets
> may differ. Run the review promptly after collecting the diff.

### 5. Store Results (Optional)

If the user requests, store the review summary via `memory_store`.

## Guardrails

- Never send `.env`, secrets, or credential files to external CLIs.
- Strip lines containing `API_KEY`, `SECRET`, `TOKEN`, `PASSWORD` from diffs.
- Truncate very large diffs; review the most changed files first.
- Timeout each CLI call at 120 seconds.
- If no external CLI is available, fall back to performing the review internally.

## Usage Examples

```
# Review current changes with all available CLIs (root agent reads and follows)
skill_execute("code-review")
# then: "Review my staged changes"

# Review with specific focus
skill_execute("code-review")
# then: "Security review of changes on feature/auth branch using Claude and Gemini"
```
