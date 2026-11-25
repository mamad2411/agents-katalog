---
name: agent-plugin-tools-integration
description: Wire agents to built-in, MCP, and extension tools with proper configuration, approval models, and sandbox constraints.
---

# Agent Tools Integration

## Specialization

Configure agents to use built-in tools (search, read, edit, web), external MCP servers (Model Context Protocol), or custom extension tools. Ensure secure tool binding with explicit approval rules and sandbox configuration.

## Supporting Activities

- Inventory available tools (built-in, MCP, extension-contributed).
- Configure MCP servers in `.mcp.json` or inline.
- Set tool approval models (pre-approved, per-request, post-review).
- Configure sandbox constraints (file/network access restrictions).
- Bind agents to tool subsets (whitelist per-agent).
- Validate tool availability and permission models.

## Workflow

1. **Inventory available tools**:
   - **Built-in**: search, read, edit, write, execute, web/fetch, grep, glob.
   - **MCP servers**: Check `.mcp.json` (workspace) or plugin `.mcp.json` for available servers.
   - **Extension tools**: Check VS Code extension contributions or installed packages.
   - Verify each tool is installed and accessible: `Chat: List Tools` or `MCP: List Servers`.

2. **Configure MCP servers** (if needed):
   - Create or update `.mcp.json` at plugin root:
     ```json
     {
       "mcpServers": {
         "server-id": {
           "command": "node",
           "args": ["/path/to/server.js"],
           "env": { "API_KEY": "${env:MY_API_KEY}" }
         }
       }
     }
     ```
   - For externally sourced servers (npm, PyPI):
     ```json
     {
       "mcpServers": {
         "playwright": {
           "command": "npx",
           "args": ["-y", "@microsoft/mcp-server-playwright"]
         }
       }
     }
     ```
   - Use plugin root token for file paths (Copilot format: none; Claude format: `${CLAUDE_PLUGIN_ROOT}`).

3. **Define tool approval model**:
   - **Pre-approved** (auto-execute): Safe, read-only operations (search, read, web fetch from trusted domains).
   - **Per-request** (ask user): Mutating operations (edit, write, execute custom commands, delete).
   - **Post-review** (execute then show): Operations with side effects (install dependencies, deploy).
   - **Domain-based approval**: Trust specific URL domains by default (e.g., `api.github.com`).

4. **Configure sandbox constraints** (MCP servers only; macOS/Linux):
   ```json
   {
     "mcpServers": {
       "restricted-server": {
         "command": "node",
         "args": ["server.js"],
         "sandboxEnabled": true,
         "sandbox": {
           "filesystem": {
             "allowRead": ["/home/user/.config"],
             "allowWrite": ["${workspaceFolder}"],
             "denyRead": ["/etc/passwd"],
             "denyWrite": ["/root"]
           },
           "network": {
             "allowedDomains": ["api.example.com"],
             "deniedDomains": ["corporate-proxy.local"]
           }
         }
       }
     }
   }
   ```

5. **Whitelist tools per-agent**:
   - In `.agent.md` frontmatter, list tools explicitly:
     ```yaml
     ---
     name: code-reviewer
     tools: ['search', 'read', 'web', 'grep']
     ---
     ```
   - For TypeScript agents, pass tool set at registration time (see agent-plugin-implementation-extension skill).

6. **Set auto-approval rules for terminal commands** (optional):
   ```jsonc
   {
     "chat.tools.terminal.autoApprove": {
       "mkdir": true,
       "ls": true,
       "pwd": true,
       "/^git (status|show|log)$/": true,  // Regex patterns
       "rm": false,
       "sudo": false
     }
   }
   ```

7. **Validate tool binding**:
   - Load the plugin or agent in VS Code.
   - Open Chat and start a message with the agent.
   - Verify: Tool picker shows only whitelisted tools.
   - Verify: MCP servers appear in tool list (if configured).
   - Test: Invoke a tool and confirm approval model is followed (pre-approved tools execute immediately; per-request tools show approval dialog).

8. **Document tool configuration**:
   - Create `TOOLS.md` in plugin root documenting:
     - Available tools (built-in + MCP + custom).
     - Approval model per tool.
     - Sandbox constraints (if applicable).
     - Example tool invocations.
     - Troubleshooting (tool not appearing, approval denied, etc.).

## Inputs

- Agent design with tool whitelist (from agent-plugin-design skill).
- Available tools inventory (built-in, MCP, extension).
- Approval policy (organization/team guidance on pre-approval vs. per-request).
- Sandbox constraints (security policy, file/network restrictions).
- MCP server configurations (if using external servers).

## Required Outputs

- MCP server configuration (`.mcp.json`) if external servers are used.
- Agent tool whitelist (in `.agent.md` or TypeScript registration).
- Approval model documented (pre-approved, per-request, post-review, domain-based).
- Sandbox constraints configured (if applicable and required by security policy).
- Validation evidence: tool picker shows correct tools, approval flows work as expected.
- TOOLS.md documentation file with inventory, models, examples, and troubleshooting.

## Done Criteria

- Tools whitelist in agent matches design document exactly.
- MCP servers (if configured) start without errors.
- Tool picker in VS Code Chat shows only whitelisted tools.
- Pre-approved tools execute immediately when invoked.
- Per-request tools show approval dialog before execution.
- Sandbox constraints are enforced (file/network access restricted as configured).
- Agent can successfully invoke tools and handle tool output.
- TOOLS.md is complete and includes examples for each tool type.

## Validation Checklist

- [ ] `.mcp.json` (if present) has valid JSON syntax.
- [ ] MCP server commands and args are correct and paths exist.
- [ ] Environment variables in MCP config are defined or set at runtime.
- [ ] Agent `tools` array lists only available tools (no typos or non-existent tools).
- [ ] Built-in tools used are confirmed to exist (search, read, edit, web, execute, etc.).
- [ ] Approval model is explicit for each tool (pre-approved, per-request, post-review).
- [ ] Sandbox constraints (if used) have valid filesystem and network rules.
- [ ] Auto-approval rules (if used) do not enable dangerous commands (rm, sudo, etc.).
- [ ] Tool picker shows correct tools when agent is selected in Chat.
- [ ] Tools can be invoked and produce expected output (tested manually in Chat).

## References

- [Agent Tools Reference](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- [MCP Servers Configuration](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Tool Approval Models](https://code.visualstudio.com/docs/copilot/customization/mcp-servers#_tool-approval)
- [Sandbox Configuration](https://code.visualstudio.com/docs/copilot/security#_sandbox)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## Trigger Conditions

Invoke this skill when any of the following is true:

- An agent needs to use MCP servers or custom tools beyond built-in ones.
- Tool approval rules must be defined (pre-approval, per-request, domain-based).
- Sandbox constraints must be configured for security hardening.
- Tool whitelist needs validation against availability and security policy.
- Multi-tool workflows require careful binding and orchestration.

