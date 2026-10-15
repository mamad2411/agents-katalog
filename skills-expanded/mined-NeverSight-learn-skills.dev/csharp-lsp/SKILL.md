---
name: csharp-lsp
description: Use this skill when exploring, understanding, or navigating C# codebases through csharp-lsp-cli, including go to definition, find references, hover, document symbols, workspace symbols, diagnostics, and managing the long-lived LSP daemon session for SDK-style .NET, .NET Core, legacy .NET Framework, OmniSharp, Roslyn, csharp-ls, or mixed C# solutions.
---

# C# LSP

## Quick Start

Use `csharp-lsp-cli` when static text search is not enough and the task needs
Roslyn-backed C# understanding.

Send one JSON request on stdin and read one JSON response from stdout:

```bash
printf '%s\n' '{"version":1,"operation":"definition","workspace":"C:/repo/app","file":"src/Program.cs","line":10,"character":5}' | csharp-lsp-cli
```

Keep stderr available for human-readable logs. Do not parse stderr as data.

## Session Rules

Treat a session as one long-lived LSP server owned by a background daemon. Each
CLI invocation sends exactly one JSON request, but requests reuse the same daemon
when their session identity is the same.

The session identity is derived from:

- resolved `workspace`
- resolved LSP server executable
- LSP server args, including OmniSharp `-s <solution>`
- LSP server environment overrides, including OmniSharp MSBuild override env

These request fields do not create a new session: `operation`, `file`, `line`,
`character`, `query`, `includeDeclaration`, and `timeoutMs`.

Use the same session fields for every related request. For OmniSharp, repeat the
same `lspServerKind`, `solution`, and any explicit `lspServerPath`,
`lspServerArgs`, or `omnisharpMsBuildPath` fields on `definition`,
`references`, `hover`, `status`, `restart`, and `stop`. If `solution` is omitted
on a later request, the CLI may default back to `csharp-ls`, producing a
different session.

Prefer absolute `solution` paths for OmniSharp sessions. If using relative
paths, run the CLI from the same current working directory each time. If using
workspace-relative file paths, keep `workspace` stable and explicit.

Use `status` to warm up or inspect a session, but the first real query can also
start the daemon. Use `restart` when the LSP server loaded stale project state
or after changing server/MSBuild configuration. Use `stop` when finished with a
workspace/solution. Changing `workspace`, `solution`, server path, server args,
or OmniSharp MSBuild override intentionally creates a separate session.

The daemon manages document lifecycle. It sends `didOpen` before queries,
`didChange` when disk content changes, and `didClose` after documents sit idle.

## Operations

Use these operation names exactly:

- `definition`: require `file`, `line`, and `character`.
- `references`: require `file`, `line`, and `character`; set `includeDeclaration` when needed.
- `hover`: require `file`, `line`, and `character`.
- `documentSymbols`: require `file`.
- `workspaceSymbols`: pass `query`; empty query is allowed.
- `diagnostics`: pass `file` for one document or omit it for cached workspace diagnostics.
- `status`: inspect the daemon/session state.
- `restart`: restart the LSP server process for the current session.
- `stop`: stop the daemon for the current session.

Line and character inputs are 1-based. Returned ranges are also 1-based and
paths are workspace-relative when possible.

## Workspace And Server

Prefer an explicit `workspace` when the user or repo makes it clear. If omitted,
the CLI discovers the workspace from the target file by walking up to `.git`,
then falls back to the current working directory.

Default to `csharp-ls`. Override only when project requirements make it useful:

```json
{
  "version": 1,
  "operation": "hover",
  "workspace": "C:/repo/app",
  "file": "Program.cs",
  "line": 3,
  "character": 12,
  "lspServerKind": "roslyn"
}
```

For OmniSharp on a workspace with multiple solution files, specify the exact
solution. If `workspace` is set, a relative `solution` is resolved from that
workspace. If `workspace` is omitted, use an absolute `solution` or one relative
to the CLI current working directory:

```json
{
  "version": 1,
  "operation": "status",
  "lspServerKind": "omnisharp",
  "solution": "C:/repo/app/App.sln",
  "timeoutMs": 180000
}
```

When `workspace` is omitted, the CLI discovers it from `file`, then from
`solution` by walking up to `.git`; if no `.git` exists, it uses the `.sln`
directory.

For legacy .NET Framework solutions, prefer an absolute `solution` path, keep
`workspace` omitted when you want the CLI to derive it from the `.sln`, and pass
`timeoutMs` around 180000 on the first request.

On Windows, the OmniSharp preset automatically checks
`CSHARP_LSP_CLI_OMNISHARP_PATH`, then `C:\dev\omnisharp\OmniSharp.exe`, then
`omnisharp` on PATH. It also tries to pin Visual Studio 2022 MSBuild through
OmniSharp configuration environment variables. Override that per request with
`omnisharpMsBuildPath` / `omnisharpMsBuildName`, or set
`omnisharpUseDefaultMsBuild` to `false` when the project should use OmniSharp's
own MSBuild discovery.

Read `references/csharp-server-selection.md` before changing server defaults,
working on legacy .NET Framework projects, or troubleshooting server startup.

## Response Handling

Expect this shape:

```json
{
  "version": 1,
  "ok": true,
  "operation": "hover",
  "session": "sha256-session-prefix",
  "result": {},
  "meta": { "durationMs": 123, "retried": false }
}
```

On `ok: false`, use `error.code` and `error.message` to decide the next step.
If `meta.retried` is true, the daemon already restarted the LSP server once for
that request; do not immediately retry in a tight loop.
