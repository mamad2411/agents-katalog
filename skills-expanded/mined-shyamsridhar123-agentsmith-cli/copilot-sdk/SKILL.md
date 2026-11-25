---
name: copilot-sdk
description: Build AI-powered applications using the GitHub Copilot SDK. Use this skill when developing apps with @github/copilot-sdk (TypeScript), github-copilot-sdk (Python), github.com/github/copilot-sdk/go (Go), or GitHub.Copilot.SDK (.NET). Covers client lifecycle, sessions, streaming, custom tools, MCP integration, and best practices.
---

# GitHub Copilot SDK

Build AI-powered applications that leverage Copilot's agentic workflows. The SDK exposes the same engine behind Copilot CLI—a production-tested agent runtime you can invoke programmatically.

**Status:** Technical Preview

## When to Use This Skill

- Creating applications that need programmatic access to GitHub Copilot
- Building custom AI agents with tool integration
- Developing CLI tools or backends powered by Copilot
- Integrating Copilot capabilities into existing applications

## Prerequisites

1. **GitHub Copilot Subscription** - Required for SDK usage
2. **Copilot CLI** - Must be installed and in PATH ([installation guide](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli))

## Installation

| Language | Package | Command |
|----------|---------|---------|
| TypeScript/Node.js | `@github/copilot-sdk` | `npm install @github/copilot-sdk` |
| Python | `github-copilot-sdk` | `pip install github-copilot-sdk` |
| Go | `github.com/github/copilot-sdk/go` | `go get github.com/github/copilot-sdk/go` |
| .NET | `GitHub.Copilot.SDK` | `dotnet add package GitHub.Copilot.SDK` |

## Architecture

```
Your Application → SDK Client → JSON-RPC → Copilot CLI (server mode)
```

---

## Quick Start Examples

### TypeScript

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
await client.start();

const session = await client.createSession({ model: "gpt-5" });

session.on((event) => {
    if (event.type === "assistant.message") {
        console.log(event.data.content);
    } else if (event.type === "session.idle") {
        // Session finished processing
    }
});

await session.send({ prompt: "What is 2+2?" });
await session.destroy();
await client.stop();
```

### Python

```python
from copilot import CopilotClient

client = CopilotClient()
await client.start()

session = await client.create_session({"model": "gpt-5"})

def on_event(event):
    if event["type"] == "assistant.message":
        print(event["data"]["content"])

session.on(on_event)
await session.send({"prompt": "What is 2+2?"})
await session.destroy()
await client.stop()
```

### Go

```go
import copilot "github.com/github/copilot-sdk/go"

client := copilot.NewClient(&copilot.ClientOptions{LogLevel: "error"})
client.Start()
defer client.Stop()

session, _ := client.CreateSession(&copilot.SessionConfig{Model: "gpt-5"})
defer session.Destroy()

done := make(chan bool)
session.On(func(event copilot.SessionEvent) {
    if event.Type == "assistant.message" && event.Data.Content != nil {
        fmt.Println(*event.Data.Content)
    }
    if event.Type == "session.idle" {
        close(done)
    }
})

session.Send(copilot.MessageOptions{Prompt: "What is 2+2?"})
<-done
```

### .NET

```csharp
using GitHub.Copilot.SDK;

await using var client = new CopilotClient();
await client.StartAsync();

await using var session = await client.CreateSessionAsync(new SessionConfig { Model = "gpt-5" });

var done = new TaskCompletionSource();
session.On(evt => {
    if (evt is AssistantMessageEvent msg) Console.WriteLine(msg.Data.Content);
    else if (evt is SessionIdleEvent) done.SetResult();
});

await session.SendAsync(new MessageOptions { Prompt = "What is 2+2?" });
await done.Task;
```

---

## Event Types

| Event | Description |
|-------|-------------|
| `assistant.message` | Complete assistant response |
| `assistant.message.delta` | Streaming message chunk |
| `assistant.reasoning` | Model reasoning content |
| `assistant.reasoning.delta` | Streaming reasoning chunk |
| `session.idle` | Session finished processing |
| `tool.invocation` | Tool being invoked |
| `tool.result` | Tool execution result |

---

## Streaming

Enable real-time incremental responses:

```typescript
const session = await client.createSession({
    model: "gpt-5",
    streaming: true,
});

