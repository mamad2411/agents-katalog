---
name: script-craft
description: "Use when crafting assistant scripts, action scripts, and function schemas for GPTs and AI agents. Consolidates ScriptCraft and Script Savvy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [gpt, agents, function-calling, schemas, automation, scripts]
---

# Script Craft

## Overview

Design and build action scripts, function schemas, and automation workflows for AI assistants (GPTs, Claude, Hermes, and custom agents). Covers the full lifecycle: identifying what should be a script vs. a prompt, writing clean function schemas (OpenAI function-calling format and OpenAPI), implementing handler logic, and testing the integration. Consolidates the ScriptCraft and Script Savvy workflows into one unified skill.

## When to Use

- "Create a GPT action that..." — building custom GPT actions
- "Write a function schema for my AI agent to..." — function/tool definitions
- "I need my assistant to call an API when..." — API integration scripts
- "Design the tools for my custom agent" — agent capability planning
- "Convert this workflow into an AI-callable script" — workflow automation

**Don't use for:** full backend APIs (use `backend-dev`), UI components, or simple prompt engineering without tool integration.

## How It Works

**Plan → Schema → Implement → Test → Document**

1. **Plan:** Determine what the agent needs to do and whether a script/tool is the right approach
2. **Schema:** Write a precise function definition (name, description, parameters with types and constraints)
3. **Implement:** Build the handler that executes the action and returns structured results
4. **Test:** Verify with edge cases, error conditions, and the agent's actual calling patterns
5. **Document:** Write usage examples so the agent (and humans) understand how to use the tool

## Steps

### 1. Capability Planning
- List all actions the agent should be able to perform
- Distinguish between: pure prompt tasks vs. tool-requiring tasks
- For each tool-requiring task, define: what input it needs, what it returns, what can go wrong

### 2. Schema Design (OpenAI Format)
```json
{
  "name": "search_knowledge_base",
  "description": "Search the company knowledge base for relevant articles. Use this when the user asks about internal policies, procedures, or documentation.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query. Use natural language keywords."
      },
      "max_results": {
        "type": "integer",
        "description": "Maximum number of results to return (1-10)",
        "minimum": 1,
        "maximum": 10,
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

### 3. Schema Design Principles
- **Descriptive `description`:** Tell the agent *when* to use the tool, not just what it does
- **Constrained types:** Use `minimum`/`maximum`, `enum`, `pattern` to prevent bad calls
- **Required vs. optional:** Only mark truly required fields — give sensible defaults for optional ones
- **Flat parameters over nested:** Agents handle flat parameter objects better than deeply nested ones

### 4. Handler Implementation
- Validate all inputs before processing (never trust the agent's call)
- Return structured, parseable results (JSON preferred)
- Include error messages that help the agent self-correct: "No results for 'xyz'. Try broader keywords."
- Handle timeouts gracefully — agents may retry

### 5. Testing the Integration
- Test happy path with expected inputs
- Test edge cases: empty input, maximum values, special characters
- Test error recovery: does the agent understand the error and retry correctly?
- Run 3-5 end-to-end conversation tests with varied phrasings

## Common Pitfalls

1. **Vague descriptions.** If the description says "searches things," the agent won't know when to call it. Be specific: "Use this when the user asks about company policies, HR procedures, or internal documentation."

2. **Missing parameter constraints.** Without `minimum`/`maximum` or `enum`, the agent can send nonsense values. Constrain aggressively.

3. **Too many tools.** Agents perform best with 5-15 well-designed tools. Beyond that, tool selection accuracy drops. Combine related actions into a single tool with an `action` parameter.

4. **Error responses that confuse the agent.** An error like "500 Internal Server Error" gives the agent nothing to work with. Instead: "Could not find document ID 'abc123'. It may have been deleted. Ask the user for an alternative ID."

5. **Forgetting the human-in-the-loop.** Destructive actions (delete, send, purchase) should require confirmation. Add a `requires_confirmation` flag or design a two-step flow.
