---
name: gemini-use-claude-acp
description: >
  Delegate a sub-task to Claude Code via the Agent Client Protocol (ACP).
  Use this skill whenever you want to hand off work to Claude — complex agentic
  coding with MCP tool access, detailed multi-file refactors, tasks requiring
  Claude's reasoning style, or anything where Claude's strengths give an advantage.
  Also invoke when the user asks you to "ask Claude", "use Claude for this", or
  "run this through Claude". The script handles subprocess lifecycle and ACP
  session setup; you just provide the prompt and read stdout.
version: 1.0.0
---

# Gemini → Claude via ACP

Spawn a Claude Code ACP adapter subprocess, send a prompt, stream the response to stdout, and terminate cleanly. No persistent session — one prompt, one response.

## When to use

- The task requires complex multi-step agentic coding with MCP tool access
- You want Claude's reasoning on a specific problem
- The user says "ask Claude", "use Claude for this", etc.
- You want a second opinion from a different model

## Setup (first use only)

```bash
cd ~/.gemini/skills/gemini-use-claude-acp/scripts
pnpm install
```

This installs `@agentclientprotocol/sdk` into the local `node_modules/`. Subsequent runs skip this step.

## Usage

```bash
CLAUDE_MODEL=claude-sonnet-4-6 \
TARGET_CWD=/path/to/project \
node ~/.gemini/skills/gemini-use-claude-acp/scripts/claude-delegate.mjs \
  "Refactor the auth module to use JWT tokens. The code is in src/auth/."
```

The response streams to stdout as Claude generates it. Capture it:

```bash
response=$(node ~/.gemini/skills/gemini-use-claude-acp/scripts/claude-delegate.mjs "your prompt")
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `CLAUDE_MODEL` | `claude-sonnet-4-6` | Model to use (applied via ACP `unstable_setSessionModel`) |
| `TARGET_CWD` | current working dir | Working directory passed to the Claude session |

## How it works

1. Spawns `pnpm dlx @zed-industries/claude-code-acp` with:
   - `CLAUDE_CODE_SKIP_PERMISSIONS=1` — auto-approves all tool calls
   - `TERM=dumb` — prevents ANSI escape sequences in output
   - `CLAUDECODE` unset — prevents the adapter refusing to start inside another Claude session
   - `~/.local/bin` prepended to `PATH` — ensures the `claude` binary is found
2. Connects via `@agentclientprotocol/sdk`'s `ClientSideConnection` + `ndJsonStream`
3. Sends `initialize` → `newSession` → `unstable_setSessionModel` → `prompt` over ACP
4. Streams `agent_message_chunk` deltas to stdout as they arrive
5. Terminates the subprocess once the prompt response completes

## Prompt construction tips

- Include all relevant context in the prompt string — this is a fresh session with no prior history
- Reference files by absolute path if you want Claude to read/edit them
- Keep prompts focused: one clear task per invocation
- Claude can use its MCP tools (filesystem, shell, etc.) during the session

## Error handling

If the script exits non-zero, check stderr for:
- `pnpm dlx` download failures (network, auth)
- Claude auth errors — ensure `claude` CLI is authenticated
- `CLAUDECODE` environment variable being set (indicates you're running inside Claude Code; the adapter refuses to nest)
- ACP initialization failures

The script does not retry — surface the error to the user and suggest re-running after fixing the root cause.
