---
name: mcp-management
description: Industrial protocol for adding, configuring, and verifying MCP servers with cross-tool adaptation.
category: Tool-Infrastructure
---

# MCP Server Management Skill (v1)

This skill provides a standardized protocol for managing MCP (Model Context Protocol) servers within the workspace.
It ensures absolute data fidelity, comprehensive documentation, and secure verification.

***

## 1. Documentation & Discovery

The agent MUST first establish the operational context:

- **Config Location**: The user will provide the target `mcp_config.json` path. If not provided, ask for it.
    - *Example (Antigravity)*: `/Users/[REDACTED]/anti-gravity-mcp_config.json`
- **Target AI Tool**: Identify the tool being configured (e.g., Antigravity, VS Code, Claude Desktop).
- **Source Documentation**: Request official documentation (URLs, `.txt`, `.md`, or `.pdf` files).
    - **URL Handling**: For web links, ALWAYS use the `firecrawl` MCP tool to extract detailed technical specifications.

### 1.1 Tool-Specific Adaptation (Extrapolation)

- If the documentation has a dedicated section for the target tool, use it directly.
- If not, research dedicated sections for other tools (e.g., Claude Desktop) to understand the required `command`
  and `args`.
- **Extrapolation**: Adapt instructions from other tools to the target tool's JSON configuration schema.
- **Fail-Safe**: If no tool-specific sections exist, determine the binary path and arguments based on the language
  runtime (Node/Python) or compiled binary status.

***

## 2. Schema & Structure

### 2.1 Dependencies

Before managing MCP servers, the agent MUST verify the following local environment:

- **Runtime Tools**: Verify existence of required runtimes (`node`, `python`, `mise`, `brew`).
- **Absolute Paths**: ALWAYS use absolute paths for the `command` field to ensure execution reliability across
  different shell environments. **Verify the path using `which <tool>` or `find`**.

### 2.2 Security & Configuration

- **Alphabetical Order**: Maintain entries in **alphabetical order** within the `mcpServers` object.
- **Standard Transport**: Default to `stdio` unless specified otherwise.
- **No Hardcoding**: Sensitive keys (API keys, tokens) MUST be managed via environment variables (`env` object)
  or secure secret stores.
- **Naming Convention**: Use uppercase, underscore-separated names for env vars (e.g., `POSTMAN_API_KEY`).

```json
"example-server": {
  "command": "/path/to/binary",
  "args": ["--option"],
  "env": {
    "API_KEY": "SECRET_VALUE"
  }
}
```

***

## 3. Integration Workflow

1. **Discovery**: Research the server's documentation for required commands and arguments.
2. **Path Verification**: Locate the underlying binary using `which` or `find`.
3. **Draft Configuration**: Formulate the JSON entry following the patterns in existing config logs.
4. **Insertion**: Insert the entry into the target `mcp_config.json` file in alphabetical order.
5. **Verification**: Execute the verification protocol defined in Section 4.

***

## 4. Verification Protocol

The agent MUST verify the new configuration before concluding the task:

1. **JSON Lint**: Run `jq . <config_file>` to ensure the file remains valid after modification.
2. **Command Dry-Run**: Run the `command` with `--help` or a version flag to ensure accessibility.
3. **Functional Pipe Test**: For `stdio` servers, perform a JSON-RPC pipe test:

```bash
# Industrial Pipe Test Sample
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | <command> <args>
```

***

## 5. Traceability & Recording

### 5.1 Redaction & Privacy

- **Absolute Paths**: When recording logs, NEVER include biological or system-specific user prefixes.
- **Redaction**: Replace sensitive prefixes (e.g., `/Users/dk/`) with `[REDACTED]`.

### 5.2 Contextual Documentation

- **Session Logs**: Store all session records in the workspace [docs/conversations/](../../../docs/conversations/) folder.
- **Permanent Link**: Create a relative link in the skill summary or AGENTS.md to the relevant session log for
  future auditability.

***

## 6. Composition by Higher-Level Skills

When the same MCP server entry needs to land in multiple AI tools (VS Code Copilot, JetBrains Copilot,
Copilot CLI, Claude Desktop, Cursor, Windsurf, etc.), do NOT hand-edit each tool's config. Use the
[MCP Cross-Tool Config Sync Skill](../mcp-cross-tool-config-sync/SKILL.md), which:

- Treats this skill's server-entry conventions (§2.2) as the SSOT for individual entries.
- Wraps them in a single canonical `mcp-servers.json`.
- Generates schema-correct per-tool files (`mcpServers` vs `servers`, `tools: ["*"]`, `inputs` passthrough).
- Distributes via symlinks so one canonical edit propagates everywhere.

***

## Related Skills

- [`opencode-remote-mcp-setup`](../opencode-remote-mcp-setup/SKILL.md) — OpenCode-specific composer for remote MCP
servers (consumes this skill)
- [`mcp-cross-tool-config-sync`](../mcp-cross-tool-config-sync/SKILL.md) — Cross-tool MCP config sync (consumes this
skill)
- [`google-workspace-mcp-account-switch`](../mcp/google-workspace-mcp-account-switch/SKILL.md) — runtime auth operation
on a configured google-workspace MCP server (account switching); complements this skill's add/configure/verify
lifecycle.

***

## Design Appendix (Design Fidelity)

| Feature | Change Note | Rationale |
| :--- | :--- | :--- |
| **Path Redaction** | Replaced `/Users/X/` with `/Users/[REDACTED]/`. | Compliance with [redaction\_portability](../redaction-portability/SKILL.md). |
| **Section Restoration** | Re-inserted "Dependencies" and "Integration Workflow". | Restored to ensure full operational guidance is not lost during summarization. |
| **Alphabetical Mandate** | Explicitly required alphabetical ordering in JSON. | Consistency and maintainability in large configuration files. |
| **Functional Pipe Test** | Added bash sample for JSON-RPC pipe verification. | Functional proof-of-work for `stdio` transport. |
| **Config Pathing** | Removed "User Provided Path" label for example. | Improves readability while maintaining privacy. |
