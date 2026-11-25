---
name: coding-agents
description: "Delegate coding tasks to external CLI coding agents — Claude Code (Anthropic), Codex (OpenAI), and OpenCode (provider-agnostic). Covers CLI flags, PTY/tmux orchestration, print mode, model configuration, and cross-agent patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Codex, OpenCode, Automation, PTY, Code-Review]
    related_skills: [github, subagent-driven-development, writing-plans]
---

# Coding Agents — External CLI Delegation

Unified guide for delegating coding tasks to external autonomous coding agents via the Hermes terminal. Covers **Claude Code** (Anthropic), **Codex** (OpenAI), and **OpenCode** (provider-agnostic open-source).

## When to Use

- User asks to use Claude Code, Codex, or OpenCode for implementation
- You need an external coding agent to implement/refactor/review code
- You need long-running coding sessions with progress checks
- You want parallel task execution in isolated worktrees

## General Principles

| Principle | Why |
|-----------|-----|
| Prefer print/exec mode for one-shot tasks | Cleaner, no dialog handling, structured output |
| Use tmux for multi-turn interactive work | Only reliable way to orchestrate TUI apps |
| Always set `workdir` | Keep agent focused on the right project |
| Set `--max-turns` (or equivalent) | Prevents infinite loops and runaway costs |
| Monitor with `process(action="poll"\|"log")` | Check progress without interfering |
| Clean up tmux sessions | Kill when done to avoid resource leaks |
| Use `--allowedTools` | Restrict capabilities to what the task needs |
| **Tell the agent to read project files first** | Always include "Read CLAUDE.md and all relevant project files for context" in your prompt — never assume it understands the project |
| **Match model to task complexity** | — **Pro** (`deepseek-v4-pro` / `claude-opus-4-7`): architectural decisions, algorithmic/mathematical correctness, constraint-aware logic, edge-case coverage, multi-file orchestration. Covers its cost on tasks where wrong output means rework.<br>— **Flash** (`deepseek-v4-flash` / `claude-sonnet-4-6`): mechanical boilerplate, matplotlib plots, heuristic baselines, trivial CRUD, re-exports, following an existing pattern. 3x cheaper, fast enough for pattern-matching.<br>— **Litmus test**: if a competent junior could do it right with clear specs, use flash. If it needs reasoning about tradeoffs and subtle constraints, use pro. |

## Prompt Architecture

When delegating to a coding agent, structure your prompt into clear sections:

```
TASK: <one-line goal>

CONTEXT:
<what project, what files to read first, relevant background>

WHAT YOU NEED TO DO:
<numbered implementation steps — specific file paths, function signatures, edge cases>

VERIFY:
<exact commands to prove correctness (tests, linters, smoke checks)>

GIT WORKFLOW:
<exact git commands for commit, push, PR creation>

Do NOT:
<things to avoid>
```

This ensures the agent has all context upfront. The verification and git sections are critical — always specify exact commands with expected outcomes so you can trust the result without re-reading every line of generated code.

---

## Section A: Claude Code (Anthropic)

### Prerequisites

```bash
npm install -g @anthropic-ai/claude-code
claude auth login              # Browser OAuth or ANTHROPIC_API_KEY
claude --version               # Requires v2.x+
claude doctor                  # Health check
```

### Print Mode (Preferred — One-Shot)

```bash
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/project", timeout=120)
```

Key flags for print mode:
- `-p, --print` — non-interactive one-shot
- `--max-turns <n>` — prevent runaway loops
- `--max-budget-usd <n>` — cap API spend
- `--output-format json` — structured JSON result with `session_id`, `total_cost_usd`, `num_turns`
- `--json-schema '{"type":"object",...}'` — force structured output
- `--allowedTools 'Read,Edit'` — whitelist specific tools
- `--model <alias>` — sonnet, opus, haiku
- `--effort <level>` — low, medium, high

### Interactive PTY Mode (via tmux)

```bash
terminal(command="tmux new-session -d -s claude -x 140 -y 40")
terminal(command="tmux send-keys -t claude 'cd /project && claude' Enter")
# Handle dialogs
terminal(command="sleep 5 && tmux send-keys -t claude Enter")  # trust
terminal(command="sleep 2 && tmux send-keys -t claude Down && sleep 0.3 && tmux send-keys -t claude Enter")  # permissions
# Send tasks
terminal(command="tmux send-keys -t claude 'Refactor auth module' Enter")
# Monitor
terminal(command="tmux capture-pane -t claude -p -S -50")
```

