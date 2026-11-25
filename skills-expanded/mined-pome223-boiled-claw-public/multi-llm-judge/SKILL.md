---
name: multi-llm-judge
description: Send the same prompt to multiple LLMs (Claude, Codex, Gemini) and compare their responses.
version: 1.1.0
author: boiled-claw
tags:
  - comparison
  - ai-cli
  - multi-llm
  - evaluation
---

# Multi-LLM Judge Skill

You are a multi-LLM evaluation orchestrator. You send the same prompt to multiple external AI CLIs, collect their responses, and produce a comparative analysis.

## Runtime Requirements

This skill is designed for **root agent execution** — it requires built-in tools
(`run_shell`, `write_file`) that are available to the root agent.
Use `skill_execute("multi-llm-judge")` to load the instructions, then follow them
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
to avoid OS argument-size limits.

```bash
python3 skills/_utils/run_ai_cli.py --detect
python3 skills/_utils/run_ai_cli.py --cli claude --prompt-file /tmp/bc_judge_prompt.txt
python3 skills/_utils/run_ai_cli.py --cli codex --prompt-file /tmp/bc_judge_prompt.txt
python3 skills/_utils/run_ai_cli.py --cli gemini --prompt-file /tmp/bc_judge_prompt.txt
```

## Workflow

### 1. Prepare the Prompt

- Use the exact same prompt text for all LLMs.
- If the task involves code, include relevant file content for context.
- Write the prompt to `/tmp/bc_judge_prompt.txt` using `write_file`.
- Keep under 10,000 characters; summarize or chunk if longer.
- Never include secrets or credentials.

### 2. Detect Available CLIs

```bash
python3 skills/_utils/run_ai_cli.py --detect
```

Require at least 2 CLIs for a meaningful comparison. If only 1, warn the user.

### 3. Send to All Available CLIs

Run each via `run_shell`. The utility pipes the prompt through stdin:

```bash
python3 skills/_utils/run_ai_cli.py --cli claude --prompt-file /tmp/bc_judge_prompt.txt --timeout 180
python3 skills/_utils/run_ai_cli.py --cli codex --prompt-file /tmp/bc_judge_prompt.txt --timeout 180
python3 skills/_utils/run_ai_cli.py --cli gemini --prompt-file /tmp/bc_judge_prompt.txt --timeout 180
```

If a CLI fails or times out, mark as "unavailable" and continue.

### 4. Compare and Evaluate

```markdown
## Multi-LLM Comparison Report

### Prompt
> {the prompt sent}

### Responses

#### Claude
{response}

#### Codex
{response}

#### Gemini
{response}

### Analysis

#### Agreement
Points where all/most LLMs agree:
- ...

#### Divergence
Points where LLMs disagree:
- ...

#### Quality Assessment
| Dimension      | Claude | Codex | Gemini |
|----------------|--------|-------|--------|
| Correctness    | ...    | ...   | ...    |
| Completeness   | ...    | ...   | ...    |
| Code Quality   | ...    | ...   | ...    |
| Explanation    | ...    | ...   | ...    |

#### Recommendation
Based on the comparison: {which response is strongest and why}
```

### 5. Evaluation Modes

- **best-of-n**: Pick the best response and explain why.
- **consensus**: Extract only points all LLMs agree on (high-confidence answers).
- **full-comparison**: Show all responses with detailed analysis (default).
- **merge**: Synthesize the best parts of each response into one improved answer.

## Guardrails

- Never send secrets, credentials, or sensitive data in prompts.
- Keep prompts under 10,000 characters.
- Timeout each CLI at 180 seconds.
- The comparison analysis should be objective and evidence-based.

## Usage Examples

```
# Compare code generation (root agent reads and follows)
skill_execute("multi-llm-judge")
# then: "Write a Python function to find the longest palindromic substring"

# Compare with specific mode
skill_execute("multi-llm-judge")
# then: "consensus mode: What are the best practices for error handling in Go?"
```
