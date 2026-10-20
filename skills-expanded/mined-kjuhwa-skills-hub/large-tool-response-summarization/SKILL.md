---
name: large-tool-response-summarization
description: When a tool result exceeds a token threshold, save the full response to disk under the session dir, feed it to a cheap summarizer (Haiku) with an intent-aware prompt, and return the summary + file reference to the agent.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [agents, summarization, large-responses, cost-control]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/utils/large-response.ts
imported_at: 2026-04-18T00:00:00Z
---

# Large tool response summarization

## When to use
- Agent calls tools that can return 60KB+ of output (log fetches, DB dumps, API list responses).
- Feeding the full response into the LLM wastes tokens and pushes context window limits.
- Want the agent to still be able to Read/Grep the full result afterward.

## How it works
1. After the tool runs, estimate tokens: `Math.ceil(text.length / 4)` (close enough, cheap).
2. If under `TOKEN_LIMIT` (~15000 tokens = ~60KB): return as-is.
3. If over: save full response to `<sessionDir>/long_responses/<timestamp>_<toolName>.<ext>` - deterministic filename so it's greppable later.
4. If response is **detectable binary** (base64-encoded image/PDF, detected via magic-byte signature): save the binary directly with the right extension.
5. If text is under `MAX_SUMMARIZATION_INPUT` (~100k tokens = ~400KB): run a small LLM (Haiku, Gemini Flash, etc.) with a prompt that includes the tool's `_intent` metadata (see `mcp-tool-intent-metadata-injection`).
6. If text is over the summarization limit: skip LLM call; return head + tail preview + file path.
7. Return to the agent a synthetic tool result like:
   ```
   <summary...>
   
   Full response saved to: long_responses/<file> (<bytes> bytes)
   Use Read/Grep to inspect details.
   ```
8. Keep the saved path *relative* to session dir so sessions stay portable when moved.

## Example
```ts
export const TOKEN_LIMIT = 15000;
export const MAX_SUMMARIZATION_INPUT = 100000;

async function guardLargeResult(text: string, opts: { sessionDir, tool, intent, runMini }) {
  const tokens = estimateTokens(text);
  if (tokens <= TOKEN_LIMIT) return text;

  const { absolutePath, relativePath } = saveToDisk(text, opts.sessionDir, opts.tool);
  if (tokens > MAX_SUMMARIZATION_INPUT) {
    return `[truncated - ${formatBytes(text.length)} saved to ${relativePath}]\n\n` +
           text.slice(0, 2000) + '\n...\n' + text.slice(-2000);
  }
  const summary = await opts.runMini({
    prompt: `Tool intent: ${opts.intent}\nSummarize this output focused on that intent:\n${text}`,
    model: 'haiku',
  });
  return `${summary}\n\nFull response: ${relativePath} (${formatBytes(text.length)})`;
}
```

## Gotchas
- Detect binary BEFORE trying to summarize - dumping 2MB of base64 into Haiku is both wasteful and unhelpful.
- Use the tool's `_intent` field (see related skill) in the summarizer prompt so summaries keep the user's goal in view.
- Save to a session-scoped directory, not a global temp - the agent should be able to Read/Grep it later in the same session.
- Keep `TOKEN_LIMIT` generous (15k) - too aggressive means the agent loses fidelity on medium-size responses.
- Use `sessionPath`-portable tokens (e.g. `{{SESSION_PATH}}`) so moving the session dir later still resolves paths.
