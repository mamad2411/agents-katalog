---
name: code-navigation
description: Jump to symbol definitions, find all references, locate interface declarations, resolve type definitions, and find implementations. Use instead of grep or text search when navigating to where a function, type, or variable is defined or used. Activated by runectl lsp.
allowed-tools: Bash(runectl:*)
---

# Code Navigation

Semantic code navigation via `runectl lsp`. Prefer these over
grep — they use the language server for precise results.

## runectl lsp definition

Go to definition.

```
Usage:
  runectl lsp definition (<file> <line> <col> | <symbol>) [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Use when you see a function call and want its source.

Example — find where the `workspaceapi.Cmd` struct is defined:

```bash
$ runectl lsp definition workspaceapi.Cmd
file:///src/rune-go-sdk/api/workspaceapi/workspace.go 52:5-52:8
```

The result points to `workspace.go` line 52, columns 5-8.

## runectl lsp references

Find all references.

```
Usage:
  runectl lsp references (<file> <line> <col> | <symbol>) [flags]

Flags:
  -d, --declaration     Include declaration
  -F, --format string   Output format: table, json, or Go template
```

Use to find every place a symbol is used across the workspace.

Example — find all usages of `workspaceapi.URI`:

```bash
$ runectl lsp references workspaceapi.URI
file:///src/rune-agent/agent/agent.go 153:39-153:42
file:///src/rune-agent/agent/agent.go 161:39-161:42
file:///src/rune-agent/agent/agent.go 174:32-174:35
...
```

Each line is a location where `URI` appears. Add `-d` to also
include the declaration itself.

## runectl lsp declaration

Go to declaration.

```
Usage:
  runectl lsp declaration (<file> <line> <col> | <symbol>) [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Use when you want the interface a method satisfies or a
forward declaration.

## runectl lsp type-definition

Go to type definition.

```
Usage:
  runectl lsp type-definition (<file> <line> <col> | <symbol>) [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Use when you have a variable and want its underlying struct or
interface type.

Example — find the type behind `workspaceapi.Cmd`:

```bash
$ runectl lsp type-definition workspaceapi.Cmd
file:///src/rune-go-sdk/api/workspaceapi/workspace.go 52:5-52:8
```

## runectl lsp implementation

Find implementations.

```
Usage:
  runectl lsp implementation (<file> <line> <col> | <symbol>) [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Use when you have an interface and want all concrete types that
implement it.

Example — find all types implementing `workspaceapi.Executor`:

```bash
$ runectl lsp implementation workspaceapi.Executor
file:///src/rune-go-sdk/api/workspaceapi/workspacerpc/client.go 44:5-44:11
file:///src/rune-agent/agent/agentools/agentools_test.go 85:5-85:14
file:///src/rune-agent/agent/agentools/agentools_test.go 123:5-123:18
...
```

Results include test doubles across the workspace and the real
client in `workspacerpc`.