session.on((event) => {
    if (event.type === "assistant.message.delta") {
        process.stdout.write(event.data.deltaContent);
    }
});
```

---

## Custom Tools

### TypeScript (with Zod)

```typescript
import { z } from "zod";
import { defineTool } from "@github/copilot-sdk";

const session = await client.createSession({
    model: "gpt-5",
    tools: [
        defineTool("get_weather", {
            description: "Get current weather for a city",
            parameters: z.object({
                city: z.string().describe("City name"),
            }),
            handler: async ({ city }) => {
                return { temp: 72, condition: "sunny", city };
            },
        }),
    ],
});
```

### Python

```python
from copilot import define_tool

@define_tool("get_weather", "Get current weather for a city")
async def get_weather(city: str) -> dict:
    return {"temp": 72, "condition": "sunny", "city": city}

session = await client.create_session({
    "model": "gpt-5",
    "tools": [get_weather]
})
```

### .NET

```csharp
using Microsoft.Extensions.AI;
using System.ComponentModel;

var session = await client.CreateSessionAsync(new SessionConfig
{
    Model = "gpt-5",
    Tools = [
        AIFunctionFactory.Create(
            ([Description("City name")] string city) => new { Temp = 72, Condition = "sunny", City = city },
            "get_weather",
            "Get current weather for a city"),
    ]
});
```

---

## Advanced Features

### Multiple Sessions

```typescript
const session1 = await client.createSession({ model: "gpt-5" });
const session2 = await client.createSession({ model: "claude-sonnet-4.5" });
// Sessions are independent
```

### File Attachments

```typescript
await session.send({
    prompt: "Analyze this file",
    attachments: [{ type: "file", path: "/path/to/file.ts", displayName: "My File" }],
});
```

### Image Support

```typescript
await session.send({
    prompt: "What's in this image?",
    attachments: [{ type: "base64", base64Content: imageBase64, mediaType: "image/png" }],
});
```

### Session Persistence

```typescript
// Save
const metadata = await session.getMetadata();
fs.writeFileSync("session.json", JSON.stringify(metadata));

// Resume
const saved = JSON.parse(fs.readFileSync("session.json"));
const resumed = await client.resumeSession({ sessionId: saved.id });
```

### Bring Your Own Key (BYOK)

```typescript
const session = await client.createSession({
    provider: { type: "openai", baseUrl: "https://api.openai.com/v1", apiKey: "your-key" },
});
```

### MCP Server Integration

```typescript
const session = await client.createSession({
    model: "gpt-5",
    mcpServers: [{
        type: "local",
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-github"],
        env: { GITHUB_TOKEN: process.env.GITHUB_TOKEN },
    }],
});
```

---

## Best Practices

1. **Client Reuse** - Use a singleton `CopilotClient`; avoid creating new instances repeatedly
2. **Session Cleanup** - Always call `session.destroy()` when done (use try/finally or disposable patterns)
3. **Error Handling** - Handle `429` (rate limit) with retry-after logic; log diagnostics
4. **Streaming** - Enable streaming for better UX with incremental responses
5. **Tool Design** - Keep handlers fast; return JSON-serializable values; provide clear parameter descriptions

---

## Error Handling

```typescript
try {
    await session.send({ prompt: "Hello" });
} catch (error) {
    if (error.code === 429) {
        // Rate limited - retry with backoff
    }
    console.error("Error:", error.message);
}
```

---

## Default Capabilities

The SDK operates with all first-party tools enabled by default:
- File system operations
- Git operations  
- Web requests

Customize via SDK client options.

---

## Billing

- Each prompt counts toward your premium request quota
- Free tier available with limited usage
- See [Requests in GitHub Copilot](https://docs.github.com/en/copilot/concepts/billing/copilot-requests)

---

## Resources

- [Getting Started Tutorial](https://github.com/github/copilot-sdk/blob/main/docs/getting-started.md)
- [Cookbook - Practical Recipes](https://github.com/github/copilot-sdk/blob/main/cookbook/README.md)
- [Node.js/TypeScript Reference](https://github.com/github/copilot-sdk/blob/main/nodejs/README.md)
- [Python Reference](https://github.com/github/copilot-sdk/blob/main/python/README.md)
- [Go Reference](https://github.com/github/copilot-sdk/blob/main/go/README.md)
- [.NET Reference](https://github.com/github/copilot-sdk/blob/main/dotnet/README.md)
- [GitHub Issues](https://github.com/github/copilot-sdk/issues)
