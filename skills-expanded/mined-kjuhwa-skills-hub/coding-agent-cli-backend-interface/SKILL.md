---
name: coding-agent-cli-backend-interface
description: Unified Go/TS interface for invoking any coding-agent CLI (Claude, Codex, OpenCode, Gemini, Cursor, etc.) behind one streaming Execute/Session/Result contract.
category: agents
version: 1.0.0
tags: [agents, cli, abstraction, streaming, llm]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Your product spawns multiple coding-agent CLIs and needs a single API to drive them.
- Each agent speaks a slightly different stream format (JSON-lines, event-stream, custom).
- You want to add a new agent provider without touching the UI or server routing layer.

## Steps

1. Define the contract once:
   ```go
   type Backend interface {
       Execute(ctx context.Context, prompt string, opts ExecOptions) (*Session, error)
   }
   type ExecOptions struct {
       Cwd, Model, SystemPrompt string
       MaxTurns                 int
       Timeout                  time.Duration
       ResumeSessionID          string
       CustomArgs               []string
       McpConfig                json.RawMessage
   }
   type Session struct {
       Messages <-chan Message   // streaming, closed on completion
       Result   <-chan Result    // exactly one value then closed
   }
   type Message struct {
       Type    MessageType  // text | thinking | tool-use | tool-result | status | error | log
       Content string
       Tool    string
       CallID  string
       Input   map[string]any
       Output  string
       Level   string
   }
   type Result struct {
       Status     string  // completed | failed | aborted | timeout
       Output     string
       Error      string
       DurationMs int64
       SessionID  string
       Usage      map[string]TokenUsage
   }
   ```
2. Factory dispatches by name:
   ```go
   func New(agentType string, cfg Config) (Backend, error) {
       switch agentType {
       case "claude":   return &claudeBackend{cfg}, nil
       case "codex":    return &codexBackend{cfg}, nil
       case "opencode": return &opencodeBackend{cfg}, nil
       // ...
       default: return nil, fmt.Errorf("unknown agent type: %q", agentType)
       }
   }
   ```
3. Each backend follows the same pattern:
   - Resolve binary path; `exec.LookPath` early to fail fast with a clear error.
   - Build args (protocol-critical flags hardcoded; user `CustomArgs` pass through a deny-list filter).
   - Spawn with a wrapping context + timeout + `WaitDelay`.
   - Stream stdout line-by-line through a buffered scanner with a 10MB max-token size.
   - Push parsed messages onto the Messages channel (non-blocking drop if full — final output is accumulated separately).
   - On exit, classify outcome: `context.DeadlineExceeded` → "timeout", `context.Canceled` → "aborted", exit error → "failed", else "completed".
4. Common helpers (shared by all backends):
   - `mergeEnv` that strips parent-agent env keys (e.g. `CLAUDECODE_*`) to prevent child-in-parent session leakage.
   - `filterCustomArgs` per-backend deny-list for protocol flags.
   - `writeMcpConfigToTemp` for agents that accept `--mcp-config <path>`.
   - `resolveSessionID` to distinguish "resume succeeded" from "fresh session with same failure".
5. Provide a stable launch header per provider for UI display:
   ```go
   var launchHeaders = map[string]string{
       "claude":   "claude (stream-json)",
       "codex":    "codex app-server",
       "opencode": "opencode run (json)",
       // ...
   }
   ```

## Example

```go
backend, err := agent.New("claude", agent.Config{ ExecutablePath: "/usr/local/bin/claude" })
session, err := backend.Execute(ctx, "fix the login bug", agent.ExecOptions{ Cwd: wd, Timeout: 20*time.Minute })
for msg := range session.Messages {
    switch msg.Type {
    case agent.MessageText:      uiStream.Text(msg.Content)
    case agent.MessageToolUse:   uiStream.ToolStart(msg.Tool, msg.CallID, msg.Input)
    case agent.MessageToolResult: uiStream.ToolEnd(msg.CallID, msg.Output)
    }
}
result := <-session.Result
persistUsage(result.SessionID, result.Usage)
```

## Caveats

- Bounded channels (e.g. 256) prevent memory blowup under slow consumers but mean some streaming messages can be dropped — always accumulate final output into `Result.Output` as a safety net.
- Token usage is per-model, not per-session: a run that switches Claude models mid-conversation has a map with multiple keys.
- When adding a new backend, mirror `claudeBackend` structure exactly; the similarity is on purpose — it's what lets the orchestrator treat all providers uniformly.
