# /anima-codex — Delegate Tasks to Codex Runtime

**Purpose:** Hand off coding tasks to OpenAI Codex for parallel execution. Use when you need a second implementation pass, deeper root-cause analysis, or want to offload substantial coding work.

---

## WHEN TO USE

- **Stuck on a bug**: hand the codebase + error to Codex for a fresh diagnosis
- **Need a second implementation**: get an alternative approach to compare
- **Heavy refactoring**: let Codex handle boilerplate while you focus on architecture
- **Code review**: have Codex review code you just wrote
- **Parallel work**: delegate independent tasks while you continue other work

## HOW TO USE

### Option 1: Codex Rescue Agent (recommended for complex tasks)
Use the `codex:codex-rescue` subagent type when spawning an Agent:

```
Agent(
  subagent_type="codex:codex-rescue",
  prompt="<detailed task description with file paths and context>",
  description="Short task summary"
)
```

The Codex rescue agent:
- Shares the same filesystem (reads/writes same repo)
- Has full bash access
- Can run tests, build, lint
- Returns results back to you

### Option 2: Direct Codex CLI
For quick tasks, run codex directly:

```bash
codex -q "task description" --file path/to/relevant/file.py
```

Flags:
- `-q` — quiet mode (less verbose)
- `--file` — point codex at specific files
- `--approval-mode full-auto` — let it run without confirmation

### Option 3: Background Codex
For long-running tasks:

```bash
nohup codex -q "task" --approval-mode full-auto > /tmp/codex_task.log 2>&1 & disown
```

## TASK DELEGATION PATTERNS

### Bug Fix
```
"Read the error in /mnt/artifacts-datai/logs/project_{module}/train.log.
The training crashes at epoch 3 with CUDA OOM.
Investigate the code in src/anima_{module}/train.py and fix the memory leak.
Run a 2-step smoke test after fixing."
```

### Code Review
```
"Review all changes in project_{module} since the last commit.
Check for: mock data usage, hardcoded paths, missing error handling,
paper alignment issues. Report findings."
```

### Implementation
```
"Implement the data loader for project_{module} following the paper spec in PRD.md.
Dataset is at /mnt/forge-data/datasets/{dataset}/.
Must handle: train/val/test splits, proper transforms, DataLoader with num_workers=4.
Write tests in tests/test_data_loader.py."
```

### Export Pipeline
```
"Run /anima-hf-strategy on project_{module}.
Export: pth → safetensors → ONNX → TRT FP16/FP32.
Push all to HuggingFace ilessio-aiflowlab/project_{module}.
Verify with dry-run after push."
```

## RULES

- ALWAYS provide full file paths (Codex doesn't know your cwd)
- ALWAYS specify the module name and what paper it implements
- ALWAYS tell Codex where data lives on disk
- Include relevant config file paths
- Tell Codex about the training standards: /home/datai/.claude/rules/training_standards.md
- Tell Codex about GPU server layout: /home/datai/.claude/rules/gpu_server.md
- Codex shares your filesystem — changes it makes are real
- Review Codex output before committing

## ON GPU SERVER

When delegating server-side tasks, SSH first:
```bash
ssh datai_srv7_development "cd /mnt/forge-data/modules/project_{module} && codex -q 'task' --approval-mode full-auto"
```

Or inside a tmux session:
```bash
tmux new -s CODEX_{MODULE} -c /mnt/forge-data/modules/project_{module}
# then run codex inside tmux
```

## DO NOT
- Don't delegate trivial tasks (reading a file, checking git status)
- Don't run Codex and Claude on the same files simultaneously without coordination
- Don't let Codex push to git without your review
- Don't forget to check Codex's output — it's good but not infallible
