---
name: harness-optimizer
description: Optimize an AI agent's harness for MCP-Atlas benchmark. Use when analyzing execution traces, diagnosing failures, and proposing improved prompts, skills, or harness code.
---

# Harness Optimizer

You are optimizing an AI agent's harness for MCP-Atlas — a benchmark
of tool-calling tasks where the agent uses Model Context Protocol (MCP) servers
to answer questions by querying APIs, databases, filesystems, and web services.

## Objective

Maximize the agent's coverage score on the benchmark. The agent receives a task
prompt and a set of MCP tools, makes tool calls to gather information, and
produces a final answer. A judge LLM scores the answer against ground-truth
claims (fulfilled=1.0, partially_fulfilled=0.5, not_fulfilled=0.0). The
**harness** controls what the agent sees (prompts, strategies) and how it
behaves before each task.

## What You Can Modify

- `prompts/system.md` — the agent's system prompt
- `skills/*/SKILL.md` — on-demand skill library (YAML frontmatter + markdown body)
- `harness.py` — scaffolding code with three hook points:
  - `build_system_prompt(base_prompt, skills, task_prompt) -> str` — override prompt assembly
  - `build_user_prompt(task_id, task_input) -> str | None` — customize per-task prompt
  - `pre_solve(task_metadata) -> dict` — preprocess task metadata before the agent loop
- `tools/` — tool implementations
- `memory/*.jsonl` — episodic memory entries

## What You Must NOT Do

- Do not modify anything under `evolution/` (read-only archive)
- Do not hardcode task-specific answers or task IDs into any file
- Do not break the agent's MCP tool interface

## The Candidate Archive

`evolution/candidates/` is your primary knowledge source. Each subdirectory contains:

```
cycle_NNN_cand_M/
├── snapshot/        # Complete workspace files at time of proposal
├── scores.json      # {score, cost, selected, pareto_optimal, ...}
└── traces/          # Symlink to observation batch (full execution traces)
```

Browse it freely:
```bash
ls evolution/candidates/
cat evolution/candidates/*/scores.json | jq '.score'
grep -r "pattern" evolution/candidates/*/snapshot/
diff evolution/candidates/cycle_001_cand_0/snapshot/harness.py \
     evolution/candidates/cycle_002_cand_0/snapshot/harness.py
cat evolution/candidates/<name>/traces/*.jsonl | jq '.task_id, .success, .score'
```

Execution traces (JSONL) contain for each task: task_id, task_input, success,
score, feedback_detail, and full conversation (every message + tool call).

## How to Work

1. **Diagnose** — Browse `evolution/candidates/`. Compare high-scoring vs
   low-scoring candidates' code and traces. Use `grep`, `jq`, `diff` selectively.
   You do NOT need to read everything.
2. **Hypothesize** — Form specific hypotheses about what causes failures and
   what patterns lead to higher scores. Look for recurring failure modes in traces.
3. **Propose** — Write new workspace files. You may:
   - Make targeted edits to the current workspace
   - Copy a high-scoring prior candidate's code and improve on it
   - Write completely new files from scratch
   Choose whichever approach your diagnosis suggests will work best.

## Tips for MCP-Atlas

- Tasks span calendars, databases (MongoDB), filesystems, git repos, web search,
  geographic/OSM queries, Wikipedia lookups, and multi-step API orchestration
- Common failure modes: incomplete answers (missing sub-parts of compound questions),
  not retrying failed tool calls with different parameters, guessing instead of
  querying tools, not exploring filesystem/repos before answering
- The `pre_solve` hook can normalize task metadata (e.g. fix tool format issues)
- Multi-part questions need systematic decomposition — count required facts, verify each
- Geographic questions need routing tools for distances, not coordinate estimation
- The agent has access to 20 MCP servers — encourage it to explore broadly
