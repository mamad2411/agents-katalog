---
name: opencode-agents
description: "Delegate tasks to oh-my-openagent agents (librarian, oracle, sisyphus, prometheus, atlas, explore, metis, momus) via the oh-my-opencode CLI. Use this skill whenever the user says 'use librarian to', 'use oracle to', 'let librarian', 'ask oracle to', '@librarian', '@oracle', or names any oh-my-openagent agent in the context of doing a task. Also triggers on Chinese equivalents: '用 librarian 做', '用 oracle 做', '让 librarian 帮'. Disambiguation: do NOT trigger for Oracle Database, Oracle Cloud, MongoDB Atlas, or general-purpose exploration verbs unrelated to oh-my-openagent."
---

# OpenCode Agents Skill

Delegate tasks to specialized oh-my-openagent subagents via the `opencode` CLI.

> **Project note**: The plugin was renamed from `oh-my-opencode` to `oh-my-openagent`.
> Canonical repo: https://github.com/code-yeongyu/oh-my-openagent

## Available Agents

| Agent | Mode | Specialization |
|-------|------|---------------|
| **sisyphus** | primary | Orchestration, task delegation, general execution |
| **atlas** | primary | Large codebase exploration, dependency analysis |
| **librarian** | subagent | External documentation lookup, web research, best practices |
| **oracle** | subagent | Analysis, Q&A, explaining complex concepts |
| **prometheus** | subagent | Planning, architecture design, high-level decisions |
| **explore** | subagent | Filesystem exploration, code search |
| **metis** | subagent | Strategy, trade-off analysis |
| **momus** | subagent | Code review, quality assurance, gap/completeness checking |

Primary agents (sisyphus, atlas) are top-level orchestrators. Subagents can be targeted directly via `--agent` but cannot be entry points for a `task()` call.

## How to Invoke

```bash
opencode run '<task prompt>'
```

Use **single quotes** to avoid shell expansion of special characters (see Shell Safety below).

### Optional Flags

| Flag | Description |
|------|-------------|
| `--agent <name>` | Route to a specific primary agent (sisyphus, atlas) |
| `--dir <path>` | Set working directory (defaults to `process.cwd()`) |
| `-m, --model <model>` | Override the model for this run |

### Routing

The message is delivered as plain text to Sisyphus via HTTP JSON — no `@mention` parsing occurs in the CLI path. Sisyphus may internally delegate to subagents via `task(subagent_type="librarian")` etc., but this is **probabilistic LLM behavior** — for simple tasks Sisyphus will often use its own tools directly.

**`--agent` only works for primary agents** (sisyphus, atlas). Passing a subagent name (e.g., `--agent librarian`) falls back to the default agent with a warning.

**To route to a specific subagent**, include its name explicitly in the prompt text. Sisyphus reads this as an instruction to delegate:
```bash
opencode run 'Use librarian to find the official React docs on useEffect'
opencode run 'Ask oracle to analyze the tradeoffs of this architecture'
```

### Examples

```bash
opencode run 'search for best practices on LND channel management'
opencode run 'explain the difference between HTLC and PTLC in Lightning'
opencode run --agent atlas 'analyze dependencies across this monorepo'
opencode run --dir /path/to/project 'find all usages of the payment module'
```

## Execution Flow

1. **Understand the task type** and whether the user named a specific agent.
2. **Read local context if needed** — use local tools (file reads, directory listings) to gather context and embed it in the prompt.
3. **Run the command** via the bash tool. If the user named a specific agent, include it explicitly in the prompt text — this signals Sisyphus to delegate:
   ```bash
   # User named an agent → embed it in the prompt
   opencode run 'Use librarian to search today'"'"'s weather in Tokyo'

   # No agent named → let Sisyphus auto-route
   opencode run 'search today'"'"'s weather in Tokyo'
   ```
4. **Return the output** to the user.
5. If the agent isn't in the list above, check `~/.config/opencode/oh-my-opencode.json` for the full configured agent list.

## Output Handling

- **stdout** — agent's response (typically Markdown)
- **stderr** — progress/debug info; ignore unless diagnosing failures
- **Exit code 0** — success; non-zero — failure
- For long outputs, summarize key findings before returning to the user

## Shell Safety

`oh-my-opencode run` passes messages as JSON over HTTP — the message itself is never shell-executed. However, the shell on the caller side will expand special characters before the CLI receives them.

Always use **single quotes**:
```bash
# Safe
opencode run 'analyze the $HOME variable usage'

# Unsafe — shell expands $HOME before the CLI sees it
opencode run "analyze the $HOME variable usage"
```

If the task contains single quotes, escape them:
```bash
opencode run 'find all usages of the it'\''s pattern'
```

## Notes

- **Config**: `~/.config/opencode/oh-my-opencode.json` — agent models and settings
- **CWD**: inherited from the calling process; override with `--dir <path>`
- **Recursion**: The `task()` tool has built-in recursion protection (max depth 3, cycle detection). Shell-invoked `oh-my-opencode run` starts an independent process tree with no cross-process guard — avoid chaining shell invocations inside tasks already started via `oh-my-opencode run`.
- **If `oh-my-opencode` is not in PATH**: report the error clearly and suggest installing via `npm install -g oh-my-opencode`
