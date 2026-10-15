---
name: claude-use-gemini-acp
description: >
  Delegate a sub-task to Gemini CLI via the Agent Client Protocol (ACP).
  Use this skill whenever you want to hand off work to Gemini — large-context
  summarization, Google Search grounding, tasks that exceed Claude's context window,
  or anything where Gemini's 1M-token window or real-time search gives an advantage.
  Also invoke when the user asks you to "ask Gemini", "check with Gemini", or
  "run this through Gemini". The script handles subprocess lifecycle and ACP
  session setup; you just provide the prompt and read stdout.
version: 1.0.0
---

# Claude → Gemini via ACP

Spawn a Gemini CLI subprocess in ACP mode, send a prompt, stream the response to stdout, and terminate cleanly. No persistent session — one prompt, one response.

## When to use

- The task requires more context than fits in Claude's window
- You want real-time Google Search grounding
- You want a second opinion from a different model
- The user says "ask Gemini", "use Gemini for this", etc.

## Setup (first use only)

```bash
cd ~/.claude/skills/claude-use-gemini-acp/scripts
pnpm install
```

This installs `@agentclientprotocol/sdk` into the local `node_modules/`. Subsequent runs skip this step — pnpm caches the result.

## Usage

```bash
GEMINI_MODEL=gemini-2.5-pro \
TARGET_CWD=/path/to/project \
node ~/.claude/skills/claude-use-gemini-acp/scripts/gemini-delegate.mjs \
  "Summarize the architecture in ARCHITECTURE.md and list the top 3 risks"
```

The response streams to stdout as Gemini generates it. Capture it for use in your response:

```bash
response=$(node ~/.claude/skills/claude-use-gemini-acp/scripts/gemini-delegate.mjs "your prompt")
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `GEMINI_MODEL` | `gemini-2.5-pro` | Model to use |
| `GEMINI_CLI_VERSION` | `nightly` | gemini-cli package version (`nightly` or a specific semver) |
| `TARGET_CWD` | current working dir | Working directory passed to the Gemini session |

## How it works

1. Spawns `pnpm dlx @google/gemini-cli@<version> --acp --yolo --model <model>`
2. Connects via `@agentclientprotocol/sdk`'s `ClientSideConnection` + `ndJsonStream`
3. Sends `initialize` → `newSession` → `prompt` over the ACP session
4. Streams `agent_message_chunk` deltas to stdout as they arrive
5. Terminates the subprocess once the prompt response completes

The `--yolo` flag (`-y`) auto-approves all tool calls inside Gemini's session.

## Prompt construction tips

- Include all relevant context in the prompt string — this is a fresh session with no prior history
- Reference files by absolute path if you want Gemini to read them (it can use its filesystem tools)
- Keep prompts focused: one clear task per invocation
- For multi-step work, do multiple sequential invocations rather than one sprawling prompt

## Error handling

If the script exits non-zero, check stderr for:
- `pnpm dlx` download failures (network, auth)
- Gemini auth errors (`gemini auth login` may be needed)
- ACP initialization failures (version mismatch)

The script does not retry — if something fails, surface the error to the user and suggest re-running after fixing the root cause.
