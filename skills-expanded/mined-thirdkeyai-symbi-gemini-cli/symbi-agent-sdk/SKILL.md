---
name: symbi-agent-sdk
description: Generate boilerplate for wrapping Gemini CLI agents in ORGA governance. Use when building headless agents that run inside Symbiont's CliExecutor or when integrating Gemini CLI with Symbiont's trust stack.
---

# Gemini CLI + ORGA Integration

Help the user create Gemini CLI agents that are governed by Symbiont's ORGA loop.

## Architecture

In the runtime-first (Mode B) pattern, Symbiont's CliExecutor spawns Gemini CLI
as a governed subprocess:

```
Symbiont Runtime (ORGA Loop)
  -> CliExecutor (sandbox + budget)
    -> Gemini CLI (execution)
      -> symbi extension (awareness bridge)
        -> parent MCP server (governance tools)
```

## DSL Executor Block

When the user wants to define a Gemini CLI agent in DSL, use the `executor` block:

```symbiont
agent task_name(input: InputType) -> OutputType {
    capabilities = ["read", "analyze", "write"]

    executor {
        type = "gemini_cli"
        allowed_tools = ["read_file", "write_file", "run_shell_command", "symbi__*"]
        extension = "symbi"
        model = "gemini-2.5-pro"
    }

    policy access_policy {
        allow: read(any) if true
        deny: write(any) if not input.approved
        audit: all_operations
    }

    with sandbox = "tier1", timeout = "30m" {
        result = execute(input)
        return result
    }
}
```

## CliExecutor Environment Variables

When Symbiont spawns Gemini CLI, these environment variables are set:

| Variable | Purpose |
|----------|---------|
| `SYMBIONT_MANAGED=true` | Signals the extension is inside a managed runtime |
| `SYMBIONT_MCP_URL` | HTTP endpoint to connect back to parent MCP server |
| `SYMBIONT_RUNTIME_SOCKET` | Unix socket for runtime communication |
| `SYMBIONT_SESSION_ID` | Unique session ID for audit correlation |
| `SYMBIONT_BUDGET_TOKENS` | Token budget for this execution |
| `SYMBIONT_BUDGET_TIMEOUT` | Timeout for this execution |

## Workflow

1. Ask what the agent should do and its security requirements
2. Create the DSL definition with an `executor` block for `gemini_cli`
3. Define Cedar policies for the agent's capabilities
4. Generate the `symbiont.toml` configuration if needed
5. Validate with `symbi__parse_dsl`
6. Explain how to run: `symbi run <agent_name> --prompt "..."`
