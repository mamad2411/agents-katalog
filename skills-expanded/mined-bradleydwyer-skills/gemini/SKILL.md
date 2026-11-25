---
name: gemini
description: Run Google's Gemini CLI as a secondary AI agent from within Claude Code. Use this skill whenever the user wants to delegate a task to Gemini, get Gemini's perspective or a second opinion, use Gemini-specific capabilities (like its native Google Search), or manage the Gemini CLI (extensions, MCP servers, sessions). Trigger on phrases like "ask Gemini", "use Gemini", "have Gemini do", "second opinion", "what does Gemini think", or any reference to the Gemini CLI tool. Also trigger when the user wants to run a task in a sandboxed Gemini environment. Note: the Gemini CLI is a software engineering agent — it does not support image generation natively.
---

# Gemini CLI Skill

Run Google's Gemini CLI (`gemini`) as a secondary AI agent directly from Claude Code. The CLI is installed at `/opt/homebrew/bin/gemini`.

## When to Use This

- The user wants Gemini to perform a task (code generation, analysis, research)
- The user wants a second opinion from a different model
- The user wants to leverage Gemini's native Google Search
- The user wants to manage Gemini CLI configuration, extensions, or MCP servers

## Core: Running Prompts (Headless Mode)

Always use `-p` for non-interactive execution from Claude Code. This runs the prompt and exits with the result.

```bash
gemini -p "your prompt here"
```

### Choosing the Right Flags

Build the command by combining these flags as needed:

| Flag | Purpose | Values |
|------|---------|--------|
| `-p "prompt"` | Headless mode (required for non-interactive use) | Any string |
| `-m model` | Model selection | `auto` (default), `pro`, `flash`, `flash-lite` |
| `-o format` | Output format | `text` (default), `json`, `stream-json` |
| `--approval-mode` | Tool approval | `default`, `auto_edit`, `yolo`, `plan` |
| `-s` | Sandbox mode | Flag only |
| `-r session` | Resume session | `latest`, index number, or UUID |

### Output Format Selection

- **`text`** (default) — Use when the user just wants to see Gemini's response. Good for most tasks.
- **`json`** — Use when you need to parse Gemini's response programmatically. Returns `{"response": "...", "stats": {...}}`.
- **`stream-json`** — Use for long-running tasks where you want progress. Returns newline-delimited JSON events.

### Approval Mode Selection

- **`yolo`** — Use for fully automated tasks where Gemini needs to read/write files, run commands, etc. without confirmation. This is the right default when Claude Code is orchestrating Gemini as a sub-agent.
- **`plan`** — Use when the user wants Gemini to research and plan without making changes.
- **`auto_edit`** — Middle ground: auto-approves file edits but confirms shell commands.
- **`default`** — Don't use from Claude Code (it requires interactive confirmation).

### Piping Input

Pipe file contents or command output as context:

```bash
cat file.py | gemini -p "review this code"
echo "data" | gemini -p "analyze this"
```

The stdin content is prepended to the prompt.

## Common Patterns

### Ask Gemini a Question
```bash
gemini -p "explain how Kubernetes services work"
```

### Get a Second Opinion on Code
```bash
cat src/auth.py | gemini -p "review this code for security issues" -m pro
```

### Automated File Operations
When Gemini needs to read/write files or run commands as part of the task:
```bash
gemini -p "refactor the error handling in src/api.ts to use a Result type" --approval-mode yolo
```

### Research with Google Search
Gemini has built-in Google Search. Useful for up-to-date information:
```bash
gemini -p "what are the latest changes in React 20?" -m flash
```

### Sandboxed Execution
Run Gemini in a sandbox when the task involves untrusted code or you want isolation:
```bash
gemini -p "run and test this script" -s --approval-mode yolo
```

### Resume a Previous Session
```bash
gemini -r latest -p "continue where we left off"
```

## Exit Codes

After running a Gemini command, check the exit code:

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Parse and present the output |
| 1 | Error (API failure, etc.) | Report the error to the user |
| 42 | Input error (bad prompt/args) | Fix the command and retry |
| 53 | Turn limit exceeded | The task was too complex; suggest breaking it down |

## CLI Management Commands

These don't need `-p` — they're direct CLI operations:

### Extensions
```bash
gemini extensions list                    # List installed extensions
gemini extensions install <git-url>       # Install from Git
gemini extensions install <path>          # Install from local path
gemini extensions enable/disable <name>   # Toggle extension
gemini extensions update --all            # Update all
```

### MCP Servers
```bash
gemini mcp list                           # List servers and tools
gemini mcp add <name> <command> [args]    # Add a server
gemini mcp remove <name>                  # Remove a server
gemini mcp enable/disable <name>          # Toggle server
```

### Sessions
```bash
gemini --list-sessions                    # List saved sessions
gemini --delete-session <index>           # Delete a session
gemini -r <index>                         # Resume a session (interactive)
```

## Tips

- For quick questions, use `-m flash` (faster, cheaper) rather than the default `pro`
- For code-heavy tasks, use `-m pro` for best quality
- Always use `--approval-mode yolo` when orchestrating Gemini as a sub-agent, unless the user specifically wants to review Gemini's actions
- If the prompt contains shell-special characters, use a heredoc or single quotes
- For very long prompts, write them to a temp file and pipe: `cat /tmp/prompt.txt | gemini -p "do this"`
- Gemini's working directory matters — it reads `.gemini/GEMINI.md` for project context, similar to Claude's `CLAUDE.md`
