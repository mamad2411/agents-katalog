---
name: code-understanding
description: Get type info, documentation, function signatures, and available methods for any symbol without reading source files. Use when you need to understand what a symbol is, what parameters a function takes, or what methods a type has. Activated by runectl lsp hover, signature-help, or completion.
allowed-tools: Bash(runectl:*)
---

# Code Understanding

Inspect symbols without reading source files.

## runectl lsp hover

Get hover info for a symbol — type signature and doc comments.

```
Usage:
  runectl lsp hover (<file> <line> <col> | <symbol>) [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Use to understand what a symbol is without finding and reading
its definition.

Example — inspect the `workspaceapi.Cmd` type:

```bash
$ runectl lsp hover workspaceapi.Cmd
```go
type Cmd struct { // size=152 (0x98), class=160 (0xa0)
	Path    string
	Dir     string
	Args    []string
	Env     []string
	Stdin   io.Reader
	Stdout  io.Writer
	Stderr  io.Writer
	Watcher ProcessWatcher

	// SysProcAttr is ignored if passed from a extension.
	SysProcAttr *syscall.SysProcAttr
}
```

---

Cmd represents an external command being prepared to run...
```

Returns the full type signature and doc comment rendered as
markdown. This gives you the complete struct layout without
reading the source file.

## runectl lsp signature-help

Get signature help at a position — parameter names and types.

```
Usage:
  runectl lsp signature-help <file> <line> <col> [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Position must be inside a function call's argument list. Use to
know a function's parameters without reading its definition.

## runectl lsp completion

Get completion suggestions at a position.

```
Usage:
  runectl lsp completion <file> <line> <col> [flags]

Flags:
  -F, --format string   Output format: table, json, or Go template
```

Returns label, kind, and detail for each completion item. Use
to discover available methods and fields on a type.
