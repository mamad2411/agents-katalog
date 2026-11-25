---
name: cloudflare-ai-agent
description: Build AI agents on Cloudflare using the Agents SDK with state management, real-time WebSockets, scheduled tasks, tool integration, and chat capabilities. Generates production-ready agent code deployed to Workers.
license: Apache 2.0
metadata:
  source: https://github.com/cloudflare/skills
  category: cloudflare
---

# Building Cloudflare AI Agents

## Retrieval Sources

| Source | URL |
|--------|-----|
| Agents SDK docs | `https://github.com/cloudflare/agents/tree/main/docs` |
| Cloudflare Agents docs | `https://developers.cloudflare.com/agents/` |
| Workers docs | `https://developers.cloudflare.com/workers/` |

## Quick Start

```bash
npm create cloudflare@latest -- my-agent --template=cloudflare/agents-starter
cd my-agent
npm start
```

## Basic Agent Structure

```typescript
import { Agent, Connection } from "agents";

interface Env {
  AI: Ai;
}

interface State {
  messages: Array<{ role: string; content: string }>;
  preferences: Record<string, string>;
}

export class MyAgent extends Agent<Env, State> {
  initialState: State = {
    messages: [],
    preferences: {},
  };

  async onStart() {
    console.log("Agent started with state:", this.state);
  }

  async onConnect(connection: Connection) {
    connection.send(JSON.stringify({
      type: "welcome",
      history: this.state.messages,
    }));
  }

  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);
    if (data.type === "chat") {
      await this.handleChat(connection, data.content);
    }
  }

  async onClose(connection: Connection) {
    console.log("Client disconnected");
  }

  onStateUpdate(state: State, source: string) {
    console.log("State updated by:", source);
  }

  private async handleChat(connection: Connection, userMessage: string) {
    const messages = [
      ...this.state.messages,
      { role: "user", content: userMessage },
    ];

    const response = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
      messages,
    });

    this.setState({
      ...this.state,
      messages: [
        ...messages,
        { role: "assistant", content: response.response },
      ],
    });

    connection.send(JSON.stringify({
      type: "response",
      content: response.response,
    }));
  }
}
```

## Entry Point

```typescript
import { routeAgentRequest } from "agents";
import { MyAgent } from "./agent";

export default {
  async fetch(request: Request, env: Env) {
    return (
      (await routeAgentRequest(request, env)) ||
      new Response("Not found", { status: 404 })
    );
  },
};

export { MyAgent };
```

## Wrangler Configuration

```jsonc
{
  "name": "my-agent",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "ai": { "binding": "AI" },
  "durable_objects": {
    "bindings": [{ "name": "MyAgent", "class_name": "MyAgent" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyAgent"] }]
}
```

## State Management

```typescript
const currentMessages = this.state.messages;
this.setState({ ...this.state, messages: [...this.state.messages, newMessage] });
```

## SQL Storage

```typescript
await this.sql`CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT)`;
await this.sql`INSERT INTO documents (title, content) VALUES (${title}, ${content})`;
const docs = await this.sql`SELECT * FROM documents WHERE title LIKE ${`%${search}%`}`;
```

## Scheduled Tasks

```typescript
await this.schedule(3600, "sendReminder", { message: data.reminderText });
await this.schedule(new Date("2025-01-01T00:00:00Z"), "taskMethod", { data });
await this.schedule("0 9 * * *", "dailyTask", {});
await this.scheduleEvery(30, "everyFiveMinutes");
const schedules = await this.getSchedules();
await this.cancelSchedule(taskId);
```

## Chat Agent (AI-Powered)

```typescript
import { AIChatAgent } from "@cloudflare/ai-chat";

export class ChatBot extends AIChatAgent<Env> {
  async onChatMessage(message: string) {
    const response = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        ...this.messages,
        { role: "user", content: message },
      ],
      stream: true,
    });
    return response;
  }
}
```

## React Client

```tsx
import { useAgent } from "agents/react";

function Chat() {
  const { state, send, connected } = useAgent({
    agent: "my-agent",
    name: userId,
  });

  return (
    <div>
      {state.messages.map((msg, i) => (
        <div key={i}>{msg.role}: {msg.content}</div>
      ))}
    </div>
  );
}
```

## Deployment

```bash
npx wrangler deploy
wrangler tail
```

## Keywords

Cloudflare, AI agent, chatbot, WebSocket, stateful, Agents SDK, Workers AI, streaming, scheduled tasks
