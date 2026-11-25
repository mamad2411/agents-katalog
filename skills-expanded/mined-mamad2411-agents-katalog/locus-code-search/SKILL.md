---
name: locus-code-search
description: Run authenticated Locus semantic code search from this Skill's bundled runtime, without requiring an MCP server. Use automatically for code discovery when a file, symbol, implementation, subsystem, caller flow, dependency path, or cross-package behavior is unknown or must be found by meaning. Also use for Locus authentication setup, index status, and refresh. Do not use for an already-known exact file or symbol, or for pure git, build, test, and formatting work.
---

# Locus Code Search

This Skill executes the bundled Locus retrieval runtime directly. It is a capability, not instructions for calling the Locus MCP server.

## Entry Point

Resolve the directory containing this `SKILL.md` as `SKILL_DIR`. Run every operation through:

```powershell
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" <command> [options]
```

Never import files under `runtime/` directly. The wrapper enforces authentication before search, index creation, refresh, or status inspection.

## Authentication

The command requires a valid ACE key. Credential precedence is:

1. `ACE_API_KEY` environment variable for CI or a temporary override.
2. Windows Credential Manager target `Ace.Locus.ApiKey` for persistent login.

Use these commands for persistent credentials:

```powershell
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" auth login
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" auth set-key
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" auth status
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" auth logout
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" auth doctor
```

Treat the PowerShell entry point as an internal implementation detail. When the user asks to configure, log in, or update authentication, run:

```powershell
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" auth launch
```

This opens a separate login window and the ACE website. Tell the user to finish browser sign-in, then retry the requested operation. The Skill receives a short-lived authorization code on `127.0.0.1`, exchanges it with PKCE, and stores the signed-in account's key in Windows Credential Manager. Do not ask the user to paste a key into the agent conversation.

Require Windows x64, PowerShell 7, and Node.js 18 or newer. `auth login` uses browser authorization. `auth set-key` is the manual fallback and securely prompts for a key without opening a browser. `auth doctor` verifies that the bundled native credential adapter can round-trip a temporary value. The Node entry point performs all Credential Manager access, including under PowerShell `ConstrainedLanguage` mode.

Do not place keys in prompts, source files, config files, command output, or search arguments. Use `--key` only for non-interactive automation when command-line exposure is acceptable; prefer `ACE_API_KEY` for CI.

The non-secret relay URL is stored in `%APPDATA%\Ace\config.json`. The default is `https://ace.panrun.me/relay`; `ACE_BASE_URL` overrides it temporarily.

```powershell
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" config set base-url "https://HOST/relay"
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" config get base-url
```

When authentication is missing or rejected, stop the discovery operation and launch the authentication window once. Do not fall back to local-only Locus retrieval or another credential.

## Search

Start with one descriptive natural-language query at the smallest plausible package root:

```powershell
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" search `
  --query "function that validates user email and returns a boolean" `
  --project-path "backend" `
  --max-turns 2
```

Supported options mirror `locus_mcp_search`:

- `--project-path PATH`
- `--path-filter PATH`
- `--tree-depth 1..6`
- `--max-turns 1..5`
- `--max-results 1..30`
- `--result-mode complete|focused`
- `--cursor CURSOR`
- `--page-size 1..100`
- `--include-all-ranges true|false`
- `--exhaustive true|false`
- `--exclude-path PATH` (repeatable)

After the first result, read at least one strong hit and nearby code. If context is incomplete, run at most one narrowed retry with `--path-filter` set to the best hit's directory. Once the file or symbol is known, use direct reads or `rg` for exact and exhaustive occurrences.

Use `--max-turns 1` or `2` for simple discovery and `3` to `5` for cross-package tracing. Prefer package roots over a monorepo root, and use `--tree-depth 1` or `2` for large repositories.

## Index Status

Authentication is required for status and refresh:

```powershell
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" index-status --project-path "backend"
pwsh -NoProfile -File "SKILL_DIR/scripts/ace.ps1" index-status --project-path "backend" --refresh
```

The runtime snapshot is private to this Skill. Updating this Skill does not edit or load the repository's MCP server files.
