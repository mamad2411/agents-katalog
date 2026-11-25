---
name: follow-create-mcp
description: Build MCP servers in Rust or TypeScript for any client, without forcing registration
argument-hint: "[scope]"
allowed-tools:
  - exec
  - read
  - write
  - edit
  - skill
  - ask_user_question
  - todo_write
  - find_file_by_name
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - follow-create-cli
  - follow-lang-rust
  - follow-lang-typescript
  - deep-review-codebase
  - follow-single-responsibility
  - deep-validate
  - create-devin-global-mcp

---

## Goal

Build a new MCP server, starting with Rust first and falling back to TypeScript when it doesn't fit; support every MCP client and transport without forcing registration into any config

## Scope

Use when a skill or project needs to expose tools, resources, or prompts over the Model Context Protocol (MCP), supporting stdio, Streamable HTTP, and SSE transports

- Build the server only; do not register it in `mcp_config.json`
- To register in the Devin global MCP config, use `/create-devin-global-mcp` afterwards
- To register in the project MCP config, use `/update-devin-project-mcp`

See also: `/deep-review-codebase`, `/follow-lang-rust`, `/follow-lang-typescript`

- SDKs: `@modelcontextprotocol/sdk` (TS — `@modelcontextprotocol/server` is legacy), `rmcp` (Rust official — `cargo add rmcp --features server`) — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then read `../follow-my-techstack/references/techstack-catalog.md` to summarize the tech stack in use
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create mcp)
3. Record the rationale for the chosen stack and libraries for future reference (create mcp)

### 2. Decide Stack

> Goal: pick the stack that fits the use case

1. Analyze requirements: performance, runtime dependency, team skill, deployment target
2. Choose Rust when: you want a single binary, high performance, zero runtime dependencies, or a native-binary deployment
3. Choose TypeScript when: the team primarily uses TS/Bun, you need rapid iteration, or you must integrate with the JS ecosystem
4. If unclear → default to Rust
5. Decision matrix — Rust: no runtime dep, single binary, high performance; TypeScript: requires Node/Bun/Deno, larger ecosystem, faster iteration

### 3. Create MCP Server Project

> Goal: scaffold per the chosen stack

1. If Rust → `cargo new` then `cargo add rmcp --features server` (community alternative: `rust-mcp-sdk`)
2. If TypeScript → `bun init` then `bun add @modelcontextprotocol/sdk` (`@modelcontextprotocol/server` is the superseded legacy package)
3. Create the entry point: `src/main.rs` for Rust or `src/index.ts` for TypeScript
4. Define the server name, version, and capabilities (tools, resources, prompts)
5. Run `/deep-review-codebase` to pick a suitable architecture (Clean not mandated), then clearly separate handlers, transport, and domain logic

### 4. Implement Tools And Resources

> Goal: expose functionality over the MCP protocol

1. Define the tools the MCP server will expose, with input schemas
2. Use native type validation such as `zod` for TypeScript or `serde` for Rust
3. Define resources and prompts if needed
4. Use `/follow-single-responsibility` to split each tool handler into its own module

### 5. Choose Transport

> Goal: pick the right transport

1. stdio: for local spawn by the client (default for Devin/Cursor/Claude Code)
2. Streamable HTTP: for remote servers or multiple clients
3. SSE: for backward compatibility
4. If unclear → use stdio as the default for CLI tools, Streamable HTTP for services

### 6. Test Server

> Goal: confirm the server works correctly

1. Run the server with the stack's command, e.g. `cargo run` or `bun run dev`
2. Test with the MCP inspector or a compatible client
3. Verify that tools can be listed and invoked
4. If the transport is stdio → test spawning through a client such as Claude Code or `npx @modelcontextprotocol/inspector` (official inspector package)

### 7. Ship

> Goal: deliver the MCP server

1. Run `/deep-validate` to check conventions, references, and security
2. Run `/ship`
3. If `ship` fails → report the status

## Rules

### 1. Stack Selection

- Rust is the default (`rmcp` or `rust-mcp-sdk`) for performance and zero runtime dependencies
- TypeScript is the fallback when the team or ecosystem favors it
- Record the rationale for the chosen stack in the README or plan

### 2. Security

- Never hardcode secrets in server code
- Use `/follow-secret-manager` to manage API keys and credentials, then inject them as environment variables
- If the server accepts client input → validate the schema before processing

### 3. Transport

- stdio is the default for tools the client spawns directly
- Streamable HTTP when serving multiple clients over the network
- Don't use SSE for new implementations except for backward compatibility

### 4. No Registry In This Skill

- Build the server only; do not register it in `mcp_config.json`
- To register in the Devin global config, hand off to `/create-devin-global-mcp`
- To register in the project config, hand off to `/update-devin-project-mcp`

### 5. Integration

- If this skill is built inside the global skills repo → update `related` and `AGENTS.md`

- Use `/open-web-for-config-secret` if needed
- Use `/follow-create-cli` if needed
- Use `/follow-lang-rust` if needed
- Use `/follow-lang-typescript` if needed

## Expected Outcome

- The MCP server works in either Rust or TypeScript
- Tools/resources/prompts are exposed over the MCP protocol
- The chosen transport has been tested and passes
- Passes `/deep-validate` and `/ship`
- Ready to hand off for registration via `/create-devin-global-mcp` or `/update-devin-project-mcp` if needed
