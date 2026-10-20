---
name: claude-code-stream-json-driver
description: Drive the Claude Code CLI non-interactively via stream-json — build input on stdin, parse typed events on stdout, handle session resume and token usage.
category: agents
version: 1.0.0
tags: [claude-code, stream-json, cli, llm, streaming]
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

- You're building a server or daemon that needs to run Claude Code autonomously (no TTY, no user confirmation).
- You need streaming events (text, tool_use, tool_result) not just a final answer.
- You want to persist session IDs so the user can resume later.

## Steps

1. Invoke Claude with the stream-json protocol flags:
   ```
   claude -p \
     --output-format stream-json \
     --input-format  stream-json \
     --verbose \
     --strict-mcp-config \
     --permission-mode bypassPermissions \
     [--model <id>] [--max-turns <n>] \
     [--append-system-prompt <text>] \
     [--resume <session_id>] \
     [--mcp-config <path-to-temp-json>]
   ```
2. Write the user prompt to stdin as one JSON line, then close stdin:
   ```go
   input := map[string]any{
     "type": "user",
     "message": map[string]any{
       "role": "user",
       "content": []map[string]string{{"type": "text", "text": prompt}},
     },
   }
   b, _ := json.Marshal(input)
   stdin.Write(append(b, '\n'))
   stdin.Close()
   ```
3. Read stdout line-by-line with a large buffer (tool results can be huge):
   ```go
   scanner := bufio.NewScanner(stdout)
   scanner.Buffer(make([]byte, 0, 1024*1024), 10*1024*1024)
   for scanner.Scan() {
     var msg claudeSDKMessage
     if err := json.Unmarshal(scanner.Bytes(), &msg); err != nil { continue }
     switch msg.Type {
     case "assistant": handleAssistantBlocks(msg) // text, thinking, tool_use
     case "user":      handleToolResultBlocks(msg)
     case "system":    sessionID = msg.SessionID
     case "result":    finalText = msg.ResultText; isError = msg.IsError
     case "log":       forwardLog(msg.Log)
     }
   }
   ```
4. Accumulate token usage per model name from `message.usage` on assistant events:
   ```go
   u := usage[content.Model]
   u.InputTokens  += content.Usage.InputTokens
   u.OutputTokens += content.Usage.OutputTokens
   u.CacheReadTokens  += content.Usage.CacheReadInputTokens
   u.CacheWriteTokens += content.Usage.CacheCreationInputTokens
   usage[content.Model] = u
   ```
5. Block protocol-critical flags from any user-provided `custom_args` so they don't break the wire format:
   ```go
   var claudeBlockedArgs = map[string]blockedArgMode{
     "-p":                blockedStandalone,
     "--output-format":   blockedWithValue,
     "--input-format":    blockedWithValue,
     "--permission-mode": blockedWithValue,
     "--mcp-config":      blockedWithValue,
   }
   ```
6. Strip parent-Claude env leakage before spawning:
   ```go
   func isFilteredChildEnvKey(key string) bool {
     return key == "CLAUDECODE" ||
            strings.HasPrefix(key, "CLAUDECODE_") ||
            strings.HasPrefix(key, "CLAUDE_CODE_")
   }
   ```
7. On failed runs where you requested `--resume <id>` and Claude emitted a different session ID, signal the caller to retry with fresh session by reporting empty session ID:
   ```go
   if failed && requestedResume != "" && emitted != "" && emitted != requestedResume {
     return ""
   }
   return emitted
   ```

## Example

Minimal Go wrapper is ~200 LOC; see `server/pkg/agent/claude.go` in the source repo for the full reference implementation.

## Caveats

- `--permission-mode bypassPermissions` makes the run fully autonomous — use only in a sandboxed environment you trust.
- If the sandbox refuses to pass MCP config by value, write the JSON to a temp file and pass `--mcp-config <path>`; clean up the file after the goroutine that owns the process exits.
- 10MB max-token is a reasonable upper bound for Read/Write tool results; bump if you see "token too long" errors.
- Don't read stderr line-by-line; pipe it to a logger that Debug-level logs lines so noise doesn't dominate.