### Session Continuation

```bash
claude -p 'Continue the refactoring' --continue --max-turns 5
claude -p 'New task' --resume <session_id> --max-turns 10
```

### PR Review

```bash
terminal(command="cd /repo && git diff main...feature | claude -p 'Review this diff for bugs' --max-turns 1", timeout=60)
# Or with --from-pr:
claude -p 'Review PR #42' --from-pr 42 --max-turns 10
```

### Key Pitfalls (Claude Code)

- Interactive mode **requires tmux** — `pty=true` alone isn't enough for TUI orchestration
- `--dangerously-skip-permissions` dialog defaults to "No, exit" — send Down then Enter in interactive, but skip entirely in `-p` mode
- `--max-turns` is print-mode only — ignored in interactive
- Session resumption requires same directory
- Always monitor context health with `/context` — quality degrades above 70%

---

## Section B: Codex (OpenAI)

### Prerequisites

```bash
npm install -g @openai/codex
# OpenAI API key configured in ~/.codex/config.toml
```

**Critical:** Codex only supports OpenAI's proprietary **Responses API (WebSocket)**. It does NOT support Chat Completions API. DeepSeek, Anthropic, and other providers are NOT compatible because they don't speak WebSocket Responses API.

### Model Configuration

```bash
codex -m gpt-5.4 exec 'prompt'       # Built-in OpenAI models
codex --oss --local-provider ollama exec 'hello'  # OSS mode
```

For custom providers, configure in `~/.codex/config.toml`:
```toml
model_provider = "my_provider"
model = "my-model-slug"
model_catalog_json = "/path/to/models.json"
wire_api = "responses"  # Only supported value
```

### One-Shot Tasks

```bash
terminal(command="codex exec 'Add dark mode toggle'", workdir="~/project", pty=true)
```

### Background Mode (Long Tasks)

```bash
terminal(command="codex exec --full-auto 'Refactor auth module'", workdir="~/project", background=true, pty=true)
# Monitor:
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")
# Send input if asked:
process(action="submit", session_id="<id>", data="yes")
```

### Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed, auto-approves file changes |
| `--yolo` | No sandbox, no approvals (fastest) |
| `--oss` | Use open-source provider (Ollama/LM Studio) |
| `-m, --model <MODEL>` | Model slug override |

### Key Pitfalls (Codex)

- **Always use `pty=true`** — hangs without a PTY
- **Git repo required** — refuses to run outside a git directory
- **WebSocket-only** — CCX proxy cannot bridge to non-OpenAI providers (CCX speaks HTTP, Codex needs WebSocket)
- **CC Switch** proxy works for Codex desktop app but NOT CLI (CLI uses WebSocket)

---

## Section C: OpenCode (Provider-Agnostic Open-Source)

### Prerequisites

```bash
npm i -g opencode-ai@latest
# or: brew install anomalyco/tap/opencode
opencode auth list              # Verify provider auth
opencode --version
```

### One-Shot Tasks

```bash
terminal(command="opencode run 'Add retry logic and update tests'", workdir="~/project")
# With file context:
terminal(command="opencode run 'Review config' -f config.yaml -f .env.example", workdir="~/project")
# Force model:
terminal(command="opencode run 'Refactor auth' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
```

### Interactive Sessions (Background)

```bash
terminal(command="opencode", workdir="~/project", background=true, pty=true)
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow")
process(action="poll", session_id="<id>")
# Exit: Ctrl+C (NOT /exit)
process(action="write", session_id="<id>", data="\x03")
```

### Key Flags

| Flag | Effect |
|------|--------|
| `run 'prompt'` | One-shot execution and exit |
| `--continue` / `-c` | Continue last session |
| `--model provider/model` | Force specific model |
| `--file <path>` / `-f` | Attach file(s) |
| `--thinking` | Show model thinking blocks |
| `--agent <name>` | Choose agent (build or plan) |

### Key Pitfalls (OpenCode)

- `/exit` is NOT a valid command — opens agent selector instead. Use Ctrl+C
- `opencode run` (one-shot) does NOT need pty; interactive TUI mode DOES
- PATH mismatch can select wrong binary — check with `which -a opencode`
- Enter may need to be pressed twice to submit in TUI

---

## Cross-Agent Comparison

