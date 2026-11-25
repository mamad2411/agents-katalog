---
name: "agent-sdk"
description: "Build AI agents using the Claude Agent SDK with tool use, memory, and multi-step orchestration"
---

# Claude Agent SDK

## When to activate
Building a Python or TypeScript application that uses Claude Code capabilities programmatically; deploying Claude as an autonomous agent inside a product; writing code that drives the `claude` CLI in non-interactive mode; scripting agentic workflows that need tool calls, retries, and context management handled automatically.

## When NOT to use
Using Claude Code interactively in the terminal — that is the default experience, not an SDK use case; building a simple chatbot or single-turn Q&A interface (use the Messages API directly); when Anthropic Managed Agents is a better fit (hosted infrastructure, automatic scaling, built-in memory persistence).

## Instructions

**What the Agent SDK is:**
Same tool loop, context management, and agent capabilities as interactive Claude Code — packaged as a library you embed in your own application. You control the infrastructure; Anthropic provides the model and agent loop.

**SDK vs alternatives — choose the right layer:**

| Need | Use |
|---|---|
| Embed agentic Claude in your app, own the infra | Agent SDK |
| Agentic Claude hosted by Anthropic, hands-off ops | Managed Agents |
| Single-turn responses, no tool loop needed | Messages API |
| Interactive terminal workflow | Claude Code CLI |

**Installation:**

Python:
```bash
pip install claude-code-sdk
```

TypeScript:
```bash
npm install @anthropic-ai/claude-code
```

**`--bare` flag via options:** Skips `CLAUDE.md` loading and MCP server discovery. Use this in CI and scripting contexts where startup speed matters — approximately 10× faster initialization.

**Billing (June 15, 2026+):** Agent SDK sessions draw from a dedicated Agent SDK credit pool, separate from interactive session limits.

**In-process tools:** Tools run in-process rather than spawning subprocesses. Use this for high-frequency calls where subprocess overhead adds up.

**Cloud provider support:** AWS Bedrock, Google Vertex AI, and Microsoft Azure AI Foundry are all supported. Configure via environment variables — no SDK code changes required.

**Python example:**
```python
import asyncio
from claude_code_sdk import query, ClaudeCodeOptions

async def run_agent(task: str):
    options = ClaudeCodeOptions(system_prompt="You are a code reviewer.")
    async for message in query(prompt=task, options=options):
        if message.type == "result":
            print(message.result)

asyncio.run(run_agent("Review this PR diff and list security issues"))
```

**TypeScript example:**
```typescript
import { query, ClaudeCodeOptions } from "@anthropic-ai/claude-code";

const options: ClaudeCodeOptions = {
  systemPrompt: "You are a code reviewer.",
};

for await (const message of query({ prompt: "Review this PR diff", options })) {
  if (message.type === "result") {
    console.log(message.result);
  }
}
```

**Agent SDK vs Managed Agents — decision guide:**
- Agent SDK: full infrastructure control, runs in your CI/CD, latency-sensitive workloads, custom logging and observability
- Managed Agents: Anthropic handles crashes, scaling, and memory persistence; no infrastructure to manage; better for non-technical teams deploying agents as a product feature

## Example

A code review pipeline in CI: on every PR open event, a GitHub Actions job calls the Agent SDK with the PR diff as the prompt. The agent reviews the diff, calls internal tools to check the test coverage database, and posts a structured review comment back to the PR via the GitHub API. The `--bare` flag keeps cold-start time under 2 seconds.

---
