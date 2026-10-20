---
allowed-tools: Agent, Read, Glob, Grep, Write, Edit, Bash, TaskCreate, TaskGet, TaskList, TaskOutput, TaskUpdate
description: Fan out parallel research-codebase agents across multiple topics and collect results
argument-hint: [comma-separated research questions] [optional: comma-separated file destinations]
model: opus
---

# Purpose

Fan out a swarm of primary agents, each invoking the `/research-codebase` skill for one research question, and collect all results into the specified file destinations. Since `/research-codebase` itself spawns parallel Explore sub-agents, this creates a two-tier agent swarm. Follow the `Instructions` and `Workflow` to orchestrate all agents and report when complete.

## Variables

QUESTIONS: $0
DESTINATIONS: $1
DEFAULT_OUTPUT_DIR: temp/research

## Instructions

- `QUESTIONS` is required — a comma-separated list of research topics
- `DESTINATIONS` is optional — a comma-separated list of file paths. If omitted, each agent saves to the `/research-codebase` default location (`DEFAULT_OUTPUT_DIR/`) and those paths are reported back
- If `DESTINATIONS` is provided, it MUST have the same length as `QUESTIONS` — each question maps 1:1 to a destination file path
- Each primary agent is launched via the Agent tool with a prompt that invokes `/research-codebase` for one question, then (if a destination is specified) moves the output to the corresponding destination
- `/research-codebase` internally spawns 2-6 Explore sub-agents per question — so expect high concurrency. This is intentional.
- Launch ALL primary agents in a SINGLE message using multiple parallel Agent tool calls — do NOT launch them sequentially
- Each agent MUST be run in the foreground (NOT background) — you need their results before you can report
- Actually, because you need ALL to complete but they are independent: launch them ALL in background, then poll with TaskList/TaskGet until all complete
- Wait for every agent to finish before producing the final report
- If an agent fails, note the failure in the report but do not abort other agents
- Each agent's prompt should instruct it to:
  1. Run `/research-codebase` with the assigned question via the Skill tool
  2. After `/research-codebase` completes, find the research document it created in `DEFAULT_OUTPUT_DIR/`
  3. If a destination was specified, move (rename) that document to the destination path, creating parent directories if needed
  4. Return the final file path (moved or default) as confirmation
- Trim whitespace from each question and destination after splitting on commas

## Workflow

1. Parse `QUESTIONS` by splitting on commas — trim each entry.
2. If `DESTINATIONS` is provided and non-empty, parse it by splitting on commas — trim each entry. Validate it has the same length as `QUESTIONS`. If lengths differ, stop and tell the user.
3. If destinations are provided, ensure each parent directory exists via Bash `mkdir -p`.
4. Launch ALL agents in parallel in a single message — one Agent tool call per question. Each agent prompt should be:
   - **With destination:**
     ```
     Run the /research-codebase skill with this question: "<question>"

     After it completes, find the most recently created .md file in temp/research/ and move it to: <destination>
     Create parent directories with mkdir -p if needed.

     Return ONLY the final file path on success, or "FAILED: <reason>" on failure.
     ```
   - **Without destination:**
     ```
     Run the /research-codebase skill with this question: "<question>"

     After it completes, find the research document it created in temp/research/.

     Return ONLY the file path on success, or "FAILED: <reason>" on failure.
     ```
5. Wait for all agents to complete.
6. Collect each agent's result — the destination path or failure message.
7. Produce the report.

## Report

Return a summary table:

```
| # | Question | Destination | Status |
|---|----------|-------------|--------|
| 1 | ...      | ...         | saved / FAILED: reason |
```

Followed by:
- Total agents launched
- Successful vs failed count
- List of all saved file paths (for easy copy-paste)
