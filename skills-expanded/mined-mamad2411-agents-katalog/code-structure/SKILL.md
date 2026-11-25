---
name: code-structure
description: List all symbols in a file or search for functions, types, methods, and variables across the workspace. Use instead of glob+grep to understand file structure or find where a symbol is defined. Activated by runectl lsp symbols, workspace-symbols, or runectl syntax searchnode/querynode.
allowed-tools: Bash(runectl:*)
---

# Code Structure

Explore code structure without reading entire files.

## runectl lsp symbols

List document symbols (functions, types, variables).

```
Usage:
  runectl lsp symbols <file> [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Use to get an overview of a file's structure.

Example — list all symbols in `bash.go`:

```bash
$ runectl lsp symbols agent/agentools/bash.go
defaultBashTimeout [Constant] 39:1-39:39
maxBashTimeout [Constant] 40:1-40:39
maxCommandOutput [Constant] 41:1-41:32
bashTool [Struct] 44:5-47:1
bashArgs [Struct] 49:5-54:1
newBash [Function] 56:0-58:1
(*bashTool).Definition [Method] 60:0-104:1
(*bashTool).Summary [Method] 106:0-112:1
(*bashTool).Execute [Method] 114:0-181:1
processWatcher [Struct] 183:5-185:1
newProcessWatcher [Function] 187:0-189:1
(*processWatcher).WatchProcess [Method] 191:0-193:1
```

Each entry shows `name [Kind] startLine:startCol-endLine:endCol`.
This gives a complete structural overview without reading the file.

## runectl lsp workspace-symbols

Search workspace symbols by name.

```
Usage:
  runectl lsp workspace-symbols <query> [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Use to locate a function or type by name across the project.

Example — search for `Service`:

```bash
$ runectl lsp workspace-symbols Service
Service Interface file:///src/rune-agent/llm/service.go:62:5
mockService Struct file:///src/rune-agent/agent/agent_test.go:2227:5
stubService Struct file:///src/rune-agent/agentshell/agentshell_test.go:1266:5
...
```

Returns all matching symbols with their kind and location.
The query is a fuzzy match on the symbol name.

## runectl syntax searchnode

Search workspace for known node types.

```
Node types: scope|namespace|reference|func|var|method|type

Usage:
  runectl syntax searchnode <node-type> [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Node types are pipe-separated. Use to find "all functions" or
"all types" workspace-wide without knowing exact names.

Example — find all type definitions:

```bash
$ runectl syntax searchnode type
file:///src/rune-agent/llm/service.go Service 62:5-62:12 local.definition.type
file:///src/rune-agent/llm/service.go ReasoningEffort 80:5-80:20 local.definition.type
file:///src/rune-agent/agent/agent.go Config 44:5-44:11 local.definition.type
...
```

Each line shows `file text line:col-endLine:endCol capture_name`.
Use `"func|method"` for all functions and methods.

## runectl syntax querynode

Query a file for known node types.

```
Node types: scope|namespace|reference|func|var|method|type

Usage:
  runectl syntax querynode <file> <node-type> [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Same as `searchnode` but scoped to a single file.

Example — find all functions in `bash.go`:

```bash
$ runectl syntax querynode agent/agentools/bash.go func
file:///src/rune-agent/agent/agentools/bash.go newBash 56:5-56:12 local.definition.function
file:///src/rune-agent/agent/agentools/bash.go newProcessWatcher 187:5-187:22 local.definition.function
```

Only free functions are returned; use `"func|method"` to
include methods as well.
