---
name: rust-dev-guide
description: "Entry point for rust-development — routes to the right sub-skill for your task"
version: "1.0.0"
git_hash: "3bc512f"
---

# Rust Development

Build Rust extensions, CLI binaries, and MCP servers for systemprompt.io. This plugin covers all Rust development from coding standards to specific extension types.

---

## Skills

### rust-coding-standards
**Load when:** writing any Rust code, reviewing code quality, authoring documentation, or working with content workflows.
**Covers:** Idiomatic Rust patterns, code locations (`extensions/*/src/`), naming conventions, error handling, documentation standards, content workflows, quality patterns. This is the foundational skill — load it alongside any other skill.

### extension-building
**Load when:** building or modifying library extensions (non-CLI, non-MCP Rust code).
**Covers:** Extension architecture, traits, schemas, API routes, jobs, code review patterns. Reference implementation: `extensions/web/`. Core principle: Rust code = extension, YAML/Markdown = service. Never modify `core/` (git submodule).

### cli-extension-building
**Load when:** building standalone CLI tools that integrate with systemprompt.
**Covers:** Clap-based CLI setup, `manifest.yaml` discovery, subprocess integration, argument parsing, output formatting. Reference implementation: `extensions/cli/discord/`. CLI extensions run as separate processes via `systemprompt plugins run <name>`.

### mcp-building
**Load when:** building MCP (Model Context Protocol) servers.
**Covers:** MCP server architecture, tool definitions, artifacts, UI resources, AI service integration, `module.yml` configuration. Reference implementation: `extensions/mcp/systemprompt/`. MCP servers live in `/extensions/mcp/`.

---

## Task Router

| I want to... | Load these skills |
|--------------|-------------------|
| Write any Rust code | `rust-coding-standards` |
| Build a library extension | `extension-building` + `rust-coding-standards` |
| Build a CLI tool | `cli-extension-building` + `rust-coding-standards` |
| Build an MCP server | `mcp-building` + `rust-coding-standards` |
| Review Rust code quality | `rust-coding-standards` |
| Add API routes to an extension | `extension-building` + `rust-coding-standards` |
| Full extension build or review | All relevant skills + `rust-coding-standards` |

---

## Skill Dependencies

```
rust-coding-standards (always required for any Rust work)
        |
        +---> extension-building (library extensions)
        |
        +---> cli-extension-building (CLI binaries)
        |
        +---> mcp-building (MCP servers)
```

**For any task:** always load `rust-coding-standards` first. Then load the specific skill for your extension type.
