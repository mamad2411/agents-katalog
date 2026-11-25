---
name: ai-integration
description: >
  Guidelines for building AI-powered features into applications. Covers
  tool-use agent patterns, Anthropic API integration, prompt engineering
  for app-internal agents, and best practices. Referenced by planner
  and generators. Not directly user-invocable.
user-invocable: false
---

# AI Integration Guidelines

This skill provides patterns and best practices for weaving AI-powered features into applications built by the ganvil. It is referenced by the planner (when designing specs) and generators (when implementing AI features).

## When to Add AI Features

Add AI features when they genuinely improve the product:
- Accelerating repetitive creative workflows (e.g., generating assets, code, or content)
- Providing intelligent defaults or suggestions based on context
- Automating multi-step processes through natural language
- Analyzing, summarizing, or transforming complex data

Do NOT add AI features just because you can. Each AI feature should solve a real user problem that would be tedious or impossible without AI.

## Building App-Internal Agents

When the spec calls for AI-powered functionality, build a proper agent that can drive the app's own functionality through tools — not just a chat widget pasted on top.

### The Tool-Use Pattern

The recommended architecture for app-internal AI features:

```
User Input (natural language)
    ↓
Agent Loop:
    1. Understand intent
    2. Plan which tools to call
    3. Execute tools (your app's own functions)
    4. Observe results
    5. Repeat or respond
    ↓
Result (action taken in the app + explanation to user)
```

### Implementation Steps

1. **Define clear, focused tools** that map to your app's core operations:
   - Each tool does one thing well
   - Parameters are typed and validated
   - Return values are structured (not free text)

2. **Build tools as standalone functions** in your app:
   - They should work independently of the AI integration
   - They should be testable without an API key

3. **Implement the agent loop**:
   - Receive user input → construct messages → call API → parse tool_use → execute → loop
   - Handle the `end_turn` stop reason to know when the agent is done
   - Accumulate tool results and feed them back as `tool_result` messages

4. **Handle errors gracefully**:
   - The agent should explain failures in natural language, not crash
   - Implement retry logic for transient API errors
   - Provide graceful degradation when the AI service is unavailable

## Anthropic API Integration

### Client Setup

```javascript
// Backend (Node.js) — recommended approach
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

```python
# Backend (Python) — recommended approach
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
```

### Tool Definition Format

```javascript
const tools = [
  {
    name: "create_item",
    description: "Creates a new item in the application with the given properties.",
    input_schema: {
      type: "object",
      properties: {
        name: { type: "string", description: "The name of the item" },
        category: { type: "string", enum: ["type_a", "type_b"], description: "Item category" },
        properties: {
          type: "object",
          description: "Additional properties for the item",
          properties: {
            color: { type: "string" },
            size: { type: "number" }
          }
        }
      },
      required: ["name", "category"]
    }
  }
];
```

### Agent Loop Implementation

```javascript
async function runAgent(userMessage, tools, systemPrompt) {
  const messages = [{ role: "user", content: userMessage }];

  while (true) {
    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 4096,
      system: systemPrompt,
      tools: tools,
      messages: messages,
    });

    // Collect the assistant's response
    messages.push({ role: "assistant", content: response.content });

    // Check if the model wants to use tools
    if (response.stop_reason === "tool_use") {
      const toolResults = [];

      for (const block of response.content) {
        if (block.type === "tool_use") {
          // Execute the tool in your app
          const result = await executeAppTool(block.name, block.input);
          toolResults.push({
            type: "tool_result",
            tool_use_id: block.id,
            content: JSON.stringify(result),
          });
        }
      }

      // Feed results back to the model
      messages.push({ role: "user", content: toolResults });
    } else {
      // Model is done (end_turn) — extract text response
      const textBlocks = response.content.filter(b => b.type === "text");
      return textBlocks.map(b => b.text).join("\n");
    }
  }
}
```

### System Prompt Best Practices

```javascript
const systemPrompt = `You are an AI assistant integrated into [App Name].
You help users by performing actions through the available tools.

Important rules:
- Always use tools to perform actions. Do not describe what you would do — do it.
- After completing actions, briefly summarize what was done.
- If a request is ambiguous, ask for clarification before acting.
- If a tool call fails, explain the error and suggest alternatives.`;
```

## API Key Management

- **Always use environment variables** for API keys (`ANTHROPIC_API_KEY`)
- **Never hardcode** keys in source code
- **Document required env vars** in the build log's "How to Run" section
- **Implement graceful degradation**: the app should be fully functional without the API key — AI features simply show a "Configure API key to enable AI features" message
- **Proxy through your backend**: Never call the Anthropic API directly from frontend JavaScript. Route through your own backend endpoint to protect the API key.

## Anti-Patterns

Avoid these common mistakes when building AI features:

1. **Chat-only integration**: Just embedding a chat widget without connecting it to app functionality. The AI should be able to *do things* in the app, not just talk about them.
2. **Overly broad tools**: One tool that does everything. Break into focused, composable tools.
3. **Missing error handling**: Crashing when the API is down or returns an error.
4. **No feedback loop**: User can't see what the AI is doing. Show progress and explain actions.
5. **Ignoring context**: The AI doesn't know what the user is currently looking at. Pass relevant app state in the system prompt or user message.
