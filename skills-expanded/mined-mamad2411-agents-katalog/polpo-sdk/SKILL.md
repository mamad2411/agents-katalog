---
name: polpo-sdk
description: Integrate Polpo AI agents into any TypeScript/JavaScript application using @polpo-ai/sdk. Use when the user wants to add AI agent chat, completions API, streaming SSE, session management, memory, webhooks, or any Polpo API integration into their code. Triggers on "polpo", "agent chat", "completions API", "polpo sdk", "@polpo-ai/sdk", "AI agent integration".
---

# Polpo SDK Integration

## Install

```bash
npm install @polpo-ai/sdk
```

## Client Setup

```typescript
import { PolpoClient } from "@polpo-ai/sdk";

// baseUrl is the root URL — SDK appends /v1/ internally.
// Do NOT add /v1/ or /api/v1/ to baseUrl.
const polpo = new PolpoClient({
  baseUrl: "https://api.polpo.sh",  // local dev: http://localhost:3890
  apiKey: process.env.POLPO_API_KEY,
});
```

## Chat Completions (Non-Streaming)

```typescript
const response = await polpo.chatCompletion({
  agent: "coder",
  messages: [{ role: "user", content: "Write a fibonacci function" }],
});

console.log(response.choices[0].message.content);
```

## Chat Completions (Streaming SSE)

```typescript
const stream = await polpo.chatCompletionStream({
  agent: "coder",
  messages: [{ role: "user", content: "Explain recursion" }],
});

// stream.sessionId — persisted session ID from server
for await (const chunk of stream) {
  const delta = chunk.choices[0]?.delta?.content;
  if (delta) process.stdout.write(delta);
}
```

## Sessions

Sessions persist conversation history. The server auto-creates sessions; use `sessionId` to continue a conversation.

```typescript
// List sessions
const sessions = await polpo.listChatSessions();

// Get messages from a session
const { session, messages } = await polpo.getChatSessionMessages(sessionId);

// Continue a session
const stream = await polpo.chatCompletionStream({
  agent: "coder",
  sessionId: existingSessionId,
  messages: [{ role: "user", content: "Now refactor it" }],
});
```

## Agents

```typescript
// List agents
const agents = await polpo.getAgents();

// Create agent
await polpo.addAgent({
  name: "reviewer",
  role: "Code reviewer",
  model: "xai/grok-4-fast",
  allowedTools: ["bash", "read", "grep"],
  systemPrompt: "You review code for bugs and security issues.",
});

// Update agent
await polpo.updateAgent("reviewer", { model: "anthropic/claude-sonnet-4" });
```

## Memory

```typescript
// Project memory (shared across all agents)
const { content } = await polpo.getMemory();
await polpo.saveMemory("# Project Context\n\nThis is a Next.js e-commerce app...");

// Agent memory (private to one agent)
const agentMem = await polpo.getAgentMemory("coder");
await polpo.saveAgentMemory("coder", "Prefers TypeScript, uses Vitest for tests.");
```

## Webhooks

```typescript
// Register a webhook
await polpo.registerWebhook({
  url: "https://myapp.com/webhook",
  events: ["task:*", "mission:completed"],
});
```

## SSE Real-Time Events

```typescript
import { EventSourceManager } from "@polpo-ai/sdk";

const sse = new EventSourceManager({
  baseUrl: "https://api.polpo.sh",
  apiKey: process.env.POLPO_API_KEY,
});

sse.connect({ filter: "task:*" });
sse.on("task:transition", (data) => {
  console.log(`Task ${data.id}: ${data.from} → ${data.to}`);
});
```

## Key Types

See [references/types.md](references/types.md) for the full type reference including `Task`, `AgentConfig`, `Mission`, `Session`, `ChatCompletionRequest`, `ChatCompletionResponse`, and all request/response DTOs.

## API Endpoints Reference

See [references/api.md](references/api.md) for the complete API endpoint list with methods, paths, and descriptions.