| Feature | Claude Code | Codex | OpenCode |
|---------|-------------|-------|----------|
| Provider support | Anthropic (OpenRouter via ACP) | OpenAI-only (WebSocket) | Any (OpenRouter, etc.) |
| One-shot mode | `-p` flag | `exec` subcommand | `run` subcommand |
| PTY needed? | Print=no / Interactive=yes | Always yes | Run=no / Interactive=yes |
| Structured output | `--output-format json` | N/A | N/A |
| Session resume | `--continue` / `--resume` | N/A | `-c` / `-s <id>` |
| Cost tracking | Built-in with `--output-format json` | N/A | `opencode stats` |
| Git worktree | `--worktree` flag | Manual | Manual |
| MCP servers | Built-in | N/A | N/A |
| Custom agents | Built-in | N/A | `--agent` flag |

## Parallel Work Pattern — Git Worktree Isolation

When running multiple coding agents on the same repo simultaneously, use **git worktree branches** to avoid conflicts:

```bash
# 1. Create and push branches (one per task)
for branch in feat/task-a feat/task-b feat/task-c; do
  git checkout -b "$branch" origin/main
  git push origin "$branch"
  git checkout main
done

# 2. Create isolated worktrees
WORKTREE_BASE="/tmp/bgg-worktree"
for branch in feat/task-a feat/task-b feat/task-c; do
  git worktree add "$WORKTREE_BASE/$branch" "$branch"
done

# 3. Launch agents in parallel, each in its own worktree
terminal(command="claude -p '$(cat /tmp/prompt-A.md)'", 
         workdir="/tmp/bgg-worktree/feat/task-a", background=true, notify_on_complete=true)
terminal(command="claude -p '$(cat /tmp/prompt-B.md)'", 
         workdir="/tmp/bgg-worktree/feat/task-b", background=true, notify_on_complete=true)

# 4. After all complete: review, push, create PRs, merge
for dir in /tmp/bgg-worktree/feat/task-*; do
  (cd "$dir" && git push origin HEAD && gh pr create --fill)
done

# 5. Check Copilot PR reviews before merging
# Copilot leaves inline comments that may flag real bugs — check before squash-merge
for branch in feat/task-a feat/task-b feat/task-c; do
  gh pr view "$branch" --json comments,reviews 2>/dev/null | python3 -c "
import json,sys
data = json.load(sys.stdin)
for r in data.get('reviews', []):
    if r.get('state') in ('CHANGES_REQUESTED', 'COMMENTED'):
        print(f'{r[\"author\"][\"login\"]}: {r[\"state\"]}')
"
  # Flag comments containing keywords suggesting real bugs
  gh pr view "$branch" --json comments | python3 -c "
import json,sys
data = json.load(sys.stdin)
for c in data.get('comments', []):
    body = c.get('body','')
    if any(kw in body.lower() for kw in ['bug','error','crash','invalid','wrong','brittle']):
        print(f'  ⚠️  {c.get(\"path\",\"?\")}:{c.get(\"line\",\"?\")}')
        print(f'     {body[:200]}')
" 2>/dev/null || true
done
# If issues found, fix them in a follow-up branch before merging main

# 5. Clean up
rm -rf /tmp/bgg-worktree/
git worktree prune
```

**Rules:**
- Each agent gets a **dedicated prompt file** with full context (see Prompt Architecture above)
- Prompts must include: context → files to read → implementation spec → verification commands → git workflow
- After completion, **you** review the diff before creating PRs
- Handle merge conflicts between branches in the main repo, not in worktrees
- Clean up both worktrees and branches after merging

Compare with simple background terminal launches (no worktree needed for one-off tasks):

## Verification

For any coding agent task, verify:
- [ ] Agent completed successfully (exit code 0, expected output)
- [ ] Expected files changed or created
- [ ] Tests pass (run relevant test suite yourself)
- [ ] No secrets or credentials in changed files
- [ ] No unintended side effects (unrelated files modified)

## Pitfalls (All Agents)

- **Don't kill slow sessions** — agents may be doing multi-step work; check progress first
- **Set timeouts generously** — complex tasks can take 5-10 minutes
- **Report actual outcomes** — summarize what changed, not just "it worked"
- **Path mismatch** — shell environments can resolve different binaries than expected
- **Shared workdir** — never share one working directory across parallel agent sessions
- **Agent may ask questions** — respond via `process(action="submit")` in background mode