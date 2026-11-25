---
name: mcp-integration
description: Model Context Protocol (MCP) server integration and tool orchestration for Orca.
---

# MCP Integration

Model Context Protocol enables dynamic tool discovery and orchestration.

## What is MCP?
MCP is a protocol that allows AI agents to dynamically discover and use external tools, resources, and prompts. It enables:
- Tool servers exposing capabilities via a standard protocol
- Resource servers providing context (files, databases, APIs)
- Prompt servers offering reusable prompt templates

## MCP Architecture in Orca
1. **Transport**: Unix socket (`ws://127.0.0.1:6768` or `.sock` file)
2. **Auth**: Token-based authentication via runtime config
3. **Discovery**: Runtime registers available skills and tools
4. **Invocation**: Agent calls tools through the runtime transport

## Built-in MCP Skills (8)
1. **computer-use**: System-level operations (mouse, keyboard, screen)
2. **linear-tickets**: Linear issue tracker integration
3. **orca-cli**: Orca CLI command execution
4. **orca-emulator**: Android/iOS emulator management
5. **orca-emulator-android**: Android-specific emulator control
6. **orca-linear**: Linear project management (advanced)
7. **orca-per-workspace-env**: Per-workspace environment isolation
8. **orchestration**: Multi-agent task coordination

## Adding Custom MCP Tools
```json
{
  "toolName": "custom-tool",
  "description": "What this tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param": { "type": "string", "description": "Parameter description" }
    },
    "required": ["param"]
  }
}
```

## Best Practices
1. Always validate tool inputs before execution
2. Handle tool timeouts gracefully
3. Log all tool invocations for debugging
4. Provide clear error messages for failed calls
5. Use streaming for long-running tool operations
